from __future__ import annotations

import argparse
import importlib
import re
import site
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR
NOT_FOUND = "Not found"

DOC_RE = re.compile(r"\b(?:[XYZ]\d{7}[A-Z]|\d{8}[A-Z])\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(
    r"(?:movil|m[oó]vil|telefono|tel[eé]fono|celular|phone|mobile)\s*[:.]?\s*((?:\+?34[\s.-]*)?[6789](?:[\s.-]?\d){8})",
    re.IGNORECASE,
)
NAME_NOISE = {
    "NOMINA",
    "TOTAL",
    "DIAS",
    "CONCEPTO",
    "DEVENGADO",
    "DEDUCCION",
    "BASE",
    "GRUPO",
    "CUOTA",
    "APORTACION",
    "FIRMA",
    "RECIBI",
    "DOMICILIO",
    "POBLACION",
    "CONTRATO",
    "CATEGORIA",
    "PUESTO",
}


@dataclass
class PersonData:
    document_id: str = NOT_FOUND
    first_name: str = NOT_FOUND
    last_name_1: str = NOT_FOUND
    last_name_2: str = NOT_FOUND
    email: str = NOT_FOUND
    mobile: str = NOT_FOUND


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def compact(text: str) -> str:
    text = normalize(text).upper()
    table = str.maketrans("ÁÉÍÓÚÜÑ", "AEIOUUN")
    return re.sub(r"[^A-Z0-9]", "", text.translate(table))


def clean_ocr_line(text: str) -> str:
    text = f" {normalize(text)} "
    replacements = {
        " D N I ": " DNI ",
        " N I F ": " NIF ",
        " N I E ": " NIE ",
        " N O M B R E ": " NOMBRE ",
        " E M A I L ": " EMAIL ",
        " T E L E F O N O ": " TELEFONO ",
        " T R A B A J A D O R L A ": " TRABAJADOR/A ",
        " T R A B A J A D O R A ": " TRABAJADORA ",
        " T R A B A J A D O R ": " TRABAJADOR ",
        " E M P R E S A ": " EMPRESA ",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return normalize(text)


def unique_keep_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output


def is_valid_document(doc: str) -> bool:
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    if re.fullmatch(r"\d{8}[A-Z]", doc):
        return doc[-1] == letters[int(doc[:8]) % 23]
    if re.fullmatch(r"[XYZ]\d{7}[A-Z]", doc):
        number = {"X": "0", "Y": "1", "Z": "2"}[doc[0]] + doc[1:8]
        return doc[-1] == letters[int(number) % 23]
    return False


def find_documents(text: str) -> list[str]:
    return unique_keep_order([doc for doc in DOC_RE.findall(text.upper()) if is_valid_document(doc)])


def normalize_name(raw: str) -> str:
    raw = normalize(raw.replace(" ,", ","))
    if "," in raw:
        left, right = [normalize(x) for x in raw.split(",", 1)]
        if left and right:
            return normalize(f"{right} {left}")
    return raw


def is_name_candidate(line: str) -> bool:
    line = normalize_name(line)
    if len(line) < 6 or re.search(r"\d", line):
        return False
    tokens = [t for t in line.upper().replace(",", " ").split() if t]
    if len(tokens) < 2:
        return False
    if any(token in NAME_NOISE for token in tokens):
        return False
    return all(re.fullmatch(r"[A-ZÁÉÍÓÚÜÑ'/-]{2,}", token) for token in tokens)


def split_full_name(full_name: str) -> tuple[str, str, str]:
    parts = normalize(full_name).split()
    if len(parts) >= 3:
        return parts[0], parts[1], " ".join(parts[2:])
    if len(parts) == 2:
        return parts[0], parts[1], NOT_FOUND
    if len(parts) == 1:
        return parts[0], NOT_FOUND, NOT_FOUND
    return NOT_FOUND, NOT_FOUND, NOT_FOUND


def fill_name(person: PersonData, full_name: str) -> None:
    if full_name == NOT_FOUND:
        return
    person.first_name, person.last_name_1, person.last_name_2 = split_full_name(full_name)


def load_pdf_reader():
    def try_import():
        for module_name in ("pypdf", "PyPDF2"):
            try:
                return importlib.import_module(module_name).PdfReader
            except ImportError:
                pass
        return None

    reader = try_import()
    if reader:
        return reader

    try:
        user_site = site.getusersitepackages()
        if user_site and user_site not in sys.path:
            sys.path.append(user_site)
        reader = try_import()
        if reader:
            return reader
    except Exception:
        pass

    print("Missing 'pypdf' and 'PyPDF2'. Trying to install 'pypdf'...")
    result = subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            "Could not install 'pypdf'.\n"
            f"Run: {sys.executable} -m pip install pypdf\n"
            f"Details: {result.stderr.strip() or result.stdout.strip()}"
        )

    importlib.invalidate_caches()
    reader = try_import()
    if not reader:
        raise SystemExit(f"Could not load PDF reader with {sys.executable}.")
    return reader


