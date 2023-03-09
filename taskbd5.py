import psycopg2
from pprint import pprint

def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        client_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        client_email VARCHAR(254)
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
            phone_id SERIAL PRIMARY KEY,
            number VARCHAR(11) UNIQUE,
            client_id INTEGER REFERENCES clients(client_id)
            );
        """)

def add_client(cur, client_name, last_name, client_email):
    cur.execute("""
    INSERT INTO clients(client_name, last_name, client_email)
    VALUES (%s, %s, %s)
    """, (client_name, last_name, client_email))

def add_phone(cur, client_id, number):
    cur.execute("""
    INSERT INTO phone_numbers(client_id, number)
    VALUES (%s, %s)
    """, (client_id, number))

def change_client():
    print("Для изменения информации о клиенте, введите номер нужной команды.\n "
        "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")

    while True:
        command_symbol = int(input())
        if command_symbol == 1:
            input_id_for_changing_name = input("Введите id клиента, имя которого хотите изменить: ")
            input_name_for_changing = input("Введите имя: ")
            cur.execute("""
            UPDATE clients SET client_name=%s WHERE client_id=%s;
            """, (input_name_for_changing, input_id_for_changing_name))
            break
        elif command_symbol == 2:
            input_id_for_changing_lastname = input("Введите id клиента, фамилию которого хотите изменить: ")
            input_lastname_for_changing = input("Введите фамилию: ")
            cur.execute("""
            UPDATE clients SET last_name=%s WHERE client_id=%s;
            """, (input_lastname_for_changing, input_id_for_changing_lastname))
            break
        elif command_symbol == 3:
            input_id_for_changing_email = input("Введите id клиента, e-mail которого хотите изменить: ")
            input_email_for_changing = input("Введите e-mail: ")
            cur.execute("""
            UPDATE clients SET client_email=%s WHERE client_id=%s;
            """, (input_email_for_changing, input_id_for_changing_email))
            break
        elif command_symbol == 4:
            input_number_change = input("Введите номер телефона который Вы хотите изменить: ")
            input_number_for_changing = input("Введите новый номер телефона: ")
            cur.execute("""
            UPDATE phone_numbers SET number=%s WHERE number=%s;
            """, (input_number_for_changing, input_number_change))
            break
        else:
            print("Вы ввели неправильную команду, пожалуйста, попробуйте снова")

def delete_phone(conn=None):
    input_id_for_delet_number = input("Введите id клиентаб номер телефона которого хотите удалить: ")
    input_number_for_delet = input("Введите номер телефона, который хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM phone_numbers WHERE client_id=%s AND number=%s
           """, (input_id_for_delet_number, input_number_for_delet))

def delete_client(conn=None):
    input_id_for_delete_client = input("Введите id клиента, которого хотите удалить: ")
    input_last_name_for_delete = input("Введите фамилию клиента, которого хотите удалить: ")
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_numbers WHERE client_id=%s
        """, (input_id_for_delete_client,))

        cur.execute("""
        DELETE FROM clients WHERE client_id=%s AND last_name=%s
        """, (input_id_for_delete_client, input_last_name_for_delete))

    def find_client():
     print("Для поиска информации о клиенте, введите команду, где:\n "
        "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
     while True:
         input_command_find = int(input("Введите команду: "))
         if input_command_find == 1:
             input_name_find = input("Введите имя: ")
             cur.execute("""
              SELECT id, client_name, last_name, client_email, number
              FROM clients AS cl
              LEFT JOIN phone_numbers AS pn ON pn.phone_id = cl.client_id
              WHERE client_name=%s
              """, (input_name_find,))
             print(cur.fetchall())
         elif input_command_find == 2:
             input_last_name_find = input("Введите фамилию: ")
             cur.execute("""
              SELECT id, client_name, last_name, client_email, number
              FROM clients AS cl
              LEFT JOIN phone_numbers AS pn ON pn.phone_id = cl.client_id
              WHERE client_surname=%s
              """, (input_last_name_find,))
             print(cur.fetchall())
         elif input_command_find == 3:
             input_email_find = input("Введите email для поиска информации о клиенте: ")
             cur.execute("""
              SELECT id, client_name, last_name, client_email, number
              FROM clients AS cl
              LEFT JOIN phone_numbers AS pn ON pn.phone_id = cl.client_id
              WHERE client_email=%s
              """, (input_email_find,))
             print(cur.fetchall())
         elif input_command_find == 4:
             input_phonenumber_find = input("Введите номер телефона для поиска информации о клиенте: ")
             cur.execute("""
              SELECT id, client_name, last_name, client_email, number
              FROM clients AS cl
              LEFT JOIN phone_numbers AS pn ON pn.phone_id = cl.client_id
              WHERE client_phonenumber=%s
              """, (input_phonenumber_find,))
             print(cur.fetchall())
         else:
             print("Вы ввели неправильную команду, попробуйте снова")

with psycopg2.connect(database="task5bd", user="postgres", password="postgres") as conn:
    with conn.cursor() as cur:
        create_tables(cur)
        check_function(cur)
        add_new_client(cur, "Tim", "Grey", "tm@g.com")
        add_new_client(cur, "Ben", "Brown", "bb@g.com")
        add_new_client(cur, "Ann", "Oldman", "ao@g.com")
        add_new_client(cur, "Kate", "Tompson", "kt@g.com")
        add_new_client(cur, "Tom", "Green", "tg@g.com")
        add_new_phonenumber(cur, 1, "79561236564")
        add_new_phonenumber(cur, 2, "96328520201")
        add_new_phonenumber(cur, 3, "45789612303")
        add_new_phonenumber(cur, 4, "10203040506")
        add_new_phonenumber(cur, 5, "98765413203")
        change_client_data()
        delete_client_phonenumber()
        delete_client()
        find_client()

conn.close()
