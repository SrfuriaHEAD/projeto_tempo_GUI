import requests
import tkinter as tk
from tkinter import messagebox

CIDADES = [
    "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador",
    "Fortaleza", "Curitiba", "Manaus", "Recife", "Porto Alegre", "Brasilia",
    "New York", "Los Angeles", "Toronto", "Mexico City", "Chicago",
    "London", "Paris", "Madrid", "Rome", "Berlin", "Lisbon", "Amsterdam",
    "Tokyo", "Beijing", "Dubai", "Bangkok", "Singapore", "Mumbai",
    "Sydney", "Melbourne", "Cairo", "Cape Town", "Lagos",
]

MUITO_FRIO = ["casaco pesado", "luvas", "gorro", "cachecol", "bota fechada", "calça grossa", "moletom por baixo"]
FRIO       = ["jaqueta", "calça jeans", "tênis fechado", "blusa de lã", "casaco leve"]
AMENO      = ["moletom", "calça jeans", "tênis", "blusa manga longa", "jaqueta leve"]
QUENTE     = ["camiseta", "bermuda ou calça leve", "tênis ou sandália", "boné", "óculos de sol"]
MUITO_QUENTE = ["camiseta regata", "shorts", "chinelo ou sandália", "boné", "óculos de sol", "protetor solar"]

def buscar_tempo(cidade):
    try:
        tempo = requests.get(
            f"https://wttr.in/{cidade}?format=j1",
            timeout=8,
            headers={"User-Agent": "curl/7.68.0"}
        )
        return int(tempo.json()["current_condition"][0]["temp_C"])
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível buscar o tempo:\n{e}")
        return None

def o_que_vestir(temp):
    if temp > 30:   return "🥵 Muito Quente", MUITO_QUENTE
    elif temp > 23: return "☀️ Quente", QUENTE
    elif temp > 15: return "🌤 Ameno", AMENO
    elif temp > 5:  return "🧥 Frio", FRIO
    else:           return "🥶 Muito Frio", MUITO_FRIO

def buscar():
    cidade = CIDADES[listbox.curselection()[0]] if listbox.curselection() else None
    if not cidade:
        messagebox.showwarning("Aviso", "Selecione uma cidade!")
        return

    temp = buscar_tempo(cidade)
    if temp is None:
        return

    clima, roupas = o_que_vestir(temp)

    label_resultado.config(text=f"{cidade}  —  {temp}°C  —  {clima}")
    lista_roupas.delete(0, tk.END)
    for roupa in roupas:
        lista_roupas.insert(tk.END, f"  • {roupa}")

janela = tk.Tk()
janela.title("Previsão do Tempo")
janela.geometry("420x520")
janela.configure(bg="#1e1e2e")
janela.resizable(False, False)

tk.Label(janela, text="🌍 Selecione a cidade", bg="#1e1e2e", fg="white", font=("Arial", 13, "bold")).pack(pady=10)

frame_lista = tk.Frame(janela, bg="#1e1e2e")
frame_lista.pack()

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, width=35, height=12,
                     bg="#313244", fg="white", selectbackground="#89b4fa",
                     font=("Arial", 11), bd=0, highlightthickness=0)
for cidade in CIDADES:
    listbox.insert(tk.END, cidade)
listbox.pack()
scrollbar.config(command=listbox.yview)

tk.Button(janela, text="Buscar", command=buscar, bg="#89b4fa", fg="#1e1e2e",
          font=("Arial", 11, "bold"), relief="flat", padx=20, pady=6).pack(pady=12)

label_resultado = tk.Label(janela, text="", bg="#1e1e2e", fg="#a6e3a1", font=("Arial", 12, "bold"))
label_resultado.pack()

tk.Label(janela, text="O que vestir:", bg="#1e1e2e", fg="#cdd6f4", font=("Arial", 11)).pack(pady=(10, 2))

lista_roupas = tk.Listbox(janela, width=35, height=8, bg="#313244", fg="#cdd6f4",
                           font=("Arial", 11), bd=0, highlightthickness=0, selectbackground="#313244")
lista_roupas.pack()

janela.mainloop()