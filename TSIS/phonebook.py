
from connect import get_connection
import psycopg2
import json
import csv


# ==========================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==========================================================

def get_group_id(conn, group_name):
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM groups WHERE name = %s",
        (group_name,)
    )

    row = cur.fetchone()

    if row:
        cur.close()
        return row[0]

    cur.execute(
        "INSERT INTO groups(name) VALUES(%s) RETURNING id",
        (group_name,)
    )

    group_id = cur.fetchone()[0]
    conn.commit()
    cur.close()

    return group_id


# ==========================================================
# ДОБАВЛЕНИЕ КОНТАКТА
# ==========================================================

def add_contact(conn):

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    group_id = get_group_id(conn, group)

    cur = conn.cursor()

    try:

        cur.execute("""
            INSERT INTO contacts
            (name,email,birthday,group_id)

            VALUES
            (%s,%s,%s,%s)

            RETURNING id
        """, (name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        while True:

            phone = input("Phone: ")
            phone_type = input("Type(home/work/mobile): ")

            cur.execute("""
                INSERT INTO phones
                (contact_id,phone,type)

                VALUES
                (%s,%s,%s)
            """, (contact_id, phone, phone_type))

            more = input("Add another phone? (y/n): ")

            if more.lower() != "y":
                break

        conn.commit()

        print("Contact added successfully.")

    except Exception as e:

        conn.rollback()
        print(e)

    finally:
        cur.close()


# ==========================================================
# ПОКАЗАТЬ ВСЕ КОНТАКТЫ
# ==========================================================

def show_contacts(conn):

    cur = conn.cursor()

    cur.execute("""

        SELECT

        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.type

        FROM contacts c

        LEFT JOIN groups g
        ON c.group_id=g.id

        LEFT JOIN phones p
        ON c.id=p.contact_id

        ORDER BY c.name

    """)

    rows = cur.fetchall()

    print()

    for row in rows:

        print("---------------------------")
        print("Name:", row[0])
        print("Email:", row[1])
        print("Birthday:", row[2])
        print("Group:", row[3])
        print("Phone:", row[4])
        print("Type:", row[5])

    print()

    cur.close()


# ==========================================================
# ПОИСК ПО EMAIL
# ==========================================================

def search_email(conn):

    email = input("Email contains: ")

    cur = conn.cursor()

    cur.execute("""

        SELECT

        name,
        email

        FROM contacts

        WHERE email ILIKE %s

    """, ('%' + email + '%',))

    rows = cur.fetchall()

    if not rows:
        print("Nothing found.")

    for row in rows:
        print(row)

    cur.close()


# ==========================================================
# ФИЛЬТР ПО ГРУППЕ
# ==========================================================

def filter_group(conn):

    group = input("Group: ")

    cur = conn.cursor()

    cur.execute("""

        SELECT

        c.name,
        c.email,
        g.name

        FROM contacts c

        JOIN groups g

        ON c.group_id=g.id

        WHERE g.name=%s

        ORDER BY c.name

    """, (group,))

    rows = cur.fetchall()

    if not rows:
        print("No contacts.")

    for row in rows:
        print(row)

    cur.close()
   
# ==========================================================
# СОРТИРОВКА
# ==========================================================

def sort_contacts(conn):

    print("\nSort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    fields = {
        "1": "c.name",
        "2": "c.birthday",
        "3": "c.created_at"
    }

    if choice not in fields:
        print("Invalid choice.")
        return

    cur = conn.cursor()

    query = f"""
        SELECT
            c.name,
            c.email,
            c.birthday,
            g.name

        FROM contacts c

        LEFT JOIN groups g
        ON c.group_id = g.id

        ORDER BY {fields[choice]}
    """

    cur.execute(query)

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()


# ==========================================================
# ДОБАВИТЬ НОВЫЙ ТЕЛЕФОН
# ==========================================================

def add_phone(conn):

    name = input("Contact name: ")
    phone = input("Phone: ")
    phone_type = input("Type (home/work/mobile): ")

    cur = conn.cursor()

    try:

        cur.execute(
            "CALL add_phone(%s,%s,%s)",
            (name, phone, phone_type)
        )

        conn.commit()

        print("Phone added successfully.")

    except Exception as e:

        conn.rollback()
        print(e)

    finally:
        cur.close()


# ==========================================================
# ПЕРЕМЕСТИТЬ В ГРУППУ
# ==========================================================

def move_to_group(conn):

    name = input("Contact name: ")
    group = input("New group: ")

    cur = conn.cursor()

    try:

        cur.execute(
            "CALL move_to_group(%s,%s)",
            (name, group)
        )

        conn.commit()

        print("Group updated.")

    except Exception as e:

        conn.rollback()
        print(e)

    finally:
        cur.close()


# ==========================================================
# ПОИСК (ИМЯ / EMAIL / ТЕЛЕФОН)
# ==========================================================

def search_contacts(conn):

    text = input("Search: ")

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM search_contacts(%s)",
        (text,)
    )

    rows = cur.fetchall()

    if not rows:
        print("Nothing found.")
    else:
        for row in rows:
            print(row)

    cur.close()


# ==========================================================
# ПАГИНАЦИЯ
# ==========================================================

def pagination(conn):

    page = 1
    limit = 5

    while True:

        offset = (page - 1) * limit

        cur = conn.cursor()

        cur.execute("""
            SELECT
                c.name,
                c.email,
                c.birthday

            FROM contacts c

            ORDER BY c.name

            LIMIT %s
            OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if rows:
            print(f"\n------ PAGE {page} ------")

            for row in rows:
                print(row)
        else:
            print("No contacts.")

        cur.close()

        command = input("\nnext / prev / quit : ").lower()

        if command == "next":
            page += 1

        elif command == "prev":
            if page > 1:
                page -= 1

        elif command == "quit":
            break

        else:
            print("Unknown command.")
            
          
# ==========================================================
# EXPORT TO JSON
# ==========================================================

def export_to_json(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.name,
            c.email,
            c.birthday,
            g.name,
            p.phone,
            p.type
        FROM contacts c
        LEFT JOIN groups g
            ON c.group_id = g.id
        LEFT JOIN phones p
            ON c.id = p.contact_id
        ORDER BY c.name;
    """)

    rows = cur.fetchall()

    data = []

    for row in rows:
        data.append({
            "name": row[0],
            "email": row[1],
            "birthday": str(row[2]) if row[2] else None,
            "group": row[3],
            "phone": row[4],
            "type": row[5]
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    cur.close()

    print("Export completed.")


# ==========================================================
# IMPORT FROM JSON
# ==========================================================

def import_from_json(conn):

    with open("contacts.json", "r", encoding="utf-8") as f:
        contacts = json.load(f)

    cur = conn.cursor()

    for c in contacts:

        cur.execute(
            "SELECT id FROM contacts WHERE name=%s",
            (c["name"],)
        )

        existing = cur.fetchone()

        if existing:

            answer = input(
                f'{c["name"]} already exists (skip/overwrite): '
            ).lower()

            if answer == "skip":
                continue

            if answer == "overwrite":

                group_id = get_group_id(conn, c["group"])

                cur.execute("""
                    UPDATE contacts
                    SET email=%s,
                        birthday=%s,
                        group_id=%s
                    WHERE id=%s
                """,
                (
                    c["email"],
                    c["birthday"],
                    group_id,
                    existing[0]
                ))

                cur.execute(
                    "DELETE FROM phones WHERE contact_id=%s",
                    (existing[0],)
                )

                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES(%s,%s,%s)
                """,
                (
                    existing[0],
                    c["phone"],
                    c["type"]
                ))

        else:

            group_id = get_group_id(conn, c["group"])

            cur.execute("""
                INSERT INTO contacts
                (name,email,birthday,group_id)

                VALUES(%s,%s,%s,%s)

                RETURNING id
            """,
            (
                c["name"],
                c["email"],
                c["birthday"],
                group_id
            ))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones
                (contact_id,phone,type)

                VALUES(%s,%s,%s)
            """,
            (
                contact_id,
                c["phone"],
                c["type"]
            ))

    conn.commit()
    cur.close()

    print("Import completed.")


# ==========================================================
# CSV IMPORT (EXTENDED)
# ==========================================================

def import_csv(conn):

    with open("contacts.csv", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        cur = conn.cursor()

        for row in reader:

            group_id = get_group_id(conn, row["group"])

            cur.execute("""
                INSERT INTO contacts
                (name,email,birthday,group_id)

                VALUES(%s,%s,%s,%s)

                ON CONFLICT(name) DO NOTHING

                RETURNING id
            """,
            (
                row["name"],
                row["email"],
                row["birthday"],
                group_id
            ))

            result = cur.fetchone()

            if result:
                contact_id = result[0]

                cur.execute("""
                    INSERT INTO phones
                    (contact_id,phone,type)

                    VALUES(%s,%s,%s)
                """,
                (
                    contact_id,
                    row["phone"],
                    row["type"]
                ))

        conn.commit()
        cur.close()

    print("CSV imported.")


# ==========================================================
# MAIN MENU
# ==========================================================

def main():

    conn = get_connection()

    if conn is None:
        return

    while True:

        print("\n========== PHONEBOOK ==========")
        print("1. Add contact")
        print("2. Show contacts")
        print("3. Search by email")
        print("4. Filter by group")
        print("5. Sort contacts")
        print("6. Add phone")
        print("7. Move to group")
        print("8. Search contacts")
        print("9. Pagination")
        print("10. Export JSON")
        print("11. Import JSON")
        print("12. Import CSV")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_contact(conn)

        elif choice == "2":
            show_contacts(conn)

        elif choice == "3":
            search_email(conn)

        elif choice == "4":
            filter_group(conn)

        elif choice == "5":
            sort_contacts(conn)

        elif choice == "6":
            add_phone(conn)

        elif choice == "7":
            move_to_group(conn)

        elif choice == "8":
            search_contacts(conn)

        elif choice == "9":
            pagination(conn)

        elif choice == "10":
            export_to_json(conn)

        elif choice == "11":
            import_from_json(conn)

        elif choice == "12":
            import_csv(conn)

        elif choice == "0":
            break

        else:
            print("Invalid option.")

    conn.close()


if __name__ == "__main__":
    main()



