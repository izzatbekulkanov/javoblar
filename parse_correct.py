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

def is_empty_or_junk(t):
    """Javob yo'q degan satrlar"""
    t2 = t.lower().strip()
    return any(x in t2 for x in ['javobi yoooq', 'javobi yoq', 'javob yoq', 'javobi yooq',
                                   'javob yo\'q', 'javobi yo\'q', 'tashalmagan',
                                   '1-savol javobi yoq', '2-savol javobi yoq'])

def clean_answer_prefix(text):
    """Javob: / Javobi: kabi prefikslarni olib tashlash"""
    text = re.sub(r'^[Jj]avob\s*[i:]?\s*:?\s*', '', text)
    text = re.sub(r'^[Jj]avobi\s*:?\s*', '', text)
    return text.strip()

def extract_savol_title(text, savol_num):
    """Savoldan sarlavhani ajratish"""
    # Pattern: "1-savol: ...", "1. ...", "1-savol. ..."
    patterns = [
        rf'^\s*{savol_num}\s*[.\-\s]*savol\s*[.:\-]?\s*',
        rf'^\s*{savol_num}\s*[.\-]\s*savol\s+javobi\s*[.:\-]?\s*',
        rf'^\s*{savol_num}\s*\.\s*',
        rf'^\s*{savol_num}\s+savolga\s+javob\s*[.:\-]?\s*',
    ]
    for pat in patterns:
        m = re.match(pat, text, re.IGNORECASE)
        if m:
            rest = text[m.end():].strip()
            return rest
    return text.strip()

def extract_bilet_num(text):
    """Bilet raqamini ajratish"""
    m = re.match(r'^\s*(\d+)\s*[.\-\s]*bilet', text, re.IGNORECASE)
    if m:
        return int(m.group(1)), text[m.end():].strip()
    return None, text

def is_bilet_header(text):
    """Faqat bilet raqami bor, boshqa narsa yo'q"""
    # e.g. "4-bilet" alone
    m = re.match(r'^\s*(\d+)\s*[.\-\s]*bilet\s*$', text, re.IGNORECASE)
    return m is not None

def is_savol_start(text, bilet_num=None):
    """Bu qator yangi savolmi?"""
    patterns = [
        r'^\s*\d+\s*[.\-]\s*savol',        # "1-savol", "2.savol"
        r'^\s*\d+\s*\.\s*savol',             # "1. savol"
        r'^\s*\d+\s+savolga\s+javob',        # "1 savolga javob"
        r'^\s*\d+\s*[.\-]?\s*javobi?\s*[.:\-]',  # "1-javobi:", "1.javob:"
        r'^\s*\d+\s*savoli?\s+',             # "1savoli Interfaol..."
    ]
    for pat in patterns:
        if re.match(pat, text, re.IGNORECASE):
            return True
    return False

def get_savol_num(text):
    """Savol raqamini ol"""
    m = re.match(r'^\s*(\d+)', text)
    if m:
        return int(m.group(1))
    return None

