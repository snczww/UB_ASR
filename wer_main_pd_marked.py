import re
import pandas as pd
import logging

from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationOnlyLineByLineStrategy, 
    WERAnnotationWholeTextStrategy, 
    WERAnnotationLineByLineStrategy,
    WERAnnotationLineByLineStrategy_marked
)
from utils.anotaion_utils import extract_lines_from_file
from mark_difference_V05 import mark_word_changes  # 引入compare_strings函数
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def remove_nak_to_end(line):
    """
    Remove content starting with 'NAK' to the end of the line.
    
    Parameters:
    line (str): The input line of text.
    
    Returns:
    str: The line with content after 'NAK' removed.
    """
    # return re.sub(r'NAK.*', '', line)
    return re.sub(r'\x15\d+_\d+\x15', '', line)


if __name__ == "__main__":
    # Define file paths
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'
    output_csv_path = 'wer_output.csv'  # Define the CSV output path

    # Extract lines from files
    ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

    # Remove content after 'NAK' from each line in both ground truth and candidate lines
    ground_truth_lines = [remove_nak_to_end(line) for line in ground_truth_lines]
    candidate_lines = [remove_nak_to_end(line) for line in candidate_lines]
    # logging.info(f"Initializing tokenizer from {ground_truth_lines}.")

    # Ensure the lengths of ground truth and candidate lines match
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines = ground_truth_lines[:min_length]
    candidate_lines = candidate_lines[:min_length]

    # 使用 mark_word_changes 函数处理每对 ground truth 和 candidate lines
    calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
    # compared_candidate_lines = calculator.mark_changes(ground_truth_lines, candidate_lines)
    compared_ground_truth_lines, compared_candidate_lines = calculator.mark_changes(ground_truth_lines, candidate_lines)


    # Initialize the WERCalculator with default fixed_annotations from fix_anotation.txt and decimal_places = 2
    calculator = WERCalculator(WERAnnotationOnlyWholeTextStrategy())  # Use default tokenizer_model_path, fixed_annotations, and decimal_places

    # Strategy 1: Calculate WER treating lists as whole texts
    overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall AnnotationOnlyWER (Whole Text): {overall_wer}")

    # Strategy 2: Calculate WER line by line and save results to CSV
    calculator.set_strategy(WERAnnotationLineByLineStrategy_marked())
    line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f'WERAnnotationLineByLineStrategy_marked{line_wer_list}')

    # Create a DataFrame to store the results with compared strings
    df = pd.DataFrame({
        # 'Ground Truth Line': ground_truth_lines,
        'Ground Truth Line': compared_ground_truth_lines,
        'Candidate Line (Compared)': compared_candidate_lines,  # 将compare_strings处理后的结果放入
        # 'Candidate Line': compared_ground_truth_lines,  # 将compare_strings处理后的结果放入
        'Line WER': line_wer_list
    })

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"WER results saved to {output_csv_path}")

    # Strategy 3: Calculate WER on annotations (whole text)
    # calculator.set_strategy(WERAnnotationWholeTextStrategy())
    calculator = WERCalculator(WERAnnotationWholeTextStrategy())

    overall_annotation_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall Annotation WER (Whole Text): {overall_annotation_wer}")

    # Strategy 4: Calculate WER on annotations (line by line)
    calculator.set_strategy(WERAnnotationLineByLineStrategy())
    annotation_line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    
    # Save annotation line WER to another CSV file
    annotation_output_csv_path = 'wer_annotation_wer_output.csv'
    annotation_df = pd.DataFrame({
        'Ground Truth Line': ground_truth_lines,
        'Candidate Line (Compared)': compared_candidate_lines,  # 再次使用compare_strings处理的结果
        # 'Candidate Line': candidate_lines,  # 将compare_strings处理后的结果放入
        'Annotation Line WER': annotation_line_wer_list
    })
    annotation_df.to_csv(annotation_output_csv_path, index=False)
    print(f"Annotation WER results saved to {annotation_output_csv_path}")
