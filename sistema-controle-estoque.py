import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import re

def add_row():
    def submit_entry():
        nome = entry_nome.get()
        quantidade = entry_quantidade.get()
        preco = entry_preco.get()
        codigo_barras = entry_codigo_barras.get()

        if not nome or not quantidade or not preco or not codigo_barras:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos", parent=top)
            return

        if len(nome) > 50 or len(quantidade) > 50 or len(preco) > 50 or len(codigo_barras) > 13:
            messagebox.showerror("Erro", "Os campos devem ter no máximo 50 caracteres", parent=top)
            return

        if not quantidade.isdigit() or int(quantidade) < 0:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo", parent=top)
            return

        if not codigo_barras.isdigit():
            messagebox.showerror("Erro", "Código de barras deve conter apenas dígitos", parent=top)
            return

        try:
            preco_num = float(preco.replace('.', '').replace(',', '.'))
            if preco_num < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número real positivo no formato correto", parent=top)
            return

        tree.insert("", "end", values=(nome, quantidade, format_price(preco_num), codigo_barras))
        save_to_json(JSON_FILE)
        top.destroy()

    def format_price(value):
        return f"R${value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    top = tk.Toplevel(root)
    top.title("Adicionar Produto")
    top.grab_set()

    tk.Label(top, text="Nome").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(top, text="Quantidade").grid(row=1, column=0, padx=10, pady=10)
    tk.Label(top, text="Preço").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(top, text="Código de Barras").grid(row=3, column=0, padx=10, pady=10)

    entry_nome = tk.Entry(top, validate="key", validatecommand=(top.register(validate_nome), "%P"))
    entry_quantidade = tk.Entry(top, validate="key", validatecommand=(top.register(validate_quantity), "%P"))
    entry_preco = tk.Entry(top, validate="key", validatecommand=(top.register(validate_price), "%P"))
    entry_codigo_barras = tk.Entry(top, validate="key", validatecommand=(top.register(validate_codigo_barras), "%P"))

    entry_nome.grid(row=0, column=1, padx=10, pady=10)
    entry_quantidade.grid(row=1, column=1, padx=10, pady=10)
    entry_preco.grid(row=2, column=1, padx=10, pady=10)
    entry_codigo_barras.grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(top, text="Adicionar Produto", command=submit_entry).grid(row=4, column=0, columnspan=2, pady=10)

    top.wait_window()

def remove_row():
    selected_items = tree.selection()
    if selected_items:
        for item in selected_items:
            tree.delete(item)
        save_to_json(JSON_FILE)
    else:
        messagebox.showwarning("Aviso", "Selecione uma ou mais linhas para remover")

def save_to_json(json_file):
    data = []
    for item in tree.get_children():
        values = tree.item(item, 'values')
        preco = values[2].replace('R$', '').replace('.', '').replace(',', '.')
        data.append({
            'Nome': values[0],
            'Quantidade': values[1],
            'Preço': preco,
            'Código de Barras': values[3]
        })
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def load_from_json(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            for item in data:
                preco = f"R${float(item['Preço']):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                tree.insert("", "end", values=(item['Nome'], item['Quantidade'], preco, item['Código de Barras']))

def validate_nome(value):
    return len(value) <= 50 or value == ""

def validate_quantity(value):
    return value.isdigit() and len(value) <= 50 or value == ""

def validate_price(value):
    return re.match(r'^\d*(,\d*)?$', value) is not None and len(value) <= 50

def validate_codigo_barras(value):
    return value.isdigit() and len(value) <= 13 or value == ""

JSON_FILE = 'dados_estoque.json'

root = tk.Tk()

root.title("Sistema de Gestão de Estoque")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tree = ttk.Treeview(frame, columns=("Nome", "Quantidade", "Preço", "Código de Barras"), show='headings', selectmode='extended')
tree.heading("Nome", text="Nome")
tree.heading("Quantidade", text="Quantidade")
tree.heading("Preço", text="Preço")
tree.heading("Código de Barras", text="Código de Barras")
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

botao_frame = ttk.Frame(frame)
botao_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

botao_adicionar = ttk.Button(botao_frame, text="Adicionar Produto", command=add_row)
botao_adicionar.pack(pady=5)

botao_remover = ttk.Button(botao_frame, text="Remover Produto", command=remove_row)
botao_remover.pack(pady=5)

load_from_json(JSON_FILE)

root.mainloop()
