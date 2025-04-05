import json

input_file = "data/mock_support_emails.json"

emails = []
with open(input_file, "r") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        try:
            emails.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"❌ Error on line {i}: {e}")
            print(f"Line content: {line}")

if emails:
    with open(input_file, "w") as f:
        json.dump(emails, f, indent=2)
    print(f"✅ Successfully converted {len(emails)} emails to JSON array.")
else:
    print("⚠️ No valid emails were found.")
