from config import get_db_connection

class KuesionerModel:
    @staticmethod
    def insert_full(data_diri, pertanyaan):
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO kuesioner 
        (kode_pt, kode_prodi, nim, nama, hp, email, tahun_lulus, nik, npwp,
        f8, f502, f505, f5a1, f5a2, f1101, f1102, f5b, f5c, f5d,
        f18a, f18b, f18c, f18d, f1201, f1202, f14, f15,
        f1761, f1762, f1763, f1764, f1765, f1766, f1767, f1768, f1769,
        f1770, f1771, f1772, f1773, f1774,
        f21, f22, f23, f24, f25, f26, f27,
        f301, f302, f303,
        f401, f402, f403, f404, f405, f406, f407, f408, f409, f410,
        f411, f412, f413, f414, f415, f416,
        f6, f7, f7a, f1001, f1002,
        f1601, f1602, f1603, f1604, f1605, f1606, f1607, f1608, f1609, f1610,
        f1611, f1612, f1613, f1614
        )
        VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,
                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                %s,%s,%s,%s)
        """
        values = (
            data_diri["kode_pt"],
            data_diri["kode_prodi"],
            data_diri["nim"],
            data_diri["nama"],
            data_diri["hp"],
            data_diri["email"],
            data_diri["tahun_lulus"],
            data_diri["nik"],
            data_diri["npwp"],
            pertanyaan[0],   # f8
            pertanyaan[1],   # f502
            pertanyaan[2],   # f505
            pertanyaan[3],   # f5a1
            pertanyaan[4],   # f5a2
            pertanyaan[5],   # f1101
            pertanyaan[6],   # f1102
            pertanyaan[7],   # f5b
            pertanyaan[8],   # f5c
            pertanyaan[9],   # f5d

            pertanyaan[10],  # f18a
            pertanyaan[11],  # f18b
            pertanyaan[12],  # f18c
            pertanyaan[13],  # f18d
            pertanyaan[14],  # f1201
            pertanyaan[15],  # f1202
            pertanyaan[16],  # f14
            pertanyaan[17],  # f15

            pertanyaan[18],  # f1761
            pertanyaan[19],  # f1762
            pertanyaan[20],  # f1763
            pertanyaan[21],  # f1764
            pertanyaan[22],  # f1765
            pertanyaan[23],  # f1766
            pertanyaan[24],  # f1767
            pertanyaan[25],  # f1768
            pertanyaan[26],  # f1769

            pertanyaan[27],  # f1770
            pertanyaan[28],  # f1771
            pertanyaan[29],  # f1772
            pertanyaan[30],  # f1773
            pertanyaan[31],  # f1774

            pertanyaan[32],  # f21
            pertanyaan[33],  # f22
            pertanyaan[34],  # f23
            pertanyaan[35],  # f24
            pertanyaan[36],  # f25
            pertanyaan[37],  # f26
            pertanyaan[38],  # f27
            
            pertanyaan[39],  # f301
            pertanyaan[40],  # f302
            pertanyaan[41],  # f303
            
            pertanyaan[42],  # f401
            pertanyaan[43],  # f402
            pertanyaan[44],  # f403
            pertanyaan[45],  # f404
            pertanyaan[46],  # f405
            pertanyaan[47],  # f406
            pertanyaan[48],  # f407
            pertanyaan[49],  # f408
            pertanyaan[50],  # f409
            pertanyaan[51],  # f410
            pertanyaan[52],  # f411
            pertanyaan[53],  # f412
            pertanyaan[54],  # f413
            pertanyaan[55],  # f414
            pertanyaan[56],  # f415
            pertanyaan[57],  # f416
            
            pertanyaan[58],  # f6
            pertanyaan[59],  # f7
            pertanyaan[60],  # f7a
            pertanyaan[61],  # f1001
            pertanyaan[62],  # f1002
            
            pertanyaan[63],  # f1601
            pertanyaan[64],  # f1602
            pertanyaan[65],  # f1603
            pertanyaan[66],  # f1604
            pertanyaan[67],  # f1605
            pertanyaan[68],  # f1606
            pertanyaan[69],  # f1607
            pertanyaan[70],  # f1608
            pertanyaan[71],  # f1609
            pertanyaan[72],  # f1610
            pertanyaan[73],  # f1611
            pertanyaan[74],  # f1612
            pertanyaan[75],  # f1613
            pertanyaan[76],  # f1614
            
        )
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM kuesioner")
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    
    @staticmethod
    def count_by_prodi():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT kode_prodi, COUNT(*) as jumlah
            FROM kuesioner
            GROUP BY kode_prodi
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
