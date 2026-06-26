import re

# 1
print(bool(re.fullmatch(r"ab*", "abbb")))

# 2
print(bool(re.fullmatch(r"ab{2,3}", "abb")))

# 3
print(re.findall(r"[a-z]+_[a-z]+", "hello_world test_string"))

# 4
print(re.findall(r"[A-Z][a-z]+", "Hello World PYTHON Test"))

# 5
print(bool(re.fullmatch(r"a.*b", "axyzb")))

# 6
text = "Python, is. awesome"
print(re.sub(r"[ ,.]", ":", text))

# 7
def snake_to_camel(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(snake_to_camel("hello_world_python"))

# 8
text = "HelloWorldPython"
print([x for x in re.split(r"(?=[A-Z])", text) if x])

# 9
print(re.sub(r"(?<!^)([A-Z])", r" \1", "HelloWorldPython"))

# 10
def camel_to_snake(text):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()

print(camel_to_snake("HelloWorldPython"))