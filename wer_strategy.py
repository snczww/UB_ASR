from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches


# Helper function to initialize tokenizer and add fixed annotations
def initialize_tokenizer(tokenizer_model_path, fixed_annotations):
    """
    Initialize the tokenizer and add fixed annotations.
    
    Parameters:
    tokenizer_model_path (str): Path to the tokenizer model.
    fixed_annotations (list): List of fixed annotations to be added as special tokens.

    Returns:
    tokenizer: The initialized tokenizer with added tokens.
    """
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
    tokenizer.add_tokens(fixed_annotations, special_tokens=True)
    return tokenizer


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

    filtered_lines = []

    all_text = ' '.join(text_lines)

    all_text_gt = collect_all_matches(all_text)

    valid_tokens = all_text_gt + fixed_annotations
    tokenizer = initialize_tokenizer(tokenizer_model_path, valid_tokens )

    for line in text_lines:

        tokens = tokenizer.tokenize(line)
        filtered_tokens = [token for token in tokens if token in valid_tokens]
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
        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations)
        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)


# Concrete strategy to calculate WER line by line
class WERLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations)
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
        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        annotations_gt = collect_all_matches(ground_truth_text)
        annotations_cand = collect_all_matches(candidate_text)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations + annotations_gt + annotations_cand)
        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)


# Concrete strategy to calculate WER on annotations line by line
class WERAnnotationLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]
        ground_truth_text = ' '.join(ground_truth_lines)
        candidate_text = ' '.join(candidate_lines)

        annotations_gt = collect_all_matches(ground_truth_text)
        annotations_cand = collect_all_matches(candidate_text)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations + annotations_gt + annotations_cand)
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
        filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations, tokenizer_model_path)
        filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations, tokenizer_model_path)

        ground_truth_text = ' '.join(filtered_ground_truth)
        candidate_text = ' '.join(filtered_candidate)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations)
        ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()

        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)


# Concrete strategy to calculate WER for annotations only, line by line
class WERAnnotationOnlyLineByLineStrategy(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

        filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations, tokenizer_model_path)
        filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations, tokenizer_model_path)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations)
        wer_list = []

        for gt_line, cand_line in zip(filtered_ground_truth, filtered_candidate):
            ground_truth_tokens = tokenizer(gt_line, max_length=4096, truncation=True).tokens()
            candidate_tokens = tokenizer(cand_line, max_length=4096, truncation=True).tokens()
            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list