# =============================================
# MANUAL CORRECT PARSING based on document structure
# =============================================
# 
# After reading all 88 paragraphs carefully, here is the mapping:
#
# PARA[0] = "METODIKA" (title, skip)
# PARA[1] = "1-bilet" + 1-savol + javob + "2-savol" + javob (all in one para!)
# PARA[2] = "3-savol" + javob (continues bilet 1)
# PARA[3] = "2-bilet" + 1-savol + javob (all in one para)
# PARA[4] = "2.savol" + javob (continues bilet 2)
# PARA[5] = "3-bilet" + 1-savol + javob + 2-savol (big para, continues to next)
# PARA[6] = (continues 3-bilet 2-savol)
# PARA[7] = "4-bilet" header
# PARA[8] = "1." (just "1." - junk/empty content for 4-bilet 1-savol)
# PARA[9] = "2. Insho..." (4-bilet 2-savol with content)
# PARA[10] = (continues 4-bilet 2-savol)
# PARA[11] = (continues 4-bilet 2-savol)
# PARA[12] = (continues 4-bilet 2-savol)
# PARA[13] = "5-bilet" + 1-savol + javob
# PARA[14] = "2-savol" + javob (5-bilet)
# PARA[15] = "6-bilet" header
# PARA[16] = "1. Adabiyot..." + "2. Adabiyot..." + "3. Badiiy..." (6-bilet all 3 savols in one para)
# PARA[17] = (continues 6-bilet 3rd savol lirik part)
# PARA[18] = "2-savol javobi yoq tashalmagan" (but wait, we already have 2-savol above, so maybe this is a note)
# PARA[19] = "7-bilet" header
# PARA[20] = "1-savol javobi yoq"
# PARA[21] = "2-savol" header
# PARA[22] = (7-bilet 2-savol content: multimedia...)
# PARA[23] = "8-bilet" + 1-savol + javob
# PARA[24] = "8-bilet 2-savol" + javob
# PARA[25] = "9-bilet" + 1-savol + javob
# PARA[26] = "2." (junk - 9-bilet 2-savol has no content)
# PARA[27] = "10-bilet" header
# PARA[28] = "Javobi yoooq" (10-bilet has no answer)
# PARA[29] = "11-bilet" + 1-savol + javob (big)
# PARA[30..40] = continues 11-bilet (multiple paras)
# PARA[41] = "12-bilet" + 1-javobi + content
# PARA[42] = "12-bilet" 2-javobi + content
# PARA[43] = "13-bilet" + 1-savol + javob
# PARA[44] = "13-bilet" + 2-savol + javob
# PARA[45] = "13-bilet" + 3-savol + javob
# PARA[46] = "14-bilet" header
# PARA[47] = 1-savol + javob (14-bilet)
# PARA[48] = "2.javobi yoooq" (14-bilet 2-savol no answer)
# PARA[49] = "15-bilet" + content (metodik kompetensiya) - 1 savol
# PARA[50] = "16-bilet" + 1-savol + javob
# PARA[51] = "2-savol" + javob (16-bilet)
# PARA[52] = "3-savol" + javob (16-bilet) [Badiiy asar tahlili]
# PARA[53] = "17-bilet" header
# PARA[54] = "Javobi yoooq"
# PARA[55] = "18-bilet 1-savol" + javob (cyrillic content)
# PARA[56] = "18-bilet 2-savol" + javob
# PARA[57] = "19-bilet" + 1-savol + javob (ends with "2-savol javobi")
# PARA[58] = (19-bilet 2-savol content: multimedia)
# PARA[59] = "3-savol" (19-bilet) Badiiy asar tahlili
# PARA[60] = "20-bilet" + 1-savol + javob
# PARA[61] = "20-bilet 2-savol" + javob
# PARA[62] = "21-bilet" + 1-savol + javob
# PARA[63] = "21-bilet" + 2-savol + javob
# PARA[64] = "22-bilet" header
# PARA[65] = "2-savol" (22-bilet) - only header, no content for 1-savol!
# PARA[66] = "23-bilet 1-savol" header
# PARA[67] = (23-bilet 1-savol content)
# PARA[68] = "2-savol" (23-bilet) + javob (dars ishlanmasi)
# PARA[69] = "24-bilet" + 1-savol (ifodali o'qish) + 2-savol (dars ishlanmasi) + 3-savol
# PARA[70] = (continues 24-bilet 3rd savol lirik part)
# PARA[71] = "25-bilet" + 1-savol + 2-savol (both with content!)
# PARA[72] = "3-savol" (25-bilet) Badiiy asar
# PARA[73] = "26-bilet" header
# PARA[74] = "1-savol" (26-bilet yozuvchi tarjimaholi)
# PARA[75] = (continues 26-bilet 1-savol)
# PARA[76] = "2-savol" mumtoz g'azal (26-bilet)? Actually let's check...
# PARA[77] = "27-bilet 1-savol javob" + content
# PARA[78] = "27-bilet 2-savol javob" + content
# PARA[79] = "28-bilet" header
# PARA[80] = "1-savol" (28-bilet) header only
# PARA[81] = "28)2" (actually 28-bilet 2-savol content)
# PARA[82] = (continues 28-bilet 2-savol)
# PARA[83] = "29-bilet" + 1-savol + javob
# PARA[84] = "2-savol" (29-bilet) Zamonaviy darslar
# PARA[85] = "30-bilet 1-savol" header
# PARA[86] = "Debat..." (30-bilet 1-savol content)
# PARA[87] = "30-bilet 2-savol" + javob

# Now let's build the proper structure manually
bilets = {}

