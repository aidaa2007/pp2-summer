import re
import json


# REGEX EXAMPLES

text = "My number is 7771234567 and backup 7019876543"

print("=== re.search() ===")
match = re.search(r"\d+", text)
if match:
print(match.group())

print("\n=== re.findall() ===")
print(re.findall(r"\d+", text))

print("\n=== re.split() ===")
print(re.split(r"\s+", text))

print("\n=== re.sub() ===")
print(re.sub(r"\d", "*", text))

print("\n=== re.match() ===")
m = re.match(r"My", text)
if m:
print(m.group())



# METACHARACTERS

print("\n=== Metacharacters ===")
print(re.findall(r".at", "cat bat rat"))
print(re.findall(r"ca*t", "ct cat caat caaat"))
print(re.findall(r"ca+t", "ct cat caat caaat"))
print(re.findall(r"ca?t", "ct cat caat"))
print(re.findall(r"[cr]at", "cat rat bat"))
print(re.findall(r"cat|rat", "cat rat bat"))




# SPECIAL SEQUENCES


sample = "Room 101 costs 50000 tenge"

print("\n=== Special Sequences ===")
print("Digits:", re.findall(r"\d+", sample))
print("Non-digits:", re.findall(r"\D+", sample))
print("Words:", re.findall(r"\w+", sample))
print("Non-words:", re.findall(r"\W+", sample))
print("Spaces:", re.findall(r"\s", sample))
print("Non-spaces:", re.findall(r"\S+", sample))



# QUANTIFIERS


print("\n=== Quantifiers ===")
print(re.findall(r"a{3}", "aaa aaaa aaaaa"))
print(re.findall(r"a{3,}", "aaa aaaa aaaaa"))
print(re.findall(r"a{3,5}", "aaa aaaa aaaaa"))



# RECEIPT PARSER


print("\n=== Receipt Parser ===")

try:
with open("raw.txt", "r", encoding="utf-8") as file:
receipt = file.read()



# Prices
prices = re.findall(r"\d+\.\d{2}", receipt)

# Date
date_match = re.search(r"\d{2}[/-]\d{2}[/-]\d{4}", receipt)
date = date_match.group() if date_match else None

# Time
time_match = re.search(r"\d{2}:\d{2}(?::\d{2})?", receipt)
time = time_match.group() if time_match else None

# Payment Method
payment_match = re.search(
    r"(VISA|MASTERCARD|CARD|CASH|AMEX)",
    receipt,
    re.IGNORECASE
)
payment_method = payment_match.group() if payment_match else None

# Products
product_pattern = r"([A-Za-zА-Яа-я\s]+)\s+(\d+\.\d{2})"
products = []

for item in re.findall(product_pattern, receipt):
    products.append({
        "name": item[0].strip(),
        "price": float(item[1])
    })

total = sum(float(price) for price in prices)

result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "products": products,
    "total": total
}

print(json.dumps(result, indent=4, ensure_ascii=False))


except FileNotFoundError:
print("raw.txt not found.")
