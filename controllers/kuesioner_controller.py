from flask import Blueprint, render_template, request, redirect, url_for, session
from models.kuesioner_model import KuesionerModel
from config import get_db_connection
from helpers.kota_helper import load_kota_mapping
from flask import Response, send_file
import io
from openpyxl import Workbook
from flask import flash

kuesioner_bp = Blueprint("kuesioner", __name__)

# ===========================
# Untuk dosen (harus login)
# ===========================
@kuesioner_bp.route("dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    statistik = KuesionerModel.count_by_prodi()
    data = KuesionerModel.get_all()
    return render_template("admin/dashboard.html", data=data, statistik=statistik)

@kuesioner_bp.route("/tracer")
def tracer_menu():
    """
    Route untuk menampilkan menu Tracer:
    - Tracer Studi Alumni
    - Tracer Pengguna Lulusan (StakeHolder)
    """
    return render_template("utama.html")

@kuesioner_bp.route("/sebaran")
def sebaran():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    # ================= Provinsi =================
    query = """
    SELECT 
        CASE f5a1
            WHEN 100000 THEN 'Prov. Jambi'
            WHEN 200000 THEN 'Prov. Sulawesi Tenggara'
            WHEN 210000 THEN 'Prov. Maluku'
            WHEN 320000 THEN 'Prov. Papua Barat'
            WHEN 330000 THEN 'Prov. Sulawesi Barat'
            WHEN 350000 THEN 'Luar Negeri'
            WHEN 300000 THEN 'Prov. Gorontalo'
            WHEN 180000 THEN 'Prov. Sulawesi Tengah'
            WHEN 190000 THEN 'Prov. Sulawesi Selatan'
            WHEN 270000 THEN 'Prov. Maluku Utara'
            WHEN 280000 THEN 'Prov. Banten'
            WHEN 170000 THEN 'Prov. Sulawesi Utara'
            WHEN 250000 THEN 'Prov. Papua'
            WHEN 260000 THEN 'Prov. Bengkulu'
            WHEN 240000 THEN 'Prov. Nusa Tenggara Timur'
            WHEN 110000 THEN 'Prov. Sumatera Selatan'
            WHEN 290000 THEN 'Prov. Kepulauan Bangka Belitung'
            WHEN 120000 THEN 'Prov. Lampung'
            WHEN 130000 THEN 'Prov. Kalimantan Barat'
            WHEN 340000 THEN 'Prov. Kalimantan Utara'
            WHEN 310000 THEN 'Prov. Kepulauan Riau'
            WHEN 160000 THEN 'Prov. Kalimantan Timur'
            WHEN 230000 THEN 'Prov. Nusa Tenggara Barat'
            WHEN 140000 THEN 'Prov. Kalimantan Tengah'
            WHEN 150000 THEN 'Prov. Kalimantan Selatan'
            WHEN 220000 THEN 'Prov. Bali'
            WHEN 10000  THEN 'Prov. D.K.I. Jakarta'
            WHEN 40000  THEN 'Prov. D.I. Yogyakarta'
            WHEN 60000  THEN 'Prov. Aceh'
            WHEN 20000  THEN 'Prov. Jawa Barat'
            WHEN 90000  THEN 'Prov. Riau'
            WHEN 30000  THEN 'Prov. Jawa Tengah'
            WHEN 50000  THEN 'Prov. Jawa Timur'
            WHEN 80000  THEN 'Prov. Sumatera Barat'
            WHEN 70000  THEN 'Prov. Sumatera Utara'
            ELSE 'Tidak Diketahui'
        END AS provinsi,
        COUNT(*) AS jumlah,
        f5a1 AS kode
    FROM kuesioner
    WHERE f5a1 IS NOT NULL AND f5a1 <> ''
    GROUP BY f5a1
    ORDER BY jumlah DESC;
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    prov_labels = [row[0] for row in rows]
    prov_data = [row[1] for row in rows]

    # ================= Pendapatan =================
    cursor.execute("SELECT f505 FROM kuesioner WHERE f505 IS NOT NULL")
    gaji_rows = cursor.fetchall()
    bawah_1_5 = sum(1 for r in gaji_rows if int(r[0]) < 1500000)
    satu_5_3 = sum(1 for r in gaji_rows if 1500000 <= int(r[0]) <= 3000000)
    di_atas_3 = sum(1 for r in gaji_rows if int(r[0]) > 3000000)
    pendapatan_data = {
        "bawah_1_5": bawah_1_5,
        "satu_5_3": satu_5_3,
        "di_atas_3": di_atas_3
    }

    # ================= f502 (bulan dapat kerja pertama) =================
    cursor.execute("SELECT nim, nama, f502 FROM kuesioner WHERE f502 IS NOT NULL AND f502 <> ''")
    f502_rows = cursor.fetchall()
    hijau = sum(1 for r in f502_rows if int(r[2]) <= 3)
    kuning = sum(1 for r in f502_rows if 6 <= int(r[2]) <= 12)
    merah = sum(1 for r in f502_rows if int(r[2]) > 12)
    kategori_f502 = {"hijau": hijau, "kuning": kuning, "merah": merah}

    conn.close()

    return render_template(
        "admin/sebaran.html",
        rows=rows,
        prov_labels=prov_labels,
        prov_data=prov_data,
        pendapatan_data=pendapatan_data,
        kategori_f502=kategori_f502,
        f502_rows=f502_rows
    )



@kuesioner_bp.route("/sebaran/detail/<kode_prov>")
def detail_sebaran(kode_prov):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nama, f5a2, nim, email, hp 
        FROM kuesioner
        WHERE f5a1 = %s
    """, (kode_prov,))
    mahasiswa = cursor.fetchall()
    conn.close()

    # Ambil mapping dari kota.html
    kota_map = load_kota_mapping()

    # Replace kode kota → nama kota
    mahasiswa_fix = []
    for mhs in mahasiswa:
        nama, kode_kota, nim, email, hp = mhs
        nama_kota = kota_map.get(str(kode_kota), kode_kota)
        mahasiswa_fix.append((nama, nama_kota, nim, email, hp))

    return render_template("admin/detail_sebaran.html", mahasiswa=mahasiswa_fix)



