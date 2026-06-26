names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 95]

# enumerate()

for index, name in enumerate(names):
    print(index, name)

# zip()

for name, score in zip(names, scores):
    print(name, score)

# sorted()

print(sorted(scores))

# Type conversion

num = "100"

print(int(num))
print(float(num))
print(str(200))