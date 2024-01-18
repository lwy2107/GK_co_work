from tkinter import *
from selenium import webdriver
import tkinter.font
import map_with_customtkinter
'''
# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="database"
)
cursor = conn.cursor()

# 사용자 정보 테이블 생성
create_table_query = 
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
cursor.execute(create_table_query)
'''
win = Tk()
win.title("로그인")
win.geometry("500x400")
win.option_add("*Font", "맑은고딕 25")
win.configure(bg='white')

font = tkinter.font.Font(family="맑은 고딕", size=17)
'''
# 사용자 정보 삽입
insert_user_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
user_values = [("admin", "password")]           ent1.get,ent2.get
cursor.executemany(insert_user_query, user_values)
conn.commit()
'''
'''
#로그인 기능 구현
def validate_login():
    username = ent1.get()
    password = ent2.get()

    # 데이터베이스에서 사용자 정보 조회
    select_user_query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(select_user_query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("로그인 성공", "로그인에 성공했습니다.")
    else:
        messagebox.showerror("로그인 실패", "잘못된 사용자 이름 또는 비밀번호입니다.")
'''
#로고
lab_d = Label(win)
img = PhotoImage(file="./image/GlobalKorea_logo_11zon.png", master=win)
# 이미지 크기 변환 img = img.subsample(8)
lab_d.config(image=img, bd=0)
lab_d.pack(pady=20)

#id 입력창
ent1 = Entry(win)
ent1.insert(0,"아이디")
ent1.config(font=font,width=29)

def clear_id(event):
    if ent1.get()=="아이디":
        ent1.delete(0,len(ent1.get()))

ent1.bind("<Button-1>", clear_id)
ent1.pack(pady=20)

#password 입력창
ent2 = Entry(win)
ent2.insert(0,"비밀번호")
ent2.config(font=font,width=29)

def clear_password(event):
    if ent2.get()=="비밀번호":
        ent2.delete(0,len(ent2.get()))
        ent2.config(show = "*")
ent2.bind("<Button-1>", clear_password)

ent2.pack()


    

#로그인 버튼
btn = Button(win, command = win.destroy)
btn.config(text="로그인")
btn.config(font=font,width=29,fg="white",bg="red")
#btn.config(command=validate_login())
#btn.config()
btn.pack(pady=30)

'''
#로그인 버튼 테스트
def login():
    my_id = ent1.get()
    my_password = ent2.get()
    print(my_id, my_password)
    lab3.config(text="[메시지] 로그인 성공!", font=font,bg="white")    
btn.config(command=login)
'''

'''
cursor.close()
conn.close()
'''

#def new_win():
    #win.destroy()

def loginstart():
    win.mainloop()
    
