# Parent class

class Person:

    def __init__(self, name):
        self.name = name

    def show_name(self):
        print(self.name)


# Child class

class Student(Person):
    pass


student = Student("Alina")

student.show_name()