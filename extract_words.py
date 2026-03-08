import pdfplumber
import json
import re

def clean_english(text):
    # Handle single spaces separating characters
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

output_data = {}

with pdfplumber.open('Theni Word List - 2026.pdf') as pdf:
    # We will just iterate through all pages 
    # to ensure we don't miss anything that has a D2.
    for page_idx, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            if not table or len(table) < 2:
                continue
                
            # Usually row 0 is heading, row 1 is headers
            heading_row = [clean_text(c) for c in table[0] if c]
            header_row = [clean_text(c).replace(' ', '') for c in table[1] if c]
            
            heading = heading_row[0] if heading_row else f"Page {page_idx+1}"
            
            if 'D2' in header_row:
                if heading not in output_data:
                    output_data[heading] = []
                    
                # Find the D2 indices. 
                # In the raw table, 'D 2' might be in column 3.
                # Let's find exactly which columns correspond to D2.
                # Since the table structure is fixed:
                # col 0: No
                # col 1: D1 Eng
                # col 2: D1 Tam
                # col 3: D2 Eng
                # col 4: D2 Tam (sometimes empty Col 4 and then Col 5 is Tam)
                # Let's be smart about it:
                for row in table[2:]:
                    # Check if it's a valid data row (starts with a number)
                    c0 = clean_text(row[0])
                    if not c0.isdigit():
                        continue
                        
                    # D2 Eng is typically at index 3
                    eng_word = clean_text(row[3], is_english=True) if len(row) > 3 else ""
                    
                    # D2 Tamil is typically the last non-empty cell or index 5
                    # Let's check col 4 and 5
                    tam_word = ""
                    if len(row) > 5 and row[5] and clean_text(row[5]):
                        tam_word = clean_text(row[5])
                    elif len(row) > 4 and row[4] and clean_text(row[4]):
                        tam_word = clean_text(row[4])
                        
                    if eng_word or tam_word:
                        output_data[heading].append({
                            "english": eng_word,
                            "tamil": tam_word
                        })
                        
# Write output
with open('D2_words.txt', 'w', encoding='utf-8') as f:
    for heading, words in output_data.items():
        f.write(f"--- {heading} ---\n")
        max_eng = max([len(w['english']) for w in words]) if words else 0
        for w in words:
            eng = w['english'].ljust(max_eng)
            tam = w['tamil']
            f.write(f"{eng} - {tam}\n")
        f.write("\n")

print("Extraction complete. Results saved in D2_words.txt.")
