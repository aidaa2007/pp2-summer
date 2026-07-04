from connect import get_connection

conn = get_connection()
cur = conn.cursor()

# UPSERT
cur.execute(
    "CALL upsert_contact(%s, %s, %s)",
    ("Ali", "Aman", "77001234567")
)

# SEARCH FUNCTION
cur.execute(
    "SELECT * FROM search_pattern(%s)",
    ("Ali",)
)
print("SEARCH:", cur.fetchall())

# PAGINATION
cur.execute(
    "SELECT * FROM get_contacts_paginated(%s, %s)",
    (5, 0)
)
print("PAGE:", cur.fetchall())

# DELETE
cur.execute(
    "CALL delete_contact(%s)",
    ("Ali",)
)

conn.commit()
cur.close()
conn.close()