import inspect
from database import Database
import json


def get_method_signatures(cls):
    method_signatures = []
    for method_name in dir(cls):
        method = getattr(cls, method_name)
        if callable(method) and not method_name.startswith(
            "__"
        ):  # Ignore special methods
            try:
                signature = inspect.signature(method)
                method_signatures.append(
                    {
                        "name": method_name,
                        "params": tuple(
                            parameter
                            for parameter in signature.parameters.keys()
                            if parameter != "self"
                        ),
                    }
                )
            except ValueError:
                # In case the signature can't be retrieved (e.g., for built-in methods)
                pass

    return method_signatures


# Open terminal interface for database if running this file
if __name__ == "__main__":
    app = Database()
    method_signatures = get_method_signatures(Database)

    quit_words = ["quit", "exit"]
    current_command = None
    while True:
        # Select a command to execute
        if current_command is None:
            print()
            for index, method_signature in enumerate(method_signatures):
                print(f"{index + 1}: {method_signature['name']}")
            try:
                print()
                command = input("Select a command to execute (quit to exit): ")
                if command.lower() in quit_words:
                    break
                index = int(command) - 1
            except ValueError:
                print("Invalid command. Please enter a number.")
                continue
            if index < 0 or index >= len(method_signatures):
                print("Invalid command index")
                continue

            if len(method_signatures[index]["params"]) == 0:
                # Can call method directly
                result = getattr(app, method_signatures[index]["name"])()
                print(json.dumps(result, indent=2))
                current_command = None
                continue

            current_command = {
                "index": index,
                "params": {
                    param_name: None
                    for param_name in method_signatures[index]["params"]
                },
            }
            continue

        # Enter parameters for the selected command
        for param_name in current_command["params"]:
            current_command["params"][param_name] = input(
                f"Enter value for {param_name}: "
            )

        # Execute the command
        result = getattr(app, method_signatures[current_command["index"]]["name"])(
            **current_command["params"]
        )
        print(json.dumps(result, indent=2))
        current_command = None
