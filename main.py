import socket

import customtkinter as ctk

from homeScreen import HomeScreen
from studyScreen import StudyScreen


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title = "言葉"

        self.geometry("800x600")

        ctk.set_appearance_mode("dark")

        powerful_almighty_main_world = ctk.CTkFrame(
            self, 
        )
        powerful_almighty_main_world.pack(
            fill="both",
            expand=True
        )

        powerful_almighty_main_world.grid_rowconfigure(0, weight= 1)
        powerful_almighty_main_world.grid_columnconfigure(0, weight=1)

        self.frames = []
        self.vocab_list = []

        self.configure(fg_color= ("#2F2A26", "#2F2A26"))
        for PageClass in [StudyScreen, HomeScreen]:
            
            frame = PageClass(parent=powerful_almighty_main_world, controller= self)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(1)

    def show_frame(self, page_number):
        print(self.vocab_list)
        if page_number == 0 and len(self.vocab_list) < 1:
            return
        self.frames[page_number].tkraise()
        if page_number == 0:
            self.frames[page_number].load_quiz()



def main():
    # fuerzo el ipv4 porque mi linux se tarda si es ipv6 brp
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(*args, **kwargs):
        responses = old_getaddrinfo(*args, **kwargs)
        return [r for r in responses if r[0] == socket.AF_INET]
    socket.getaddrinfo = new_getaddrinfo

    #main 
    ctk.ThemeManager.theme["CTk"]["fg_color"] = ["#2F2A26", "#2F2A26"]

    #label 
    ctk.ThemeManager.theme["CTkLabel"]["text_color"] = ["white", "white"]
    ctk.ThemeManager.theme["CTkLabel"]["font"] = ["Segoe UI", 28, "bold"]

    #button 
    ctk.ThemeManager.theme["CTkButton"]["fg_color"] = ["#68625E", "#68625E"]
    ctk.ThemeManager.theme["CTkButton"]["hover_color"] = ["#77ABD5", "#77ABD5"]
    ctk.ThemeManager.theme["CTkButton"]["text_color"] = ["white", "white"] 
    ctk.ThemeManager.theme["CTkButton"]["corner_radius"] = 12
    ctk.ThemeManager.theme["CTkButton"]["font"] = ["Segoe UI", 10, "bold"]


    #Frame
    ctk.ThemeManager.theme["CTkFrame"]["fg_color"] = "transparent"
    ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"] = "transparent"


    #entries
    ctk.ThemeManager.theme["CTkEntry"]["border_width"] = 0
    ctk.ThemeManager.theme["CTkEntry"]["fg_color"] = "#68625E"

    app = App()

    app.mainloop()

main()