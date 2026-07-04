from connect import get_connection

conn = get_connection()
cur = conn.cursor()

try:
    # ======================
    # UPSERT
    # ======================
    cur.execute(
        "CALL upsert_contact(%s, %s, %s)",
        ("Ali", "Aman", "77001234567")
    )
    conn.commit()

    # ======================
    # SEARCH FUNCTION
    # ======================
    cur.execute(
        "SELECT * FROM search_pattern(%s::text)",
        ("Ali",)
    )
    print("SEARCH RESULT:")
    print(cur.fetchall())

    # ======================
    # PAGINATION FUNCTION
    # ======================
    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s, %s)",
        (5, 0)
    )
    print("PAGINATION RESULT:")
    print(cur.fetchall())

    # ======================
    # DELETE PROCEDURE
    # ======================
    cur.execute(
        "CALL delete_contact(%s)",
        ("Ali",)
    )
    conn.commit()

except Exception as e:
    print("ERROR:", e)

finally:
    cur.close()
    conn.close()