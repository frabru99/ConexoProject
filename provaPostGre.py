import psycopg2




conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="ciao",
                        port="5432")


cursor = conn.cursor()

id = 5
name = "Mario"
sur = "Rossi"
email = "ciao5@gmail.com"

"""
try:
    cursor.execute('INSERT INTO Employee(idEmployee, nameEmployee, surname, email) values(%s, %s, %s, %s)', (id, name, sur, email) )

    conn.commit()

except (Exception, psycopg2.DatabaseError) as error:

    print(error)

"""

position = 'Napoli'

cursor.execute('SELECT * FROM CABINET WHERE idPOP = ( SELECT idPOP FROM POP WHERE popPosition = %s )', [position])

allCabinets = cursor.fetchall()

print(allCabinets) 