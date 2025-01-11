from utils.agent import create_clevrr_agent
from utils.prompt import prompt
from utils.contants import *

import time

import pyautogui as pg

pg.PAUSE = 2

import argparse
from tkinter import *


def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Launch the application with optional model and UI settings.")
    
    # Add arguments
    parser.add_argument('--model', type=str, default='gemini', choices=['openai', 'gemini'],
                        help="Choose the model to use. Default is 'gemini'. Options: 'openai', 'gemini'.")
    parser.add_argument('--float-ui', type=int, default=1, choices=[0, 1],
                        help="Enable or disable the float UI. Default is 1 (enabled). Pass 0 to disable.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Convert float-ui argument to boolean
    float_ui = bool(args.float_ui)

    # Print out the configurations
    print(f"Using model: {args.model}")
    print(f"Float UI is {'enabled' if float_ui else 'disabled'}")

    # Create the agent executor
    agent_executor = create_clevrr_agent(MODELS[args.model], prompt)

    # Initialize the GUI
    root = Tk()
    root.title("Clevrr Computer")
    
    # Set the window size to fill the whole screen vertically and 20% horizontally
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.3)
    window_height = screen_height - 150
    root.geometry(f"{window_width}x{window_height}")

    # Define the send function
    def send():
        # pg.hotkey("alt", "tab")
        user_input = e.get().lower()
        txt.insert(END, f"\nYou -> {user_input}")
        time.sleep(1.5)
        response = agent_executor.invoke({"input": user_input})
        txt.insert(END, f"\nBot -> {response.get('output')}")

        e.delete(0, END)
    
    # Set up the GUI components
    Label(root, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome to Clevrr Computer", font=FONT_BOLD, pady=10, width=30, height=2).grid(row=0)
    
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=40, height=30)
    txt.grid(row=1, column=0, columnspan=2)
    
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    
    e = Entry(root, bg="#FCFCFC", fg=TEXT_COLOR, font=FONT, width=30)
    e.grid(row=2, column=0)
    
    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send).grid(row=2, column=1)

    # Set window attributes and start the main loop
    root.attributes('-topmost', float_ui)
    root.mainloop()

if __name__ == "__main__":
    main()
