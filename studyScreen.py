import customtkinter as ctk


class StudyScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.back_button = ctk.CTkButton(
            self,
            text="Home",
            command= lambda page_number=1 :self.controller.show_frame(page_number)
        )
        self.back_button.pack(
            side="top",
            pady=10
        )
        self.card_study_frame = ctk.CTkScrollableFrame(
            self,
            width=600,
            height=800
        )
        self.card_study_frame.pack(
            fill="both",
            expand=True,
            padx=10
            
        )
        self.card_study_frame.grid_columnconfigure((0,1,2), weight=1)
        
    def load_quiz(self):
        for index, item in enumerate(self.controller.vocab_list):
            row = index // 3
            col = index % 3

            card = ctk.CTkFrame(
                self.card_study_frame,
                corner_radius=12,
                border_width = 0,
                fg_color= "#68625E"

            )

            card.grid(
                row= row,
                column = col,
                padx = 10,
                pady = 10,
                sticky = "nsew"
            )

            card_title = ctk.CTkLabel(
                card,
                text=item.word,
                font=("Segoe UI", 16, "bold")
            )
            card_title.pack(
                side="top",
                pady= 15
            )

            card_entry = ctk.CTkEntry(
                card,
                height=30,
                fg_color="#d4d6d5",
                text_color="black",
                placeholder_text="Type your answer..."
            )
            card_entry.pack(
                side="top",
                pady= 5
            )


            card_check_answer = ctk.CTkLabel(
                card,
                text="",
            )
            card_check_answer.pack(
                side="top",
                pady= 5
            )

            card_button = ctk.CTkButton(
                card,
                text="Check",
                command=lambda entry_widget = card_entry, check_answer_widget = card_check_answer, correct_answer = item.english: self.check_answers(entry_widget, check_answer_widget, correct_answer),
                
                fg_color="#77ABD5"
            )
            card_button.pack(
                side="top",
                pady= (5,20)
            )    



    def check_answers(self, entry_widget, check_answer_widget, correct_answer):
        user_text = entry_widget.get().lower().strip()

        if user_text == correct_answer:
            check_answer_widget.configure(text="Correct!")
        else:
            check_answer_widget.configure(text="Wrong!")

