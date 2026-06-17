students = [
    ("Alina", 85),
    ("Amina", 95),
    ("Sabina", 78)
]

sorted_students = sorted(
    students,
    key=lambda student: student[1]
)

print(sorted_students)