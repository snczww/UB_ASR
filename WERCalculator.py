from transformers import AutoTokenizer
from utils.ASR_utils import read_file
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches
import concurrent.futures
import os

class WERCalculator:
    def __init__(self, tokenizer_model_path, fixed_annotations_path=None):
        # 初始化，加载tokenizer和固定注释
        self.tokenizer_model_path = tokenizer_model_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        self.fixed_annotations = self._load_fixed_annotations(fixed_annotations_path)

    def _load_fixed_annotations(self, path):
        # 加载固定注释
        if path:
            return read_file(path)
        return []

    def load_and_tokenize_texts(self, ground_truth, candidate, annotations=None):
        # 将文本标记化
        if annotations:
            self.tokenizer.add_tokens(annotations, special_tokens=True)
        ground_truth_tokens = self.tokenizer(ground_truth, max_length=4096, truncation=True).tokens()
        candidate_tokens = self.tokenizer(candidate, max_length=4096, truncation=True).tokens()
        return ground_truth_tokens, candidate_tokens

    def calculate_wer(self, ground_truth_text, candidate_text, decimal_places=3):
        # 计算整体 WER
        ground_truth_tokens, candidate_tokens = self.load_and_tokenize_texts(ground_truth_text, candidate_text, self.fixed_annotations)
        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

    def calculate_line_wer(self, ground_truth_lines, candidate_lines, decimal_places=3):
        # 逐行计算 WER
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

        wer_list = []
        for gt, cand in zip(ground_truth_lines, candidate_lines):
            wer = self.calculate_wer(gt, cand, decimal_places)
            wer_list.append(wer)

        return wer_list

    def calculate_annotation_wer(self, ground_truth, candidate, decimal_places=3):
        # 基于注释计算 WER
        annotations = collect_all_matches(ground_truth) + collect_all_matches(candidate) + self.fixed_annotations
        ground_truth_tokens, candidate_tokens = self.load_and_tokenize_texts(ground_truth, candidate, annotations)
        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

    def calculate_overall_and_line_wer(self, ground_truth_lines, candidate_lines, decimal_places=3):
        # 同时计算整体和逐行 WER
        overall_wer = self.calculate_wer(' '.join(ground_truth_lines), ' '.join(candidate_lines), decimal_places)
        line_wer = self.calculate_line_wer(ground_truth_lines, candidate_lines, decimal_places)
        return overall_wer, line_wer


# 示例用法
if __name__ == "__main__":
    tokenizer_model_path = 'allenai/longformer-base-4096'
    fixed_annotations_path = 'anotation/fix_anotation.txt'
    
    # 创建 WER 计算器实例
    wer_calculator = WERCalculator(tokenizer_model_path, fixed_annotations_path)
    
    # 定义 ground truth 和 candidate 的文件路径
    ground_truth_lines = ['这是一段测试文本', '另一行文本']
    candidate_lines = ['这是测试文本', '另一行错的文本']
    
    # 计算整体 WER 和逐行 WER
    overall_wer, line_wer = wer_calculator.calculate_overall_and_line_wer(ground_truth_lines, candidate_lines)
    
    print(f"Overall WER: {overall_wer}")
    print(f"Line-by-line WER: {line_wer}")
