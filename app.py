from flask import Flask, request, render_template_string
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>🚀 ثغرة تنفيذ الأوامر</h2>
    <form action="/cmd" method="get">
        <input type="text" name="command" placeholder="اكتب أمراً..." style="width:60%">
        <input type="submit" value="تنفيذ">
    </form>
    '''

@app.route('/cmd')
def cmd():
    command = request.args.get('command', '')
    if command:
        try:
            output = subprocess.check_output(command, shell=True, text=True)
            return f'<pre>{output}</pre>'
        except Exception as e:
            return f'<pre>خطأ: {e}</pre>'
    return 'اكتب أمراً!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100)
