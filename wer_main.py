# main.py

from wer_context import WERContext
from wer_strategy import (
    WERWholeTextStrategy, 
    WERLineByLineStrategy, 
    WERAnnotationWholeTextStrategy, 
    WERAnnotationLineByLineStrategy
)
from utils.ASR_utils import read_file
from utils.anotaion_utils import extract_lines_from_file

if __name__ == "__main__":
    # Define tokenizer model and file paths
    tokenizer_model_path = 'allenai/longformer-base-4096'
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'
    fixed_annotations = read_file('anotation/fix_anotation.txt')
    decimal_places = 3

    # Extract lines from files
    ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

    # Strategy 1: Calculate WER treating lists as whole texts
    context = WERContext(WERWholeTextStrategy())
    overall_wer = context.calculate(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)
    print(f"Overall WER (Whole Text): {overall_wer}")

    # Strategy 2: Calculate WER line by line
    context.set_strategy(WERLineByLineStrategy())
    line_wer_list = context.calculate(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)
    print(f"Line-by-Line WER: {line_wer_list}")

    # Strategy 3: Calculate WER on annotations (whole text)
    context.set_strategy(WERAnnotationWholeTextStrategy())
    overall_annotation_wer = context.calculate(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)
    print(f"Overall Annotation WER (Whole Text): {overall_annotation_wer}")

    # Strategy 4: Calculate WER on annotations (line by line)
    context.set_strategy(WERAnnotationLineByLineStrategy())
    annotation_line_wer_list = context.calculate(ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places)
    print(f"Line-by-Line Annotation WER: {annotation_line_wer_list}")
