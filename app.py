from flask import Flask, request, send_file, render_template
import fitz  # PyMuPDF
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    file = request.files['file']
    if file and file.filename.endswith('.pdf'):
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        text = ''
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()

        txt_filename = file.filename.rsplit('.', 1)[0] + '.txt'
        txt_path = os.path.join(DOWNLOAD_FOLDER, txt_filename)

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(text)

        return send_file(txt_path, as_attachment=True)
    return "শুধু পিডিএফ ফাইল দিন!"

if __name__ == '__main__':
    app.run(debug=True)
