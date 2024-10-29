#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   wer_strategy.py
@Time    :   2024/09/20 18:05:01
@Author  :   Victor Z 
@Version :   1.0
@Contact :   snczww@gmail.com
@Desc    :   None
'''

# here put the import lib
import logging
from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches
import re  # Regular expressions for removing HTML tags

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# def mark_word_changes(s2_words, s1_words):
#     # s1_words = s1.split()
#     # s2_words = s2.split()
#     # s1_words = [word.replace("Ġ", " ") for word in s1_words]
#     # s2_words = [word.replace("Ġ", " ") for word in s2_words]
#     s1_words = [word.replace("Ġ", "").strip() for word in s1_words if word not in ['<s>', '</s>'] and word.strip()]
#     s2_words = [word.replace("Ġ", "").strip() for word in s2_words if word not in ['<s>', '</s>'] and word.strip()]
#     s1_words = list(filter(None, s1_words))
#     s2_words = list(filter(None, s2_words))
#     logging.info(f"s1_words is {s1_words}.")
#     logging.info(f"s2_words is {s2_words}.")
    
#     i, j = 0, 0
#     result = []
    
#     while i < len(s1_words) and j < len(s2_words):
#         if s1_words[i] == s2_words[j]:
#             # No change
#             result.append(s1_words[i])
#             i += 1
#             j += 1
#         elif s1_words[i] != s2_words[j]:
#             if i + 1 < len(s1_words) and s1_words[i + 1] == s2_words[j]:
#                 # Deletion in s1
#                 # result.append(f"-{s1_words[i]}-")
#                 result.append(f'<span style="color: red;">{s1_words[i]}</span>')

#                 i += 1
#             elif j + 1 < len(s2_words) and s1_words[i] == s2_words[j + 1]:
#                 # Insertion in s2
#                 # result.append(f"+{s2_words[j]}+")
#                 result.append(f'<span style="color: green;">{s2_words[j]}</span>')
#                 j += 1
#             else:
#                 # Replacement
#                 # result.append(f"*{s1_words[i]}*")
#                 result.append(f'<span style="color: blue;">{s1_words[i]}</span>')
#                 i += 1
#                 j += 1
    
#     # Handle remaining words in either s1 or s2
#     while i < len(s1_words):
#         # result.append(f"-{s1_words[i]}-")
#         result.append(f'<span style="color: red;">{s1_words[i]}</span>')
#         i += 1
    
#     while j < len(s2_words):
#         # result.append(f"+{s2_words[j]}+")
#         result.append(f'<span style="color: green;">{s2_words[j]}</span>')

#         j += 1
    
#     return " ".join(result)

def mark_word_changes_onlys2(s2, s1):
    """
    Highlight the operations (insert, delete, replace) needed to transform s2 into s1.
    - Replacement: <span style="color: green;"></span>
    - Insertion: <span style="color: blue;"></span>
    - Deletion: <span style="color: red;"></span>

    Args:
    s1 (list): Target sequence.
    s2 (list): Source sequence.

    Returns:
    str: A string representing the highlighted transformations.
    """
    import numpy as np
    s1 = [word.replace("Ġ", "").strip() for word in s1 if word not in ['<s>', '</s>'] and word.strip()]
    s2 = [word.replace("Ġ", "").strip() for word in s2 if word not in ['<s>', '</s>'] and word.strip()]
    s1 = list(filter(None, s1))
    s2 = list(filter(None, s2))

    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    # Fill the dp array
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,   # Deletion
                               dp[i][j - 1] + 1,   # Insertion
                               dp[i - 1][j - 1] + 1)  # Replacement

    # Backtrack to determine operations
    i, j = m, n
    result = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            result.append(s1[i - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Replacement
            # result.append(f"<span style=\"color: green;\">{s2[j - 1]} → {s1[i - 1]}</span>")
            result.append(f"<span style=\"color: green;\">{s1[i - 1]}</span>")
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Insertion
            result.append(f"<span style=\"color: blue;\">{s2[j - 1]}</span>")
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Deletion
            result.append(f"<span style=\"color: red;\">{s1[i - 1]}</span>")
            i -= 1

    # Reverse the result since we built it backwards
    result.reverse()

    return ' '.join(result)


def mark_word_changes_list(s2, s1):
    """
    Highlight the operations (insert, delete, replace) needed to transform s2 into s1.
    - Replacement: <span style="color: green;"></span>
    - Insertion: <span style="color: blue;"></span>
    - Deletion: <span style="color: red;"></span>

    Args:
    s1 (list): Target sequence.
    s2 (list): Source sequence.

    Returns:
    tuple: (marked_s1, s2modify)
    """
    import numpy as np
    # Helper function to escape < and > for HTML
    def escape_html(word):
        return word.replace("<", "&lt;").replace(">", "&gt;")
    
    # Helper function to remove HTML tags
    def remove_html_tags(text):
        return re.sub(r'<[^>]+>', '', text)

    # Helper function to escape < and > for HTML
    # def escape_html(word):
    #     return word.replace("<", "&lt;").replace(">", "&gt;")
    
    # Preprocess s1 and s2
    s1 = [escape_html(word.replace("Ġ", "").strip()) for word in s1 if word not in ['<s>', '</s>'] and word.strip()]
    s2 = [escape_html(word.replace("Ġ", "").strip()) for word in s2 if word not in ['<s>', '</s>'] and word.strip()]
    s1 = list(filter(None, s1))
    s2 = list(filter(None, s2))

    m, n = len(s1), len(s2)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    # Fill the dp array
    for i in range(1, m + 1):
        dp[i][0] = i
    for j in range(1, n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,   # Deletion
                               dp[i][j - 1] + 1,   # Insertion
                               dp[i - 1][j - 1] + 1)  # Replacement

    # Backtrack to determine operations
    i, j = m, n
    s2modify_list = []
    marked_s1_list = []

    while i > 0 or j > 0:
        if i > 0 and j > 0 and s1[i - 1] == s2[j - 1]:
            s2modify_list.append(s1[i - 1])
            marked_s1_list.append(s1[i - 1])
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            # Replacement
            s2modify_list.append(f"<span style=\"color: green;\">{s2[j - 1]}</span>")
            marked_s1_list.append(f"<span style=\"color: green;\">{s1[i - 1]}</span>")
            i -= 1
            j -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            # Insertion
            s2modify_list.append(f"<span style=\"color: blue;\">{s2[j - 1]}</span>")
            marked_s1_list.append('-' * len(remove_html_tags(s2[j - 1])))  # Fill with '-' of same length
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            # Deletion
            s2modify_list.append('-' * len(remove_html_tags(s1[i - 1])))  # Fill with '-' of same length
            marked_s1_list.append(f"<span style=\"color: red;\">{s1[i - 1]}</span>")
            i -= 1

    # Reverse the lists since we built them backwards
    s2modify_list.reverse()
    marked_s1_list.reverse()
    
    for i in range(len(marked_s1_list)):
        marked_length = len(remove_html_tags(marked_s1_list[i]))  # Remove HTML tags for length
        s2modify_length = len(remove_html_tags(s2modify_list[i]))  # Remove HTML tags for length
        # print(f'remove_html_tags(s2modify_list[i]):{remove_html_tags(s2modify_list[i])}')
        if marked_length > s2modify_length:
            s2modify_list[i] += '#' * (marked_length - s2modify_length)
        elif s2modify_length > marked_length:
            marked_s1_list[i] += '#' * (s2modify_length - marked_length)



     # Balance lengths of marked_s1_list and s2modify_list
    # for i in range(len(marked_s1_list)):
    #     marked_length = len(marked_s1_list[i])
    #     s2modify_length = len(s2modify_list[i])
    #     print(f's2modify_list:{s2modify_list}')
    #     print(f'marked_length:{marked_length},s2modify_length:{s2modify_length}')
        
    #     if marked_length > s2modify_length:
    #         s2modify_list[i] += '#' * (marked_length - s2modify_length)
    #     elif s2modify_length > marked_length:
    #         marked_s1_list[i] += '#' * (s2modify_length - marked_length)

    # marked_s1 = ' '.join(marked_s1_list)
    # s2modify = ' '.join(s2modify_list)
    return marked_s1_list,s2modify_list
    # return marked_s1, s2modify


def mark_word_changes(s2, s1):
    marked_s1_list,s2modify_list=mark_word_changes_list(s2, s1)
    marked_s1 = ' '.join(marked_s1_list)
    s2modify = ' '.join(s2modify_list)

    return marked_s1, s2modify




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
    # logging.info(f"Initializing tokenizer from {fixed_annotations}.")

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model_path,use_fast=False)
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
        # ground_truth_tokens = tokenizer(ground_truth_text, max_length=4096, truncation=True).tokens()
        # candidate_tokens = tokenizer(candidate_text, max_length=4096, truncation=True).tokens()


        # 对 ground truth 和 candidate 进行 tokenization
        ground_truth_ids = tokenizer.encode(ground_truth_text, max_length=4096, truncation=True)
        candidate_ids = tokenizer.encode(candidate_text, max_length=4096, truncation=True)

        # 解码成 tokens
        ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
        candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

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
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码成 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)
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
        ground_truth_ids = tokenizer.encode(ground_truth_lines, max_length=4096, truncation=True)
        candidate_ids = tokenizer.encode(candidate_lines, max_length=4096, truncation=True)

        # 解码成 tokens
        ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
        candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

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
            # annotations_gt = collect_all_matches(gt_line)
            # annotations_cand = collect_all_matches(cand_line)
            # tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations + annotations_gt + annotations_cand)
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码成 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

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
        ground_truth_ids = tokenizer.encode(ground_truth_text, max_length=4096, truncation=True)
        candidate_ids = tokenizer.encode(candidate_text, max_length=4096, truncation=True)

        # 解码成 tokens
        ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
        candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

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
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码成 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)
            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list
# Concrete strategy to calculate WER for annotations only, line by line
class WERAnnotationOnlyLineByLineStrategy_marked(WERStrategy):
    def calculate_wer(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, decimal_places):
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines, candidate_lines = ground_truth_lines[:min_length], candidate_lines[:min_length]

        filtered_ground_truth = filter_text_by_annotations(ground_truth_lines, fixed_annotations, tokenizer_model_path)
        filtered_candidate = filter_text_by_annotations(candidate_lines, fixed_annotations, tokenizer_model_path)

        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations)
        wer_list = []

        for gt_line, cand_line in zip(filtered_ground_truth, filtered_candidate):
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码成 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)
            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list

    # New method to mark changes
    def mark_changes_line(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, return_type='string'):
        """
        统一的标记函数，用于标记字符串或 token 列表中的更改。
        
        Args:
        - ground_truth_lines (list): Ground truth 的文本行列表。
        - candidate_lines (list): Candidate 的文本行列表。
        - tokenizer_model_path (str): 用于初始化标记的 tokenizer 模型路径。
        - fixed_annotations (list): 固定的注释列表。
        - return_type (str): 指定返回类型，'list' 表示返回 token 列表，'string' 表示返回标记后的字符串。

        Returns:
        - tuple: (marked_ground_truth, marked_candidate)，可以是 token 列表或标记后的字符串列表。
        """
        # 收集所有的注释
        annotations_gt = collect_all_matches(' '.join(ground_truth_lines))
        annotations_cand = collect_all_matches(' '.join(candidate_lines))

        # 初始化 tokenizer
        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations + annotations_gt + annotations_cand)

        # 存储标记后的结果
        marked_ground_truth = []
        marked_candidate = []

        # 遍历每一对 gt_line 和 cand_line
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines):
            # 收集行内注释
            annotations_gt = collect_all_matches(gt_line)
            annotations_cand = collect_all_matches(cand_line)
            
            # 编码为 ID
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码为 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

            # 调用 mark_word_changes_list 或 mark_word_changes 函数
            if return_type == 'list':
                # 返回 token 列表
                marked_gt, marked_cand = mark_word_changes_list(candidate_tokens, ground_truth_tokens)
            else:
                # 返回标记后的字符串
                marked_gt, marked_cand = mark_word_changes(candidate_tokens, ground_truth_tokens)

            # 添加到结果列表中
            marked_ground_truth.append(marked_gt)
            marked_candidate.append(marked_cand)

        return marked_ground_truth, marked_candidate


# Concrete strategy to calculate WER on annotations line by line
class WERAnnotationLineByLineStrategy_marked(WERStrategy):
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
            # annotations_gt = collect_all_matches(gt_line)
            # annotations_cand = collect_all_matches(cand_line)

            # ground_truth_tokens = tokenizer(gt_line, max_length=4096, truncation=True).tokens()
            # candidate_tokens = tokenizer(cand_line, max_length=4096, truncation=True).tokens()

                    # 对 ground truth 和 candidate 进行 tokenization
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码成 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)
            # print(f'ground_truth_tokens:{ground_truth_tokens}')
            # print(f'candidate_tokens:{candidate_tokens}')

            wer = word_list_error_rate(ground_truth_tokens, candidate_tokens)
            wer_list.append(round(wer, decimal_places))

        return wer_list



  
    def mark_changes_line(self, ground_truth_lines, candidate_lines, tokenizer_model_path, fixed_annotations, return_type='string'):
        """
        统一的标记函数，用于标记字符串或 token 列表中的更改。
        
        Args:
        - ground_truth_lines (list): Ground truth 的文本行列表。
        - candidate_lines (list): Candidate 的文本行列表。
        - tokenizer_model_path (str): 用于初始化标记的 tokenizer 模型路径。
        - fixed_annotations (list): 固定的注释列表。
        - return_type (str): 指定返回类型，'list' 表示返回 token 列表，'string' 表示返回标记后的字符串。

        Returns:
        - tuple: (marked_ground_truth, marked_candidate)，可以是 token 列表或标记后的字符串列表。
        """
        # 收集所有的注释
        annotations_gt = collect_all_matches(' '.join(ground_truth_lines))
        annotations_cand = collect_all_matches(' '.join(candidate_lines))

        # 初始化 tokenizer
        tokenizer = initialize_tokenizer(tokenizer_model_path, fixed_annotations + annotations_gt + annotations_cand)

        # 存储标记后的结果
        marked_ground_truth = []
        marked_candidate = []

        # 遍历每一对 gt_line 和 cand_line
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines):
            # 收集行内注释
            annotations_gt = collect_all_matches(gt_line)
            annotations_cand = collect_all_matches(cand_line)
            
            # 编码为 ID
            ground_truth_ids = tokenizer.encode(gt_line, max_length=4096, truncation=True)
            candidate_ids = tokenizer.encode(cand_line, max_length=4096, truncation=True)

            # 解码为 tokens
            ground_truth_tokens = tokenizer.convert_ids_to_tokens(ground_truth_ids)
            candidate_tokens = tokenizer.convert_ids_to_tokens(candidate_ids)

            # 调用 mark_word_changes_list 或 mark_word_changes 函数
            if return_type == 'list':
                # 返回 token 列表
                marked_gt, marked_cand = mark_word_changes_list(candidate_tokens, ground_truth_tokens)
            else:
                # 返回标记后的字符串
                marked_gt, marked_cand = mark_word_changes(candidate_tokens, ground_truth_tokens)

            # 添加到结果列表中
            marked_ground_truth.append(marked_gt)
            marked_candidate.append(marked_cand)

        return marked_ground_truth, marked_candidate
