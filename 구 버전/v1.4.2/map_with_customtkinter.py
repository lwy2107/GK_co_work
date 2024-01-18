

import customtkinter
import math
from tkintermapview import TkinterMapView

from Draw_line import CanvasPath, CanvasPositionMarker
import tkinter as tk

from tkinter import *
from PIL import Image
import login2
import communication
import threading
import warnings

warnings.filterwarnings('ignore')
customtkinter.set_default_color_theme("blue")



class tkinetmapview(TkinterMapView):
    global Marker
    global Path
    Marker = []
    Draw_line = []
    Path = []
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.canvas.delete('button') #줌인 줌 아웃 제거
        #필요 없는 기능들 제거(unbind)
        self.canvas.unbind("<B1-Motion>") 
        self.canvas.unbind("<MouseWheel>")
        self.canvas.unbind("<Button-4>")
        self.canvas.unbind("<Button-5>")
        self.canvas.unbind("<Button-1>")
        #self.canvas.bind("<space>",self.destroy_all)
        self.canvas.focus_set()
        self.image_Marker = PhotoImage(file="image\\red_marker1.png")


    def set_path(self, position_list: list, **kwargs) -> CanvasPath:
        path = CanvasPath(self, position_list, **kwargs)
        path.draw()
        self.canvas_path_list.append(path)
        return path
    
    def set_marker(self, deg_x: float, deg_y: float, text: str = None, **kwargs) -> CanvasPositionMarker:
        marker = CanvasPositionMarker(self, (deg_x, deg_y), text=text, **kwargs)
        marker.draw()
        self.canvas_marker_list.append(marker)
        return marker
    
    def mouse_click(self, event):
        coordinate_mouse_pos = self.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        x = round(coordinate_mouse_pos[0], 6) #float
        y = round(coordinate_mouse_pos[1], 6) #float

        if len(Marker) >= 10:
            Marker[0].delete()
            Path[0].delete()
            Path.pop(0)
            
            Marker.pop(0)
        Marker.append(map_widget.set_marker(x, y, text="마커", image_zoom_visibility=(0, float("inf")),icon = self.image_Marker))
        self.Draw_line.append([x, y])
        
        if len(self.Draw_line) >= 2:
                Path.append(map_widget.set_path(self.Draw_line))
                self.Draw_line.pop(0)


        

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x300+1600+700")
        self.title("컨트롤러")
        
        stick_bgimg = PhotoImage(file='./image/circle.png')
        stick_bgimg = stick_bgimg.subsample(6)
        stick_img = PhotoImage(file='./image/stick.png')
        stick_img = stick_img.subsample(8)
        
        self.stick_background = customtkinter.CTkLabel(self, image=stick_bgimg, text="", width=300, height=300,fg_color="White")
        self.stick_background.grid(pady=(0, 0), padx=(0, 0), sticky="nsew", row=1, column=1)
        
        self.stick = customtkinter.CTkLabel(self, image=stick_img, text="",fg_color="White")
        self.stick.grid(pady=(135,0), padx=(135, 0), sticky="nw", row=1, column=1)
        
        self.stick_background.bind("<Button-1>", self.stick_motion)
        self.stick_background.bind("<B1-Motion>", self.stick_motion)
        self.stick_background.bind("<ButtonRelease-1>", self.stick_reset)
        
    def stick_motion(self, event):
        x , y = event.x-5, event.y-5
        center = 150 - 15
        fun_x = x
        fun_x300 = -x+300
        E_dist=250
        F_dist=25
        print(f"x:{x}")
        print(f"y:{y}")
        
        if x >= E_dist:
            x = E_dist
        if x <= F_dist:
            x = F_dist
        if y >= E_dist:
            y = E_dist
        if y <= F_dist:
            y = F_dist
            
        if x < center:
            if y >= fun_x and y < fun_x300:
                y = center
        if x > center:
            if y >= fun_x300 and y < fun_x:
                y = center
        if y < center:
            if y <= fun_x and y < fun_x300:
                x = center
        if y > center:
            if y >= fun_x300 and y > fun_x:
                x = center    
            
        self.stick.grid(pady=(y,0), padx=(x, 0), sticky="nw", row=1, column=1)
        
    def stick_reset(self, event):
        self.stick.grid(pady=(135,0), padx=(135, 0), sticky="nw", row=1, column=1)

