import sys
import os

# 获取上一层目录的路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将上一层目录添加到sys.path
sys.path.insert(0, parent_dir)

from flask import Flask, render_template
from wer_calculator import WERCalculator
from wer_strategy import WERAnnotationLineByLineStrategy
from utils.anotaion_utils import extract_lines_from_file
from difflib import ndiff

app = Flask(__name__)

# 用来标记candidate中与groundtruth不同的部分
def mark_differences(gt_line, candidate_line):
    gt_tokens = gt_line.split()
    candidate_tokens = candidate_line.split()
    diff = list(ndiff(gt_tokens, candidate_tokens))

    marked_candidate = []
    for token in diff:
        if token.startswith('- '):  # 表示在groundtruth中有，在candidate中没有（缺失）
            marked_candidate.append(f'<span style="color:red; text-decoration:line-through;">{token[2:]}</span>')
        elif token.startswith('+ '):  # 表示在candidate中有，在groundtruth中没有（多余的）
            marked_candidate.append(f'<span style="color:green;">{token[2:]}</span>')
        elif token.startswith('? '):  # 这个符号行只用于说明修改内容，通常不用在此场景中标记
            continue
        else:  # 相同的token
            marked_candidate.append(token[2:])

    return ' '.join(marked_candidate)

@app.route('/')
def index():
    # 定义文件路径
    ground_truth_path = 'anotation/cha_files/758_2.cha'
    candidate_path = 'anotation/cha_files/758_AI.cha'

    # 提取文件中的行
    ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
    candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

    # 初始化WER计算器
    calculator = WERCalculator(WERAnnotationLineByLineStrategy())
    
    # 计算逐行WER
    line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)

    # 对candidate_line进行标记
    marked_lines = [
        mark_differences(gt_line, cand_line) 
        for gt_line, cand_line in zip(ground_truth_lines, candidate_lines)
    ]

    return render_template('index.html', 
                           overall_wer=sum(line_wer_list) / len(line_wer_list), 
                           ground_truth_lines=ground_truth_lines, 
                           marked_candidate_lines=marked_lines,
                           line_wer_list=line_wer_list)

if __name__ == "__main__":
    app.run(debug=True)
