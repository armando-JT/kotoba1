import json
import os
import urllib.request

import customtkinter as ctk
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

class VocabItem(BaseModel):
    word: str
    hiragana: str
    english: str

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # ACTUAL VARIABLES BRO
        self.counter = 0
        self.entry_text = ""
        self.controller.vocab_list = []
        
        self.entryFrame = ctk.CTkFrame(
            self,

        )
        self.entryFrame.pack(
            pady = 30,
            expand = True
        )

        self.counterLabel = ctk.CTkLabel(
            self.entryFrame,
            text="Welcome back bro i missed you, ready to pick a subject and study together?",
            
        )
        self.counterLabel.pack(side="top", pady= 5)



        self.entry = ctk.CTkEntry(
            self.entryFrame,
            placeholder_text="Topic...",
            height= 40        
        )
        self.entry.pack(
            fill= "x",
            side= "top",
            pady= 30
        )

        self.button_frame = ctk.CTkFrame(
            self.entryFrame,

        )
        self.button_frame.pack(
            side="top",
            pady = 5
        )

        self.extract_text_button = ctk.CTkButton(
            self.button_frame,
            text="Extract",
            command= self.extract_text
        )
        self.extract_text_button.pack(
            side= "left",

            padx = 5
        )

        self.submit_Button = ctk.CTkButton(
            self.button_frame,
            text="Generate",
            command= self.submit_text
        )
        self.submit_Button.pack(
            side="left",

            padx = 5
        )

        self.study_button = ctk.CTkButton(
            self.button_frame,
            text="Study",
            command= lambda page=0: self.controller.show_frame(page)
        )
        
        self.study_button.pack(
            side="left",
            padx=5
        )

        self.delete_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            command= self.reset
        )

        self.delete_button.pack(
            side= "left",
            padx= 5
        )

        self.cardsFrame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height = 400
        )
        self.cardsFrame.pack(
            fill="both",
            expand = True,
            pady= 15
        )

        self.anki_button = ctk.CTkButton(
            self.cardsFrame,
            text="+Anki",
            fg_color= "#77ABD5",
            command= self.send_to_anki
            
        )

    
    
    
    def send_to_anki(self):
        actions = []
        for item in self.controller.vocab_list:
            actions.append(
                {
                    "action": "addNote",
                    "params": {
                        "note": {
                            "deckName": "言葉",
                            "modelName": "Basic",
                            "fields": {
                                "Front": f"{item.word}<br>{item.hiragana}",
                                "Back": item.english
                            },
                            "options": {
                                "allowDuplicate": False
                            }
                        }
                    }
                }
            )

        payload = {
        "action": "multi",
        "version": 6,
        "params": {
            "actions": actions
        }
        }
        
        try:
            request_data = json.dumps(payload).encode('utf-8')
            request = urllib.request.Request('http://localhost:8765', data=request_data, headers={'Content-Type': 'application/json'})
            
            with urllib.request.urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get("error"):
                    print(f"Anki Error: {result['error']}")
                else:
                    print("Successfully added to Anki!")
        except Exception as e:
            print(f"Could not connect to Anki. Is Anki open? Error: {e}")
    
    
    
    
    def generate_cards(self):
        max_columns = 3
        self.cardsFrame.grid_columnconfigure((0, 1, 2), weight=1)
        
        for index, item in enumerate(self.controller.vocab_list):
            
            row = index // max_columns
            col = index % max_columns

            card = ctk.CTkFrame(
                self.cardsFrame,
                corner_radius=12,
                border_width = 0,
                fg_color= "#68625E"

            )

            card.grid(
                row= row,
                column = col,
                padx = 10,
                pady = 20,
                sticky = "nsew"
            )

            card_title = ctk.CTkLabel(
                card,
                text= item.word,
                font=("Segoe UI", 16, "bold")
                
            )

            card_title.pack(
                side="top",
                pady = 15
            )

            card_pronunciation = ctk.CTkLabel(
                card,
                text=item.hiragana
            )

            card_pronunciation.pack(
                side = "top",
                pady = 10
            )

            card_button = ctk.CTkButton(
                card,
                text="Show",
                border_width= 1,
                command= lambda current_item= item, label= card_title: label.configure(text= current_item.english if label.cget("text") == current_item.word else current_item.word)
            )

            card_button.pack(
                side="top",
                pady= 15,
                padx= 20
            )
        
        
        last_row = (len(self.controller.vocab_list) - 1) // max_columns + 1
        self.anki_button.grid(
            row = last_row,
            column = 1,
            pady = 10
            )
    
    def reset(self):
        self.controller.vocab_list.clear()
        self.entry.delete(0, "end")
        self.entry_text = ""
        for widget in self.cardsFrame.winfo_children():
            if widget != self.anki_button:
                widget.destroy()
            else:
                self.anki_button.grid_forget()
        
    def extract_text(self):
        self.entry_text = self.entry.get()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(
            api_key = api_key
        )

        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite", 
                contents=f"Extract key Japanese vocabulary words in their dictionary form from this text:\n\n{self.entry_text}",
                config=types.GenerateContentConfig(
                    system_instruction="Exclude particles and punctuation. Keep English translations concise (1-3 words).",
                    response_mime_type="application/json",
                    response_schema=list[VocabItem],
                    temperature=0.1, 
                ),
            )

            self.controller.vocab_list = response.parsed
        except Exception as e:
            print("get the chair bro gemini is with someone else")

            self.controller.vocab_list = [
                VocabItem(word="エラー", hiragana="えらー", english="Error (Server Busy)"),
                VocabItem(word="試す", hiragana="ためす", english="To try again"),
            ]

        self.generate_cards()

    def submit_text(self):
        self.entry_text = self.entry.get()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(
            api_key = api_key
        )

        try:
        
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=f"Generate 21 common Japanese vocabulary words related to the topic: {self.entry_text}",
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "Provide dictionary-form nouns, verbs, or adjectives. "
                        "Always write the 'hiragana' field strictly in hiragana (convert katakana readings to hiragana). "
                        "Exclude particles and punctuation. Keep English translations concise (1-3 words)."
                    ),
                    response_mime_type="application/json",
                    response_schema=list[VocabItem],
                    temperature=0.3,
                ),
            )

            self.controller.vocab_list = response.parsed
        except Exception as e:
            print("sorry bro gemini is getting pounded hard as you are reading this")
            print(e)
            self.controller.vocab_list = [
                VocabItem(word="エラー", hiragana="えらー", english="Error (Server Busy)"),
                VocabItem(word="試す", hiragana="ためす", english="To try again"),
            ]

        
        

        self.generate_cards()
    
