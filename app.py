from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import os
from werkzeug.utils import secure_filename
from utils.extractor import process_document
from utils.db_utils import insert_resume_data, get_all_data, get_pending_data, approve_record
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import pandas as pd
from io import BytesIO

app = Flask(__name__)
app.secret_key = "fornova_secret_key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ----------- File Validation -----------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ----------- Routes -----------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == "admin@fornova.com" and password == "admin123":
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('login'))
    data = get_all_data()
    return render_template('dashboard.html', data=data)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            extracted_data = process_document(filepath)
            insert_resume_data(extracted_data)
            flash("Document processed successfully!", "success")
            return render_template('result.html', data=extracted_data)
        else:
            flash("Invalid file format!", "danger")
    return render_template('upload.html')


@app.route('/review')
def review():
    if 'admin' not in session:
        return redirect(url_for('login'))
    data = get_pending_data()
    return render_template('review.html', data=data)


@app.route('/approve/<int:id>')
def approve(id):
    approve_record(id)
    flash("Record approved!", "success")
    return redirect(url_for('review'))


@app.route('/export')
def export():
    df = pd.DataFrame(get_all_data())
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, download_name="fornova_extracted.xlsx", as_attachment=True)


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)