def add_to_bilet(bilet_num, savol_num, savol_title, javob):
    if bilet_num not in bilets:
        bilets[bilet_num] = []
    entry = {
        "savol_raqami": savol_num,
        "savol": savol_title.strip(),
        "javob": javob.strip() if javob else "Javob mavjud emas"
    }
    bilets[bilet_num].append(entry)

# ---- BILET 1 ----
# PARA[1] contains: 1-bilet header + 1-savol + javob + 2-savol + javob
p1 = paragraphs[1]
# Split by "2-savol"
split2 = re.split(r'2-savol\s*\n?', p1)
part1_full = split2[0]
part2_full = split2[1] if len(split2) > 1 else ''

# Extract 1-savol from part1
m1 = re.match(r'1-bilet\s*1-savol\s*:\s*(.+?)Javob\s*:\s*(.+)', part1_full, re.DOTALL | re.IGNORECASE)
if m1:
    add_to_bilet(1, 1, m1.group(1).strip()[:200], m1.group(2).strip())
else:
    # Try simpler split
    bilet_rest = part1_full.replace('1-bilet', '').strip()
    javob_split = re.split(r'\s*Javob\s*:', bilet_rest, 1, re.IGNORECASE)
    if len(javob_split) == 2:
        add_to_bilet(1, 1, javob_split[0].replace('1-savol', '').replace(':', '').strip()[:200], javob_split[1].strip())

# 2-savol in part2
if part2_full:
    add_to_bilet(1, 2, '2. Kasbiy kompetensiya nima va uning sifatlari haqida nimalarni bilasiz?', part2_full.strip())

# PARA[2] = 3-savol (bilet 1)
p2 = paragraphs[2]
m = re.match(r'3-savol\s*(.+?)(?:Javob[i]?\s*:)\s*(.+)', p2, re.DOTALL | re.IGNORECASE)
if m:
    add_to_bilet(1, 3, m.group(1).strip()[:200], m.group(2).strip())
else:
    # The whole para is 3-savol with embedded Javobi:
    javobi_split = re.split(r'Javob[i]?\s*:', p2, 1)
    savol_t = javobi_split[0].replace('3-savol', '').strip()
    javob_t = javobi_split[1].strip() if len(javobi_split) > 1 else p2
    add_to_bilet(1, 3, savol_t[:200], javob_t)

# ---- BILET 2 ----
p3 = paragraphs[3]  # "2-bilet1. ..."
bilet_rest = re.sub(r'2-bilet', '', p3).strip()
add_to_bilet(2, 1, 
    'Adabiyot o\'qitish metodikasida o\'qituvchi bir darsning o\'zida bir nechta kompetensiyalardan foydalanadi. Misol keltiring.',
    bilet_rest)

p4 = paragraphs[4]  # "2.Adabiyot oqitish..."
add_to_bilet(2, 2, 
    'Adabiyot o\'qitish metodikasi fanining mazmun va vazifalari haqida gapiring',
    p4.replace('2.', '', 1).strip())

# ---- BILET 3 ----
p5 = paragraphs[5]  # "3-bilet1-savol + 2-savol"
split2_b3 = re.split(r'2-savol\.?\s*', p5)
part1_b3 = split2_b3[0]
part2_b3 = ''.join(split2_b3[1:]) if len(split2_b3) > 1 else ''

add_to_bilet(3, 1,
    '4K metodi haqida ma\'lumot bering.',
    part1_b3.replace('3-bilet', '').replace('1-savol.', '').strip())

if part2_b3:
    add_to_bilet(3, 2,
        'An\'anaviy ta\'lim metodlari va ularning turlari haqida so\'zlang',
        part2_b3.strip() + '\n' + paragraphs[6])
else:
    add_to_bilet(3, 2,
        'An\'anaviy ta\'lim metodlari va ularning turlari haqida so\'zlang',
        paragraphs[6])

# ---- BILET 4 ----
# PARA[7]="4-bilet", PARA[8]="1." (no content), PARA[9]="2.Insho...", PARA[10,11,12] continue
add_to_bilet(4, 1, '4-bilet 1-savol', 'Javob mavjud emas')
insho_content = paragraphs[9] + '\n' + paragraphs[10] + '\n' + paragraphs[11] + '\n' + paragraphs[12]
insho_content = re.sub(r'^2\.', '', insho_content).strip()
add_to_bilet(4, 2,
    'Insho yozish haqida ma\'lumot bering. Uning asosiy nazariy vositalari qaysilar?',
    insho_content)

