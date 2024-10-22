from flask import Flask, request, render_template, send_file
import pandas as pd
import os
from werkzeug.utils import secure_filename
from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationOnlyLineByLineStrategy, 
    WERAnnotationLineByLineStrategy_marked
)
from utils.anotaion_utils import extract_lines_from_file
import re

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def remove_nak_to_end(line):
    """Remove content starting with 'NAK' to the end of the line."""
    return re.sub(r'\x15\d+_\d+\x15', '', line)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save uploaded files
        ground_truth_file = request.files['ground_truth_file']
        candidate_file = request.files['candidate_file']

        ground_truth_filename = secure_filename(ground_truth_file.filename)
        candidate_filename = secure_filename(candidate_file.filename)

        ground_truth_path = os.path.join(app.config['UPLOAD_FOLDER'], ground_truth_filename)
        candidate_path = os.path.join(app.config['UPLOAD_FOLDER'], candidate_filename)

        ground_truth_file.save(ground_truth_path)
        candidate_file.save(candidate_path)

        # Extract lines from files
        ground_truth_lines = extract_lines_from_file(ground_truth_path, '*CHI:')
        candidate_lines = extract_lines_from_file(candidate_path, '*PAR0:')

        # Remove content after 'NAK' from each line in both ground truth and candidate lines
        ground_truth_lines = [remove_nak_to_end(line) for line in ground_truth_lines]
        candidate_lines = [remove_nak_to_end(line) for line in candidate_lines]

        # Ensure the lengths of ground truth and candidate lines match
        min_length = min(len(ground_truth_lines), len(candidate_lines))
        ground_truth_lines = ground_truth_lines[:min_length]
        candidate_lines = candidate_lines[:min_length]

        # Mark word changes
        calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
        compared_candidate_lines = calculator.mark_changes(ground_truth_lines, candidate_lines)

        # Strategy 1: Calculate WER treating lists as whole texts
        calculator = WERCalculator(WERAnnotationOnlyWholeTextStrategy())
        overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)

        # Strategy 2: Calculate WER line by line
        calculator.set_strategy(WERAnnotationOnlyLineByLineStrategy())
        line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)

        # Create a DataFrame to store the results with compared strings
        df = pd.DataFrame({
            'Ground Truth Line': ground_truth_lines,
            'Candidate Line (Compared)': compared_candidate_lines,
            'Line WER': line_wer_list
        })

        # Save the DataFrame to a CSV file
        output_csv_path = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')
        df.to_csv(output_csv_path, index=False)

        # Return the CSV file for download
        return send_file(output_csv_path, as_attachment=True, download_name='wer_output.csv')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
