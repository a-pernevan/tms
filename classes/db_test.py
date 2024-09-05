from database.datab import connection, cursor


# connection._open_connection()
# sql = """INSERT INTO angajati (nume, prenume, functie, filiala, status_angajat, 
#                     data_angajare, data_nastere, zile_concediu, casatorit, copii, 
#                     buletin, emitent_buletin, data_buletin, cnp, cetatenie, strada, 
#                     nr_strada, bloc, scara, etaj, apartament, 
#                     sector, oras_domiciliu, judet_domiciliu, tel_personal, tel_firma, 
#                     email_personal, email_firma, permis_auto, categ_a, 
#                     categ_b, categ_c, categ_ce, categ_d, categ_de) VALUES
#                     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
#                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
# values = ("Pernevan", "Andrei", "Dispecer", \
#                       "Semlac", "Activ", "2019-05-21", \
#                     "1985-09-01", 21, 1, 1, \
#                         "AR776208", "Pol Arad", "2016-09-01", \
#                         1850901450012, "Romana", "Poetului", 1, "R4", \
#                         "-", 2, 45, "-", "Arad", \
#                         "Arad", "0752179815", "-", "apernevan@outlook.com", "andrei@tauros.ro", \
#                         "A01234", 0, 1, 0, 0, 0, \
#                         0)
# print(sql)
# print(values)
# cursor.execute(sql, values)
# connection.commit()

id_angajat = 2

try:
    connection._open_connection()
    sql = "SELECT * from angajati WHERE id = %s"

    values = (id_angajat, )

    cursor.execute(sql, values)

    result = cursor.fetchall()

    print(result)

except:
    print("Eroare la selectare")