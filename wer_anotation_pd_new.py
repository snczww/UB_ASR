import os
import pandas as pd
from transformers import AutoTokenizer
from utils.ASR_utils import read_file
from wer_by_path import calculate_overall_wer_by_path, calculate_line_wer_by_path
from utils.anotaion_utils import *

if __name__ == "__main__":
    # 定义模型路径和文件路径
    tokenizer_model_path = 'allenai/longformer-base-4096'
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'

    # 加载固定的注释标记
    fixed_annotations = read_file('anotation/fix_anotation.txt')

    # 设置小数位数
    decimal_places = 3

    # 计算整体 WER
    overall_wer = calculate_overall_wer_by_path(
        ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places
    )

    # 计算逐行 WER
    wer_list = calculate_line_wer_by_path(
        ground_truth_path, candidate_path, tokenizer_model_path, fixed_annotations, decimal_places
    )

    # 从文件中提取逐行文本
    ground_truth_lines = extract_lines_from_file(ground_truth_path, prefix='*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, prefix='*PAR0:')

    # 确保两边的文本行数匹配
    min_length = min(len(ground_truth_lines), len(candidate_lines))
    ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

    # 将结果存储到DataFrame
    data = {
        'Ground Truth Line': ground_truth_lines,
        'Candidate Line': candidate_lines,
        'Line-by-line WER': wer_list
    }
    
    df = pd.DataFrame(data)
    output_csv_path = 'wer_output.csv'
    df.to_csv(output_csv_path, index=False)

    # 打印整体 WER 结果和逐行 WER 表
    print(f"Overall WER: {overall_wer}")
    print("Line-by-line WER Table:")
    print(df)
