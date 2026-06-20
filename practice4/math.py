import math
import random

numbers = [10, 25, -7, 3, 50]

print("Built-in Math Functions")
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Absolute:", abs(-25))
print("Round:", round(3.14159, 2))
print("Power:", pow(2, 5))

print("\nMath Module Functions")
print("Square Root:", math.sqrt(64))
print("Ceil:", math.ceil(4.2))
print("Floor:", math.floor(4.8))
print("Sin(90°):", math.sin(math.radians(90)))
print("Cos(0°):", math.cos(math.radians(0)))
print("Pi:", math.pi)
print("Euler's Number:", math.e)

print("\nRandom Module")
print("Random Float:", random.random())
print("Random Integer:", random.randint(1, 100))

colors = ["red", "green", "blue", "yellow"]

print("Random Choice:", random.choice(colors))

random.shuffle(colors)

print("Shuffled List:", colors)