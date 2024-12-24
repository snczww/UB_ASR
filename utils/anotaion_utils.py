
def extract_lines_text_from_file(file_path, prefix='*CHI:'):
    """
    Extracts lines that start with a specific prefix from a file and returns them as a single string.

    Parameters:
    file_path (str): Path to the input file.
    prefix (str): The prefix to filter lines that start with it. Default is '*CHI:'.

    Returns:
    str: A string containing all lines that start with the specified prefix, 
         with the prefix removed and lines separated by newline characters.
    """
    try:
        # Open the file and read all lines
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if prefix is None:
            # Return all lines as a single string, stripped of leading/trailing whitespace
            filtered_lines = [line.strip() for line in lines]
        else:
            # Filter lines that start with the specified prefix and remove the prefix
            prefix_length = len(prefix)
            filtered_lines = [line.strip()[prefix_length:].strip() for line in lines if line.startswith(prefix)]


        # # Filter lines that start with the specified prefix and remove the prefix
        # prefix_length = len(prefix)
        # filtered_lines = [line.strip()[prefix_length:].strip() for line in lines if line.startswith(prefix)]

        # Join the list of filtered lines into a single string separated by newline characters
        filtered_lines_str = "\n".join(filtered_lines)

        return filtered_lines_str
    
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
def extract_lines_from_file(file_path, prefix='*CHI:'):
    """
    Extracts lines that start with a specific prefix from a file and returns them as a list of strings.

    Parameters:
    file_path (str): Path to the input file.
    prefix (str): The prefix to filter lines that start with it. Default is '*CHI:'.

    Returns:
    list: A list containing all lines that start with the specified prefix, 
          with the prefix removed and lines stripped of leading/trailing whitespace.
    """
    print(prefix)
    try:
        # Open the file and read all lines
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        print(lines)
        if prefix is None:
            # Return all lines, stripped of leading/trailing whitespace
            filtered_lines= [line.strip() for line in lines]
        else:
            print(prefix,len(prefix))
            # Filter lines that start with the specified prefix and remove the prefix
            prefix_length = len(prefix)
            filtered_lines= [line.strip()[prefix_length:].strip() for line in lines if line.startswith(prefix)]


        # # Filter lines that start with the specified prefix and remove the prefix
        # prefix_length = len(prefix)
        # filtered_lines = [line.strip()[prefix_length:].strip() for line in lines if line.startswith(prefix)]

        return filtered_lines
    
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"
