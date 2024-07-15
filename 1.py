while True:
    a = input("link: ")
    b = input("name: ")
    print("ffmpeg -i \"%s\" -c copy %s.ts " %(a,b))