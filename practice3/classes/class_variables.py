class Student:

    # Class variable
    school = "KBT University"

    def __init__(self, name):
        self.name = name


s1 = Student("Ali")
s2 = Student("Sabina")

print(Student.school)
print(s1.school)
print(s2.school)

# Instance variable
s1.name = "Amina"

print(s1.name)
print(s2.name)