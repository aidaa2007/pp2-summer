#Multiline strings
a = """Hello! My name is blabla.
I am studying mathematics and computer science.
This summer I am learning Git and Python programming.
It is a bit difficult, but I am trying my best!"""
print(a)

#Slicing
b = "Hello, World!"
print(b[2:5]) #from 2 to 5(not incl)

#Modifying
a = "Hello, World!"
print(a.upper())

a = "Hello, World!"
print(a.lower())

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#f-string
age = 36
txt = f"My name is John, I am {age}"
print(txt)