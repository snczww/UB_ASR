# main.py

from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationOnlyLineByLineStrategy, 
    WERAnnotationWholeTextStrategy, 
    WERAnnotationLineByLineStrategy
)
from utils.anotaion_utils import extract_lines_from_file

if __name__ == "__main__":
    # Define file paths
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'

    # Extract lines from files
    ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

    # Initialize the WERCalculator with default fixed_annotations from fix_anotation.txt and decimal_places = 2
    calculator = WERCalculator(WERAnnotationOnlyWholeTextStrategy())  # Use default tokenizer_model_path, fixed_annotations, and decimal_places

    # User can override the fixed_annotations, decimal_places, or tokenizer_model_path if desired
    user_fixed_annotations = ['<custom_annotation1>', '<custom_annotation2>']  # User provided annotations
    calculator.set_fixed_annotations(user_fixed_annotations)  # Optional: set custom fixed_annotations
    # calculator.set_decimal_places(3)  # Optional: change decimal_places to 3
    # calculator.set_tokenizer_model_path('another/tokenizer/path')  # Optional: change tokenizer_model_path

    # Strategy 1: Calculate WER treating lists as whole texts
    overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall WER (Whole Text): {overall_wer}")

    # Strategy 2: Calculate WER line by line
    calculator.set_strategy(WERAnnotationOnlyLineByLineStrategy())
    line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Line-by-Line WER: {line_wer_list}")

    # Strategy 3: Calculate WER on annotations (whole text)
    calculator.set_strategy(WERAnnotationWholeTextStrategy())
    overall_annotation_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall Annotation WER (Whole Text): {overall_annotation_wer}")

    # Strategy 4: Calculate WER on annotations (line by line)
    calculator.set_strategy(WERAnnotationLineByLineStrategy())
    annotation_line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Line-by-Line Annotation WER: {annotation_line_wer_list}")
