# Saving all the provided Python code files into separate .py files

# 1. wer_strategy.py content
wer_strategy_code = '''
from abc import ABC, abstractmethod
from transformers import AutoTokenizer
from utils.wer_by_tokens import word_list_error_rate
from utils.find_all_anotations import collect_all_matches

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
'''

# 2. wer_calculator.py content
wer_calculator_code = '''
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
'''

# 3. main.py content
main_code = '''
from wer_calculator import WERCalculator
from wer_strategy import (
    WERWholeTextStrategy, 
    WERLineByLineStrategy, 
    WERAnnotationWholeTextStrategy, 
    WERAnnotationLineByLineStrategy
)
from utils.anotaion_utils import extract_lines_from_file

if __name__ == "__main__":
    # Define file paths
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'

    # Extract lines from files
    ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

    # Initialize the WERCalculator with default fixed_annotations from fix_anotation.txt and decimal_places = 2
    calculator = WERCalculator(WERWholeTextStrategy())  # Use default tokenizer_model_path, fixed_annotations, and decimal_places

    # User can override the fixed_annotations, decimal_places, or tokenizer_model_path if desired
    user_fixed_annotations = ['<custom_annotation1>', '<custom_annotation2>']  # User provided annotations
    calculator.set_fixed_annotations(user_fixed_annotations)  # Optional: set custom fixed_annotations
    # calculator.set_decimal_places(3)  # Optional: change decimal_places to 3
    # calculator.set_tokenizer_model_path('another/tokenizer/path')  # Optional: change tokenizer_model_path

    # Strategy 1: Calculate WER treating lists as whole texts
    overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall WER (Whole Text): {overall_wer}")

    # Strategy 2: Calculate WER line by line
    calculator.set_strategy(WERLineByLineStrategy())
    line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Line-by-Line WER: {line_wer_list}")

    # Strategy 3: Calculate WER on annotations (whole text)
    calculator.set_strategy(WERAnnotationWholeTextStrategy())
    overall_annotation_wer = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Overall Annotation WER (Whole Text): {overall_annotation_wer}")

    # Strategy 4: Calculate WER on annotations (line by line)
    calculator.set_strategy(WERAnnotationLineByLineStrategy())
    annotation_line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)
    print(f"Line-by-Line Annotation WER: {annotation_line_wer_list}")
'''

# Writing to files
with open("/mnt/data/wer_strategy.py", "w") as f:
    f.write(wer_strategy_code)

with open("/mnt/data/wer_calculator.py", "w") as f:
    f.write(wer_calculator_code)

with open("/mnt/data/main.py", "w") as f:
    f.write(main_code)

"/mnt/data/wer_strategy.py, /mnt/data/wer_calculator.py, /mnt/data/main.py files are created."
