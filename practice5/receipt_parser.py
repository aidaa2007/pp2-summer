import re
import json

# Read receipt from file
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Extract product names
products = re.findall(r"\d+\.\s*\n(.+?)\n\d+,\d{3}\s*x", text, re.DOTALL)
products = [product.replace("\n", " ").strip() for product in products]

# Extract prices
price_strings = re.findall(r"\n(\d[\d ]*,\d{2})\nСтоимость", text)
prices = [float(price.replace(" ", "").replace(",", ".")) for price in price_strings]

# Calculate total amount
calculated_total = sum(prices)

# Extract total from receipt
total_match = re.search(r"ИТОГО:\s*\n([\d ]*,\d{2})", text)
receipt_total = (
    float(total_match.group(1).replace(" ", "").replace(",", "."))
    if total_match
    else 0
)

# Extract date and time
datetime_match = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})",
    text
)

date = datetime_match.group(1) if datetime_match else "Not found"
time = datetime_match.group(2) if datetime_match else "Not found"

# Extract payment method
payment_match = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment_match.group(1) if payment_match else "Not found"

# Store all information
receipt = {
    "products": products,
    "prices": prices,
    "calculated_total": calculated_total,
    "receipt_total": receipt_total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

# Print formatted output
print("========== RECEIPT ==========")
print(f"Date: {date}")
print(f"Time: {time}")
print(f"Payment Method: {payment_method}")
print()

print("Products:")
for product, price in zip(products, prices):
    print(f"- {product} : {price:.2f} KZT")

print()
print(f"Calculated Total: {calculated_total:.2f} KZT")
print(f"Receipt Total: {receipt_total:.2f} KZT")

print("\nJSON Output:")
print(json.dumps(receipt, indent=4, ensure_ascii=False))
