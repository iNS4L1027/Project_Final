import tkinter as tk
from tkinter import *
from tkinter.simpledialog import *
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import threading
import pickle

# 알림 상태 저장
notification_enabled = True

# 알림 쓰레드 설정
notification_thread = None

# 알림 보내기
def send_notification(time, message):
    current_time = datetime.now()
    notification_time = datetime.strptime(time + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    time_diff = (notification_time - current_time).total_seconds()

    if time_diff <= 0:
        messagebox.showinfo("할 일 알림", message)
    else:
        global notification_thread
        notification_thread = threading.Timer(time_diff, messagebox.showinfo, args=("할 일 알림", message))
        notification_thread.start()

# 알림 설정 온/오프
def toggle_notification():
    global notification_enabled
    notification_enabled = not notification_enabled
    if notification_enabled:
        toggle_button.config(text="알림 끄기")
    else:
        toggle_button.config(text="알림 켜기")

# 데이터 파일 설정
data_file = "todo_data.pkl"

# 목록을 저장할 리스트 생성
todo_list = []

# 할 일 추가 함수
def add_todo():
    todo = entry.get()
    deadline = cal.get_date()
    notification_time = deadline + timedelta(hours=9)
    if todo and deadline:
        todo_list.append((todo, deadline))
        listbox.insert(tk.END, f"{todo} (기한: {deadline})")
        entry.delete(0, tk.END)
        cal.set_date(None)
        save_data()
        if notification_enabled:
            send_notification(str(notification_time), f"{todo}의 마감일입니다.")

# 할 일 제거 함수
def delete_todo():
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        listbox.delete(index)
        todo_list.pop(index)
        save_data()

# 데이터 저장 함수
def save_data():
    with open(data_file, "wb") as file:
        pickle.dump(todo_list, file)

# 데이터 로드 함수
def load_data():
    try:
        with open(data_file, "rb") as file:
            data = pickle.load(file)
            todo_list.extend(data)
            for todo, deadline in data:
                listbox.insert(tk.END, f"{todo} (기한: {deadline})")
    except FileNotFoundError:
        return

# 창 설정
window = tk.Tk()
window.title("TO_DO")
window.geometry("775x695")
window.resizable(width=False, height=False)
window.configure(bg="#1C1C1C")

# 날짜 선택
cal = DateEntry(window, width=12, background='#424242',
                foreground='white', borderwidth=2)
cal.grid(row=0, column=0)

# 할 일 입력 칸
entry = tk.Entry(window, font="맑은고딕, 15", background="#424242", fg="White", width=50)
entry.grid(row=0, column=1)


# 할 일 추가 버튼
add_button = tk.Button(window, text="추가", bg="#424242", font="맑은고딕, 13", fg="White", command=add_todo)
add_button.grid(row=0, column=2)


# 할 일 목록 표시 리스트박스
listbox = tk.Listbox(window, font="맑은고딕, 15", background="#424242", fg="White", height=30, width=70)
listbox.grid(row=1, column=0, columnspan=3)


# 할 일 삭제 버튼
delete_button = tk.Button(window, text="삭제", bg="#424242", font="맑은고딕, 13", fg="White", command=delete_todo)
delete_button.grid(row=2, column=0, columnspan=2)

# 알림 설정 온/오프 버튼
toggle_button = tk.Button(window, text="알림 끄기", bg="#424242", font="맑은고딕, 13", fg="White", command=toggle_notification)
toggle_button.grid(row=2, column=2, columnspan=2)

# 데이터 로드
load_data()

# 데이터 저장
def on_closing():
    save_data()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)


window.mainloop()