PdfReader = load_pdf_reader()


def extract_pdf_text(pdf_path: Path) -> str:
    return "\n".join((page.extract_text() or "") for page in PdfReader(str(pdf_path)).pages)


def extract_ocr_lines(pdf_path: Path) -> tuple[list[str], str | None]:
    try:
        import numpy as np
        import pypdfium2 as pdfium
        from rapidocr_onnxruntime import RapidOCR
    except ImportError as exc:
        return [], str(exc)

    ocr = RapidOCR()
    lines: list[str] = []
    for page in pdfium.PdfDocument(str(pdf_path)):
        result, _ = ocr(np.array(page.render(scale=2).to_pil()))
        if not result:
            continue
        for item in result:
            line = clean_ocr_line(item[1])
            if line:
                lines.append(line)
    return lines, None


def extract_content(pdf_path: Path) -> tuple[str, list[str], bool, str | None]:
    text = extract_pdf_text(pdf_path)
    lines = [normalize(line) for line in text.splitlines() if normalize(line)]

    def looks_garbled(sample: list[str]) -> bool:
        head = " ".join(sample[:200])
        split_letters = re.findall(r"(?:\b[A-Za-zÁÉÍÓÚÜÑ]\s){4,}[A-Za-zÁÉÍÓÚÜÑ]\b", head)
        return len(split_letters) >= 2

    if len("".join(lines)) >= 80 and not looks_garbled(lines):
        return text, lines, False, None

    ocr_lines, ocr_error = extract_ocr_lines(pdf_path)
    if ocr_lines:
        return "\n".join(ocr_lines), ocr_lines, True, None
    return text, lines, False, ocr_error


def find_label_index(lines: list[str], target: str) -> int:
    for idx, line in enumerate(lines):
        c = compact(line)
        if target == "company" and "EMPRESA" in c and "APORTACION" not in c and "FIRMA" not in c:
            return idx
        if target == "worker" and "TRABAJADOR" in c and "APORTACION" not in c and "FIRMA" not in c:
            return idx
    return -1


def name_after(lines: list[str], idx: int) -> str:
    if idx < 0:
        return NOT_FOUND
    for j in range(idx + 1, min(idx + 10, len(lines))):
        candidate = normalize_name(lines[j])
        if is_name_candidate(candidate):
            return candidate
    return NOT_FOUND


def top_name_candidates(lines: list[str], limit: int = 25) -> list[str]:
    names = [normalize_name(lines[i]) for i in range(min(limit, len(lines))) if is_name_candidate(lines[i])]
    return unique_keep_order(names)


def documents_from_lines(lines: list[str]) -> list[str]:
    docs: list[str] = []
    for line in lines:
        docs.extend(find_documents(line))
    return unique_keep_order(docs)


