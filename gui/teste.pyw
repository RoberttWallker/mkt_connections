import tkinter as tk
from tkinter import Menu
from dotenv import load_dotenv
import os
from frame_update_access_token_facebook import abrir_update_token_frame

load_dotenv()

import tkinter as tk

class CampoTextoInfo(tk.Frame):
    def __init__(self, parent, label_text, value, **kwargs):
        super().__init__(parent, **kwargs)

        # Label descritiva
        tk.Label(
            self,
            text=label_text,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill="x", padx=10, pady=(5, 0))

        # Campo de texto
        campo = tk.Text(
            self,
            height=1,
            wrap="none",
            background="white"
        )
        campo.pack(fill="x", padx=10, pady=(0, 5))
        campo.insert("1.0", value)
        campo.config(state="disabled")

        self.campo = campo  # guarda referência se precisar acessar depois


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

        # TÍTULO PÁGINA
        label = tk.Label(
            self.content_frame,
            text="Bem-vindo ao Data Smart ND!",
            font=("Segoe UI", 12),
            anchor="w",
            padx=10
            )
        label.pack(
            side="top",
            fill="x"
            )
        
        # DADOS CONEXÕES
        ## FACEBOOK ADS
        label = tk.Label(
            self.content_frame,
            text="FACEBOOK ADS",
            font=("Segoe UI", 12),
            anchor="w",
            padx=10,
            pady=10
            )
        label.pack(
            side="top",
            fill="x"
            )
        ACCESS_TOKEN = CampoTextoInfo(self.content_frame, "Access Token", os.getenv("ACCESS_TOKEN")).pack(fill="x")
        ACCOUNT_ID = CampoTextoInfo(self.content_frame, "Account ID", os.getenv("ACCOUNT_ID")).pack(fill="x")
        APP_ID = CampoTextoInfo(self.content_frame, "App ID", os.getenv("APP_ID")).pack(fill="x")
        APP_SECRET = CampoTextoInfo(self.content_frame, "App Secret", os.getenv("APP_SECRET")).pack(fill="x")
        ACCESS_TOKEN_VALIDITY = CampoTextoInfo(self.content_frame, "Access Token Validity", os.getenv("ACCESS_TOKEN_VALIDITY")).pack(fill="x")

        ## GOOGLE ADS
        
        label = tk.Label(
            self.content_frame,
            text="GOOGLE ADS",
            font=("Segoe UI", 12),
            anchor="w",
            padx=10,
            pady=10
            )
        label.pack(
            side="top",
            fill="x"
            )
        DEVELOPER_TOKEN = CampoTextoInfo(self.content_frame, "Developer Token", os.getenv("DEVELOPER_TOKEN", "")).pack(fill="x")
        CLIENT_ID = CampoTextoInfo(self.content_frame, "Client ID", os.getenv("CLIENT_ID", "")).pack(fill="x")
        CLIENT_SECRET = CampoTextoInfo(self.content_frame, "Cliente Secret", os.getenv("CLIENT_SECRET", "")).pack(fill="x")
        CUSTOMER_ID = CampoTextoInfo(self.content_frame, "Customer ID", os.getenv("CUSTOMER_ID", "")).pack(fill="x")
        LOGIN_CUSTOMER_ID = CampoTextoInfo(self.content_frame, "Login Customer ID", os.getenv("LOGIN_CUSTOMER_ID", "")).pack(fill="x")
        REFRESH_TOKEN = CampoTextoInfo(self.content_frame, "Refresh Token", os.getenv("REFRESH_TOKEN", "")).pack(fill="x")
        ACCESS_TOKEN_GOOGLE = CampoTextoInfo(self.content_frame, "Access Token Google", os.getenv("ACCESS_TOKEN_GOOGLE", "")).pack(fill="x")


app = MainApp()
app.mainloop()