import csv
from datetime import datetime

FILE_NAME = "items.csv"
FIELDS = ["id", "type", "name", "category", "color", "location", "date", "status"]


def load_items():
    """Load item records from the CSV file."""
    items = []
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(field in row for field in FIELDS):
                    items.append({field: row[field] for field in FIELDS})
    except FileNotFoundError:
        print("File not found. Starting with an empty record list.")
    except (OSError, csv.Error) as error:
        print("Could not read the data file:", error)
    return items


def save_items(items):
    """Save all item records to the CSV file."""
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(items)
        print("Records saved successfully.")
    except OSError as error:
        print("Could not save the data file:", error)


def generate_id(items, kind):
    """Generate the next available ID for lost or found items."""
    numbers = []
    for item in items:
        if item["type"] == kind and item["id"].startswith(kind):
            suffix = item["id"][1:]
            if suffix.isdigit():
                numbers.append(int(suffix))
    next_number = max(numbers, default=0) + 1
    return kind + str(next_number).zfill(3)


def get_valid_date():
    """Accept only a real date in YYYY-MM-DD format."""
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Invalid date. Enter a real date in YYYY-MM-DD format.")


def add_item(items, kind):
    """Register a lost or found item."""
    item = {
        "id": generate_id(items, kind),
        "type": kind,
        "name": input("Item name: ").strip().lower(),
        "category": input("Category: ").strip().lower(),
        "color": input("Color: ").strip().lower(),
        "location": input("Location: ").strip().lower(),
        "date": get_valid_date(),
        "status": "open"
    }
    if not all(item[field] for field in ["name", "category", "color", "location"]):
        print("Item details cannot be empty. Record was not added.")
        return
    items.append(item)
    print("Saved with ID:", item["id"])


def display_items(items):
    """Display all item records."""
    if not items:
        print("No records available.")
        return
    for item in items:
        print(" | ".join(item[field] for field in FIELDS))


def search_items(items):
    """Search item records using a keyword."""
    word = input("Enter word to search: ").strip().lower()
    matches = []
    for item in items:
        searchable_text = " ".join(item[field].lower() for field in FIELDS)
        if word in searchable_text:
            matches.append(item)
    if matches:
        display_items(matches)
    else:
        print("No matching records found.")


def calculate_match_score(lost, found):
    """Calculate a match score out of 100."""
    score = 0
    if lost["category"] == found["category"]:
        score += 25
    lost_words = set(lost["name"].split())
    found_words = set(found["name"].split())
    if lost_words & found_words:
        score += 25
    if lost["color"] == found["color"]:
        score += 15
    if lost["location"] == found["location"]:
        score += 20
    lost_date = datetime.strptime(lost["date"], "%Y-%m-%d")
    found_date = datetime.strptime(found["date"], "%Y-%m-%d")
    if abs((lost_date - found_date).days) <= 2:
        score += 15
    return score


def find_matches(items):
    """Find possible found-item matches for a lost item."""
    lost_id = input("Enter lost item ID (example L001): ").strip().upper()
    lost = None
    for item in items:
        if item["id"].upper() == lost_id and item["type"] == "L":
            lost = item
            break
    if lost is None:
        print("Lost item not found.")
        return
    found_items = [
        item for item in items
        if item["type"] == "F" and item["status"] == "open"
    ]
    if not found_items:
        print("No open found-item records available.")
        return
    for found in found_items:
        score = calculate_match_score(lost, found)
        if score >= 80:
            result = "Strong match"
        elif score >= 50:
            result = "Possible match"
        else:
            result = "Weak match"
        print(found["id"], found["name"], "- Score:",
              str(score) + "%", "-", result)


def update_status(items):
    """Update the status of an existing item."""
    item_id = input("Enter item ID: ").strip().upper()
    valid_statuses = ["matched", "returned", "closed"]
    for item in items:
        if item["id"].upper() == item_id:
            while True:
                new_status = input(
                    "New status (matched/returned/closed): "
                ).strip().lower()
                if new_status in valid_statuses:
                    item["status"] = new_status
                    print("Status updated successfully.")
                    return
                print("Invalid status. Please enter matched, returned or closed.")
    print("Item ID not found.")


def show_summary(items):
    """Display summary statistics for all records."""
    if not items:
        print("No records available for summary.")
        return
    categories = [item["category"] for item in items]
    locations = [item["location"] for item in items]
    lost_count = sum(1 for item in items if item["type"] == "L")
    found_count = sum(1 for item in items if item["type"] == "F")
    print("Total records:", len(items))
    print("Lost reports:", lost_count)
    print("Found reports:", found_count)
    print("Most common category:", max(set(categories), key=categories.count))
    print("Most common location:", max(set(locations), key=locations.count))


def main():
    """Run the main menu of the Lost and Found system."""
    items = load_items()
    while True:
        print("\n===== CAMPUS LOST & FOUND SYSTEM =====")
        print("1. Add lost item")
        print("2. Add found item")
        print("3. View all records")
        print("4. Search items")
        print("5. Find matches")
        print("6. Update status")
        print("7. Summary")
        print("8. Save and exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_item(items, "L")
        elif choice == "2":
            add_item(items, "F")
        elif choice == "3":
            display_items(items)
        elif choice == "4":
            search_items(items)
        elif choice == "5":
            find_matches(items)
        elif choice == "6":
            update_status(items)
        elif choice == "7":
            show_summary(items)
        elif choice == "8":
            save_items(items)
            print("Thank you for using Campus Lost & Found!")
            break
        else:
            print("Invalid choice! Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
