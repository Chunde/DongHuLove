from flask import Flask, request, render_template, session
from werkzeug.utils import secure_filename
import pandas as pd
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Random secret key for session management
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_men_ids = None
    selected_women_ids = None

    if request.method == 'POST':
        # Check if file was uploaded
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                session['filename'] = filename
                print("File uploaded and filename stored in session")

        if 'num_men' in request.form and 'num_women' in request.form:
            num_men = int(request.form['num_men'])
            num_women = int(request.form['num_women'])

        if 'filename' in session:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], session['filename'])
        else:
            file_path = "uploads/default.xlsx"
            df = pd.read_excel(file_path)
            # print(f"Data retrieved from uploaded file: {df}")
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
