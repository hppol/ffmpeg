from tkinter import *
from tkinter import messagebox
import subprocess

window = Tk()
window.geometry("700x300")
window.title("download")
def click():
    link = entry1.get()
    name = entry2.get()
    if not link or not name:
        messagebox.showwarning("경고", "링크와 이름을 모두 입력하세요.")
        return
    
    command = f'ffmpeg -i "{link}" -c copy {name}.ts'
    
    entry1.delete(0, len(entry1.get()))
    entry2.delete(0, len(entry2.get()))
    
    #버튼 비활성화
    button.config(state=DISABLED)
    
    try:
        # FFmpeg 명령어 실행
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("성공", f"{name}.ts 다운로드가 완료되었습니다.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("오류", f"다운로드에 실패했습니다: {e}")
    finally:
        # 버튼 다시 활성화
        button.config(state=NORMAL)


label1 = Label(window, text="link")
label1.place(x=30, y=10)
entry1 = Entry(window)
entry1.place(x=70, y=10, width=250, height=25)

label2 = Label(window, text="name")
label2.place(x=30, y=40)
entry2 = Entry(window)
entry2.place(x=70, y=40, width=250, height=25)

button = Button(window, text="download", width=8, height=3, command=click)
button.place(x=330, y=10)


window.mainloop()