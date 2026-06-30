import csv
import psycopg2
from connect import connect


def create_table(conn):
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook(
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL
        );
    """)

    conn.commit()
    cur.close()


def insert_console(conn):
    username = input("Enter name: ")
    phone = input("Enter phone: ")

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO PhoneBook(username, phone) VALUES(%s,%s)",
            (username, phone)
        )
        conn.commit()
        print("Contact added.")

    except Exception as e:
        conn.rollback()
        print(e)

    cur.close()


def insert_csv(conn, filename):
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                cur.execute(
                    """
                    INSERT INTO PhoneBook(username, phone)
                    VALUES(%s,%s)
                    ON CONFLICT(username)
                    DO NOTHING
                    """,
                    (row["username"], row["phone"])
                )
            except Exception:
                conn.rollback()

    conn.commit()
    cur.close()
    print("CSV imported.")


def show_contacts(conn):
    cur = conn.cursor()

    cur.execute("SELECT * FROM PhoneBook ORDER BY id")

    rows = cur.fetchall()

    print()

    for row in rows:
        print(row)

    print()

    cur.close()


def search_name(conn):
    name = input("Enter name: ")

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM PhoneBook WHERE username ILIKE %s",
        (f"%{name}%",)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()


def search_phone(conn):
    prefix = input("Phone prefix: ")

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM PhoneBook WHERE phone LIKE %s",
        (prefix + "%",)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()


def update_contact(conn):
    username = input("Contact name: ")

    print("1. Update name")
    print("2. Update phone")

    choice = input("Choice: ")

    cur = conn.cursor()

    if choice == "1":
        new_name = input("New name: ")

        cur.execute(
            """
            UPDATE PhoneBook
            SET username=%s
            WHERE username=%s
            """,
            (new_name, username)
        )

    elif choice == "2":
        new_phone = input("New phone: ")

        cur.execute(
            """
            UPDATE PhoneBook
            SET phone=%s
            WHERE username=%s
            """,
            (new_phone, username)
        )

    conn.commit()

    print("Updated.")

    cur.close()


def delete_contact(conn):
    value = input("Enter username or phone: ")

    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM PhoneBook
        WHERE username=%s OR phone=%s
        """,
        (value, value)
    )

    conn.commit()

    print("Deleted.")

    cur.close()


def menu():
    conn = connect()

    create_table(conn)

    while True:

        print("""
1. Import CSV
2. Add contact
3. Show contacts
4. Search by name
5. Search by phone prefix
6. Update contact
7. Delete contact
0. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            insert_csv(conn, "contacts.csv")

        elif choice == "2":
            insert_console(conn)

        elif choice == "3":
            show_contacts(conn)

        elif choice == "4":
            search_name(conn)

        elif choice == "5":
            search_phone(conn)

        elif choice == "6":
            update_contact(conn)

        elif choice == "7":
            delete_contact(conn)

        elif choice == "0":
            break

    conn.close()


menu()