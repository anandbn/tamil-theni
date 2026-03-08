import fitz

doc = fitz.open('Theni Word List - 2026.pdf')
page = doc[3]  # page 4

tables = page.find_tables()
if tables:
    for table in tables:
        rows = table.extract()
        for i, row in enumerate(rows[:5]):
            print(f"Row {i}: {row}")
else:
    print("No tables found")
