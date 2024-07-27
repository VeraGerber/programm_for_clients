import psycopg2

    #Функция, создающая структуру БД (таблицы).
    def create_db(conn):
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Clients(
                client_id INTEGER UNIQUE PRIMARY KEY,
                first_name VARCHAR(30),
                last_name VARCHAR(40),
                email VARCHAR(50)
                );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS phones(
               id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES Clients(client_id),
                phone VARCHAR(12)
                );""")
        conn.commit()


# Функция, позволяющая добавить нового клиента.
def add_client(conn, client_id, first_name, last_name, email, phones=None):
    cur = conn.cursor()
    cur.execute("""
  INSERT INTO clients(client_id, first_name, last_name, email) VALUES (%s, %s, %s, %s);
  """, (client_id, first_name, last_name, email))
    conn.commit()


cur = conn.cursor()
cur.execute("""
SELECT * FROM Clients;
            """)
print(cur.fetchall())
cur.execute("""
INSERT INTO phones(client_id, phone) VALUES (%s, %s);
""", (client_id, phones)) # type: ignore
conn.commit()
cur.execute("""
SELECT * FROM phones;
""")
print(cur.fetchall())
conn.commit()


#Функция, позволяющая добавить телефон для существующего клиента
def add_phone(conn, client_id, phone):
    cur = conn.cursor()
    cur.execute("""
              UPDATE phones SET phone = %s WHERE client_id = %s;
              """, (phone, client_id))
    conn.commit()


#Функция, позволяющая изменить данные о клиенте
def change_client(conn, client_id, firt_name=None, email=None, phones=None):
    cur = conn.cursor()
    cur.execute("""
              UPDATE Clients SET first_name = %s, last_name = %s, email = %s WHERE client_id = %s;
              """, (first_name, last_name, email, client_id)) # type: ignore
    cur.execute("""
              SELECT * FROM phones;
              """)
    print(cur.fetchall())


#Функция, позволяющая удалить телефон для существующего клиента
def delete_phone(conn, client_id):
    cur = conn.cursor()
    cur.execute("""
              UPDATE phones SET phone = %s WHERE client_id = %s;
              """, ('Null', client_id))
    cur.execute("""
              SELECT * FROM phones;
              """)
    print(cur.fetchall())

    #Функция, позволяющая удалить существующего клиента
    def delete_client(conn, client_id):
        cur = conn.cursor()
        cur.execute("""
                DELETE FROM Clients WHERE client_id = %s;
                """, (client_id))
        cur.execute("""
                SELECT * FROM Clients;
                """)
        print(cur.fetchall())

        cur.execute("""
                DELETE FROM phones WHERE client_id = %s;
                """, (client_id))
        cur.execute("""
                SELECT * FROM phones;
                """)

    print(cur.fetchall())


#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def search_client(conn, first_name=None, last_name=None, email=None, phone=None):
    cur = conn.cursor()
    cur.execute("""
              SELECT * FROM Clients c JOIN phones p ON c.client_id = p.client_id WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR p.phone LIKE %s;
              """, (first_name, last_name, email, phone))
    print(cur.fetchall())

cur.close()

with psycopg2.connect(database="learning", user="postgres", password="250299D") as conn:
    create_db(conn)
    add_client(conn, 1, 'Pavel', 'Durov', 'Paveldurov@vk.com', '+79273456145')
    add_client(conn, 2, 'Oleg', 'Buligin', 'olegbuligin@mail.ru', '+79222223147')
    add_client(conn, 3, 'Michail', 'Posov', 'Michailpos@gmail.com', '+79275674780')
    add_client(conn, 4, 'Oksana', 'Dyatlova', 'Oksik@ya.ru', '+79459087659')

    add_phone(conn, 1, +79765867435)
    add_phone(conn, 2, +79078932081)

    change_client(conn, 1, 'Oleg', 'Durov', 'Olegdurov@vk.com', '+79273456145')

    delete_phone(conn, 3)

    delete_client(conn, 4) # type: ignore

    search_client(conn, first_name='Oleg')
    search_client(conn, last_name='Michail')
    search_client(conn, email='Oksik@ya.ru')
    search_client(conn, phone="+79275674780")
