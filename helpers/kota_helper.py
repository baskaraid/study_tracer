from bs4 import BeautifulSoup

def load_kota_mapping():
    mapping = {}
    with open("templates/kota.html", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for opt in soup.find_all("option"):
        if opt.get("value"):
            kode = opt["value"].strip()
            nama = opt.text.strip()
            mapping[kode] = nama
    return mapping
