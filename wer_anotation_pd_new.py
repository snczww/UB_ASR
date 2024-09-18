import os
from wer_by_list import (
    calculate_annotation_overall_wer_by_list,
    calculate_annotation_line_wer_by_list
)
from utils.ASR_utils import read_file
from utils.anotaion_utils import extract_lines_from_file, extract_lines_text_from_file

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

    # Extract lines from files
    ground_truth_lines = extract_lines_from_file(ground_truth_path, prefix=prefix_ground_truth)
    candidate_lines = extract_lines_from_file(candidate_path, prefix=prefix_candidate)

    # Ensure matching line lengths
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines = ground_truth_lines[:min_length]
    candidate_lines = candidate_lines[:min_length]

    # Calculate overall WER
    overall_wer = calculate_annotation_overall_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)

    # Calculate line-by-line WER
    wer_list = calculate_annotation_line_wer_by_list(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)

    return overall_wer, wer_list


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
    overall_wer, wer_list = calculate_overall_and_line_wer(tokenizer_model_path, ground_truth_path, candidate_path, fixed_annotations, decimal_places)

    # Output results
    print(f"Overall WER: {overall_wer}")
    print(f"Line-by-line WER: {wer_list}")
