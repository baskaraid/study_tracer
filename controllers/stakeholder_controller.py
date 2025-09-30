from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.stakeholder_model import StakeholderModel

stakeholder_bp = Blueprint("stakeholder", __name__)


@stakeholder_bp.route("data_responden")
def data_responden():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    statistik = StakeholderModel.count_by_prodi()
    data = StakeholderModel.get_all()
    return render_template("admin/data_responden_pengguna.html", data=data, statistik=statistik)

@stakeholder_bp.route("/tracer-stakeholder", methods=["GET", "POST"])
def tracer_stakeholder():
    if request.method == "POST":
        data = {
            "nama_pengisi": request.form.get("nama_pengisi"),
            "posisi_jabatan": request.form.get("posisi_jabatan"),
            "nama_instansi": request.form.get("nama_instansi"),
            "alamat_instansi": request.form.get("alamat_instansi"),
            "no_hp": request.form.get("no_hp"),
            "email": request.form.get("email"),
            "nama_alumni": request.form.get("nama_alumni"),
            "prodi": request.form.get("prodi"),
            "bidang_pekerjaan": request.form.get("bidang_pekerjaan"),

            # tambahan aspek penilaian
            "integritas": request.form.get("integritas"),
            "penguasaan_konsep": request.form.get("penguasaan_konsep"),
            "keterampilan_umum": request.form.get("keterampilan_umum"),
            "keterampilan_khusus": request.form.get("keterampilan_khusus"),
            "bahasa_asing": request.form.get("bahasa_asing"),
            "teknologi_informasi": request.form.get("teknologi_informasi"),
            "komunikasi": request.form.get("komunikasi"),
            "kerjasama_tim": request.form.get("kerjasama_tim"),
            "pengembangan_diri": request.form.get("pengembangan_diri"),
            "kompetensi_lulusan": request.form.get("kompetensi_lulusan"),
            "saran": request.form.get("saran")
        }

        StakeholderModel.create(data)
        flash("Data tracer stakeholder berhasil disimpan!", "success")
        return redirect(url_for("stakeholder.tracer_stakeholder"))

    return render_template("stakeholder_form.html")
