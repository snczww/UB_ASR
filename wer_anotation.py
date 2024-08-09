from transformers import AutoTokenizer
from anotation.find_all_anotations import collect_all_matches
from utils.ASR_utils import read_file 
from utils.wer_by_tokens import word_list_error_rate
from utils.anotaion_utils import extract_lines_from_file


# Define model path and file paths
tokenizer_model_path = 'allenai/longformer-base-4096'
ground_truth_path = 'anotation/cha_files/758_2.cha'
candidate_path = 'anotation/cha_files/758_AI.cha'

def calculate_wer(ground_truth_path, candidate_path,tokenizer_model_path='allenai/longformer-base-4096'):
    """
    Calculate the Word Error Rate (WER) between a ground truth text and a candidate text.

    Parameters:
    tokenizer_model_path (str): The path to the pretrained tokenizer model.
    ground_truth_path (str): The file path to the ground truth text.
    candidate_path (str): The file path to the candidate text.

    Returns:
    float: The calculated Word Error Rate (WER).
    """

    # Read the fixed annotations from a file
    fix_anotation = read_file('anotation/fix_anotation.txt')

    # Extract lines from ground truth and candidate files based on specific prefixes
    ground_truth_text = extract_lines_from_file(ground_truth_path, prefix='*CHI:')
    candidate_text = extract_lines_from_file(candidate_path, prefix='*PAR0:')

    # Collect all matches from both ground truth and candidate texts, and combine with fixed annotations
    all_matches = (
        collect_all_matches(ground_truth_text) + 
        collect_all_matches(candidate_text) + 
        fix_anotation
    )

    # Initialize the tokenizer from the specified model path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

    # Add custom tokens (annotations) to the tokenizer
    tokenizer.add_tokens(all_matches, special_tokens=True)

    # Tokenize the ground truth and candidate texts
    ground_truth_text_split_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
    candidate_text_split_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

    # Calculate the Word Error Rate (WER) between the tokenized ground truth and candidate texts
    wer = word_list_error_rate(ground_truth_text_split_tokens, candidate_text_split_tokens)
    
    return wer



# Read the fixed annotations from a file
# fix_anotation = read_file('anotation/fix_anotation.txt')

# # Extract lines from ground truth and candidate files based on specific prefixes
# ground_truth_text = extract_lines_from_file(ground_truth_path, prefix='*CHI:')
# candidate_text = extract_lines_from_file(candidate_path, prefix='*PAR0:')

# # Collect all matches from both ground truth and candidate texts, and combine with fixed annotations
# all_matches = collect_all_matches(ground_truth_text) + collect_all_matches(candidate_text) + fix_anotation

# # Initialize the tokenizer from the specified model path
# tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

# # Add custom tokens (annotations) to the tokenizer
# num_added_toks = tokenizer.add_tokens(all_matches, special_tokens=True)

# # Tokenize the ground truth and candidate texts
# ground_truth_text_split_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
# candidate_text_split_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

# # Calculate the Word Error Rate (WER) between the tokenized ground truth and candidate texts
# wer = word_list_error_rate(ground_truth_text_split_tokens, candidate_text_split_tokens)

wer = calculate_wer(ground_truth_path, candidate_path,tokenizer_model_path)

print(f"Word Error Rate: {wer * 100:.2f}%")
