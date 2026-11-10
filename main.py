import socket


from textwrap import fill
import tkinter as tk
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai



def main():
    # FORCE IPv4 ONLY (Prevents the 3-minute network hang)
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(*args, **kwargs):
        responses = old_getaddrinfo(*args, **kwargs)
        return [r for r in responses if r[0] == socket.AF_INET]
    socket.getaddrinfo = new_getaddrinfo

    rootWindow = tk.Tk()
    api_key = os.getenv("GEMINI_API_KEY")

    rootWindow.title("言葉")
    rootWindow.geometry("800x600")

    client = genai.Client(
        api_key=api_key
        )

    # Input Field (Entry)
    entry_field = tk.Entry(rootWindow, width=25)
    entry_field.grid(row=0, column=1, padx=10, pady=10)

    def read_input():
        
        subject = entry_field.get()
        
        words = []
        words_back = []
        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"Write 10 words that relate to {subject}. For example: Road, Car, Traffic, Highway, Street, Sign, Lane, Intersection, Pedestrian, Vehicle. Do not include any other text or punctuation. Only return the words in a list format."
            )
            print(f"Response: {response.text}")
            words = response.text.split()

            response2 = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"{response.text} write these words but in japanese. For example: 道路, 車, 交通, 自動車, 街道, サイン, レーン, 交差点, 歩行者, 車両. Do not include any other text or punctuation. Only return the words in a list format."
            )
            print(f"Response2: {response2.text}")
            words_back = response2.text.split()

            
        except Exception as e:
            words = ["Car", "Road", "Traffic", "Highway", "Street", "Sign", "Lane", "Intersection", "Pedestrian", "Vehicle"]
            words_back = ["道路", "車", "交通", "自動車", "街道", "サイン", "レーン", "交差点", "歩行者", "車両"]
            print(f"Error generating content: {e}")
            

        

        generate_cards(words, words_back) 
    
    btn = tk.Button(rootWindow, text="Check Value", command=read_input)
    btn.grid(row=1, column=1)


    
    
    card_frame = tk.Frame(rootWindow)
    card_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def generate_cards(words, words_back):
        for widget in card_frame.winfo_children():
            widget.destroy()  

        max_columns = 3

        for index, word in enumerate(words):
            row = index // max_columns
            column = index % max_columns
            card = tk.Frame(
                card_frame, 
                width=400, 
                height=200, 
                bg="lightblue", 
                relief="raised", 
                borderwidth=2
                )

            card.grid(row= row, column=column, padx=10, pady=10)

            word_label = tk.Label(card, text=word, font=("Arial", 16), bg="lightblue")
            word_label.pack(anchor="w", pady=(5,10))

            def on_card_click(target_label, current_index):
                target_label.config(text=words_back[current_index])

            action_btn = tk.Button(
                card,
                text="Click Me",
                command=lambda lbl=word_label, idx=index: on_card_click(lbl, idx),
                bg="black",
                fg="white"
                
            )
            action_btn.pack(fill="x")

    

    rootWindow.mainloop()

main()