@kuesioner_bp.route("data_responden")
def data_responden():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    statistik = KuesionerModel.count_by_prodi()
    data = KuesionerModel.get_all()
    return render_template("admin/data_responden.html", data=data, statistik=statistik)

@kuesioner_bp.route("/unduh_data")
def unduh_data_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("admin/unduh_data.html")

@kuesioner_bp.route("/unduh_data/download")
def unduh_data_download():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Daftar kolom sesuai urutan yang kamu mau di Excel
    columns = [
        "kode_pt","kode_prodi","nim","nama","hp","email","tahun_lulus","nik","npwp",
        "f8","f502","f505","f5a1","f5a2","f1101","f1102","f5b","f5c","f5d",
        "f18a","f18b","f18c","f18d","f1201","f1202","f14","f15",
        "f1761","f1762","f1763","f1764","f1765","f1766","f1767","f1768","f1769","f1770","f1771","f1772","f1773","f1774",
        "f21","f22","f23","f24","f25","f26","f27",
        "f301","f302","f303",
        "f401","f402","f403","f404","f405","f406","f407","f408","f409","f410","f411","f412","f413","f414","f415","f416",
        "f6","f7","f7a","f1001","f1002",
        "f1601","f1602","f1603","f1604","f1605","f1606","f1607","f1608","f1609","f1610","f1611","f1612","f1613","f1614"
    ]

    # Query dengan kolom urut
    cursor.execute(f"SELECT {', '.join(columns)} FROM kuesioner")
    rows = cursor.fetchall()
    conn.close()

    # Buat workbook Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Kuesioner"

    # Header
    header_mapping = {
        "kode_pt": "Kode PT",
        "kode_prodi": "Kode Prodi",
        "nim": "NIM/Nomor Mahasiswa",
    }
    ws.append([header_mapping.get(col, col.upper()) for col in columns])

    # Tambahkan data baris per baris, PAKSA semua ke string
    for row in rows:
        ws.append([str(val) if val is not None else "" for val in row])

    # Semua kolom diformat sebagai TEXT
    for col_idx in range(1, len(columns) + 1):
        for cell in ws.iter_cols(min_col=col_idx, max_col=col_idx, min_row=2):
            for c in cell:
                c.number_format = "@"

    # Simpan ke memory
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="kuesioner_data.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )




