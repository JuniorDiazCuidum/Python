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
    "CONTRATO",
    "EMPLEADOR",
    "TRABAJADOR",
    "TRABAJADORA",
    "MINISTERIO",
    "SEPE",
    "NIF",
    "NIE",
    "DNI",
    "DOMICILIO",
    "MUNICIPIO",
    "PAIS",
    "FIRMA",
    "CLAUSULA",
    "ESTATUTO",
    "CUENTA",
    "COTIZACION",
    "CENTRO",
    "TRABAJO",
    "AFILIACION",
    "SEGURIDAD",
    "SOCIAL",
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
        " E M P L E A D O R ": " EMPLEADOR ",
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
    if len("".join(lines)) >= 80:
        return text, lines, False, None

    ocr_lines, ocr_error = extract_ocr_lines(pdf_path)
    if ocr_lines:
        return "\n".join(ocr_lines), ocr_lines, True, None
    return text, lines, False, ocr_error


def get_section(lines: list[str], role: str, size: int = 180) -> list[str]:
    if role == "company":
        start_tokens = [("DATOS", "EMPRESA"), ("EMPLEADOR",), ("EMPRESA",)]
        stop_tokens = ["TRABAJADOR", "TRABAJADORA", "CLAUSULA"]
    else:
        start_tokens = [("DATOS", "TRABAJADOR"), ("DATOS", "TRABAJADORA"), ("TRABAJADOR",), ("TRABAJADORA",)]
        stop_tokens = ["CLAUSULA", "PRIMERA", "SEGUNDA", "TERCERA", "CUARTA", "QUINTA"]

    start = -1
    for i, line in enumerate(lines):
        c = compact(line)
        if any(all(token in c for token in group) for group in start_tokens):
            start = i
            break
    if start == -1:
        return []

    end = min(len(lines), start + size)
    for j in range(start + 1, end):
        c = compact(lines[j])
        if any(token in c for token in stop_tokens):
            end = j
            break
    return lines[start:end]


def documents_from_lines(lines: list[str]) -> list[str]:
    docs: list[str] = []
    for line in lines:
        docs.extend(find_documents(line))
    return unique_keep_order(docs)


def best_name(lines: list[str], doc: str = NOT_FOUND) -> str:
    if doc != NOT_FOUND:
        for i, line in enumerate(lines):
            if doc not in line:
                continue
            near = lines[max(0, i - 3) : min(len(lines), i + 4)]
            candidates = [normalize_name(x) for x in near if is_name_candidate(x)]
            if candidates:
                return max(candidates, key=lambda x: (len(x.split()), len(x)))
    candidates = [normalize_name(line) for line in lines if is_name_candidate(line)]
    return max(candidates, key=lambda x: (len(x.split()), len(x))) if candidates else NOT_FOUND


def choose_person(section_lines: list[str], excluded_docs: set[str] | None = None) -> tuple[str, str]:
    excluded_docs = excluded_docs or set()
    pairs: list[tuple[str, str]] = []
    for i, line in enumerate(section_lines):
        docs = [d for d in find_documents(line) if d not in excluded_docs]
        if docs:
            for j in (i - 2, i - 1, i + 1, i + 2):
                if 0 <= j < len(section_lines) and is_name_candidate(section_lines[j]):
                    pairs.append((normalize_name(section_lines[j]), docs[0]))
                    break
        if is_name_candidate(line):
            for j in range(i, min(i + 4, len(section_lines))):
                docs2 = [d for d in find_documents(section_lines[j]) if d not in excluded_docs]
                if docs2:
                    pairs.append((normalize_name(line), docs2[0]))
                    break

    if pairs:
        return max(pairs, key=lambda p: (len(p[0].split()), len(p[0])))

    docs = [d for d in documents_from_lines(section_lines) if d not in excluded_docs]
    doc = docs[0] if docs else NOT_FOUND
    return best_name(section_lines, doc), doc


def extract_people(text: str, lines: list[str]) -> tuple[PersonData, PersonData]:
    company_section = get_section(lines, "company") or lines
    worker_section = get_section(lines, "worker") or lines

    company_name, company_doc = choose_person(company_section)
    worker_name, worker_doc = choose_person(worker_section, {company_doc} if company_doc != NOT_FOUND else set())

    company = PersonData(document_id=company_doc)
    worker = PersonData(document_id=worker_doc)
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


def build_payload(pdf_path: Path, company: PersonData, worker: PersonData) -> dict:
    return {"pdf": pdf_path.name, "company": asdict(company), "worker": asdict(worker)}


def default_contract_pdf() -> Path | None:
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        return None
    contracts = [pdf for pdf in pdfs if "contrato" in pdf.name.lower() or "contract" in pdf.name.lower()]
    return contracts[0] if contracts else pdfs[0]


def resolve_pdf(pdf_arg: str | None) -> Path:
    if pdf_arg:
        candidate = Path(pdf_arg).expanduser()
        if not candidate.is_absolute():
            from_cwd = (Path.cwd() / candidate).resolve()
            from_nominas = (PDF_DIR / candidate).resolve()
            candidate = from_cwd if from_cwd.exists() else from_nominas
    else:
        candidate = default_contract_pdf()
        if candidate is None:
            raise SystemExit("No PDF files found in the 'Nominas' folder.")

    if not candidate.exists():
        raise SystemExit(f"PDF file not found: {pdf_arg}")
    if candidate.suffix.lower() != ".pdf":
        raise SystemExit(f"File is not a PDF: {candidate}")
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a contract PDF and print company/worker data.")
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
        import json

        print("\nJSON:")
        print(json.dumps(build_payload(pdf_path, company, worker), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
