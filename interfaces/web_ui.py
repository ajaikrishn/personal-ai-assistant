import tkinter as tk
from tkinter import scrolledtext
from agent.agent_maneger import process_user_input  # Use the correct import

def handle_input(user_input):
    try:
        return process_user_input(user_input)
    except Exception as e:
        return f"Error: {str(e)}"

# GUI setup
root = tk.Tk()
root.title("Personal AI Assistant")
root.geometry("600x400")


entry = tk.Entry(root, width=80)
entry.pack(padx=10, pady=(0, 10), side=tk.LEFT, fill=tk.X, expand=True)

def submit():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    response = handle_input(user_input)

    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_input}\n")
    chat_window.insert(tk.END, f"Assistant: {response}\n\n")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

    entry.delete(0, tk.END)


chat_window = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD)
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


submit_button = tk.Button(root, text="Send", command=submit)
submit_button.pack(padx=10, pady=(0, 10), side=tk.RIGHT)

root.mainloop()