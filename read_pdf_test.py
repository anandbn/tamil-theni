import pypdf

reader = pypdf.PdfReader('Theni Word List - 2026.pdf')

page4 = reader.pages[3]
text = page4.extract_text()

print("--- Page 4 Text ---")
print(text)
