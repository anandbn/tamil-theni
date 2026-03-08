import pdfplumber
import json
import re

def clean_english(text):
    if not text:
        return ""
    text = text.replace('  ', '<SPACE>')
    text = text.replace(' ', '')
    text = text.replace('<SPACE>', ' ')
    return text

def clean_text(text, is_english=False):
    if not text:
        return ""
    text = text.replace('(cid:0)', '')
    text = text.strip()
    if is_english:
        text = clean_english(text)
    return text

d1_data = {"categories": []}
d2_data = {"categories": []}

def add_word(dataObj, category_name, eng, tam):
    # Find category
    cat = next((c for c in dataObj["categories"] if c["name"] == category_name), None)
    if not cat:
        cat = {"name": category_name, "words": []}
        dataObj["categories"].append(cat)
    cat["words"].append({"english": eng, "tamil": tam})

with pdfplumber.open('Theni Word List - 2026.pdf') as pdf:
    # We iterate through all pages, the tables match our D1/D2 structure
    for page_idx, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            heading_row = [clean_text(c) for c in table[0] if c]
            header_row = [clean_text(c).replace(' ', '') for c in table[1] if c]
            
            heading = heading_row[0] if heading_row else f"Page {page_idx+1}"
            
            # Identify our table by checking for D1 or D2
            if 'D1' in header_row or 'D2' in header_row:
                for row in table[2:]:
                    c0 = clean_text(row[0])
                    # Ensure it's a data row by checking the 'No' column
                    if not c0.isdigit():
                        continue
                        
                    # D1 Words are typically in column 1 (English) and 2 (Tamil)
                    d1_eng = clean_text(row[1], is_english=True) if len(row) > 1 else ""
                    d1_tam = clean_text(row[2]) if len(row) > 2 else ""
                    if d1_eng or d1_tam:
                        add_word(d1_data, heading, d1_eng, d1_tam)
                        
                    # D2 Words are typically in column 3 (English) and 4/5 (Tamil)
                    d2_eng = clean_text(row[3], is_english=True) if len(row) > 3 else ""
                    d2_tam = ""
                    if len(row) > 5 and row[5] and clean_text(row[5]):
                        d2_tam = clean_text(row[5])
                    elif len(row) > 4 and row[4] and clean_text(row[4]):
                        d2_tam = clean_text(row[4])
                        
                    if d2_eng or d2_tam:
                        add_word(d2_data, heading, d2_eng, d2_tam)

# Write output to JSON
with open('D1_words.json', 'w', encoding='utf-8') as f:
    json.dump(d1_data, f, ensure_ascii=False, indent=2)

with open('D2_words.json', 'w', encoding='utf-8') as f:
    json.dump(d2_data, f, ensure_ascii=False, indent=2)

print("Extraction complete. Results saved in D1_words.json and D2_words.json.")
