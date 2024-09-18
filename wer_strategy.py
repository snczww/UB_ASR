# wer_strategy.py

from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches

# Helper function to filter tokens based on annotations and fixed annotations
def filter_text_by_annotations(text_lines, fixed_annotations, tokenizer_model_path='allenai/longformer-base-4096'):
    """
    Filter each line in the provided list to retain only tokens that match annotations or fixed annotations.

    Parameters:
    text_lines (list): List of text lines to filter.
    fixed_annotations (list): List of fixed annotations.
    tokenizer_model_path (str): Path to the tokenizer model (default is 'allenai/longformer-base-4096').

    Returns:
    list: List of filtered text lines, containing only matched annotations and fixed annotations.
    """
    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)

    filtered_lines = []
    for line in text_lines:
        # Find all matches from the line using collect_all_matches
        annotation_matches = collect_all_matches(line)
        # Combine matches with fixed annotations
        valid_tokens = annotation_matches + fixed_annotations

        # Tokenize the line
        tokens = tokenizer.tokenize(line)
        # Filter the tokens to keep only the valid tokens
        filtered_tokens = [token for token in tokens if token in valid_tokens]
        # Join the filtered tokens back into a string, or replace with a single space if empty
        filtered_line = ' '.join(filtered_tokens) if filtered_tokens else ' '
        filtered_lines.append(filtered_line)

    return filtered_lines


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
        tokenizer.add_tokens(fixed_annotations+annotations_gt+annotations_cand, special_tokens=True)

        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

# Concrete strategy to calculate WER on annotations line by line
class WERAnnotationLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Ensure lists have the same length
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        annotations_gt = collect_all_matches(ground_truth_text)
        annotations_cand = collect_all_matches(candidate_text)

        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations+annotations_gt+annotations_cand, special_tokens=True)

        wer_list = []
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines):
            annotations_gt = collect_all_matches(gt_line)
            annotations_cand = collect_all_matches(cand_line)

            ground_truth_tokens = tokenizer(gt_line, max_length=4096, truncation=True).tokens()
            candidate_tokens = tokenizer(cand_line, max_length=4096, truncation=True).tokens()

            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list
# Concrete strategy to calculate WER for annotations only, treating lists as whole text
class WERAnnotationOnlyWholeTextStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Filter both ground truth and candidate lines by annotations and fixed_annotations
        filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations,tokenizer_model_path)
        filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations,tokenizer_model_path)

        # Combine the filtered lines into full texts
        ground_truth_text = ' '.join(filtered_ground_truth)
        candidate_text = ' '.join(filtered_candidate)

        # Tokenize and calculate WER for filtered text
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)
        
        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)


# Concrete strategy to calculate WER for annotations only, line by line
class WERAnnotationOnlyLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        # Ensure the lists have the same length
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        # Filter both ground truth and candidate lines by annotations and fixed_annotations
        filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations,tokenizer_model_path)
        filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations,tokenizer_model_path)

        # Tokenize and calculate WER for each line
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        tokenizer.add_tokens(fixed_annotations, special_tokens=True)

        wer_list = []
        for gt_line, cand_line in zip(filtered_ground_truth, filtered_candidate):
            ground_truth_tokens = tokenizer(gt_line, max_length=4096, truncation=True).tokens()
            candidate_tokens = tokenizer(cand_line, max_length=4096, truncation=True).tokens()

            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list