from flask import Flask, request, redirect, url_for, flash
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'secret_key'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Upload PE3 CSV File</title>
    <h1>Upload a PE3 CSV file</h1>
    <form method="POST" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('upload_form'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('upload_form'))
    
    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = pd.read_csv(filepath)
            converted_df = convert_pe3_data(df)
            converted_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'converted_' + filename)
            converted_df.to_csv(converted_filepath, index=False)
            flash('File successfully uploaded and converted')
            return redirect(url_for('upload_form'))
        
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            return redirect(url_for('upload_form'))

def convert_pe3_data(df):
    df.columns = [col.strip().lower() for col in df.columns]
    return df

if __name__ == '__main__':
    app.run(debug=True)