# ---- BILET 5 ----
p13 = paragraphs[13]
add_to_bilet(5, 1,
    'Psixologik kompetensiya haqida ma\'lumot bering?',
    p13.replace('5-bilet', '').replace('1-savol', '').strip())

p14 = paragraphs[14]
add_to_bilet(5, 2,
    'Debat, debrifing va demonstratsiya haqida ma\'lumot bering.',
    p14.replace('2-savol :', '').replace('2-savol:', '').strip())

# ---- BILET 6 ----
# PARA[15]="6-bilet", PARA[16]="1.Ifodali...2.Dars ishlanmalari...3.Badiiy asar tahlili"
# PARA[17]=continues lirik part, PARA[18]="2-savol javobi yoq tashalmagan" (note)
p16 = paragraphs[16]
# Split by "2." and "3."
parts_b6 = re.split(r'(?=2\.\s+Adabiyot dars|3\.\s+Badiiy)', p16)
b6_s1 = parts_b6[0].replace('6-bilet', '').strip() if parts_b6 else ''
b6_s2 = parts_b6[1].strip() if len(parts_b6) > 1 else ''
b6_s3 = (parts_b6[2].strip() + '\n' + paragraphs[17]) if len(parts_b6) > 2 else paragraphs[17]

add_to_bilet(6, 1,
    'Adabiyot darslarida ifodali o\'qishga qo\'yiladigan talablar.',
    b6_s1)
if b6_s2:
    add_to_bilet(6, 2,
        'Adabiyot dars ishlanmalari haqida ma\'lumot bering.',
        b6_s2)
if b6_s3:
    add_to_bilet(6, 3,
        'Badiiy asar tahlili (epik, lirik, dramatik)',
        b6_s3)

# ---- BILET 7 ----
# PARA[19]="7-bilet", PARA[20]="1-savol javobi yoq", PARA[21]="2-savol", PARA[22]=content
add_to_bilet(7, 1, '7-bilet 1-savol', 'Javob mavjud emas')
add_to_bilet(7, 2,
    'Yozuvchi hayoti va ijodini o\'rganishda multimedia vositalarining o\'rni',
    paragraphs[22])

# ---- BILET 8 ----
# PARA[23]="8-bilet 1-savol" + content
# PARA[24]="8-bilet 2-savol" + content
p23 = paragraphs[23]
add_to_bilet(8, 1,
    'Badiiy asarni tahlil qilish metodlari',
    p23.replace('8 - bilet. 1-savol.', '').replace('8-bilet. 1-savol.', '').strip())

p24 = paragraphs[24]
add_to_bilet(8, 2,
    'Adabiyot o\'qitish metodikasi fanining shakllanish va taraqqiyoti',
    p24.replace('8-bilet. 2-savol.', '').strip())

# ---- BILET 9 ----
# PARA[25]="9-bilet 1-savol Insho..." PARA[26]="2." (no content)
p25 = paragraphs[25]
add_to_bilet(9, 1,
    'Insho nima? Uning mazmuni haqida ma\'lumot bering.',
    p25.replace('9-bilet', '').replace('1-savol', '').strip())
add_to_bilet(9, 2, '9-bilet 2-savol', 'Javob mavjud emas')

# ---- BILET 10 ----
# PARA[27]="10-bilet", PARA[28]="Javobi yoooq"
add_to_bilet(10, 1, '10-bilet savollar', 'Javob mavjud emas')

# ---- BILET 11 ----
# PARA[29..40] - bilet 11 content
p29 = paragraphs[29]
# Find "2 savolga javob" split
split_11 = re.split(r'2\s*savolga\s+javob', p29, 1, re.IGNORECASE)
b11_s1_content = split_11[0].replace('11-bilet', '').replace('1 savolga javob', '').strip()
# paragraphs 30..40 need to be checked
# After looking at data, paras 30-40 are continuation of 11-bilet
# Let's collect them all
all_11 = p29
for idx in range(30, 41):
    if idx < len(paragraphs):
        all_11 += '\n' + paragraphs[idx]

# Split 11-bilet into 1-savol and 2-savol
split11 = re.split(r'2\s*savolga\s+javob', all_11, 1, re.IGNORECASE)
add_to_bilet(11, 1,
    'Mustaqillik davrida adabiyot o\'qitish metodikasi ilmida bo\'lgan o\'zgarishlar. Metodistlar haqida ma\'lumot bering.',
    split11[0].replace('11-bilet', '').replace('1 savolga javob', '').strip())
