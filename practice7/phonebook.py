import csv
from connect import get_connection


# ===================== CREATE TABLE =====================
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# ===================== ADD CONTACT =====================
def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook(first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Added")


# ===================== SHOW ALL =====================
def show_all():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM phonebook")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# ===================== SEARCH =====================
def search():
    text = input("Search name: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s",
        ('%' + text + '%',)
    )

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


# ===================== DELETE =====================
def delete():
    value = input("Name or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE first_name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()

    print("Deleted")


# ===================== UPDATE =====================
def update_contact():
    old_name = input("Current name: ")
    new_name = input("New name: ")
    new_phone = input("New phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE phonebook
        SET first_name=%s,
            phone=%s
        WHERE first_name=%s
    """, (new_name, new_phone, old_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Updated")


# ===================== IMPORT CSV =====================
def import_csv():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            cur.execute("""
                INSERT INTO phonebook(first_name, phone)
                VALUES (%s, %s)
            """, (row[0], row[1]))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported")


# ===================== MAIN =====================
create_table()

while True:
    print("""
1 - add
2 - show
3 - search
4 - delete
5 - import CSV
6 - update contact
0 - exit
""")

    choice = input("> ")

    if choice == "1":
        add_contact()

    elif choice == "2":
        show_all()

    elif choice == "3":
        search()

    elif choice == "4":
        delete()

    elif choice == "5":
        import_csv()

    elif choice == "6":
        update_contact()

    elif choice == "0":
        break

    else:
        print("Wrong choice")