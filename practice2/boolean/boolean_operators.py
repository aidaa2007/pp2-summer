x = 200
print(isinstance(x, int))


a = 200
b = 33
c = 500

if a > b and c > a:
    print("Both conditions are True")

if a > b or b > c:
    print("At least one of the conditions is True")

print("Not operator:", not(a > b))