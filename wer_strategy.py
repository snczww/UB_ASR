# wer_strategy.py

from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from utils.wer_by_tokens import word_list_error_rate
from anotation.find_all_anotations import collect_all_matches

# Strategy interface for WER calculation
class WERStrategy(ABC):
    @abstractmethod
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        pass

# Concrete strategy to calculate WER treating lists as a whole text
class WERWholeTextStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Combine lines into a single string
        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        # Tokenize and calculate WER
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)
        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

# Concrete strategy to calculate WER line by line
class WERLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Ensure lists have the same length
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)

        # Tokenize and calculate WER for each line
        wer_list = []
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines):
            ground_truth_tokens = tokenizer(gt_line, max_length=4096, truncation=True).tokens()
            candidate_tokens = tokenizer(cand_line, max_length=4096, truncation=True).tokens()
            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list

# Concrete strategy to calculate WER on annotations treating lists as whole text
class WERAnnotationWholeTextStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Collect annotation matches
        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        annotations_gt = collect_all_matches(ground_truth_text)
        annotations_cand = collect_all_matches(candidate_text)

        # Tokenize and calculate WER for annotations
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)

        ground_truth_tokens = tokenizer(' '.join(annotations_gt), max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(' '.join(annotations_cand), max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

# Concrete strategy to calculate WER on annotations line by line
class WERAnnotationLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Ensure lists have the same length
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)

        wer_list = []
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines):
            annotations_gt = collect_all_matches(gt_line)
            annotations_cand = collect_all_matches(cand_line)

            ground_truth_tokens = tokenizer(' '.join(annotations_gt), max_length=4096, truncation=True).tokens()
            candidate_tokens = tokenizer(' '.join(annotations_cand), max_length=4096, truncation=True).tokens()

            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list
