from langchain_core.tools import tool

@tool
def technical_search(topic: str) -> str:
    """Searches the encyclopedia for factual definitions, scientific constants, and historical facts.
    
    Args:
        topic: The search query or scientific concept (e.g. 'Photosynthesis', 'Speed of Light').
    """
    knowledge_base = {
        "photosynthesis": "Photosynthesis is the biological process used by plants to convert light energy into chemical energy stored in glucose. Formula: 6CO2 + 6H2O + light -> C6H12O6 + 6O2.",
        "speed of light": "The speed of light in vacuum is exactly 299,792,458 meters per second (approx 3.0 x 10^8 m/s). Symbol: c.",
        "dna": "Deoxyribonucleic acid (DNA) is a polymer composed of two polynucleotide chains that coil around each other to form a double helix.",
        "binary search": "Binary search is an efficient algorithm for finding an item from a sorted list of items with time complexity O(log n)."
    }
    clean_topic = topic.lower().strip()
    return knowledge_base.get(clean_topic, f"No detailed encyclopedia entry found for '{topic}'. Try checking spelling or general terminology.")

@tool
def calculate(a: float, b: float, operation: str) -> str:
    """Performs basic arithmetic on two numbers: add, subtract, multiply, or divide.
    
    Args:
        a: The first number.
        b: The second number.
        operation: The arithmetic operation: 'add', 'subtract', 'multiply', or 'divide'.
    """
    op = operation.lower().strip()
    if op == "add":
        return str(a + b)
    elif op == "subtract":
        return str(a - b)
    elif op == "multiply":
        return str(a * b)
    elif op == "divide":
        return str(a / b) if b != 0 else "Error: Division by zero."
    return f"Unsupported operation: {operation}. Use add, subtract, multiply, or divide."

@tool
def save_note(title: str, content: str) -> str:
    """Saves an organized note into the local file 'research_notes.md'.
    
    Args:
        title: The title or heading of the note.
        content: The body text or bullet points of the note.
    """
    filename = "research_notes.md"
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"\n\n## 📌 {title}\n")
            f.write(f"{content}\n")
            f.write("-" * 40 + "\n")
        return f"Successfully saved note '{title}' to {filename}."
    except Exception as e:
        return f"File Error: Could not save note. Details: {str(e)}"