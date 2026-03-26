
import re

text = "aaaba"
pattern = "a*"
matches = re.findall(pattern, text)
print(matches)  


text = "dddd aaa ccc a bb aa casa"
pattern = "a+"
matches = re.findall(pattern, text)
print(matches)

text = "aaabacd"
pattern = "a?b"
matches = re.findall(pattern, text)
print(matches)

text = "aaaaaaa"
pattern = "a{3}"
matches = re.findall(pattern, text)
print(matches)

text = "u uu uuu u"
pattern = "u{2,3}"
matches = re.findall(pattern, text)
print(matches)

words = "ala casa del arbol leon cinco murcielago"
pattern = r"\b\w{4,6}\b"
matches = re.findall(pattern, words)
print(matches)


