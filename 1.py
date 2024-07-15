import pyperclip
import subprocess
while True:
    a = input("link: ")
    b = input("name: ")
    pyperclip.copy("ffmpeg -i \"%s\" -c copy %s.ts " %(a,b))
    subprocess.call('start', shell = True)


