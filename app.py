from flask import Flask, request, send_from_directory, jsonify, redirect, url_for,render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"  # Folder for static files like index.html, contact.html, and all_files.html
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to serve the index.html from the static folder
@app.route('/')
def home():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# Route to serve upload.html, which should be located in the templates folder
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# API endpoint to get the list of the latest 3 uploaded files (for index.html display)
@app.route('/latest-files')
def latest_files():
    files = sorted(os.listdir(UPLOAD_FOLDER), key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
    recent_files = files[:3]  # Take the first 3 newest files
    return jsonify(recent_files)

# API endpoint to get the list of all uploaded files (for all_files.html display)
@app.route('/all-files-data')
def all_files_data():
    files = os.listdir(app.config['UPLOAD_FOLDER'])  # Get the list of files in the upload folder
    return jsonify(files)  # Return the list as JSON

# Route to serve the contact.html from the static folder
@app.route('/contact')
def contact():
    return send_from_directory(STATIC_FOLDER, 'contact.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('upload_page'))
    file = request.files['file']
    if file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('upload_page'))

# Route to handle file downloads
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
