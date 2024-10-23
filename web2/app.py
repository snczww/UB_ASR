from flask import Flask, request, render_template_string, send_file
import pandas as pd
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from werkzeug.utils import secure_filename
from wer_calculator import WERCalculator
from wer_strategy import (
    WERAnnotationOnlyWholeTextStrategy, 
    WERAnnotationOnlyLineByLineStrategy, 
    WERAnnotationLineByLineStrategy_marked
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
    """Remove content starting with 'NAK' to the end of the line."""
    return re.sub(r'\x15\d+_\d+\x15', '', line)

def highlight_candidate_line(text):
    """
    Process Candidate Line to replace marked words with colored HTML:
    *word* -> red, +word+ -> blue, -word- -> orange
    """
    text = re.sub(r'\*(\w+)\*', r'<span style="color: red;">\1</span>', text)
    text = re.sub(r'\+(\w+)\+', r'<span style="color: blue;">\1</span>', text)
    text = re.sub(r'\-(\w+)\-', r'<span style="color: orange;">\1</span>', text)
    return text

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
        compared_candidate_lines = [highlight_candidate_line(line) for line in compared_candidate_lines]

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

        # Display the table with pagination
        return display_csv(df)
    else:
        return '''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Upload Files</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <h1>Upload Ground Truth and Candidate Files</h1>
                <form method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="ground_truth_file" class="form-label">Ground Truth File</label>
                        <input type="file" class="form-control" name="ground_truth_file" required>
                    </div>
                    <div class="mb-3">
                        <label for="candidate_file" class="form-label">Candidate File</label>
                        <input type="file" class="form-control" name="candidate_file" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Upload and Calculate WER</button>
                </form>
            </div>
        </body>
        </html>
        '''

@app.route('/display')
def display_csv(data=None):
    if data is None:
        csv_file = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')
        data = pd.read_csv(csv_file)

    # Get page number and rows per page
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Calculate pagination
    start_row = (page - 1) * per_page
    end_row = start_row + per_page
    page_data = data[start_row:end_row]

    # Calculate total pages
    total_rows = len(data)
    total_pages = (total_rows // per_page) + (1 if total_rows % per_page else 0)

    # Convert the data to HTML table
    table_html = page_data.to_html(classes='table table-striped', index=False, table_id='csvTable')

    # Render the HTML template
    html_template = f'''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Table</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1>CSV Data</h1>
            <div class="mb-4">{table_html}</div>

            <!-- Pagination Controls -->
            <nav aria-label="Page navigation">
                <ul class="pagination">
                    {"".join([f'<li class="page-item{" active" if p == page else ""}"><a class="page-link" href="/display?page={p}&per_page={per_page}">{p}</a></li>' for p in range(1, total_pages + 1)])}
                </ul>
            </nav>
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
