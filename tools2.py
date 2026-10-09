from langchain_core.tools import tool

@tool
def search_product_catalog(item_name: str) -> str:
    """Checks if a specific product or item is available in the inventory catalog.
    
    Args:
        item_name: The name or category of the item.
    """
    catalog = {
        "python programming": "Available in Section B, Shelf 4 (3 copies left).",
        "data structures": "Checked out. Available for reservation from Oct 15.",
        "machine learning": "Available in Digital e-Library only.",
    }
    key = item_name.lower().strip()
    return catalog.get(key, f"No catalog entry found for '{item_name}'.")

@tool
def get_daily_menu(day_of_week: str) -> str:
    """Returns the special lunch menu for a given day of the week.
    
    Args:
        day_of_week: Day of the week (e.g. Monday, Tuesday, Friday).
    """
    menus = {
        "monday": "Rajma Chawal & Cucumber Raita",
        "tuesday": "Chole Bhature & Pickle",
        "wednesday": "Masala Dosa & Coconut Chutney",
        "thursday": "Paneer Butter Masala & Naan",
        "friday": "Vegetable Biryani & Raita"
    }
    return menus.get(day_of_week.lower().strip(), "Vegetable Pulao & Dal Tadka.")

@tool
def calculate_score_percentage(obtained_marks: float, total_marks: float) -> str:
    """Calculates the percentage and tier given obtained and total score.
    
    Args:
        obtained_marks: Total score achieved.
        total_marks: Maximum possible score.
    """
    if total_marks <= 0:
        return "Error: Total marks must be greater than zero."
    pct = (obtained_marks / total_marks) * 100
    grade = "A" if pct >= 90 else "B" if pct >= 80 else "C" if pct >= 70 else "F"
    return f"{pct:.2f}% (Grade: {grade})"
