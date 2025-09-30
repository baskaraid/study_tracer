import pandas as pd

# Ganti sesuai nama file Excel
excel_file = "Master_Kota.xlsx"
df = pd.read_excel(excel_file)

# Nama kolom persis dari Excel
prov_col = "Kode Provinsi"
kode_col = "Kode Kota/Kabupaten"
nama_col = "Nama Kota/Kabupaten"
prov_name_col = "Nama Provinsi"  # kalau ada

# Output file
output_file = "templates/kota.html"

with open(output_file, "w", encoding="utf-8") as f:
    f.write('<option value="">-- Pilih Kota/Kabupaten --</option>\n')

    for prov_id, group in df.groupby(prov_col):
        prov_name = str(group[prov_name_col].iloc[0]) if prov_name_col in df.columns else prov_id
        f.write(f'<optgroup label="{prov_name}" data-prov="{prov_id}">\n')

        for _, row in group.iterrows():
            kode = str(row[kode_col]).strip()
            nama = str(row[nama_col]).strip()
            f.write(f'  <option value="{kode}">{nama}</option>\n')

        f.write('</optgroup>\n')

print(f"✅ Berhasil generate {output_file} dengan grouping provinsi")
