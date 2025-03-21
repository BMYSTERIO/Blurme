import json
from ui.asni import Colors


def load_config(config_file="default.json"):
    config_path = f"config/{config_file}"
    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"{Colors.RED}[Error]{Colors.RESET} Config file not found!")
        return None
    except json.JSONDecodeError:
        print(f"{Colors.RED}[Error]{Colors.RESET} Invalid JSON format!")
        return None
