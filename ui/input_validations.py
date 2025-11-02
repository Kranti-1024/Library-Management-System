# This is 'ui/input_validations.py'

def get_non_empty_input(prompt):
    """Asks for input until a non-empty string is given."""
    user_input = ""
    while not user_input:
        user_input = input(prompt).strip() # .strip() removes whitespace
        if not user_input:
            print("Input cannot be empty. Please try again.")
    return user_input

def get_positive_integer_input(prompt):
    """Asks for input until a valid positive integer is given."""
    while True:
        try:
            user_input = input(prompt).strip()
            value = int(user_input)
            if value > 0:
                return value
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")