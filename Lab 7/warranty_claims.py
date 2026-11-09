import math

def parse_claim(text):
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    plan, months = text.split(':')
    plan = plan.strip()
    try:
        months = float(months)
    except ValueError:
        return None
    if not plan or not math.isfinite(months) or months < 0:
        return None
    return plan.title(), months

def age_average(ages_csv):
    if not isinstance(ages_csv, str):
        return None
    try:
        values = [int(r) for r in ages_csv.split(',')]
    except ValueError:
        return None
    if any(v < 0 for v in values):
        return None
    return sum(values) // len(values)

def payable_charge(text):
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    charge, discount = text.split('|')
    try:
        charge, discount = float(charge), float(discount)
    except ValueError:
        return None
    if not (math.isfinite(charge) and math.isfinite(discount)) or charge < 0 or discount < 0:
        return None
    total = charge * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)

def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result if result is not None else "Invalid input")

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result if result is not None else "Invalid input")

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result if result is not None else "Invalid input")

if __name__ == "__main__":
    main()
