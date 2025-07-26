from datetime import datetime
import os
from tkinter import END, Tk, Label, Entry, Button, messagebox
from dotenv import load_dotenv
load_dotenv()
import connection

# def open_token_input_gui():
#     def on_submit():
#         token = token_entry.get()
#         if token:
#             status = connection.update_long_lived_access_token(token)
#             if status.get("status") == "OK":
#                 messagebox.showinfo(
#                     "Sucesso",  # Título da janela
#                     f"Token atualizado com sucesso no arquivo:\n\n{os.path.abspath('.env')}\n\n"
#                     f"Data/hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"  # Timestamp
#                 )
#             else:
#                 messagebox.showinfo("Erro ao atualizar o arquivo .env!")
#             root.destroy()
#         else:
#             messagebox.showwarning("Aviso", "Por favor, insira um token válido")

#     # Configuração da janela
#     root = Tk()
#     root.title("Atualizador de Token Facebook")
#     root.geometry("400x150")
    
#     # Elementos da interface
#     Label(root, text="Insira o Token Temporário do Facebook:", pady=10).pack()
    
#     token_entry = Entry(root, width=50)
#     token_entry.pack(pady=5)
    
#     submit_btn = Button(root, text="Atualizar Token", command=on_submit)
#     submit_btn.pack(pady=10)
    
#     root.mainloop()

def open_token_input_gui():
    def on_submit():
        token = token_entry.get().strip()
        if not token:
            messagebox.showwarning("Aviso", "Por favor, insira o token.")
            return
        
        try:
            result = connection.update_long_lived_access_token(token)
            status = result.get("status")
            message = result.get("message")
            
            if status == "ERRO":
                messagebox.showerror(
                    status,
                    f"Não foi possível converter o token:\n\n{message}\n\n"
                    f"Por favor:\n"
                    f"1. Verifique se o token está correto\n"
                    f"2. Obtenha um novo token temporário\n"
                    f"3. Tente novamente"
                )
                token_entry.select_range(0, END)  # Seleciona o texto para fácil substituição
                token_entry.focus_set()
            else:
                messagebox.showinfo(
                    "Conversão Bem-sucedida",
                    f"✅ Token convertido e salvo com sucesso!\n\n"
                    f"Detalhes:\n{message}"
                )
                root.destroy()  # Só fecha em caso de sucesso

        except Exception as e:
            messagebox.showerror(
                "Erro Inesperado",
                f"Ocorreu um erro não esperado:\n\n{str(e)}\n\n"
                f"Tente novamente ou reinicie o aplicativo."
            )
            token_entry.focus_set()

    # Configuração da janela (mantida igual)
    root = Tk()
    root.title("Atualizador de Token Facebook")
    root.geometry("450x200")  # Aumentado para mensagens maiores
    
    # Elementos da interface
    Label(root, text="Insira o Token Temporário do Facebook:", pady=10).pack()
    token_entry = Entry(root, width=50)
    token_entry.pack(pady=5)
    Button(root, text="Atualizar Token", command=on_submit).pack(pady=10)
    
    token_entry.focus_set()
    root.mainloop()

if __name__ == "__main__":
    from tkinter import messagebox
    try:
        open_token_input_gui()  # Sua função principal
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível iniciar: {str(e)}")
        raise