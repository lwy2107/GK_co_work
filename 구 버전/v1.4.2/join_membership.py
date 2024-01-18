from tkinter import *
from selenium import webdriver
import tkinter.font

'''
# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="database"
)
cursor = conn.cursor()
'''
win = Tk()
win.title("회원가입")
win.geometry("800x800")
win.option_add("*Font", "맑은고딕 25")
win.configure(bg='white')

font = tkinter.font.Font(family="맑은 고딕", size=17)

#로고
lab_d = Label(win)
img = PhotoImage(file="./image/GlobalKorea_logo_11zon.png", master=win)
    # 이미지 크기 변환 img = img.subsample(8)
lab_d.config(image=img, bd=0)
lab_d.pack(pady=20)


#id 라벨
lab1 = Label(win)
lab1.config(text="ID")
lab1.pack(pady=20)

#id 입력창
ent1 = Entry(win)
ent1.insert(0,"아이디")
ent1.config(font=font,width=29)
def clear_id(event):
    if ent1.get()=="아이디":
        ent1.delete(0,len(ent1.get()))
ent1.bind("<Button-1>", clear_id)

ent1.pack(pady=20)

#password 라벨
lab2 = Label(win)
lab2.config(text="Password")
lab2.pack(pady=20)

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

#전화번호 라벨
lab3 = Label(win)
lab3.config(text="Phone Number")
lab3.pack(pady=20)

#전화번호 입력창
ent3 = Entry(win)
ent3.insert(0,"'-'빼고 숫자만 입력")
ent3.config(font=font, width=29)
def clear_phonenumber(event):
    if ent3.get()=="'-'빼고 숫자만 입력":
        ent3.delete(0,len(ent3.get()))
ent3.bind("<Button-1>", clear_phonenumber)
ent3.pack()


#회원가입 버튼
btn = Button(win)
btn.config(text="회원가입")
btn.config(font=font,width=29,fg="white",bg="red")


btn.pack(pady=30)
win.mainloop()

''''''''''''''''''''''''''''''''''''''''''''''''
#회원가입 기능 구현