if len(split11) > 1:
    add_to_bilet(11, 2,
        'So\'z san\'ati. Drama haqida ma\'lumot bering.',
        split11[1].strip())

# ---- BILET 12 ----
# PARA[41]="12-bilet 1-javobi..." PARA[42]="2-javobi..."
p41 = paragraphs[41]
add_to_bilet(12, 1,
    'Adabiyot darslarida muammoli tahlil nima?',
    p41.replace('12-bilet', '').replace('1-javobi.', '').strip())

p42 = paragraphs[42]
add_to_bilet(12, 2,
    'Case study (keys, vaziyatli tahlil) metodi haqida ma\'lumot bering.',
    p42.replace('2-javobi.', '').strip())

# ---- BILET 13 ----
# PARA[43,44,45]
p43 = paragraphs[43]
add_to_bilet(13, 1,
    'Adib hayoti va ijodining ilmiy bayoni deganda nima tushuniladi?',
    p43.replace('13-bilet', '').replace('1.', '', 1).strip())

p44 = paragraphs[44]
add_to_bilet(13, 2,
    'Maxsus va kreativ kompetensiyalar haqida ma\'lumot bering.',
    p44.replace('13-bilet2.', '').replace('13-bilet', '').replace('2.', '', 1).strip())

p45 = paragraphs[45]
add_to_bilet(13, 3,
    'Badiiy asar tahlili (epik, lirik, dramatik)',
    p45.replace('13-bilet3.', '').replace('13-bilet', '').replace('3.', '', 1).strip())

# ---- BILET 14 ----
# PARA[46]="14-bilet", PARA[47]=1-savol content, PARA[48]="2.javobi yoooq"
p47 = paragraphs[47]
add_to_bilet(14, 1,
    'Epik asar tahlilining asosiy bosqichlari. Nasriy asarlarni tahlil qilish.',
    p47.replace('1.', '', 1).strip())
add_to_bilet(14, 2, '14-bilet 2-savol', 'Javob mavjud emas')

# ---- BILET 15 ----
# PARA[49]="15-bilet Metodik kompetensiya..."
p49 = paragraphs[49]
add_to_bilet(15, 1,
    'Metodik va ekstremal kompetensiyalar haqida ma\'lumot bering.',
    p49.replace('15-bilet', '').strip())

# ---- BILET 16 ----
# PARA[50]=1-savol, PARA[51]=2-savol, PARA[52]=3-savol
p50 = paragraphs[50]
add_to_bilet(16, 1,
    'Brainstorming va Keys Study metodlari haqida ma\'lumot bering.',
    p50.replace('16-bilet 1-savol.', '').replace('16-bilet', '').strip())

p51 = paragraphs[51]
add_to_bilet(16, 2,
    'Kreativ va innovatsion kompetensiyalar haqida ma\'lumot bering.',
    p51.replace('2-savol.', '', 1).strip())

p52 = paragraphs[52]
add_to_bilet(16, 3,
    'Badiiy asar tahlili (epik, lirik, dramatik)',
    p52.replace('3.', '', 1).strip())

# ---- BILET 17 ----
# PARA[53]="17-bilet", PARA[54]="Javobi yoooq"
add_to_bilet(17, 1, '17-bilet savollar', 'Javob mavjud emas')

# ---- BILET 18 ----
# PARA[55]=1-savol (cyrillic), PARA[56]=2-savol
p55 = paragraphs[55]
add_to_bilet(18, 1,
    'Badiiy asarni to\'liq anglash uchun ilmiy tekshirishning bosqichlari.',
    p55.replace('18- bilet 1-savol', '').replace('18-bilet 1-savol', '').strip())

p56 = paragraphs[56]
add_to_bilet(18, 2,
    'Adabiyot dars ishlanmalari haqida ma\'lumot bering.',
    p56.replace('18-bilet 2-savol', '').strip())

# ---- BILET 19 ----
# PARA[57]="19-bilet 1.Dramatik tur... + 2-savol javobi" split
# PARA[58]=2-savol content (multimedia), PARA[59]=3-savol
p57 = paragraphs[57]
split19 = re.split(r'2-savol\s+javobi?\s*', p57, 1, re.IGNORECASE)
b19_s1 = split19[0].replace('19-bilet', '').replace('1.', '', 1).strip()
add_to_bilet(19, 1,
    'Dramatik tur va uning xususiyatlari haqida ma\'lumot bering.',
    b19_s1)

