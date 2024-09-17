import subprocess
import threading
from tkinter import *
from tkinter import messagebox
import os

# FFmpeg 작업을 스레드에서 실행
def download_video(link, name):
    command = f'ffmpeg -i "{link}" -c copy {name}.ts'

    # CMD 창을 숨기기 위한 플래그 설정 (Windows용)
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        # FFmpeg 명령어 실행 (cmd 창을 숨기고)
        subprocess.Popen(command, shell=True, startupinfo=startupinfo).wait()
        messagebox.showinfo("성공", f"{name}.ts 다운로드가 완료되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"다운로드에 실패했습니다: {e}")
    finally:
        button.config(state=NORMAL)

# 다운로드 버튼 클릭 시 실행
def click():
    link = entry1.get()
    name = entry2.get()

    if not link or not name:
        messagebox.showwarning("경고", "링크와 이름을 모두 입력하세요.")
        return

    # 입력 필드 초기화
    entry1.delete(0, len(entry1.get()))
    entry2.delete(0, len(entry2.get()))

    # 다운로드가 진행되는 동안 버튼 비활성화
    button.config(state=DISABLED)

    # 새 스레드에서 다운로드 시작
    threading.Thread(target=download_video, args=(link, name)).start()

# 창 설정
window = Tk()
window.geometry("700x300")
window.title("FFmpeg Video Downloader")

# 링크 입력 레이블 및 텍스트 입력 필드
label1 = Label(window, text="Link")
label1.place(x=30, y=10)
entry1 = Entry(window)
entry1.place(x=70, y=10, width=250, height=25)

# 파일 이름 입력 레이블 및 텍스트 입력 필드
label2 = Label(window, text="Name")
label2.place(x=30, y=40)
entry2 = Entry(window)
entry2.place(x=70, y=40, width=250, height=25)

# 다운로드 버튼
button = Button(window, text="Download", width=8, height=3, command=click)
button.place(x=330, y=10)

# Tkinter 메인 루프 실행
window.mainloop()