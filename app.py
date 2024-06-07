from flask import Flask, request, render_template
import pandas as pd
import random

app = Flask(__name__)

# Global variable to store the dataframe
df = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global df
    file = request.files['file']
    num_men = int(request.form['num_men'])
    num_women = int(request.form['num_women'])

    if file:
        df = pd.read_excel(file)
        return process_selection(num_men, num_women)
    return "未上传文件", 400

def process_selection(num_men, num_women):
    global df
    if df is None:
        return "没有可用的数据", 400

    men_ids = df[df['性别'] == '男']['编号'].tolist()
    women_ids = df[df['性别'] == '女']['编号'].tolist()

    if len(men_ids) < num_men or len(women_ids) < num_women:
        return "数据不足", 400

    selected_men_ids = random.sample(men_ids, num_men)
    selected_women_ids = random.sample(women_ids, num_women)

    return render_template('results.html', selected_men_ids=selected_men_ids, selected_women_ids=selected_women_ids)

if __name__ == '__main__':
    app.run(debug=True)
