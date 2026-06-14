import json
import os

DB_FILE = "Library.json"

def load_raw_data():
    """Reads the JSON file and returns the dictionary. Automatically initializes if missing."""
    if not os.path.exists(DB_FILE):
        initial_structure = {"users": [], "books": [], "borrows": []}
        save_raw_data(initial_structure)
        return initial_structure
        
    with open(DB_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"users": [], "books": [], "borrows": []}

def save_raw_data(data):
    """Writes the dictionary data back down into the JSON file."""
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)