# Iterator Example

my_list = [1, 2, 3, 4, 5]

my_iter = iter(my_list)

print("Iterator:")
print(next(my_iter))
print(next(my_iter))
print(next(my_iter))

# Loop through iterator
print("\nLooping through iterator:")
for item in iter(my_list):
    print(item)


# Custom Iterator
class CountUp:
    def __init__(self, max_num):
        self.max_num = max_num
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max_num:
            num = self.current
            self.current += 1
            return num
        raise StopIteration


print("\nCustom Iterator:")
counter = CountUp(5)
for number in counter:
    print(number)


# Generator Function
def squares(n):
    for i in range(1, n + 1):
        yield i * i


print("\nGenerator Function:")
for value in squares(5):
    print(value)


# Generator Expression
print("\nGenerator Expression:")
gen = (x * x for x in range(5))

for value in gen:
    print(value)