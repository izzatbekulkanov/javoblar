import zipfile, xml.etree.ElementTree as ET, sys

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

with open(r'D:\Farangiz\metodica\all_paragraphs.txt', 'w', encoding='utf-8') as f:
    for i, p in enumerate(paragraphs):
        f.write(f'=== PARA [{i}] ===\n')
        f.write(p + '\n\n')

print(f'Jami: {len(paragraphs)} ta paragraf')
print('all_paragraphs.txt ga saqlandi')
