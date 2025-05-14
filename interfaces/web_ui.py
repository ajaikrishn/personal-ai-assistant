# gui.py

import customtkinter as ctk
from agent.main import handle_input


# ... inside your GUI submit function
user_input = entry.get()
response = handle_input(user_input)

class PersonalAssistantGUI:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Personal AI Assistant")
        self.app.geometry("600x500")

        # Title label
        self.title_label = ctk.CTkLabel(self.app, text="Personal AI Assistant", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=10)

        # Chat display
        self.chat_display = ctk.CTkTextbox(self.app, height=300, width=550, wrap="word", state="disabled")
        self.chat_display.pack(padx=10, pady=(0, 10))

        # Input field
        self.input_field = ctk.CTkEntry(self.app, placeholder_text="Type your message here...", width=450)
        self.input_field.pack(padx=10, pady=5, side="left", expand=False)

        # Send button
        self.send_button = ctk.CTkButton(self.app, text="Send", command=self.process_input)
        self.send_button.pack(padx=10, pady=5, side="left")

        self.app.bind("<Return>", lambda event: self.process_input())  # Enter key support

    def append_chat(self, sender, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"{sender}: {message}\n")
        self.chat_display.configure(state="disabled")
        self.chat_display.see("end")

    def process_input(self):
        user_input = self.input_field.get()
        if user_input.strip() == "":
            return

        self.append_chat("You", user_input)
        self.input_field.delete(0, "end")

        try:
            response = handle_input(user_input)
            self.append_chat("Assistant", response)
        except Exception as e:
            self.append_chat("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    gui = PersonalAssistantGUI()
    gui.run()
