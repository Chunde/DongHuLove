from flask import Flask, request, render_template, session, redirect, url_for
import pandas as pd
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secret key for session management

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_men_ids = None
    selected_women_ids = None

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                df = pd.read_excel(file)
                session['data'] = df.to_dict(orient='list')
        if 'num_men' in request.form and 'num_women' in request.form:
            num_men = int(request.form['num_men'])
            num_women = int(request.form['num_women'])

        if 'data' in session:
            df = pd.DataFrame(session['data'])
            selected_men_ids, selected_women_ids = process_selection(df, num_men, num_women)

    return render_template('index.html', selected_men_ids=selected_men_ids, selected_women_ids=selected_women_ids)

def process_selection(df, num_men, num_women):
    men_ids = df[df['性别'] == '男']['编号'].tolist()
    women_ids = df[df['性别'] == '女']['编号'].tolist()

    if len(men_ids) < num_men or len(women_ids) < num_women:
        return "数据不足", 400

    selected_men_ids = random.sample(men_ids, num_men)
    selected_women_ids = random.sample(women_ids, num_women)

    return selected_men_ids, selected_women_ids

if __name__ == '__main__':
    app.run(debug=True)
