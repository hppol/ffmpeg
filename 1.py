while True:
    a = input("link: ")
    b = input("number: ")
    print("ffmpeg -i \"%s\" -c copy %s.ts " %(a,b))