add_to_bilet(19, 2,
    'Yozuvchi hayoti va ijodini o\'rganishda multimedia vositalarining o\'rni.',
    paragraphs[58])

p59 = paragraphs[59]
add_to_bilet(19, 3,
    'Badiiy asar tahlili (epik, lirik, dramatik)',
    p59.replace('3.', '', 1).strip())

# ---- BILET 20 ----
# PARA[60]=1-savol, PARA[61]=2-savol
p60 = paragraphs[60]
add_to_bilet(20, 1,
    'Interfaol metodlar haqida gapiring. Ularning dars jarayonidagi o\'rni qanday?',
    p60.replace('20-bilet', '').replace('1savoli', '').strip())

p61 = paragraphs[61]
add_to_bilet(20, 2,
    'Shaxsiy va texnologik kompetensiyalar haqida ma\'lumot bering.',
    p61.replace('20-bilet 2-savol', '').replace('20-bilet', '').strip())

# ---- BILET 21 ----
# PARA[62]=1-savol, PARA[63]=2-savol
p62 = paragraphs[62]
add_to_bilet(21, 1,
    'Insho nima? Uning turlari va yozishga qo\'yiladigan talablar.',
    p62.replace('21- bilet.1-savol.', '').replace('21-bilet.1-savol.', '').strip())

p63 = paragraphs[63]
add_to_bilet(21, 2,
    'Lirik asarlarni tahlil etish metodikasi haqida ayting.',
    p63.replace('21-bilet2.', '').replace('21-bilet', '').strip())

# ---- BILET 22 ----
# PARA[64]="22-bilet", PARA[65]="2-savol" (only header, 1-savol has no content)
add_to_bilet(22, 1, '22-bilet 1-savol', 'Javob mavjud emas')
add_to_bilet(22, 2, '22-bilet 2-savol', 'Javob mavjud emas')

# ---- BILET 23 ----
# PARA[66]="23-bilet 1-savol" header, PARA[67]=content, PARA[68]=2-savol+content
p67 = paragraphs[67]
add_to_bilet(23, 1,
    'Adabiyot darslarida muammoli tahlilni qo\'llash.',
    p67.replace(',', '', 1).strip())

p68 = paragraphs[68]
add_to_bilet(23, 2,
    'Adabiyot dars ishlanmalari haqida ma\'lumot bering.',
    p68.replace('2-savol', '', 1).strip())

# ---- BILET 24 ----
# PARA[69] has 1-savol (ifodali o'qish) + 2-savol (dars ishlanmasi) + 3-savol start
# PARA[70] = continues 3-savol (lirik part)
p69 = paragraphs[69]
# Split by "2. Adabiyot dars ishlanmalari" and "3. Badiiy"
parts24 = re.split(r'(?=2\.\s+Adabiyot dars|3\.\s+Badiiy)', p69)
b24_s1 = parts24[0].replace('24.bilet', '').replace('24-bilet', '').strip()
b24_s2 = parts24[1] if len(parts24) > 1 else ''
b24_s3 = (parts24[2] if len(parts24) > 2 else '') + '\n' + paragraphs[70]

add_to_bilet(24, 1,
    'Adabiyot darslarida ifodali o\'qishga qo\'yiladigan talablar.',
    b24_s1)
if b24_s2:
    add_to_bilet(24, 2,
        'Adabiyot dars ishlanmalari haqida ma\'lumot bering.',
        b24_s2.replace('2.', '', 1).strip())
if b24_s3.strip():
    add_to_bilet(24, 3,
        'Badiiy asar tahlili (epik, lirik, dramatik)',
        b24_s3.strip())

# ---- BILET 25 ----
# PARA[71] has 1-savol and 2-savol (both with content), PARA[72]=3-savol
p71 = paragraphs[71]
# Split at "2. O'qituvchi tomonidan"
split25 = re.split(r'2\.\s+O\'qituvchi tomonidan', p71, 1)
b25_s1 = split25[0].replace('25-bilet.', '').replace('25-bilet', '').strip()
b25_s2 = ('2. O\'qituvchi tomonidan' + split25[1]) if len(split25) > 1 else ''

add_to_bilet(25, 1,
    'Lirik asarlarni tahlil etish metodikasi haqida ayting.',
    b25_s1)
