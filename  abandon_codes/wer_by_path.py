from wer_by_list import (
    calculate_overall_wer_by_list,
    calculate_line_wer_by_list,
    calculate_annotation_line_wer_by_list,
    calculate_annotation_overall_wer_by_list
)
from utils.anotaion_utils import extract_lines_text_from_file
import os

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


# 新增功能：calculate_annotation_overall_wer_by_path
def calculate_annotation_overall_wer_by_path(ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places=3, prefix_ground_truth='*CHI:', prefix_candidate='*PAR0:'):
    """
    Calculate overall WER after filtering input lists to only retain annotation matches and fixed annotations.
    This function processes files from the provided paths.
    
    Parameters:
    ground_truth_path (str): Path to the ground truth .cha file.
    candidate_path (str): Path to the candidate .cha file.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): List of fixed annotations.
    decimal_places (int): Number of decimal places to round the WER result.
    prefix_ground_truth (str): Prefix to filter ground truth lines (default '*CHI:').
    prefix_candidate (str): Prefix to filter candidate lines (default '*PAR0:').

    Returns:
    float: The overall WER after processing the filtered input files.
    """
    if not os.path.exists(ground_truth_path) or not os.path.exists(candidate_path):
        raise FileNotFoundError("One or both input files are missing.")
    
    # Extract lines from files
    ground_truth_lines = extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix=prefix_candidate)

    # Use the existing calculate_annotation_overall_wer_by_list function
    return calculate_annotation_overall_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)


# 新增功能：calculate_annotation_line_wer_by_path
def calculate_annotation_line_wer_by_path(ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places=3, prefix_ground_truth='*CHI:', prefix_candidate='*PAR0:'):
    """
    Calculate line-by-line WER after filtering input lists to only retain annotation matches and fixed annotations.
    This function processes files from the provided paths.
    
    Parameters:
    ground_truth_path (str): Path to the ground truth .cha file.
    candidate_path (str): Path to the candidate .cha file.
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): List of fixed annotations.
    decimal_places (int): Number of decimal places to round the WER result.
    prefix_ground_truth (str): Prefix to filter ground truth lines (default '*CHI:').
    prefix_candidate (str): Prefix to filter candidate lines (default '*PAR0:').

    Returns:
    list: List of WER values for each line after processing the filtered input files.
    """
    if not os.path.exists(ground_truth_path) or not os.path.exists(candidate_path):
        raise FileNotFoundError("One or both input files are missing.")
    
    # Extract lines from files
    ground_truth_lines = extract_lines_text_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_text_from_file(candidate_path, prefix=prefix_candidate)

    # Use the existing calculate_annotation_line_wer_by_list function
    return calculate_annotation_line_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)
