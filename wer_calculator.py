from transformers import AutoTokenizer
from utils.ASR_utils import read_file
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches
import concurrent.futures
import os


class WERCalculator:
    """
    A class to calculate Word Error Rate (WER) for automatic speech recognition (ASR) models.

    Attributes:
    tokenizer_model_path: str
        Path to the pre-trained tokenizer model.
    tokenizer: AutoTokenizer
        The tokenizer object initialized with the provided model.
    fixed_annotations: list
        A list of fixed annotations that are loaded from an external file.
    """

    def __init__(self, tokenizer_model_path, fixed_annotations_path=None):
        """
        Initializes the WERCalculator with a tokenizer and optional fixed annotations.

        Parameters:
        tokenizer_model_path (str): Path to the tokenizer model (e.g., 'allenai/longformer-base-4096').
        fixed_annotations_path (str, optional): Path to the file containing fixed annotations.
        """
        self.tokenizer_model_path = tokenizer_model_path
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path)
        self.fixed_annotations = self._load_fixed_annotations(fixed_annotations_path)

    def _load_fixed_annotations(self, path):
        """
        Loads fixed annotations from a file.

        Parameters:
        path (str): Path to the file containing fixed annotations.

        Returns:
        list: A list of fixed annotations if a path is provided, otherwise an empty list.
        """
        if path:
            return read_file(path)
        return []

    def load_and_tokenize_texts(self, ground_truth, candidate, annotations=None):
        """
        Tokenizes the ground truth and candidate texts using the provided tokenizer and annotations.

        Parameters:
        ground_truth (str): The ground truth text.
        candidate (str): The candidate text.
        annotations (list, optional): A list of additional annotations to add to the tokenizer.

        Returns:
        tuple: Tokenized ground truth and candidate texts.
        """
        if annotations:
            self.tokenizer.add_tokens(annotations, special_tokens=True)
        ground_truth_tokens = self.tokenizer(ground_truth, max_length=4096, truncation=True).tokens()
        candidate_tokens = self.tokenizer(candidate, max_length=4096, truncation=True).tokens()
        return ground_truth_tokens, candidate_tokens

    def calculate_wer(self, ground_truth_text, candidate_text, decimal_places=3):
        """
        Calculates the Word Error Rate (WER) between two texts.

        Parameters:
        ground_truth_text (str): The ground truth text.
        candidate_text (str): The candidate text.
        decimal_places (int, optional): Number of decimal places to round the WER result (default is 3).

        Returns:
        float: The WER value rounded to the specified decimal places.
        """
        ground_truth_tokens, candidate_tokens = self.load_and_tokenize_texts(ground_truth_text, candidate_text, self.fixed_annotations)
        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

    def calculate_line_wer(self, ground_truth_lines, candidate_lines, decimal_places=3):
        """
        Calculates the WER for each line between two sets of text lines.

        Parameters:
        ground_truth_lines (list): List of ground truth lines.
        candidate_lines (list): List of candidate lines.
        decimal_places (int, optional): Number of decimal places to round the WER result (default is 3).

        Returns:
        list: List of WER values for each line, rounded to the specified decimal places.
        """
        # Ensure the two lists have the same number of lines
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

        wer_list = []
        for gt, cand in zip(ground_truth_lines, candidate_lines):
            wer = self.calculate_wer(gt, cand, decimal_places)
            wer_list.append(wer)

        return wer_list

    def calculate_annotation_wer(self, ground_truth, candidate, decimal_places=3):
        """
        Calculates the WER between two texts based on annotations.

        Parameters:
        ground_truth (str): The ground truth text.
        candidate (str): The candidate text.
        decimal_places (int, optional): Number of decimal places to round the WER result (default is 3).

        Returns:
        float: The WER value rounded to the specified decimal places, based on annotations.
        """
        # Collect annotations from both the ground truth and candidate texts
        annotations = collect_all_matches(ground_truth) + collect_all_matches(candidate) + self.fixed_annotations
        ground_truth_tokens, candidate_tokens = self.load_and_tokenize_texts(ground_truth, candidate, annotations)
        wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
        return round(wer, decimal_places)

    def calculate_overall_and_line_wer(self, ground_truth_lines, candidate_lines, decimal_places=3):
        """
        Calculates both the overall WER and line-by-line WER between two sets of text lines.

        Parameters:
        ground_truth_lines (list): List of ground truth lines.
        candidate_lines (list): List of candidate lines.
        decimal_places (int, optional): Number of decimal places to round the WER result (default is 3).

        Returns:
        tuple: Overall WER and a list of line-by-line WERs.
        """
        # Calculate the overall WER
        overall_wer = self.calculate_wer(' '.join(ground_truth_lines), ' '.join(candidate_lines), decimal_places)
        # Calculate WER for each line
        line_wer = self.calculate_line_wer(ground_truth_lines, candidate_lines, decimal_places)
        return overall_wer, line_wer


# Example usage
if __name__ == "__main__":
    tokenizer_model_path = 'allenai/longformer-base-4096'
    fixed_annotations_path = '/mnt/data/fix_anotation.txt'  # Path to your fixed annotation file

    # Create a WERCalculator instance
    wer_calculator = WERCalculator(tokenizer_model_path, fixed_annotations_path)

    # Define ground truth and candidate text lines
    ground_truth_lines = [
        "a rabbit and his dog are making a sandcastle.",
        "and now the rabbit gots a shovel and his bucket."
    ]
    candidate_lines = [
        "rabbit and dog are making a sandcastle.",
        "now rabbit got shovel and his bucket."
    ]

    # Calculate overall WER and line-by-line WER
    overall_wer, line_wer = wer_calculator.calculate_overall_and_line_wer(ground_truth_lines, candidate_lines)

    print(f"Overall WER: {overall_wer}")
    print(f"Line-by-line WER: {line_wer}")