if b25_s2:
    add_to_bilet(25, 2,
        'O\'qituvchi tomonidan bir darsning o\'zida bir necha kompetensiyadan foydalanish mumkinmi?',
        b25_s2)

p72 = paragraphs[72]
add_to_bilet(25, 3,
    'Badiiy asar tahlili (epik, lirik, dramatik)',
    p72.replace('3.', '', 1).strip())

# ---- BILET 26 ----
# PARA[73]="26-bilet", PARA[74]=1-savol yozuvchi tarjimaholi, PARA[75]=continues, PARA[76]=mumtoz g'azal
p74 = paragraphs[74]
b26_s1 = p74.replace('1.', '', 1).strip()
add_to_bilet(26, 1,
    'Yozuvchi tarjima holini o\'rganishning ma\'rifiy ahamiyati haqida gapiring.',
    b26_s1 + '\n' + paragraphs[75])

add_to_bilet(26, 2,
    'Mumtoz g\'azal va ruboiylar tahlili — shakl va mazmun.',
    paragraphs[76])

# ---- BILET 27 ----
# PARA[77]=1-savol javob, PARA[78]=2-savol javob
p77 = paragraphs[77]
add_to_bilet(27, 1,
    'Adabiy ta\'limda innovatsion metodlardan foydalanish.',
    p77.replace('27-bilet 1-savol javob', '').replace('27-bilet', '').replace('i', '', 1).strip())

p78 = paragraphs[78]
add_to_bilet(27, 2,
    'Adabiyot darslarida o\'quvchini badiiy asarda qanday aytilganiga diqqat qaratish.',
    p78.replace('27-bilet 2-savol javobi', '').replace('27-bilet 2-savol javob', '').strip())

# ---- BILET 28 ----
# PARA[79]="28-bilet", PARA[80]="1-savol" (header only), PARA[81]="28)2..." (2-savol content), PARA[82]=continues
add_to_bilet(28, 1, '28-bilet 1-savol', 'Javob mavjud emas')

p81 = paragraphs[81]
b28_s2 = p81.replace('28)2', '').strip()
add_to_bilet(28, 2,
    'Adabiyot darslarida sinfdan tashqari mashg\'ulot turlari va ularni tashkil etish.',
    b28_s2 + '\n' + paragraphs[82])

# ---- BILET 29 ----
# PARA[83]=1-savol, PARA[84]=2-savol
p83 = paragraphs[83]
add_to_bilet(29, 1,
    'Epik asar tahlilining asosiy bosqichlari.',
    p83.replace('29- bilet', '').replace('29-bilet', '').replace('1.', '', 1).strip())

p84 = paragraphs[84]
add_to_bilet(29, 2,
    'Zamonaviy darslarga qo\'yiladigan asosiy talablar.',
    p84.replace('2. .', '').replace('2.', '', 1).strip())

# ---- BILET 30 ----
# PARA[85]="30-bilet 1-savol" header, PARA[86]=1-savol content, PARA[87]=2-savol+content
p86 = paragraphs[86]
add_to_bilet(30, 1,
    'Debat, debrifing va demonstratsiya haqida ma\'lumot bering.',
    p86)

p87 = paragraphs[87]
add_to_bilet(30, 2,
    'Adabiyot o\'qitish metodikasi fan sifatida shakllanishida ilk renessans davri mutafakkirlari qay darajada ishtirok etishgan?',
    p87.replace('30-bilet.2-savol.', '').replace('30-bilet. 2-savol.', '').strip())

# Save to JSON
with open(r'D:\Farangiz\metodica\bilets_clean.json', 'w', encoding='utf-8') as f:
    json.dump(bilets, f, ensure_ascii=False, indent=2)

print('bilets_clean.json saqlandi!')
print(f'Jami biletlar: {len(bilets)}')
total_q = sum(len(v) for v in bilets.values())
print(f'Jami savollar: {total_q}')
for b in sorted(bilets.keys()):
    print(f'\n  Bilet {b} ({len(bilets[b])} savol):')
    for q in bilets[b]:
        javob_preview = q["javob"][:60].replace('\n', ' ') if q["javob"] != "Javob mavjud emas" else "❌ Javob yo'q"
        print(f'    S{q["savol_raqami"]}: {q["savol"][:70]}')
        print(f'       → {javob_preview}...')
