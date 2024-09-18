import re
import pandas as pd
from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationOnlyLineByLineStrategy, 
    WERAnnotationWholeTextStrategy, 
    WERAnnotationLineByLineStrategy
)
from utils.anotaion_utils import extract_lines_from_file

def remove_nak_to_end(line):
    """
    Remove content starting with 'NAK' to the end of the line.
    
    Parameters:
    line (str): The input line of text.
    
    Returns:
    str: The line with content after 'NAK' removed.
    """
    return re.sub(r'NAK.*', '', line)

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

    # Ensure the lengths of ground truth and candidate lines match
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines = ground_truth_lines[:min_length]
    candidate_lines = candidate_lines[:min_length]

    # Initialize the WERCalculator with default fixed_annotations from fix_anotation.txt and decimal_places = 2
    calculator = WERCalculator(WERAnnotationOnlyWholeTextStrategy())  # Use default tokenizer_model_path, fixed_annotations, and decimal_places

    # Strategy 1: Calculate WER treating lists as whole texts
    overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall AnnotationOnlyWER (Whole Text): {overall_wer}")

    # Strategy 2: Calculate WER line by line and save results to CSV
    calculator.set_strategy(WERAnnotationOnlyLineByLineStrategy())
    line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)

    # Create a DataFrame to store the results
    df = pd.DataFrame({
        'Ground Truth Line': ground_truth_lines,
        'Candidate Line': candidate_lines,
        'Line WER': line_wer_list
    })

    # Save the DataFrame to a CSV file
    df.to_csv(output_csv_path, index=False)
    print(f"WER results saved to {output_csv_path}")

    # Strategy 3: Calculate WER on annotations (whole text)
    calculator.set_strategy(WERAnnotationWholeTextStrategy())
    overall_annotation_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall Annotation WER (Whole Text): {overall_annotation_wer}")

    # Strategy 4: Calculate WER on annotations (line by line)
    calculator.set_strategy(WERAnnotationLineByLineStrategy())
    annotation_line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    
    # Save annotation line WER to another CSV file
    annotation_output_csv_path = 'wer_annotation_wer_output.csv'
    annotation_df = pd.DataFrame({
        'Ground Truth Line': ground_truth_lines,
        'Candidate Line': candidate_lines,
        'Annotation Line WER': annotation_line_wer_list
    })
    annotation_df.to_csv(annotation_output_csv_path, index=False)
    print(f"Annotation WER results saved to {annotation_output_csv_path}")
