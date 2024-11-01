import os
from transformers import AutoTokenizer
from wer_by_list import (
    calculate_overall_wer_by_list,
    calculate_line_wer_by_list,
    calculate_annotation_overall_wer_by_list,
    calculate_annotation_line_wer_by_list
)
from utils.ASR_utils import read_file
from utils.anotaion_utils import extract_lines_text_from_file

if __name__ == "__main__":
    # 定义模型路径和文件路径
    tokenizer_model_path = 'allenai/longformer-base-4096'

    # 假设已经有一些ground truth和candidate的文本行，用作测试
    ground_truth_lines = [
        "I want to eat an apple",
        "It is a sunny day",
        "The cat is sleeping on the couch"
    ]

    candidate_lines = [
        "I want to eat apple",
        "It was a sunny day",
        "The cat is sleep on the couch"
    ]

    # 定义固定的注释
    fixed_annotations = ["<unk>", "[UNK]"]  # 示例注释

    # 设置小数位数
    decimal_places = 3

    print("### Test: calculate_overall_wer_by_list ###")
    overall_wer = calculate_overall_wer_by_list(
        ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places
    )
    print(f"Overall WER: {overall_wer}")

    print("\n### Test: calculate_line_wer_by_list ###")
    line_wer = calculate_line_wer_by_list(
        ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places
    )
    print(f"Line-by-line WER: {line_wer}")

    print("\n### Test: calculate_annotation_overall_wer_by_list ###")
    annotation_overall_wer = calculate_annotation_overall_wer_by_list(
        ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places
    )
    print(f"Annotation Overall WER: {annotation_overall_wer}")

    print("\n### Test: calculate_annotation_line_wer_by_list ###")
    annotation_line_wer = calculate_annotation_line_wer_by_list(
        ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places
    )
    print(f"Annotation Line-by-line WER: {annotation_line_wer}")
