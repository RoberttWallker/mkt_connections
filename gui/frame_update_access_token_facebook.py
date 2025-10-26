import tkinter as tk
from tkinter import ttk

def abrir_update_token_frame(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    frame = ttk.Frame(parent)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    ttk.Label(frame, text="Atualizar Access Token", font=("Segoe UI", 12, "bold")).pack(pady=10)
    ttk.Label(frame, text="Novo Token").pack(pady=5)

    entry_token = ttk.Entry(frame, width=40)
    entry_token.pack(pady=5)

    def salvar():
        token = entry_token.get()
        ttk.Label(frame, text=f"Token salvo: {token}", foreground="green").pack(pady=5)

    ttk.Button(frame, text="Salvar", command=salvar).pack(pady=10)