class App(customtkinter.CTk):
    in_out = True
    APP_NAME = "문보트"
    controller_state = "내부"
    WIDTH = 1280
    HEIGHT = 720
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        
        self.frame_left = customtkinter.CTkFrame(master=self, fg_color="white", corner_radius=0)
        self.frame_left.grid(row=0, rowspan=2, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
        
        self.frame_right = customtkinter.CTkFrame(master=self, fg_color="white", corner_radius=0, width=100)
        self.frame_right.grid(row=0, rowspan=1, column=2, columnspan=1, padx=0, pady=0, sticky="nsew")
        
        App.choice_screen(self)
        self.toplevel_window = None
        
        # ============ frame_left(지도) ============
        image_boat = PhotoImage(file='./image/moon_boat.png')
        image_boat = image_boat.subsample(25)

        self.marker_list = []
        
        self.frame_left.grid_columnconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(1, weight=0)
        
        global map_widget
        map_widget = tkinetmapview(self.frame_left, corner_radius=0)
        map_widget.grid(row=0, rowspan=2, column=0, columnspan=2, sticky="nsew", padx=(0, 0), pady=(0, 0))
        
        map_widget.set_position(36.5769, 128.7606)
        map_widget.set_zoom(17.4)
        ##배의 위치 마크 띄우는 공간 (숫자에 gps 값을 받으면 될듯)
        
        marker1 = map_widget.set_marker(36.5755834, 128.7598695, text="문보트1", icon = image_boat, image_zoom_visibility=(0, float("inf")))
        marker2 = map_widget.set_marker(36.575599, 128.760965, text="문보트2", icon = image_boat, image_zoom_visibility=(0, float("inf")))
        marker3 = map_widget.set_marker(36.575065, 128.759613, text="문보트3", icon = image_boat, image_zoom_visibility=(0, float("inf")))
        marker4 = map_widget.set_marker(36.574703, 128.760525, text="문보트4", icon = image_boat, image_zoom_visibility=(0, float("inf")))
        marker5 = map_widget.set_marker(36.574453, 128.759849, text="문보트5", icon = image_boat, image_zoom_visibility=(0, float("inf")))
        
        # ============ frame_right(클릭) ============
        image_logo = PhotoImage(file='./image/GlobalKorea_logo.png')
        image_boat_GPS = PhotoImage(file="./image/image_GPS.png")
        image_list = PhotoImage(file="./image/list.png")
        image_Rotation = PhotoImage(file="./image/image_Rotation.png")
        image_Option = PhotoImage(file="./image/image_option.png")
        image_list = image_list.subsample(15)
        
        self.frame_right.grid_columnconfigure(2, weight=0)
        self.frame_right.grid_rowconfigure(0, weight=1)

        
        #gpsmove = false
        self.init_button(image_logo, "Global Korea", 0, 0, 0, 0, "nw", self.choice_screen)
        self.init_button(image_boat_GPS, "좌표", 0, 0, 0, 99, "nw", self.GPS_screen)

        self.remote_button = customtkinter.CTkButton(master=self.frame_right, text="원격조종", image=image_Rotation, command=self.option, 
                                              height=100, width=100, fg_color='white', text_color='black' , corner_radius=0, compound='top',state="disabled")
        self.remote_button.grid(padx=(0, 0), pady=(198, 0), sticky="nw", row=0, column=3)
        # self.option_button = customtkinter.CTkButton(master=self.frame_right, text="옵션", image=image_Option, command=self.option, 
        #                                       height=100, width=100, fg_color='white', text_color='black' , corner_radius=0, compound='top',state="disabled")
        # self.option_button.grid(padx=(0, 0), pady=(297, 0), sticky="nw", row=0, column=3)


        # self.init_button(image_Rotation, "원격 조종", 0, 0, 0, 198, "nw", self.open_toplevel )
        # self.init_button(image_Option, "옵션", 0, 0, 0, 297, "nw", self.option)
        self.GPS = customtkinter.CTkLabel(self.frame_right,text=Marker, font =('normal', 20))
        
    def choice_screen(self):
        try:
            #app.option_button.configure(state="disabled")
            app.remote_button.configure(state="disabled")
        except NameError:
            pass
        try:
            map_widget.canvas.unbind('<Button-1>')
            for _ in range(len(Marker)):
                Marker[0].delete()
                Marker.pop(0)
            for _ in range(len(Path)):
                Path[0].delete()
                Path.pop(0)
            for _ in range(len(map_widget.Draw_line)):
                map_widget.Draw_line.pop(0)
        except NameError:
            pass
        try:
            self.toplevel_window.destroy()
            self.controller_statestate = "내부"
            app.whwjdrks_button.configure(text = "조정간 상태 : " + self.controller_statestate)
            self.in_out = True
        except AttributeError:
            pass
        #전체 행렬 생성 
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        #공간 설정
        self.frame_middle = customtkinter.CTkScrollableFrame(master=self, fg_color="white", corner_radius=0, border_width=1, border_color="gray", width=280)
        self.frame_middle.grid(row=0, rowspan=1, column=1, columnspan=1, padx=0, pady=0, sticky="nsew")
        
        # ============ frame_middle(보트,베터리) ============
        
        #사용할 공간에 할당할 행렬
        self.frame_middle.grid_columnconfigure(1, weight=0)
        self.frame_middle.grid_rowconfigure(0, weight=1)
        
        boat_status = [['boat1', '70%'], ['boat2', '80%'], ['boat3', '50%'], ['boat4', '30%'], ['boat5', '50%']]
        
        for i, boat_status in enumerate(boat_status):
            boat = customtkinter.CTkButton(master=self.frame_middle, text= f"{boat_status[0]} {boat_status[1]}", command = self.status_screen, font=(None,15),
                                           height=30, width=180, border_color='black', border_width=2, fg_color='white', text_color='black' , corner_radius=10)
            boat.grid(pady=(10 + (50 * i), 0), padx=(50, 0), sticky="n", row=0, column=1)

    def GPS_screen(self):
        try:
            self.toplevel_window.destroy()
            self.controller_statestate = "내부"
            app.whwjdrks_button.configure(text = "조정간 상태 : " + self.controller_statestate)
            self.in_out = True
        except AttributeError:
            pass
        #app.option_button.configure(state="disabled")
        app.remote_button.configure(state="disabled")
        map_widget.canvas.bind('<Button-1>',map_widget.mouse_click)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.frame_middle = customtkinter.CTkFrame(master=self, fg_color="white", corner_radius=0, border_width=1, border_color="gray")
        self.frame_middle.grid(row=0, rowspan=1, column=1, columnspan=1, padx=0, pady=0, sticky="nsew")
        
        # ============ frame_middle(좌표) ============
        self.frame_middle.grid_columnconfigure(1, weight=0)
        self.frame_middle.grid_rowconfigure(0, weight=1)
        
        self.GPS_button("좌표값 업데이트", 0, 5, 0, 10, "n", self.gpsMarker)
        self.GPS_button("전송", 0, 5, 10, 0, "sw", self.set_marker_event)
        self.GPS_button("삭제", 0, 150, 10, 0, "se", self.destroy_all)

    def option(self):
        
        #self.open_toplevel()
        map_widget.canvas.unbind('<Button-1>')
        # map_widget.canvas.bind('<Button-1>',map_widget.mouse_click)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.frame_middle = customtkinter.CTkFrame(master=self, fg_color="white", corner_radius=0, border_width=1, border_color="gray")
        self.frame_middle.grid(row=0, rowspan=1, column=1, columnspan=1, padx=0, pady=0, sticky="nsew")
        
        # ============ frame_middle(좌표) ============
        self.frame_middle.grid_columnconfigure(1, weight=0)
        self.frame_middle.grid_rowconfigure(0, weight=1)
        if self.in_out:
            self.controller_statestate = "내부"
        else:
            self.controller_statestate = "외부"
        
        self.Option_button("조정간 상태 : " + self.controller_statestate , 0, 5, 0, 10, "nw", self.inout)
        self.innerController()
        

        
        

    def innerController(self):
        stick_bgimg = PhotoImage(file='./image/circle.png')
        stick_bgimg = stick_bgimg.subsample(6)
        stick_img = PhotoImage(file='./image/stick.png')
        stick_img = stick_img.subsample(8)
        
        self.stick_background = customtkinter.CTkLabel(master=self.frame_middle, image=stick_bgimg, text="", width=295, height=295,fg_color="White")
        self.stick_background.grid(pady=(0, 0), padx=(0, 0), sticky="nsew", row=1, column=1)
        
        self.stick = customtkinter.CTkLabel(master=self.frame_middle, image=stick_img, text="",fg_color="White")
        self.stick.grid(pady=(135,0), padx=(135, 0), sticky="nw", row=1, column=1)
        
        self.stick_background.bind("<Button-1>", self.stick_motion)
        self.stick_background.bind("<B1-Motion>", self.stick_motion)
        self.stick_background.bind("<ButtonRelease-1>", self.stick_reset)
        
    
    def Destroy_innerController(self):
        self.stick_background.destroy()
        self.stick.destroy()

    def inout(self):
        if self.controller_statestate=="내부":
            self.controller_statestate = "외부"
            app.whwjdrks_button.configure(text = "조정간 상태 : " + self.controller_statestate)
            self.Destroy_innerController()
            self.toplevel_window = ToplevelWindow(self)
            app.in_out = False
        else:
            self.controller_statestate = "내부"
            app.whwjdrks_button.configure(text = "조정간 상태 : " + self.controller_statestate)
            self.innerController()
            self.toplevel_window.destroy()
            app.in_out = True

    def status_screen(self):
        #app.option_button.configure(state="normal")
        app.remote_button.configure(state="normal")
        global Marker
        map_widget.canvas.unbind('<Button-1>')
        for _ in range(len(Marker)):
            Marker[0].delete()
            Marker.pop(0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.frame_middle = customtkinter.CTkFrame(master=self, fg_color="white", corner_radius=0, border_width=1, border_color="gray")
        self.frame_middle.grid(row=0, rowspan=1, column=1, columnspan=1, padx=0, pady=0, sticky="nsew")
        
        # ============ frame_middle ============
        self.frame_middle.grid_columnconfigure(1, weight=0)
        self.frame_middle.grid_rowconfigure(0, weight=1)
        
        image_boat_GPS = PhotoImage(file="./image/image_GPS.png")
        image_Battery = PhotoImage(file="./image/image_Battery.png")
        image_speed = PhotoImage(file="./image/image_speed.png")
        image_Temp = PhotoImage(file="./image/image_Temp.png")
        image_Rotation = PhotoImage(file="./image/image_Rotation.png")
        
        e_pd = 0; w_pd = 50; n_pd = 80; s_pd = 0; point = "n"
        self.button = customtkinter.CTkButton(master=self.frame_middle, text="문보트", hover=False, font=(None,25),
                                                anchor='', height=50, width=200, border_color='black', border_width=2, fg_color='white', text_color='black', corner_radius=10)
        self.button.grid(padx=(w_pd, e_pd), pady=(n_pd*0+20, s_pd), sticky=point, row=0, column=1)
        
        self.status_button(image_boat_GPS, "X 123.123", e_pd, w_pd, s_pd, n_pd*1+20, point)
        self.status_button(image_boat_GPS, "Y 123.123", e_pd, w_pd, s_pd, n_pd*2+20, point)
        self.status_button(image_Battery, "70%", e_pd, w_pd, s_pd, n_pd*3+20, point)
        self.status_button(image_speed, "10", e_pd, w_pd, s_pd, n_pd*4+20, point)
        self.status_button(image_Temp, "25", e_pd, w_pd, s_pd, n_pd*5+20, point)
        self.status_button(image_Rotation, "10, 상", e_pd, w_pd, s_pd, n_pd*6+20, point)
    
    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.focus()
            
    def status_button(self, img, txt, e, w, s, n, pos):
        self.button = customtkinter.CTkButton(master=self.frame_middle, text=txt, image=img, hover=False, font=(None,25),
                                              anchor='w', height=50, width=200, border_color='black', border_width=2, fg_color='white', text_color='black', corner_radius=10)
        self.button.grid(padx=(w, e), pady=(n, s), sticky=pos, row=0, column=1)
    
    def init_button(self, img, txt, e, w, s, n, pos, cmd):
        self.button = customtkinter.CTkButton(master=self.frame_right, text=txt, image=img, command=cmd, 
                                              height=100, width=100, fg_color='white', text_color='black' , corner_radius=0, compound='top')
        self.button.grid(padx=(w, e), pady=(n, s), sticky=pos, row=0, column=3)
        
    def GPS_button(self, txt, e, w, s, n, pos, cmd):
        self.button = customtkinter.CTkButton(master=self.frame_middle, text=txt, command=cmd, font=(None,15),
                                              height=35, width=140, border_color='black', border_width=2, fg_color='white', text_color='black', corner_radius=10)
        self.button.grid(padx=(w, e), pady=(n, s), sticky=pos, row=0, column=1)

    def Option_button(self, txt, e, w, s, n, pos, cmd):
        self.whwjdrks_button = customtkinter.CTkButton(master=self.frame_middle, text=txt, command=cmd, font=(None,15),
                                              height=60, width=280, border_color='black', border_width=2, fg_color='white', text_color='black', corner_radius=10)
        self.whwjdrks_button.grid(padx=(w, e), pady=(n, s), sticky=pos, row=0, column=1)
           
    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.marker_list.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def clear_marker_event(self):
        for marker in self.marker_list:
            marker.delete()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()

    def destroy_all(self):
        #global Marker
        print("Marker remove")
        for i in range (len(Marker)):
            Marker[0].delete()
            Marker.pop(0)
        for _ in range(len(Path)):
                Path[0].delete()
                Path.pop(0)
        for _ in range(len(map_widget.Draw_line)):
            map_widget.Draw_line.pop(0)
        #self.GPS.configure(text = '')
        #self.GPS_label.configure(text = '')

    def gpsMarker(self):
        marker_point = ''
        cnt = 1
        for i in range(len(Marker)):
            #marker_point = str(Marker[i].position)
            marker_point = marker_point + str(Marker[i].position) + '\n'
            #self.button = customtkinter.CTkButton(master=self.frame_middle, text=marker_point, hover=False, font=(None,15), height=30, width=200, border_color='black',
            #border_width=2, fg_color='white', text_color='black', corner_radius=10)
            #self.button.grid(padx=(25, 0), pady=(50 + (50 * i), 0), sticky="n", row=0, column=1)
            cnt += 1

        marker_point = marker_point.replace("(", "")
        marker_point = marker_point.replace(")", "")
        
        self.GPS_label = customtkinter.CTkLabel(master=self.frame_middle,fg_color="transparent", height=30, width=200,
                                                font=('NanumSquareOTF_acB', 17), corner_radius=30)
        self.GPS_label.grid(padx=(25, 0), pady=(100, 0), sticky="n", row=0, column=1)
        self.GPS_label.configure(text=str(marker_point))
        print(marker_point)
        #self.GPS.configure(text = marker_point)

    def check_threading():
        if result_msg.find('202'):
            status_msg = result_msg[4:]

    def stick_motion(self, event):
        x , y = event.x-5, event.y-5
        center = 150 - 15
        fun_x = x
        fun_x300 = -x+300
        E_dist=250
        F_dist=25
        print(f"x:{x}")
        print(f"y:{y}")
        
        if x >= E_dist:
            x = E_dist
        if x <= F_dist:
            x = F_dist
        if y >= E_dist:
            y = E_dist
        if y <= F_dist:
            y = F_dist
            
        if x < center:
            if y >= fun_x and y < fun_x300:
                y = center
        if x > center:
            if y >= fun_x300 and y < fun_x:
                y = center
        if y < center:
            if y <= fun_x and y < fun_x300:
                x = center
        if y > center:
            if y >= fun_x300 and y > fun_x:
                x = center    
            
        self.stick.grid(pady=(y,0), padx=(x, 0), sticky="nw", row=1, column=1)
        
    def stick_reset(self, event):
        self.stick.grid(pady=(135,0), padx=(135, 0), sticky="nw", row=1, column=1)
        

if __name__ == "__main__":
    win = login2.loginstart()
    communication.start_send()
    t = threading.Thread(target = communication.received)
    t.daemon = True
    t.start()
    app = App()
    app.mainloop()