# ===========================
# Untuk mahasiswa (tanpa login)
# ===========================
@kuesioner_bp.route("/isi", methods=["GET", "POST"])
def isi():
    if request.method == "POST":
        nik = request.form.get("nik", "").strip()

        # Validasi wajib isi NIK
        if not nik:
            flash("⚠️ NIK wajib diisi!", "warning")
            return redirect(url_for("kuesioner.isi"))

        # Cek apakah NIK sudah dipakai
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM kuesioner WHERE nik = %s", (nik,))
        exists = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if exists > 0:
            flash("❌ NIK ini sudah digunakan oleh mahasiswa lain!", "danger")
            return redirect(url_for("kuesioner.isi"))

        # Kalau valid → simpan data diri minimal
        session["data_diri"] = {
            "kode_pt": request.form.get("kode_pt", ""),
            "kode_prodi": request.form.get("kode_prodi", ""),
            "nim": "0",   # selalu 0 walaupun ada field di form
            "nama": request.form.get("nama", ""),
            "hp": request.form.get("hp", ""),
            "email": request.form.get("email", ""),
            "tahun_lulus": request.form.get("tahun_lulus", ""),
            "nik": nik,
            "npwp": "0"   # selalu 0 walaupun ada field di form
        }

        return redirect(url_for("kuesioner.isi_pertanyaan"))

    return render_template("kuesioner_data_diri.html")



@kuesioner_bp.route("/pertanyaan", methods=["GET", "POST"])
def isi_pertanyaan():
    if request.method == "POST":
        form_data = (
            request.form.get("f8", "0"),
            request.form.get("f502", "0"),
            request.form.get("f505", "0"),
            request.form.get("f5a1", "0"),
            request.form.get("f5a2", "0"),
            request.form.get("f1101", "0"),
            request.form.get("f1102", "0"),
            request.form.get("f5b", "0"),
            request.form.get("f5c", "0"),
            request.form.get("f5d", "0"),
            request.form.get("f18a", "0"),
            request.form.get("f18b", "0"),
            request.form.get("f18c", "0"),
            request.form.get("f18d", "0"),
            request.form.get("f1201", "0"),
            request.form.get("f1202", "0"),
            request.form.get("f14", "0"),
            request.form.get("f15", "0"),
            request.form.get("f1761", "0"),
            request.form.get("f1762", "0"),
            request.form.get("f1763", "0"),
            request.form.get("f1764", "0"),
            request.form.get("f1765", "0"),
            request.form.get("f1766", "0"),
            request.form.get("f1767", "0"),
            request.form.get("f1768", "0"),
            request.form.get("f1769", "0"),
            request.form.get("f1770", "0"),
            request.form.get("f1771", "0"),
            request.form.get("f1772", "0"),
            request.form.get("f1773", "0"),
            request.form.get("f1774", "0"),
            request.form.get("f21", "0"),
            request.form.get("f22", "0"),
            request.form.get("f23", "0"),
            request.form.get("f24", "0"),
            request.form.get("f25", "0"),
            request.form.get("f26", "0"),
            request.form.get("f27", "0"),
            request.form.get("f301", "0"),
            request.form.get("f302", "0"),
            request.form.get("f303", "0"),
            
            request.form.get("f401", "0"),
            request.form.get("f402", "0"),
            request.form.get("f403", "0"),
            request.form.get("f404", "0"),
            request.form.get("f405", "0"),
            request.form.get("f406", "0"),
            request.form.get("f407", "0"),
            request.form.get("f408", "0"),
            request.form.get("f409", "0"),
            request.form.get("f410", "0"),
            request.form.get("f411", "0"),
            request.form.get("f412", "0"),
            request.form.get("f413", "0"),
            request.form.get("f414", "0"),
            request.form.get("f415", "0"),
            request.form.get("f416", "0"),   # ini text input, jadi default string kosong
            request.form.get("f6", "0"),
            request.form.get("f7", "0"),
            request.form.get("f7a", "0"),
            request.form.get("f1001", "0"),
            request.form.get("f1002", "0"), 
            
            request.form.get("f1601", "0"),
            request.form.get("f1602", "0"),
            request.form.get("f1603", "0"),
            request.form.get("f1604", "0"),
            request.form.get("f1605", "0"),
            request.form.get("f1606", "0"),
            request.form.get("f1607", "0"),
            request.form.get("f1608", "0"),
            request.form.get("f1609", "0"),
            request.form.get("f1610", "0"),
            request.form.get("f1611", "0"),
            request.form.get("f1612", "0"),
            request.form.get("f1613", "0"),  # Checkbox "Lainnya"
            request.form.get("f1614", "0"),   # Input teks jika memilih "Lainnya"


        )

        # Ambil data diri dari session
        data_diri = session.get("data_diri")

        if data_diri:
            # Simpan data diri + pertanyaan sekaligus ke database
            KuesionerModel.insert_full(data_diri, form_data)

            # Hapus session agar tidak dobel
            session.pop("data_diri", None)

        return render_template("thank_you.html")
    return render_template("kuesioner_pertanyaan.html")
