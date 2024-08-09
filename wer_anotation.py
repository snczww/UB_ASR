from transformers import AutoTokenizer
from anotation.find_all_anotations import collect_all_matches
from utils.ASR_utils import read_file 
from utils.wer_by_tokens import word_list_error_rate
from utils.anotaion_utils import extract_lines_text_from_file,extract_lines_from_file


def prepare_and_tokenize_text(ground_truth, candidate, tokenizer_model_path):
    """
    Prepare and tokenize the ground truth and candidate texts.

    Parameters:
    ground_truth (str): The ground truth text as a string.
    candidate (str): The candidate text as a string.
    tokenizer_model_path (str): The path to the pretrained tokenizer model.

    Returns:
    tuple: A tuple containing two lists of tokens (ground_truth_tokens, candidate_tokens).
    """
    # Read the fixed annotations from a predefined file
    fix_anotation = read_file('anotation/fix_anotation.txt')

    # Collect all matches from both ground truth and candidate texts, and combine with fixed annotations
    all_matches = (
        collect_all_matches(ground_truth) + 
        collect_all_matches(candidate) + 
        fix_anotation
    )

    # Initialize the tokenizer from the specified model path
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

    # Add custom tokens (annotations) to the tokenizer
    tokenizer.add_tokens(all_matches, special_tokens=True)

    # Tokenize the ground truth and candidate texts
    ground_truth_tokens = tokenizer(ground_truth, max_length=4096, truncation=True).tokens()
    candidate_tokens = tokenizer(candidate, max_length=4096, truncation=True).tokens()

    return ground_truth_tokens, candidate_tokens


def calculate_wer_bypath(ground_truth_path, candidate_path, tokenizer_model_path='allenai/longformer-base-4096'):
    """
    Calculate the Word Error Rate (WER) between a ground truth text and a candidate text 
    by providing the file paths for both texts.

    Parameters:
    ground_truth_path (str): The file path to the ground truth text.
    candidate_path (str): The file path to the candidate text.
    tokenizer_model_path (str): The path to the pretrained tokenizer model. 
                                Default is 'allenai/longformer-base-4096'.

    Returns:
    float: The calculated Word Error Rate (WER).
    """
    
    # Extract lines from ground truth and candidate files based on specific prefixes
    ground_truth_text = extract_lines_text_from_file(ground_truth_path, prefix='*CHI:')
    candidate_text = extract_lines_text_from_file(candidate_path, prefix='*PAR0:')

    # Prepare and tokenize the texts
    ground_truth_tokens, candidate_tokens = prepare_and_tokenize_text(
        ground_truth_text, candidate_text, tokenizer_model_path
    )

    # Calculate the Word Error Rate (WER)
    wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
    
    return wer


def calculate_wer_bysentence(ground_truth, candidate, tokenizer_model_path='allenai/longformer-base-4096'):
    """
    Calculate the Word Error Rate (WER) between a ground truth text and a candidate text 
    directly by providing the text strings.

    Parameters:
    ground_truth (str): The ground truth text as a string.
    candidate (str): The candidate text as a string.
    tokenizer_model_path (str): The path to the pretrained tokenizer model. 
                                Default is 'allenai/longformer-base-4096'.

    Returns:
    float: The calculated Word Error Rate (WER).
    """
    
    # Prepare and tokenize the texts
    ground_truth_tokens, candidate_tokens = prepare_and_tokenize_text(
        ground_truth, candidate, tokenizer_model_path
    )

    # Calculate the Word Error Rate (WER)
    wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
    
    return wer


if __name__ == "__main__":
    # Define model path and file paths
    tokenizer_model_path = 'allenai/longformer-base-4096'
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'
    wer = calculate_wer_bypath(ground_truth_path, candidate_path,tokenizer_model_path)

    ground_truth_lines= extract_lines_text_from_file(ground_truth_path, prefix='*CHI:')
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix='*PAR0:')
    # print(ground_truth_lines)
    # print(candidate_lines)
    for i in range(len(ground_truth_lines)):
        weri = calculate_wer_bypath(ground_truth_lines[i],candidate_lines[i])
        print(f"Word Error Rate: {weri * 100:.2f}%")

    print(f"Word Error Rate: {wer * 100:.2f}%")