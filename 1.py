import subprocess
while True:
    a = input("link: ")
    b = input("name: ")
    c = f'ffmpeg -i "{a}" -c copy {b}.ts'
    get = subprocess.call(c)


