import subprocess
import threading
from tkinter import *
from tkinter import messagebox, ttk
import os
import re

# FFmpeg 작업을 스레드에서 실행 (진행 상태 표시)
def download_video(link, name, progress_bar, progress_label):
    command = f'ffmpeg -i "{link}" -c copy {name}.ts'

    # CMD 창을 숨기기 위한 플래그 설정 (Windows용)
    startupinfo = None
    if os.name == 'nt':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        # FFmpeg 명령어 실행 및 진행률 파싱
        process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)

        # stderr에서 진행률을 파싱하는 반복문
        for line in process.stderr:
            # 진행률 정보 파싱 (ex: "frame=1000 fps=24 q=-1.0 size=500kB time=00:00:10.00 bitrate=4000kbits/s speed=1x")
            match = re.search(r'time=(\d+):(\d+):(\d+).(\d+)', line)
            if match:
                hours, minutes, seconds, milliseconds = map(int, match.groups())
                total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 100
                # 총 시간 대비 현재 시간으로 진행률 계산 (예시로 100초를 최대 시간으로 가정)
                total_duration = 100  # 다운로드 할 파일의 총 시간을 알 수 있다면 이를 사용
                progress = (total_seconds / total_duration) * 100

                # 진행률 업데이트 (UI 스레드에서 업데이트)
                update_progress(progress, progress_bar, progress_label)

        process.wait()
        if process.returncode == 0:
            messagebox.showinfo("성공", f"{name}.ts 다운로드가 완료되었습니다.")
        else:
            messagebox.showerror("오류", "다운로드 중 오류가 발생했습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"다운로드에 실패했습니다: {e}")
    finally:
        button.config(state=NORMAL)

# 진행 상태 업데이트
def update_progress(progress, progress_bar, progress_label):
    # Tkinter의 UI 업데이트는 메인 스레드에서만 가능하므로 after()를 사용
    progress_bar.after(0, lambda: progress_bar.config(value=progress))
    progress_label.after(0, lambda: progress_label.config(text=f"Progress: {progress:.2f}%"))

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
    threading.Thread(target=download_video, args=(link, name, progress_bar, progress_label)).start()

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

# 진행 상태 라벨 및 프로그레스 바
progress_label = Label(window, text="Progress: 0%")
progress_label.place(x=30, y=80)

progress_bar = ttk.Progressbar(window, orient="horizontal", length=400, mode="determinate")
progress_bar.place(x=70, y=110)

# Tkinter 메인 루프 실행
window.mainloop()