import os
from transformers import AutoTokenizer
from anotation.find_all_anotations import collect_all_matches
from utils.ASR_utils import read_file 
from utils.wer_by_tokens import word_list_error_rate
from utils.anotaion_utils import extract_lines_text_from_file
import concurrent.futures
from anotation.find_all_anotations import *

def load_and_tokenize_texts(ground_truth, candidate, tokenizer, annotations):
    """
    Tokenize both ground truth and candidate texts.

    Parameters:
    ground_truth (str): The ground truth text.
    candidate (str): The candidate text.
    tokenizer (AutoTokenizer): Tokenizer object.
    annotations (list): Custom tokens to add to the tokenizer.

    Returns:
    tuple: Tokenized ground truth and candidate texts.
    """
    tokenizer.add_tokens(annotations, special_tokens=True)
    return (tokenizer(ground_truth, max_length=4096, truncation=True).tokens(),
            tokenizer(candidate, max_length=4096, truncation=True).tokens())


def prepare_and_tokenize_text(ground_truth, candidate, tokenizer_model_path, fixed_annotations):
    """
    Prepare and tokenize both ground truth and candidate texts.

    Parameters:
    ground_truth (str): The ground truth text.
    candidate (str): The candidate text.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.

    Returns:
    tuple: Tokenized ground truth and candidate texts.
    """
    all_matches = collect_all_matches(ground_truth) + collect_all_matches(candidate) + fixed_annotations
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

    return load_and_tokenize_texts(ground_truth, candidate, tokenizer, all_matches)


def calculate_wer(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations, decimal_places):
    """
    General function to calculate WER between two texts.
    
    Parameters:
    ground_truth_text (str): The ground truth text.
    candidate_text (str): The candidate text.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER result.

    Returns:
    float: WER rounded to the specified decimal places.
    """
    ground_truth_tokens, candidate_tokens = prepare_and_tokenize_text(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations)
    wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
    return round(wer, decimal_places)


def calculate_overall_and_line_wer(tokenizer_model_path, ground_truth_path, candidate_path, fixed_annotations, decimal_places=3, prefix_ground_truth='*CHI:', prefix_candidate='*PAR0:'):
    """
    Calculate the overall and line-by-line WER for given text files.

    Parameters:
    tokenizer_model_path (str): Path to the tokenizer model.
    ground_truth_path (str): Path to the ground truth .cha file.
    candidate_path (str): Path to the candidate .cha file.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER results.
    prefix_ground_truth (str): Prefix to filter ground truth lines (default '*CHI:').
    prefix_candidate (str): Prefix to filter candidate lines (default '*PAR0:').

    Returns:
    tuple: Overall WER and line-by-line WERs.
    """
    # Ensure file paths exist
    if not os.path.exists(ground_truth_path) or not os.path.exists(candidate_path):
        raise FileNotFoundError("One or both input files are missing.")

    # Extract full texts from files
    ground_truth_text = ' '.join(extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth))
    candidate_text = ' '.join(extract_lines_text_from_file(candidate_path, prefix=prefix_candidate))

    # Calculate overall WER
    overall_wer = calculate_wer(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations, decimal_places)

    # Extract lines for line-by-line WER
    ground_truth_lines = extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix=prefix_candidate)

    # Ensure matching line lengths
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

    # Use parallel processing only if there are enough lines
    if min_length > 10:
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            wer_list = list(executor.map(lambda pair: calculate_wer(pair[0], pair[1], tokenizer_model_path, fixed_annotations, decimal_places), 
                                         zip(ground_truth_lines, candidate_lines)))
    else:
        wer_list = [calculate_wer(gt, cand, tokenizer_model_path, fixed_annotations, decimal_places) for gt, cand in zip(ground_truth_lines, candidate_lines)]

    return overall_wer, wer_list


# if __name__ == "__main__":
#     # Define model and file paths
#     tokenizer_model_path = 'allenai/longformer-base-4096'
#     ground_truth_path = 'anotation/cha_files/758_2.cha'
#     candidate_path = 'anotation/cha_files/758_AI.cha'

#     # Load fixed annotations
#     fixed_annotations = read_file('anotation/fix_anotation.txt')
    

#     # Set number of decimal places
#     decimal_places = 3

#     # Calculate overall and line-by-line WER
#     overall_wer, wer_list = calculate_overall_and_line_wer(tokenizer_model_path, ground_truth_path, candidate_path, fixed_annotations, decimal_places)
    
#     # Output results
#     print(f"Overall WER: {overall_wer}")
#     print(f"Line-by-line WER: {wer_list}")


if __name__ == "__main__":
    # Define model and file paths
    tokenizer_model_path = 'allenai/longformer-base-4096'
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'

    # Load fixed annotations
    fixed_annotations = read_file('anotation/fix_anotation.txt')

    # Set number of decimal places
    decimal_places = 3

    # Calculate overall and line-by-line WER
    overall_wer, wer_list, ground_truth_lines, candidate_lines = calculate_overall_and_line_wer(
        tokenizer_model_path, ground_truth_path, candidate_path, fixed_annotations, decimal_places)
    
    # Create a DataFrame to display the results in a table format
    data = {
        'Ground Truth Line': ground_truth_lines,
        'Candidate Line': candidate_lines,
        'Line-by-line WER': wer_list
    }
    
    df = pd.DataFrame(data)
    
    # Display the DataFrame as a table
    print(f"Overall WER: {overall_wer}")
    print("Line-by-line WER Table:")
    print(df)