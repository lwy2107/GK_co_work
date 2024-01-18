import tkinter as tk
from collections import deque
import time
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk
import requests
import json
import threading

class Window(tk.Tk):
    def publish_clear_message(self, duration):
        time.sleep(duration * 60)
        self.client.publish("lwy/ro", "clear")

    def __init__(self):
        super().__init__()

        self.text1 = "(주)글로벌코리아\n\n 안녕하세요!\n안동 월영교 방문을\n 환영합니다ミ✭︎"
        self.text2 = "저희 문보트를\n찾아 주셔서\n정말 감사 드립니다\n\n즐거운 추억들을\n만들고 가세요☪"
        self.text3 = "찾아 주셔서\n정말 감사합니다.\n\n 행복한 하루\n되시길 빕니다☆彡"
        self.text4 = "╔ღ═╗╔╗                  \n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝"
        self.text5 = "⁎⭑⛧꙳⭒☪︎⭒꙳⛧＊⭑\n즐거운 나날이\n언제나 계속 되시길\n⁎⭑⛧꙳⭒☪︎⭒꙳⛧＊⭑"

        self.geometry("1280x1024")
        self.title("문보트 전광판")
        self.count_thread_stop_event = None

        res = requests.get("https://date.nager.at/api/v3/NextPublicHolidays/KR")
        holidays = json.loads(res.text)
        today = time.strftime("%Y-%m-%d")
        is_holiday = any(holiday["date"] == today for holiday in holidays)

        if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6 or is_holiday:
            self.image_paths = ["문1.jpg", "황1.jpg", "문2.jpg", "황3.jpg", "문3.jpg", "황5.jpg", "문4.jpg", "황6.jpg",
                                "문7.jpg", "문8.jpg", "문9.jpg", "문10.jpg"]
            self.current_image_index = 0
        else:
            self.image_paths = ["문1.jpg", "황1.jpg", "문2.jpg", "황3.jpg", "문3.jpg", "황5.jpg", "문4.jpg", "황6.jpg",
                                "문7.jpg", "문8.jpg", "문9.jpg", "문10.jpg"]
            self.current_image_index = 0

        try:
            self.images = [ImageTk.PhotoImage(Image.open(path).resize((1280, 1024)), Image.LANCZOS) for path in
                           self.image_paths]
            self.image_label = tk.Label(self, image=self.images[self.current_image_index])
            self.image_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor="ne")
        except FileNotFoundError:
            print("Image file not found")

        self.count_label = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.count_label.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)
        self.main_label = tk.Label(self, text=self.text1, font=("Arial", 50, "bold"))
        self.main_label.place(relx=0.25, rely=0.35, anchor="center")
        self.time_label = tk.Label(self, text="", font=("Arial", 30, "bold"))
        self.time_label.place(relx=1.0, rely=1.0, anchor='se')

        self.count_title = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.count_title.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)
        self.store_label = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.store_label.place(relx=0.1, rely=0.1, anchor="center")
        self.slide_thread_stop_event = threading.Event()
        self.slide_thread = threading.Thread(target=self.slide_texts, args=(
            [self.text1, self.text2, self.text3, self.text4, self.text5], self.main_label,
            self.slide_thread_stop_event))
        self.slide_thread.start()
        self.update_label()
        self.update_time()

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect("broker.mqtt-dashboard.com", 1883)
        self.client.subscribe("moonboat/andong/GK_0715*")
        self.client.subscribe("moonboat/andong/GK_0715*2")
        self.client.loop_start()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        if topic == "moonboat/andong/GK_0715*":
            if payload.startswith('time:'):
                try:
                    time_in_minutes = int(payload.split(':')[1])
                    self.count_label.config(text=f": {time_in_minutes:02d}:00", fg="white")
                    self.count_label.lift()
                    if hasattr(self, "count_thread") and self.count_thread.is_alive():
                        self.count_thread_stop_event.set()
                        self.count_label.config(text="")
                        self.count_label.lower()
                    self.count_thread_stop_event = threading.Event()
                    self.count_thread = threading.Thread(target=self.countdown, args=(time_in_minutes, self.count_label, self.count_thread_stop_event))
                    self.count_thread.start()
                except ValueError:
                    print(f"Invalid time format in payload: {payload}")

            elif payload == "clear":
                self.main_label.config(fg="black", font=("Arial", 50, "bold"))
                self.main_label.place(relx=0.25, rely=0.35, anchor="center")
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()
                    self.blink_thread.join()
                self.slide_thread_stop_event = threading.Event()
                self.slide_thread = threading.Thread(target=self.slide_texts, args=(
                    [self.text1, self.text2, self.text3,self.text4,self.text5], self.main_label, self.slide_thread_stop_event))
                self.slide_thread.start()

            elif payload.startswith("moon:"):
                try:
                    duration = int(payload.split(":")[1])
                    hours = duration // 60
                    minutes = duration % 60
                    if hours > 0:
                        self.main_label.config(text=f"문보트 대기시간\n{hours}시간 {minutes}분", font=("Arial", 50, "bold"), fg="red")
                    else:
                        self.main_label.config(text=f"문보트 대기시간\n{minutes}분", font=("Arial", 50, "bold"), fg="red")
                    self.main_label.place(relx=0.5, rely=0.5, anchor="center")
                    if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                        self.slide_thread_stop_event.set()
                        self.slide_thread.join()
                    if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                        self.blink_thread_stop_event.set()
                        self.blink_thread.join()
                    self.slide_thread_stop_event = threading.Event()
                    self.import tkinter as tk