def extract_people(text: str, lines: list[str]) -> tuple[PersonData, PersonData]:
    company = PersonData()
    worker = PersonData()

    company_label_idx = find_label_index(lines, "company")
    worker_label_idx = find_label_index(lines, "worker")

    company_name = name_after(lines, company_label_idx)
    worker_name = name_after(lines, worker_label_idx)

    # Common payroll layout: "Empresa" and "Trabajador/a" headers side by side.
    if company_label_idx >= 0 and worker_label_idx >= 0 and abs(company_label_idx - worker_label_idx) <= 3:
        start = min(company_label_idx, worker_label_idx)
        nearby = [normalize_name(lines[i]) for i in range(start + 1, min(start + 14, len(lines))) if is_name_candidate(lines[i])]
        nearby = unique_keep_order(nearby)
        if len(nearby) >= 2:
            company_name, worker_name = nearby[0], nearby[1]

    if company_name == NOT_FOUND or worker_name == NOT_FOUND:
        candidates = top_name_candidates(lines)
        if company_name == NOT_FOUND and candidates:
            company_name = candidates[0]
        if worker_name == NOT_FOUND and len(candidates) > 1:
            worker_name = candidates[1]

    docs = documents_from_lines(lines)
    if len(docs) >= 2:
        company.document_id, worker.document_id = docs[0], docs[1]
    elif len(docs) == 1:
        worker.document_id = docs[0]

    fill_name(company, company_name)
    fill_name(worker, worker_name)

    emails = unique_keep_order(EMAIL_RE.findall(text))
    phones: list[str] = []
    for match in PHONE_RE.finditer(text):
        number = re.sub(r"\D", "", match.group(1))
        if len(number) == 11 and number.startswith("34"):
            number = number[2:]
        if len(number) == 9:
            phones.append(number)
    phones = unique_keep_order(phones)

    if emails:
        company.email = emails[0]
    if len(emails) > 1:
        worker.email = emails[1]
    if phones:
        company.mobile = phones[0]
    if len(phones) > 1:
        worker.mobile = phones[1]
    return company, worker


def print_form_block(title: str, person: PersonData) -> None:
    width = 116
    col_title, col_l_key, col_l_val, col_r_key, col_r_val = 22, 18, 34, 10, 24

    def cut(value: str, limit: int) -> str:
        return value if len(value) <= limit else value[: limit - 3] + "..."

    def row(left_key: str, left_val: str, right_key: str = "", right_val: str = "", side_title: str = "") -> str:
        return (
            f"{cut(side_title, col_title):<{col_title}} "
            f"{cut(left_key, col_l_key):<{col_l_key}} "
            f"{cut(left_val, col_l_val):<{col_l_val}} "
            f"{cut(right_key, col_r_key):<{col_r_key}} "
            f"{cut(right_val, col_r_val):<{col_r_val}}"
        )

    border = "-" * width
    print()
    print(border)
    print(row("", "", "", "", title))
    print(row("ID", person.document_id, "Email", person.email))
    print(row("First name", person.first_name, "Mobile", person.mobile))
    print(row("Last name 1", person.last_name_1))
    print(row("Last name 2", person.last_name_2))
    print(border)


def print_json(company: PersonData, worker: PersonData) -> None:
    import json

    payload = {"company": asdict(company), "worker": asdict(worker)}
    print("\nJSON:")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def first_payroll_pdf() -> Path | None:
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        return None
    payrolls = [pdf for pdf in pdfs if "nomina" in pdf.name.lower() or "nómina" in pdf.name.lower() or "payroll" in pdf.name.lower()]
    return payrolls[0] if payrolls else pdfs[0]


def resolve_pdf(pdf_arg: str | None) -> Path:
    if pdf_arg:
        candidate = Path(pdf_arg).expanduser()
        if not candidate.is_absolute():
            from_cwd = (Path.cwd() / candidate).resolve()
            from_nominas = (PDF_DIR / candidate).resolve()
            candidate = from_cwd if from_cwd.exists() else from_nominas
    else:
        candidate = first_payroll_pdf()
        if candidate is None:
            raise SystemExit("No PDF files found in the 'Nominas' folder.")

    if not candidate.exists():
        raise SystemExit(f"PDF file not found: {pdf_arg}")
    if candidate.suffix.lower() != ".pdf":
        raise SystemExit(f"File is not a PDF: {candidate}")
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a payroll PDF and print company/worker data.")
    parser.add_argument("pdf", nargs="?", help="Path to the PDF file.")
    parser.add_argument("--json", action="store_true", help="Also print JSON output.")
    args = parser.parse_args()

    pdf_path = resolve_pdf(args.pdf)
    print(f"Reading: {pdf_path}")

    text, lines, used_ocr, ocr_error = extract_content(pdf_path)
    if used_ocr:
        print("OCR enabled: scanned PDF detected.")
    if len("".join(lines)) < 20 and ocr_error:
        print("OCR is not available in this Python environment.")
        print(f"Details: {ocr_error}")
        print(f"Install OCR with: {sys.executable} -m pip install pypdfium2 rapidocr_onnxruntime pillow")

    company, worker = extract_people(text, lines)
    print_form_block("Company data", company)
    print_form_block("Worker data", worker)
    if args.json:
        print_json(company, worker)


if __name__ == "__main__":
    main()
