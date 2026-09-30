import win32com.client
import sys

def run():
    word = win32com.client.GetObject(Class='Word.Application')
    doc = None
    for d in word.Documents:
        if 'heru skripsi' in d.Name.lower():
            doc = d
            break
            
    if not doc:
        print("Document not found!")
        return

    # Find Paragraph indices
    p_babi = None
    p_latar = None
    p_rumusan = None
    p_tujuan = None
    p_batasan = None
    p_pustaka = None
    p_logbook = None

    for i in range(1, doc.Paragraphs.Count + 1):
        txt = doc.Paragraphs(i).Range.Text.strip()
        u = txt.upper()
        if i >= 120 and i <= 130 and 'PENDAHULUAN' in u and not p_babi:
            p_babi = i
        elif i >= 120 and i <= 130 and 'LATAR BELAKANG' in u and not p_latar:
            p_latar = i
        elif i >= 128 and i <= 136 and 'RUMUSAN MASALAH' in u and not p_rumusan:
            p_rumusan = i
        elif i >= 134 and i <= 142 and 'TUJUAN' in u and not p_tujuan:
            p_tujuan = i
        elif i >= 142 and i <= 152 and 'BATASAN' in u and not p_batasan:
            p_batasan = i
        elif i >= 380 and 'DAFTAR PUSTAKA' in u and not p_pustaka:
            p_pustaka = i
        elif i >= 400 and 'LOGBOOK PENELITIAN' in u and not p_logbook:
            p_logbook = i

    print(f"Indices found: BabI={p_babi}, Latar={p_latar}, Rumusan={p_rumusan}, Tujuan={p_tujuan}, Batasan={p_batasan}, Pustaka={p_pustaka}, Logbook={p_logbook}")
    
    with open(r"d:\SecondBrain\00_system\word_update_plan.txt", "w", encoding="utf-8") as f:
        f.write(f"BabI={p_babi}, Latar={p_latar}, Rumusan={p_rumusan}, Tujuan={p_tujuan}, Batasan={p_batasan}, Pustaka={p_pustaka}, Logbook={p_logbook}\n")

if __name__ == '__main__':
    run()