import time
import paho.mqtt.client as mqtt
from PIL import Image, ImageTk
import requests
import json
import threading
from collections import deque

class Window(tk.Tk):
    def publish_clear_message(self, duration):
        # 문보트 대기시간을 초기화하는 함수
        time.sleep(duration * 60)  # duration 분 후에 clear 메시지를 발행
        self.client.publish("lwy/ro", "clear")

    def __init__(self):
        super().__init__()

        # 메인라벨의 슬라이드 문구
        self.text1 = "(주)글로벌코리아\n\n 안녕하세요!\n안동 월영교 방문을\n 환영합니다ミ✭︎"
        self.text2 = "저희 문보트를\n찾아 주셔서\n정말 감사 드립니다\n\n즐거운 추억들을\n만들고 가세요☪"
        self.text3 = "찾아 주셔서\n정말 감사합니다.\n\n 행복한 하루\n되시길 빕니다☆彡"
        self.text4 = "╔ღ═╗╔╗                  \n╚╗╔╝║║ღ═╦╦╦═ღ\n╔╝╚╗ღ╚╣║║║║╠╣\n╚═ღ╝╚═╩═╩ღ╩═╝"
        self.text5 = "⁎⭑⛧꙳⭒☪︎⭒꙳⛧＊⭑\n즐거운 나날이\n언제나 계속 되시길\n⁎⭑⛧꙳⭒☪︎⭒꙳⛧＊⭑"

        # 전광판 크기와 이름
        self.geometry("1280x1024")
        self.title("문보트 전광판")
        self.count_thread_stop_event = None

        # 공휴일 API 호출
        res = requests.get("https://date.nager.at/api/v3/NextPublicHolidays/KR")
        holidays = json.loads(res.text)
        # 오늘이 공휴일인지 여부 체크
        today = time.strftime("%Y-%m-%d")
        is_holiday = any(holiday["date"] == today for holiday in holidays)
        # 이미지 설정
        if time.localtime().tm_wday == 5 or time.localtime().tm_wday == 6 or is_holiday:  
            self.image_paths = ["문1.jpg", "황1.jpg", "문2.jpg", "황3.jpg", "문3.jpg", "황5.jpg", "문4.jpg", "황6.jpg",
                                "문7.jpg", "문8.jpg", "문9.jpg", "문10.jpg"]
            self.current_image_index = 0
        else:
            self.image_paths = ["문1.jpg", "황1.jpg", "문2.jpg", "황3.jpg", "문3.jpg", "황5.jpg", "문4.jpg", "황6.jpg",
                                "문7.jpg", "문8.jpg", "문9.jpg", "문10.jpg"]
            self.current_image_index = 0
        
        try: 
            self.images = [ImageTk.PhotoImage(Image.open(path), Image.LANCZOS) for path in self.image_paths]
            self.image_label = tk.Label(self, image=self.images[self.current_image_index])
            self.image_label.pack(side=tk.RIGHT, padx=10, pady=10, anchor="ne")
        except FileNotFoundError:
            print("Image file not found")

        # 기타 라벨
        self.count_label = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.count_label.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)
        self.main_label = tk.Label(self, text=self.text1, font=("Arial", 50, "bold"))
        self.main_label.place(relx=0.25, rely=0.35, anchor="center")
        self.time_label = tk.Label(self, text="", font=("Arial", 30, "bold"))
        self.time_label.place(relx=1.0, rely=1.0, anchor='se')

        self.count_title = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.count_title.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)
        self.store_label = tk.Label(self, text="", font=("Helvetica", 50, "bold"), fg="white")
        self.store_label.place(relx=0.1, rely=0.1, anchor="center")
        self.slide_thread_stop_event = threading.Event()
        self.slide_thread = threading.Thread(target=self.slide_texts, args=(
            [self.text1, self.text2, self.text3, self.text4, self.text5], self.main_label,
            self.slide_thread_stop_event))
        self.slide_thread.start()
        self.update_label()
        self.update_time()

        # MQTT 서버와 연결
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect("broker.mqtt-dashboard.com", 1883)
        self.client.subscribe("moonboat/andong/GK_0715*")
        self.client.subscribe("moonboat/andong/GK_0715*2")
        self.client.loop_start()

        # 대기자 명단 및 대기자 라벨 초기화
        self.waiting_queue = deque()
        self.waiting_labels = []
        for i in range(3):
            label = tk.Label(self, text="", font=("Arial", 30), fg="green")
            label.pack()
            label.lower()
            self.waiting_labels.append(label)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic == "moonboat/andong/GK_0715*":
            if payload.startswith('time:'):
                try:
                    time_in_minutes = int(payload.split(':')[1])
                    self.count_label.config(text=f": {time_in_minutes:02d}:00", fg="white")
                    self.count_label.lift()
                    if hasattr(self, "count_thread") and self.count_thread.is_alive():
                        self.count_thread_stop_event.set()
                        self.count_label.config(text="")
                        self.count_label.lower()
                    self.count_thread_stop_event = threading.Event()
                    self.count_thread = threading.Thread(target=self.countdown, args=(time_in_minutes, self.count_label, self.count_thread_stop_event))
                    self.count_thread.start()
                except ValueError:
                    print(f"Invalid time format in payload: {payload}")
            elif payload == "clear":
                self.main_label.config(fg="black", font=("Arial", 50, "bold"))
                self.main_label.place(relx=0.25, rely=0.35, anchor="center")
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()
                    self.blink_thread.join()
                self.slide_thread_stop_event = threading.Event()
                self.slide_thread = threading.Thread(target=self.slide_texts, args=(
                    [self.text1, self.text2, self.text3,self.text4,self.text5], self.main_label, self.slide_thread_stop_event))
                self.slide_thread.start()
            elif payload.startswith("moon:"):
                try:
                    duration = int(payload.split(":")[1])
                    hours = duration // 60
                    minutes = duration % 60
                    if hours > 0:
                        self.main_label.config(text=f"문보트 대기시간\n{hours}시간 {minutes}분", font=("Arial", 50, "bold"),fg="red")
                    else:
                        self.main_label.config(text=f"문보트 대기시간\n{minutes}분", font=("Arial", 50, "bold"), fg="red")
                    self.main_label.place(relx=0.5, rely=0.5, anchor="center")
                    if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                        self.slide_thread_stop_event.set()
                        self.slide_thread.join()
                    if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                        self.blink_thread_stop_event.set()
                        self.blink_thread.join()
                    self.slide_thread_stop_event = threading.Event()
                    self.blink_thread_stop_event = threading.Event()
                    self.blink_thread = threading.Thread(target=self.blink_text, args=(f"문보트 대기시간 \n{hours}시간 {minutes}분",), daemon=True)
                    self.blink_thread.start()
                    self.clear_thread = threading.Thread(target=self.publish_clear_message, args=(duration,), daemon=True)
                    self.clear_thread.start()
                except ValueError:
                    self.main_label.config(text="잘못된 입력입니다.", font=("Arial", 50, "bold"), fg="red")
                    self.main_label.place(relx=0.5, rely=0.5, anchor="center")
            elif payload.startswith("notice:"):
                notice_text = payload.replace("notice:", "").replace("\r", "\n")
                self.main_label.place_forget()
                self.main_label.config(text=notice_text, font=("Arial", 140, "bold"), fg="red")
                self.main_label.place(relx=0.5, rely=0.5, anchor="center")
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()
            elif payload.startswith('wait:'):
                try:
                    wait_count = int(payload.split(':')[1])
                    self.update_waiting(wait_count)
                except ValueError:
                    print(f"Invalid wait format in payload: {payload}")
            elif payload.startswith('wdel:'):
                try:
                    number_to_remove = int(payload.split(':')[1])
                    self.remove_waiting(number_to_remove)
                except ValueError:
                    print(f"Invalid wdel format in payload: {payload}")
            elif payload.startswith('wdelall'):
                self.waiting_queue.clear()
                self.update_waiting_labels()
            else:
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()
                    self.blink_thread.join()
                self.main_label.place(relx=0.25, rely=0.35, anchor="center")
                self.main_label.config(font=("Arial", 50, "bold"), text=payload.replace("\r", "\n"),fg="black")
        if topic == "moonboat/andong/GK_0715*2":
            if payload == "clear":
                self.store_label.place_forget()
            else:
                self.store_label.lift()
                self.store_label.config(font=("Arial", 100, "bold"), text=payload.replace("\r", "\n"), fg="black")
                self.store_label.place(relx=0.5, rely=0.5, anchor="center", width=2000, height=2000)

    def slide_texts(self, text_list, label, stop_event):
        index = 0
        while not stop_event.is_set():
            text = text_list[index]
            label.config(text=text)
            index += 1
            if index == len(text_list):
                index = 0
            time.sleep(5)

    def countdown(self, time_in_minutes, ch_count_label, stop_event):
        time_in_seconds = time_in_minutes * 60
        for i in range(time_in_seconds):
            if stop_event.is_set():
                break
            minutes = (time_in_seconds - i) // 60
            seconds = (time_in_seconds - i) % 60
            if minutes >= 60:
                hours = minutes // 60
                minutes %= 60
                ch_count_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}", fg="red")
            else:
                ch_count_label.config(text=f"{minutes:02d}:{seconds:02d}", fg="red")
            time.sleep(1)
            self.count_title.config(text="황포돛배 출항 시간", fg="black")
        ch_count_label.config(text="")
        ch_count_label.lower()
        self.count_title.config(text="", fg="black")

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)

    def blink_text(self, text):
        while not self.blink_thread_stop_event.is_set():
            self.main_label.config(text=text)
            if self.blink_thread_stop_event.is_set():
                break
            time.sleep(0.5)
            self.main_label.config(text="")
            if self.blink_thread_stop_event.is_set():
                break
            time.sleep(0.5)

    def update_label(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.image_label.config(image=self.images[self.current_image_index])
        self.after(3000, self.update_label)

    def update_waiting(self, count):
        self.waiting_queue.append(count)
        if len(self.waiting_queue) > 3:
            self.waiting_queue.popleft()
        self.update_waiting_labels()

    def remove_waiting(self, number_to_remove):
        if number_to_remove in self.waiting_queue:
            self.waiting_queue.remove(number_to_remove)
        self.update_waiting_labels()

    def update_waiting_labels(self):
        for i, label in enumerate(self.waiting_labels):
            if i < len(self.waiting_queue):
                label.config(text=f"대기자 {i + 1}: {self.waiting_queue[i]}", fg="green")
                label.lift()
            else:
                label.config(text="")
                label.lower()

window = Window()
window.mainloopblink_thread_stop_event = threading.Event()
                    self.blink_thread = threading.Thread(target=self.blink_text,args=(f"문보트 대기시간 \n{hours}시간 {minutes}분",), daemon=True)
                    self.blink_thread.start()
                    self.clear_thread = threading.Thread(target=self.publish_clear_message, args=(duration,),daemon=True)
                    self.clear_thread.start()
                except ValueError:
                    self.main_label.config(text="잘못된 입력입니다.", font=("Arial", 50, "bold"), fg="red")
                    self.main_label.place(relx=0.5, rely=0.5, anchor="center")

            elif payload.startswith("notice:"):
                notice_text = payload.replace("notice:", "").replace("\r", "\n")
                self.main_label.place_forget()
                self.main_label.config(text=notice_text, font=("Arial", 140, "bold"), fg="red")
                self.main_label.place(relx=0.5, rely=0.5, anchor="center")
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()

            elif payload.startswith('wait:'):
                try:
                    wait_count = int(payload.split(':')[1])
                    self.update_waiting(wait_count)
                except ValueError:
                    print(f"Invalid wait format in payload: {payload}")

            elif payload.startswith('wdel:'):
                try:
                    number_to_remove = int(payload.split(':')[1])
                    self.remove_waiting(number_to_remove)
                except ValueError:
                    print(f"Invalid wdel format in payload: {payload}")

            elif payload.startswith('wdelall'):
                self.waiting_queue.clear()
                self.update_waiting_labels()
            else:
                if hasattr(self, "slide_thread") and self.slide_thread.is_alive():
                    self.slide_thread_stop_event.set()
                if hasattr(self, "blink_thread") and self.blink_thread.is_alive():
                    self.blink_thread_stop_event.set()
                self.main_label.place(relx=0.25, rely=0.35, anchor="center")
                self.main_label.config(font=("Arial", 50, "bold"), text=payload.replace("\r", "\n"),fg="black")

        if topic == "moonboat/andong/GK_0715*2":
            if payload == "clear":
                self.store_label.place_forget()
            else:
                self.store_label.lift()
                self.store_label.config(font=("Arial", 100, "bold"), text=payload.replace("\r", "\n"), fg="black")
                self.store_label.place(relx=0.5, rely=0.5, anchor="center",width=2000,height=2000)

    def slide_texts(self, text_list, label, stop_event):
        index = 0
        while not stop_event.is_set():
            text = text_list[index]
            label.config(text=text)
            index += 1
            if index == len(text_list):
                index = 0
            time.sleep(5)

    def countdown(self, time_in_minutes, ch_count_label, stop_event):
        time_in_seconds = time_in_minutes * 60
        for i in range(time_in_seconds):
            if stop_event.is_set():
                break
            minutes = (time_in_seconds - i) // 60
            seconds = (time_in_seconds - i) % 60
            if minutes >= 60:
                hours = minutes // 60
                minutes %= 60
                ch_count_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}", fg="red")
            else:
                ch_count_label.config(text=f"{minutes:02d}:{seconds:02d}", fg="red")
            time.sleep(1)
            self.count_title.config(text="황포돛배 출항 시간", fg="black")
        ch_count_label.config(text="")
        ch_count_label.lower()
        self.count_title.config(text="", fg="black")

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.time_label.after(1000, self.update_time)

    def blink_text(self, text):
        while not self.blink_thread_stop_event.is_set():
            self.main_label.config(text=text)
            if self.blink_thread_stop_event.is_set():
                break
            time.sleep(0.5)
            self.main_label.config(text="")
            if self.blink_thread_stop_event.is_set():
                break
            time.sleep(0.5)

    def update_label(self):
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.image_label.config(image=self.images[self.current_image_index])
        self.after(3000, self.update_label)

    def update_waiting(self, count):
        self.waiting_queue.append(count)
        self.update_waiting_labels()

    def remove_waiting(self, number_to_remove):
        if number_to_remove in self.waiting_queue:
            self.waiting_queue.remove(number_to_remove)
        self.update_waiting_labels()

    def update_waiting_labels(self):
        for i, label in enumerate(self.waiting_labels):
            if i < len(self.waiting_queue):
                label.config(text=f"대기자 {i + 1}: {self.waiting_queue[i]}", fg="green")
                label.lift()
            else:
                label.config(text="")
                label.lower()

if __name__ == "__main__":
    window = Window()
    window.mainloop()
