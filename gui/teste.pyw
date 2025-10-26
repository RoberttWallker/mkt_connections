import tkinter as tk
from tkinter import Menu
from frame_update_access_token_facebook import abrir_update_token_frame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Data Smart ND")
        self.geometry("600x400")

        # ---------------- Barra de Menu ----------------
        menubar = Menu(self)
        ### ------------- HOME ------------
        menubar.add_command(
            label="Home",
            command=self.show_home
        )
        
        ### ------------- Menu Facebook Ads ------------
        menu_facebook = Menu(menubar, tearoff=0)
        menu_facebook.add_command(
            label="Atualizar Access Token",
            command=lambda: abrir_update_token_frame(self.content_frame)
        )
        menubar.add_cascade(label="Menu Facebook", menu=menu_facebook)


        self.config(menu=menubar)

        # ---------------- Área de menu lateral ----------------
        self.sidebar = tk.Frame(self, width=150, bg="gray")
        self.sidebar.pack(side="left", fill="y")

        # ---------------- Área de conteúdo ----------------
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(expand=True, fill="both")

        self.show_home()

    def show_home(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        label = tk.Label(self.content_frame, text="Bem-vindo ao Data Smart ND!", font=("Segoe UI", 12))
        label.pack(expand=True)

app = MainApp()
app.mainloop()