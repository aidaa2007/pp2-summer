# *args example

def add_numbers(*args):
    return sum(args)


print(add_numbers(1, 2, 3, 4))


# **kwargs example

def display_profile(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

display_profile(name="Tima", age=20, city="Almaty")