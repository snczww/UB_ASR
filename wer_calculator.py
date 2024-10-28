#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wer_calculator.py
@Time    :   2024/09/20 17:38:56
@Author  :   Victor Z 
@Version :   1.0
@Contact :   snczww@gmail.com
@Desc    :   None
'''

# here put the import lib

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
def mark_changes(self, ground_truth, candidate, return_type='string'):
    """
    计算 WER 并标记更改，使用当前的 strategy、fixed_annotations、decimal_places 和 tokenizer_model_path。

    Args:
    - ground_truth (list): Ground truth 文本行列表。
    - candidate (list): Candidate 文本行列表。
    - return_type (str): 指定返回类型，'list' 表示返回 token 列表，'string' 表示返回标记后的字符串。

    Returns:
    - tuple: (marked_ground_truth, marked_candidate)，可以是 token 列表或标记后的字符串列表。
    """
    if return_type == 'list':
        # 调用 strategy 的 mark_changes_list 方法
        return self.strategy.mark_changes_list(ground_truth, candidate, self.tokenizer_model_path, self.fixed_annotations)
    else:
        # 调用 strategy 的 mark_changes_line 方法
        return self.strategy.mark_changes_line(ground_truth, candidate, self.tokenizer_model_path, self.fixed_annotations)
