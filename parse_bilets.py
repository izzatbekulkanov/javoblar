import zipfile, xml.etree.ElementTree as ET, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'D:\Farangiz\metodica\METODIKA.docx'

with zipfile.ZipFile(docx_path, 'r') as z:
    with z.open('word/document.xml') as f:
        tree = ET.parse(f)

root = tree.getroot()

paragraphs = []
for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = []
    for r in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
        if r.text:
            texts.append(r.text)
    text = ''.join(texts).strip()
    if text:
        paragraphs.append(text)

print(f'Total paragraphs: {len(paragraphs)}')

# Parse bilets structure
bilets = {}
bilet_pattern = re.compile(r'^(\d+)[.\-\s]*bilet', re.IGNORECASE)
savol_pattern = re.compile(r'^(\d+)[.\-\s]*(savol|javobi|javob)', re.IGNORECASE)

current_bilet = None
current_q_idx = 0
current_q_title = None
current_q_text = []

def save_question():
    global current_q_text, current_q_title, current_q_idx
    if current_bilet is not None and current_q_text:
        text = '\n'.join(current_q_text).strip()
        if text and len(text) > 10:
            if current_bilet not in bilets:
                bilets[current_bilet] = []
            bilets[current_bilet].append({
                'title': current_q_title or f'Savol {current_q_idx}',
                'content': text
            })
    current_q_text = []
    current_q_title = None

for i, p in enumerate(paragraphs):
    bilet_match = bilet_pattern.match(p)
    if bilet_match:
        save_question()
        current_bilet = int(bilet_match.group(1))
        current_q_idx = 0
        rest = p[bilet_match.end():].strip()
        if rest and len(rest) > 10:
            # This paragraph has question content too
            current_q_idx = 1
            current_q_title = rest[:120] if len(rest) > 120 else rest
            current_q_text = [p]
        # else it's just a header line
    else:
        if current_bilet is not None:
            sv_match = savol_pattern.match(p)
            if sv_match and current_bilet is not None:
                save_question()
                current_q_idx += 1
                current_q_title = p[:150]
                current_q_text = [p]
            else:
                if current_q_text or (not savol_pattern.match(p)):
                    current_q_text.append(p)

save_question()

# Print result summary
for b_num in sorted(bilets.keys()):
    qs = bilets[b_num]
    print(f'Bilet {b_num}: {len(qs)} savol')
    for j, q in enumerate(qs):
        print(f'  [{j+1}] {q["title"][:80]}')

print(f'\nJami biletlar: {len(bilets)}')

# Save to JSON
with open(r'D:\Farangiz\metodica\bilets.json', 'w', encoding='utf-8') as f:
    json.dump(bilets, f, ensure_ascii=False, indent=2)

print('bilets.json saqlandi!')
