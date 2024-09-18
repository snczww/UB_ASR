# wer_calculator.py

from wer_strategy import WERStrategy
from utils.ASR_utils import read_file

class WERCalculator:
    def __init__(self, strategy: WERStrategy, fixed_annotations=None, decimal_places=2, tokenizer_model_path='allenai/longformer-base-4096'):
        """
        Initialize the WERCalculator with a strategy, default fixed_annotations, and decimal_places.
        """
        self.strategy = strategy
        # If no fixed_annotations are provided, load the default fix_anotation.txt file
        if fixed_annotations is None:
            self.fixed_annotations = read_file('utils/fix_anotation.txt')  # Default file
        else:
            self.fixed_annotations = fixed_annotations
        self.decimal_places = decimal_places
        self.tokenizer_model_path = tokenizer_model_path

    def set_strategy(self, strategy: WERStrategy):
        """
        Set a different WER calculation strategy
        """
        self.strategy = strategy

    def set_fixed_annotations(self, fixed_annotations):
        """
        Update the fixed annotations list
        """
        self.fixed_annotations = fixed_annotations

    def set_decimal_places(self, decimal_places):
        """
        Update the decimal places for WER calculation
        """
        self.decimal_places = decimal_places

    def set_tokenizer_model_path(self, tokenizer_model_path):
        """
        Update the tokenizer model path
        """
        self.tokenizer_model_path = tokenizer_model_path

    def calculate(self, ground_truth, candidate):
        """
        Calculate WER using the current strategy, fixed_annotations, decimal_places, and tokenizer_model_path.
        """
        return self.strategy.calculate_wer(ground_truth, candidate, self.tokenizer_model_path, self.fixed_annotations, self.decimal_places)
