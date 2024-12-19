from flask import Flask, request, render_template, redirect, url_for,session
import pandas as pd
import os
import re
import sys

# Add parent directory to the module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.utils import secure_filename
from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationLineByLineStrategy_marked,
    WERAnnotationWholeTextStrategy
)
from utils.anotaion_utils import extract_lines_from_file

app = Flask(__name__)

# Set upload and output folders
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def remove_nak_to_end(line):
    if not isinstance(line, str):
        line = str(line)
    return re.sub(r'\x15\d+_\d+\x15', '', line)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ground_truth_file = request.files.get('ground_truth_file')
        candidate_file = request.files.get('candidate_file')

        if not ground_truth_file or not candidate_file:
            return render_template('index.html', error="Both files are required!")

        ground_truth_filename = secure_filename(ground_truth_file.filename)
        candidate_filename = secure_filename(candidate_file.filename)

        ground_truth_path = os.path.join(app.config['UPLOAD_FOLDER'], ground_truth_filename)
        candidate_path = os.path.join(app.config['UPLOAD_FOLDER'], candidate_filename)

        ground_truth_file.save(ground_truth_path)
        candidate_file.save(candidate_path)

        ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
        candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

        ground_truth_lines = [remove_nak_to_end(line) for line in ground_truth_lines]
        candidate_lines = [remove_nak_to_end(line) for line in candidate_lines]

        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        # Calculate WER with the marked strategy and return lists of lists
        calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
        compared_ground_truth_lines, compared_candidate_lines = calculator.mark_changes(ground_truth_lines, candidate_lines, 'list')

        # Calculate WER again for line-by-line results
        calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
        line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)

        # Calculate WER again for overall results
        calculator = WERCalculator(WERAnnotationWholeTextStrategy())
        overall_annotation_wer = calculator.calculate(ground_truth_lines, candidate_lines)



        df = pd.DataFrame({
            'Ground Truth Line': compared_ground_truth_lines,
            # 'Ground Truth Line': " ".join(compared_ground_truth_lines),
            'Candidate Line (Compared)': compared_candidate_lines,
            # 'Candidate Line (Compared)': " ".join(compared_candidate_lines),
            'Line WER': line_wer_list
        })

        # 统计 "substitution" (绿色) 的个数
        green_count = sum(
            str(line).count('<span style="color: green;">') 
            for line in compared_ground_truth_lines + compared_candidate_lines
        )
        blue_count = sum(
            str(line).count('<span style="color: blue;">') 
            for line in compared_ground_truth_lines + compared_candidate_lines
        )
        red_count = sum(
            str(line).count('<span style="color: red;">') 
            for line in compared_ground_truth_lines + compared_candidate_lines
        )
        print(compared_ground_truth_lines[0])

        output_csv_path = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')
        df.to_csv(output_csv_path, index=False)
        #deliver WER score 
        # session['overall_annotation_wer'] = overall_annotation_wer


        return redirect(url_for('display', page=1, 
                                per_page=10,overall_wer=overall_annotation_wer,
                                green_count=int(green_count/2),red_count=red_count,
                                blue_count=blue_count))
    else:
        return render_template('index.html')

@app.route('/display')
def display():
    csv_file = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')

    if not os.path.exists(csv_file):
        return redirect(url_for('index'))

    df = pd.read_csv(csv_file, converters={'Ground Truth Line': eval, 'Candidate Line (Compared)': eval})

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    overall_wer = request.args.get('overall_wer', 'N/A')
    green_count = request.args.get('green_count', 'N/A',)
    red_count = request.args.get('red_count', 'N/A')
    blue_count = request.args.get('blue_count', 'N/A')

    total_rows = len(df)
    total_pages = (total_rows // per_page) + (1 if total_rows % per_page else 0)

    start_row = (page - 1) * per_page
    end_row = start_row + per_page
    page_data = df.iloc[start_row:end_row]

    return render_template(
        'display.html',
        table=page_data,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        overall_annotation_wer=overall_wer,
        total_substitution=green_count,
        total_omission=red_count,
        total_addition=blue_count

    )


# def display():
#     csv_file = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')

#     if not os.path.exists(csv_file):
#         return redirect(url_for('index'))

#     df = pd.read_csv(csv_file, converters={'Ground Truth Line': eval, 'Candidate Line (Compared)': eval})
    
#     # df['Ground Truth Line'] = df['Ground Truth Line'].apply(lambda x: ' '.join(x))
#     # df['Candidate Line (Compared)'] = df['Candidate Line (Compared)'].apply(lambda x: ' '.join(x))

#     page = request.args.get('page', 1, type=int)
#     per_page = request.args.get('per_page', 10, type=int)

#     total_rows = len(df)
#     total_pages = (total_rows // per_page) + (1 if total_rows % per_page else 0)

#     start_row = (page - 1) * per_page
#     end_row = start_row + per_page
#     page_data = df.iloc[start_row:end_row]

#     return render_template(
#         'display.html',
#         table=page_data,
#         page=page,
#         per_page=per_page,
#         total_pages=total_pages
#     )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5860)
