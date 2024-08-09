from transformers import AutoTokenizer
from anotation.find_all_anotations import collect_all_matches
from utils.ASR_utils import read_file
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

        # # Use list comprehension to filter lines that start with '*CHI:'
        # chi_lines = [line.strip() for line in lines if line.startswith('*CHI:')]

        # # Use list comprehension to filter lines that start with '*CHI:' whitout chi

        chi_lines = [line.strip()[5:].strip() for line in lines if line.startswith('*CHI:')]

        # Join the list of lines into a single string with newline characters separating them
        chi_lines_str = "\n".join(chi_lines)

        return chi_lines_str
    
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

fix_anotation=read_file('/home/jovyan/work/anotation/fix_anotation.txt')
all_matches=[]
dictionary_path='/home/jovyan/work/audio_files/758.txt'
transcript_text = extract_chi_lines_from_file(dictionary_path)
print(type(transcript_text))
# for i in transcript_text:
#     single_line_matches=collect_all_matches(i)
#     all_matches = single_line_matches + all_matches
all_matches = collect_all_matches(transcript_text) + fix_anotation
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
  
num_added_toks = tokenizer.add_tokens(all_matches, special_tokens=True)
  
print("We have added", num_added_toks, "tokens")
split_tokens=tokenizer(transcript_text).tokens()
# print(tokenizer(transcript_text).tokens())
# print(type(tokenizer(transcript_text).tokens()))
for item in split_tokens:
    print(item)