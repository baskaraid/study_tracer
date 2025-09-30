from config import get_db_connection

class StakeholderModel:
    @staticmethod
    def create(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO stakeholder_tracer
            (nama_pengisi, posisi_jabatan, nama_instansi, alamat_instansi,
             no_hp, email, nama_alumni, prodi, bidang_pekerjaan,
             integritas, penguasaan_konsep, keterampilan_umum, keterampilan_khusus,
             bahasa_asing, teknologi_informasi, komunikasi, kerjasama_tim,
             pengembangan_diri, kompetensi_lulusan, saran)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s)
        """
        cursor.execute(query, (
            data['nama_pengisi'],
            data['posisi_jabatan'],
            data['nama_instansi'],
            data['alamat_instansi'],
            data['no_hp'],
            data['email'],
            data['nama_alumni'],
            data['prodi'],
            data['bidang_pekerjaan'],
            data['integritas'],
            data['penguasaan_konsep'],
            data['keterampilan_umum'],
            data['keterampilan_khusus'],
            data['bahasa_asing'],
            data['teknologi_informasi'],
            data['komunikasi'],
            data['kerjasama_tim'],
            data['pengembangan_diri'],
            data['kompetensi_lulusan'],
            data['saran']
        ))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM stakeholder_tracer")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def count_by_prodi():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT prodi, COUNT(*) as total
            FROM stakeholder_tracer
            GROUP BY prodi
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
