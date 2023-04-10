import re

# Function to extract and remove the first action from a string
def extract_and_remove_first_action(s, action_syntax):
    # Create a regex pattern for the action syntax
    pattern = re.compile(action_syntax)
    # Find the first match of the action syntax in the string
    match = pattern.search(s)
    if match:
        # Extract the matched action
        action_to_remove = match.group(0)
        # Remove the action from the string
        s = s.replace(action_to_remove, '', 1)
        print(f"Removed action: {action_to_remove}")
        return action_to_remove
    else:
        print("No matching action found")
        return None

# Example usage
long_string = 'action1PRE:action1:POSTaction2PRE:action2:POSTaction3...'
action_syntax = r'PRE:(.*?):POST'  # Regular expression for the action syntax

# Extract and remove the first action from the long string
long_string = extract_and_remove_first_action(long_string, action_syntax)

if long_string is not None:
    print("Remaining string:", long_string)
else:
    print("No action found, remaining string is None")
