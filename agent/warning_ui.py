import tkinter as tk

def show_warning():
    root = tk.Tk()
    root.title("CRYPTRIX SECURITY ALERT")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.attributes("-topmost", True)

    label = tk.Label(
        root, 
        text="UNAUTHORIZED ACCESS DETECTED\n\nIP ADDRESS LOGGED\nSESSION TERMINATED\nSYSTEM TRACE ACTIVE", 
        fg="red", 
        bg="black", 
        font=("Courier", 30, "bold"),
        justify="center"
    )
    label.pack(expand=True)

    def close_warning(event=None):
        root.destroy()

    # Close on Escape for testing, but in production this would be harder to bypass
    root.bind("<Escape>", close_warning)
    
    root.mainloop()

if __name__ == "__main__":
    show_warning()
