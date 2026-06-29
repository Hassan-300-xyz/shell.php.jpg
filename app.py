from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# صفحة رفع ملفات عادية جداً (مثل أي موقع)
upload_page = '''
<!DOCTYPE html>
<html>
<head>
    <title>رفع الملفات</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        form { display: inline-block; padding: 20px; border: 1px solid #ddd; border-radius: 10px; }
        input[type="file"] { margin: 10px; }
        input[type="submit"] { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        input[type="submit"]:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h2>📁 رفع الملفات</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <br>
        <input type="submit" value="رفع">
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return upload_page

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    os.makedirs('uploads', exist_ok=True)
    filename = f.filename
    filepath = os.path.join('uploads', filename)
    f.save(filepath)

    # ✅ صفحة عادية جداً: تظهر فقط اسم الملف، لا روابط ولا شيء!
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>تم الرفع</title>
        <style>
            body {{ font-family: Arial, text-align: center; margin-top: 50px; }}
            .filename {{ font-size: 20px; color: #333; }}
        </style>
    </head>
    <body>
        <h3>✅ تم رفع الملف:</h3>
        <div class="filename">{filename}</div>
        <br>
        <a href="/" style="color: #007bff; text-decoration: none;">⬅️ رفع ملف آخر</a>
    </body>
    </html>
    '''

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=8000)
