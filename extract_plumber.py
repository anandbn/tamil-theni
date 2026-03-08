import pdfplumber

with pdfplumber.open('Theni Word List - 2026.pdf') as pdf:
    # Page 3 is index 2, Page 23 is index 22
    page = pdf.pages[3] # Testing Page 4
    
    # Try text with layout
    text = page.extract_text(layout=True)
    print("--- Layout Text ---")
    print(text)
    
    # Try table extraction
    table = page.extract_table()
    print("\n--- Table ---")
    print(table)
