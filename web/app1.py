from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def display_csv():
    # Use your provided local file path
    csv_file = '/home/victor/ASR_UB/UB_ASR/wer_output.csv'  # Your CSV file path
    data = pd.read_csv(csv_file)
    
    # 获取页数和每页行数参数
    page = request.args.get('page', 1, type=int)  # 获取当前页数，默认为第1页
    per_page = request.args.get('per_page', 10, type=int)  # 每页显示行数，默认为10行
    
    # 分页计算
    start_row = (page - 1) * per_page  # 起始行号
    end_row = start_row + per_page  # 结束行号
    
    # 根据页数进行数据切片
    page_data = data[start_row:end_row]
    
    # 总页数计算
    total_rows = len(data)
    total_pages = (total_rows // per_page) + (1 if total_rows % per_page else 0)
    
    # 将数据转换为HTML表格
    table_html = page_data.to_html(classes='table table-striped', index=False, table_id='csvTable', escape=False)

    # Create a basic HTML template with JavaScript for row click functionality
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
    /* 定义 2x2 表格布局 */
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
                    <div><span style="color: red;">Insertion</span></div>
                    <div><span style="color: blue;">Omition</span></div>
                    <div><span style="color: green;">Subtitution</span></div>
                </div>
            </div>
            
            <!-- Section to show selected rows' Ground Truth and Candidate Line -->
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
                    {% if page > 1 %}
                    <li class="page-item">
                        <a class="page-link" href="/?page=1&per_page={{ per_page }}" aria-label="First">
                            <span aria-hidden="true">&laquo;&laquo;</span>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="/?page={{ page - 1 }}&per_page={{ per_page }}" aria-label="Previous">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    {% endif %}
                    
                    {% for p in range(1, total_pages + 1) %}
                        <li class="page-item {% if p == page %}active{% endif %}">
                            <a class="page-link" href="/?page={{ p }}&per_page={{ per_page }}">{{ p }}</a>
                        </li>
                    {% endfor %}
                    
                    {% if page < total_pages %}
                    <li class="page-item">
                        <a class="page-link" href="/?page={{ page + 1 }}&per_page={{ per_page }}" aria-label="Next">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                    <li class="page-item">
                        <a class="page-link" href="/?page={{ total_pages }}&per_page={{ per_page }}" aria-label="Last">
                            <span aria-hidden="true">&raquo;&raquo;</span>
                        </a>
                    </li>
                    {% endif %}
                </ul>
            </nav>
        </div>

        <!-- JavaScript to handle row clicks -->
        <script>
        $(document).ready(function() {
            $('#csvTable tbody tr').on('click', function() {
                // Get the data from the clicked row
                var rowData = $(this).children("td").map(function() {
                    return $(this).html();
                }).get();

                // Assuming the columns are like [Ground Truth, Candidate Line, ...]
                var groundTruth = rowData[0];  // Adjust index according to your CSV structure
                var candidateLine = rowData[1]; // Adjust index according to your CSV structure

                $('#ground-truth').html(groundTruth);
                $('#candidate-line').html(candidateLine);  // 使用 .html() 渲染 HTML 而不是纯文本
            });
        });
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(html_template, table=table_html, page=page, per_page=per_page, end_row=end_row, total_rows=total_rows, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)
