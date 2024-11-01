#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wer_calculator.py
@Time    :   2024/09/20 17:38:56
@Author  :   Victor Z 
@Version :   1.0
@Contact :   snczww@gmail.com
@Desc    :   Word Error Rate (WER) calculator class implementation
'''

# Import necessary libraries and modules
from wer_strategy import WERStrategy
from utils.ASR_utils import read_file

class WERCalculator:
    def __init__(self, strategy: WERStrategy, fixed_annotations=None, decimal_places=2, tokenizer_model_path='allenai/longformer-base-4096'):
        """
        Initializes the WERCalculator with a specified WER calculation strategy, fixed annotations, 
        decimal precision for rounding results, and a tokenizer model path.

        Args:
        - strategy (WERStrategy): A strategy instance that defines the specific WER calculation method.
        - fixed_annotations (list or None): A list of pre-defined annotations for accuracy adjustments in WER calculation. 
          If None, the default 'fix_anotation.txt' file is loaded.
        - decimal_places (int): Number of decimal places to round the WER result to (default is 2).
        - tokenizer_model_path (str): The file path to the tokenizer model used for tokenizing text in WER calculation.
        """
        self.strategy = strategy
        # Load default fixed annotations if none are provided
        if fixed_annotations is None:
            self.fixed_annotations = read_file('utils/fix_anotation.txt')  # Default annotation file
        else:
            self.fixed_annotations = fixed_annotations
        self.decimal_places = decimal_places
        self.tokenizer_model_path = tokenizer_model_path

    def set_strategy(self, strategy: WERStrategy):
        """
        Updates the WER calculation strategy.

        Args:
        - strategy (WERStrategy): The new strategy to use for WER calculation.
        """
        self.strategy = strategy

    def set_fixed_annotations(self, fixed_annotations):
        """
        Updates the list of fixed annotations used in WER calculation.

        Args:
        - fixed_annotations (list): New list of annotations to be fixed during calculation.
        """
        self.fixed_annotations = fixed_annotations

    def set_decimal_places(self, decimal_places):
        """
        Updates the decimal precision for WER result rounding.

        Args:
        - decimal_places (int): Number of decimal places for rounding the WER result.
        """
        self.decimal_places = decimal_places

    def set_tokenizer_model_path(self, tokenizer_model_path):
        """
        Updates the tokenizer model path for tokenizing text in WER calculation.

        Args:
        - tokenizer_model_path (str): File path of the tokenizer model.
        """
        self.tokenizer_model_path = tokenizer_model_path

    def calculate(self, ground_truth, candidate):
        """
        Calculates the Word Error Rate (WER) between ground truth and candidate texts.

        Args:
        - ground_truth (str): The ground truth text.
        - candidate (str): The candidate text to compare against the ground truth.

        Returns:
        - float: The calculated WER value, rounded to the specified decimal precision.
        """
        return self.strategy.calculate_wer(ground_truth, candidate, self.tokenizer_model_path, self.fixed_annotations, self.decimal_places)

    def mark_changes(self, ground_truth, candidate, return_type):
        """
        Calculates WER and marks the changes between ground truth and candidate texts.

        Args:
        - ground_truth (list): A list of lines containing the ground truth text.
        - candidate (list): A list of lines containing the candidate text.
        - return_type (str): Specifies the return format, either 'list' for tokens or 'string' for marked text.

        Returns:
        - tuple: A tuple (marked_ground_truth, marked_candidate) where each element is either a list of tokens 
          or a marked-up string, depending on the specified return_type.
        """
        return self.strategy.mark_changes_line(ground_truth, candidate, self.tokenizer_model_path, self.fixed_annotations, return_type)
