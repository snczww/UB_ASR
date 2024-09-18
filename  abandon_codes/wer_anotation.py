import os
import concurrent.futures
from transformers import AutoTokenizer
from find_all_anotations import collect_all_matches
from utils.ASR_utils import read_file
from utils.wer_by_tokens import word_list_error_rate
from utils.anotaion_utils import *

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

def calculate_overall_wer(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate overall WER between ground truth and candidate texts.

    Parameters:
    ground_truth_text (str): The ground truth text.
    candidate_text (str): The candidate text.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER result.

    Returns:
    float: The overall WER.
    """
    return calculate_wer(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations, decimal_places)

def calculate_line_wer(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate WER for each line between ground truth and candidate lines.

    Parameters:
    ground_truth_lines (list): List of ground truth lines.
    candidate_lines (list): List of candidate lines.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER results.

    Returns:
    list: List of WER values for each line.
    """
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

    return wer_list

def calculate_line_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate line-by-line WER after processing the input lists with collect_all_matches.

    Parameters:
    ground_truth_lines (list): List of ground truth lines.
    candidate_lines (list): List of candidate lines.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER results.

    Returns:
    list: List of WER values for each line after processing annotations.
    """
    # Collect all matches from both lists
    all_matches = collect_all_matches(' '.join(ground_truth_lines)) + collect_all_matches(' '.join(candidate_lines)) + fixed_annotations
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

    # Tokenize each line with annotations
    ground_truth_tokens_list = [tokenizer(gt, max_length=4096, truncation=True).tokens() for gt in ground_truth_lines]
    candidate_tokens_list = [tokenizer(cand, max_length=4096, truncation=True).tokens() for cand in candidate_lines]

    # Calculate WER for each tokenized line
    wer_list = [word_list_error_rate(gt_tokens, cand_tokens) for gt_tokens, cand_tokens in zip(ground_truth_tokens_list, candidate_tokens_list)]
    
    # Round the WER results
    wer_list = [round(wer, decimal_places) for wer in wer_list]

    return wer_list

def calculate_overall_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate overall WER after processing the input lists with collect_all_matches.

    Parameters:
    ground_truth_lines (list): List of ground truth lines.
    candidate_lines (list): List of candidate lines.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER results.

    Returns:
    float: The overall WER after processing the input lists.
    """
    # Combine all lines into a single text for ground truth and candidate
    ground_truth_text = ' '.join(ground_truth_lines)
    candidate_text = ' '.join(candidate_lines)

    # Collect all matches
    all_matches = collect_all_matches(ground_truth_text) + collect_all_matches(candidate_text) + fixed_annotations

    # Tokenize and calculate overall WER
    return calculate_wer(ground_truth_text, candidate_text, tokenizer_model_path, all_matches, decimal_places)

def calculate_overall_wer_by_path(ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places=3, prefix_ground_truth='*CHI:', prefix_candidate='*PAR0:'):
    """
    Calculate overall WER based on the file paths of ground truth and candidate.

    Parameters:
    ground_truth_path (str): Path to the ground truth .cha file.
    candidate_path (str): Path to the candidate .cha file.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER result.
    prefix_ground_truth (str): Prefix to filter ground truth lines (default '*CHI:').
    prefix_candidate (str): Prefix to filter candidate lines (default '*PAR0:').

    Returns:
    float: The overall WER based on the input file paths.
    """
    if not os.path.exists(ground_truth_path) or not os.path.exists(candidate_path):
        raise FileNotFoundError("One or both input files are missing.")
    
    # Extract lines from files
    ground_truth_lines = extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix=prefix_candidate)

    # Use the existing calculate_overall_wer_by_list function
    return calculate_overall_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)

def calculate_line_wer_by_path(ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places=3, prefix_ground_truth='*CHI:', prefix_candidate='*PAR0:'):
    """
    Calculate line-by-line WER based on the file paths of ground truth and candidate.

    Parameters:
    ground_truth_path (str): Path to the ground truth .cha file.
    candidate_path (str): Path to the candidate .cha file.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): Fixed annotations to be included in tokenization.
    decimal_places (int): Number of decimal places to round the WER results.
    prefix_ground_truth (str): Prefix to filter ground truth lines (default '*CHI:').
    prefix_candidate (str): Prefix to filter candidate lines (default '*PAR0:').

    Returns:
    list: List of WER values for each line.
    """
    if not os.path.exists(ground_truth_path) or not os.path.exists(candidate_path):
        raise FileNotFoundError("One or both input files are missing.")
    
    # Extract lines from files
    ground_truth_lines = extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix=prefix_candidate)

    # Use the existing calculate_line_wer_by_list function
    return calculate_line_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)

def filter_text_by_annotations(text_lines, fixed_annotations):
    """
    Filter each line in the provided list to retain only words that match annotations or fixed annotations.

    Parameters:
    text_lines (list): List of text lines to filter.
    fixed_annotations (list): List of fixed annotations.

    Returns:
    list: List of filtered text lines, containing only matched annotations and fixed annotations.
    """
    filtered_lines = []
    for line in text_lines:
        # Find all matches from the line using collect_all_matches
        annotation_matches = collect_all_matches(line)
        # Combine matches with fixed annotations
        valid_tokens = annotation_matches + fixed_annotations
        # Filter the line to keep only the valid tokens
        filtered_line = ' '.join([word for word in line.split() if word in valid_tokens])
        filtered_lines.append(filtered_line)
    return filtered_lines


def calculate_annotation_overall_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate overall WER after filtering input lists to only retain annotation matches and fixed annotations.

    Parameters:
    ground_truth_lines (list): List of ground truth lines.
    candidate_lines (list): List of candidate lines.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): List of fixed annotations.
    decimal_places (int): Number of decimal places to round the WER result.

    Returns:
    float: The overall WER after processing the filtered input lists.
    """
    # Filter both ground truth and candidate lines
    filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations)
    filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations)

    # Combine the filtered lines into full texts
    ground_truth_text = ' '.join(filtered_ground_truth)
    candidate_text = ' '.join(filtered_candidate)

    # Calculate the overall WER using the existing function
    return calculate_wer(ground_truth_text, candidate_text, tokenizer_model_path, fixed_annotations, decimal_places)


def calculate_annotation_line_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places=3):
    """
    Calculate line-by-line WER after filtering input lists to only retain annotation matches and fixed annotations.
    
    Parameters:
    ground_truth_lines (list): List of ground truth lines.
    candidate_lines (list): List of candidate lines.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): List of fixed annotations.
    decimal_places (int): Number of decimal places to round the WER result.
    
    Returns:
    list: List of WER values for each line after processing the filtered input lists.
    """
    # Ensure the lists have the same length
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines = ground_truth_lines[:min_length]
    candidate_lines = candidate_lines[:min_length]

    # Filter both ground truth and candidate lines
    filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations)
    filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations)

    # Replace empty lines with a single space
    filtered_ground_truth = [' ' if not line.strip() else line for line in filtered_ground_truth]
    filtered_candidate = [' ' if not line.strip() else line for line in filtered_candidate]

    # Use parallel processing to calculate WER line by line if there are enough lines
    if min_length > 10:
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            wer_list = list(executor.map(
                lambda pair: calculate_wer(pair[0], pair[1], tokenizer_model_path, fixed_annotations, decimal_places),
                zip(filtered_ground_truth, filtered_candidate)
            ))
    else:
        wer_list = [
            calculate_wer(gt, cand, tokenizer_model_path, fixed_annotations, decimal_places)
            for gt, cand in zip(filtered_ground_truth, filtered_candidate)
        ]

    return wer_list

