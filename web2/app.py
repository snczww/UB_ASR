from flask import Flask, request, render_template_string, send_file
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
    if not isinstance(line, str):
        line = str(line)
    return re.sub(r'\x15\d+_\d+\x15', '', line)

def highlight_candidate_line(text):
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'\*(\w+)\*', r'<span style="color: red;">\1</span>', text)
    text = re.sub(r'\+(\w+)\+', r'<span style="color: blue;">\1</span>', text)
    text = re.sub(r'\-(\w+)\-', r'<span style="color: orange;">\1</span>', text)
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ground_truth_file = request.files['ground_truth_file']
        candidate_file = request.files['candidate_file']

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

        calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
        compared_ground_truth_lines, compared_candidate_lines = calculator.mark_changes(ground_truth_lines, candidate_lines)

        compared_candidate_lines = [' '.join(line) if isinstance(line, list) else line for line in compared_candidate_lines]

        calculator = WERCalculator(WERAnnotationOnlyWholeTextStrategy())
        overall_wer = calculator.calculate(ground_truth_lines, candidate_lines)

        # calculator.set_strategy(WERAnnotationOnlyLineByLineStrategy())
        calculator = WERCalculator(WERAnnotationLineByLineStrategy_marked())
        line_wer_list = calculator.calculate(ground_truth_lines, candidate_lines)

        min_length = min(len(compared_ground_truth_lines), len(compared_candidate_lines), len(line_wer_list))
        compared_ground_truth_lines = compared_ground_truth_lines[:min_length]
        compared_candidate_lines = compared_candidate_lines[:min_length]
        line_wer_list = line_wer_list[:min_length]

        df = pd.DataFrame({
            'Ground Truth Line': compared_ground_truth_lines,
            'Candidate Line (Compared)': compared_candidate_lines,
            'Line WER': line_wer_list
        })

        output_csv_path = os.path.join(app.config['OUTPUT_FOLDER'], 'wer_output.csv')
        df.to_csv(output_csv_path, index=False)

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

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    start_row = (page - 1) * per_page
    end_row = start_row + per_page
    page_data = data[start_row:end_row]

    total_rows = len(data)
    total_pages = (total_rows // per_page) + (1 if total_rows % per_page else 0)

    table_html = page_data.to_html(classes='table table-striped', index=False, table_id='csvTable', escape=False)

    html_template = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CSV Table</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            .comparison-table {
                display: grid;
                grid-template-columns: auto 1fr;
                grid-gap: 10px;
                margin-bottom: 20px;
            }
            .comparison-cell {
                padding: 5px;
            }
            .label {
                font-size: 14px;
                text-align: left;
            }
            .content {
                font-family: monospace;
                font-size: 22px;
                white-space: pre-wrap;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5">CSV Data</h1>
            <div class="legend mb-3">
                <h5>Legend:</h5>
                <div style="display: flex; gap: 20px;">
                    <div><span style="color: red;">omittion</span></div>
                    <div><span style="color: blue;">addtion</span></div>
                    <div><span style="color: green;">subtitution</span></div>
                </div>
            </div>

            <div id="comparison-display" class="mb-4">
                <h3>Comparison:</h3>
                <div class="comparison-table">
                    <div class="comparison-cell label">Ground Truth:</div>
                    <div class="comparison-cell content"><pre id="ground-truth">None</pre></div>
                    <div class="comparison-cell label">Candidate Line (Compared):</div>
                    <div class="comparison-cell content"><pre id="candidate-line">None</pre></div>
                </div>
            </div>

            <div>{{ table|safe }}</div>

            <!-- Pagination -->
            <form method="get" class="mb-4">
                <label for="per_page">Rows per page:</label>
                <select name="per_page" id="per_page" onchange="this.form.submit()">
                    <option value="5" {% if per_page == 5 %}selected{% endif %}>5</option>
                    <option value="10" {% if per_page == 10 %}selected{% endif %}>10</option>
                    <option value="20" {% if per_page == 20 %}selected{% endif %}>20</option>
                    <option value="50" {% if per_page == 50 %}selected{% endif %}>50</option>
                </select>
                <input type="hidden" name="page" value="{{ page }}">
            </form>

            <nav aria-label="Page navigation">
                <ul class="pagination">
                    {% for p in range(1, total_pages + 1) %}
                        <li class="page-item {% if p == page %}active{% endif %}">
                            <a class="page-link" href="/display?page={{ p }}&per_page={{ per_page }}">{{ p }}</a>
                        </li>
                    {% endfor %}
                </ul>
            </nav>
        </div>

        <!-- JavaScript to handle row clicks -->
        <script>
        $(document).ready(function() {
            $('#csvTable tbody tr').on('click', function() {
                var rowData = $(this).children("td").map(function() {
                    return $(this).html();
                }).get();

                var groundTruth = rowData[0];  // Adjust index according to CSV structure
                var candidateLine = rowData[1]; // Adjust index accordingly

                $('#ground-truth').html(groundTruth);
                $('#candidate-line').html(candidateLine);
            });
        });
        </script>
    </body>
    </html>
    '''

    return render_template_string(html_template, table=table_html, page=page, per_page=per_page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
