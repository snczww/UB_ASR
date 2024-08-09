def extract_chi_lines_from_file(file_path):
    """
    This function extracts lines that start with '*CHI:' from a file and returns them as a single string.

    Parameters:
    file_path (str): Path to the input file.

    Returns:
    str: A string containing all lines that start with '*CHI:', separated by newline characters.
    """
    try:
        # Open the file and read all lines
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Use list comprehension to filter lines that start with '*CHI:'
        chi_lines = [line.strip() for line in lines if line.startswith('*CHI:')]

        # Join the list of lines into a single string with newline characters separating them
        chi_lines_str = "\n".join(chi_lines)

        return chi_lines_str
    
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# 示例调用方式
file_path = '/home/jovyan/work/audio_files/758.txt'

# 使用函数提取*CHI:开头的行，并返回字符串
chi_lines_str = extract_chi_lines_from_file(file_path)

# 打印结果

