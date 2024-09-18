# wer_context.py

from wer_strategy import WERStrategy

# Context class for managing the WER calculation strategy
class WERContext:
    def __init__(self, strategy: WERStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: WERStrategy):
        """
        Set a different WER calculation strategy
        """
        self.strategy = strategy

    def calculate(self, ground_truth, candidate, tokenizer_model_path, fixed_annotations, decimal_places=3):
        """
        Calculate WER using the current strategy
        """
        return self.strategy.calculate_wer(ground_truth, candidate, tokenizer_model_path, fixed_annotations, decimal_places)
