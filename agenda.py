import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
#* Importa as bibliotecas 

#* Classe contato
class Contato:
    def __init__(self, id, nome, telefone, email):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.email = email
        
#* Classe agenda
class Agenda:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda Telefonica")
        
        self.contatos = [] #* Lista de contatos
        self.load_contatos() #* Carrega os contatos do json
        
        #* Configurar a fonte
        fonte_padrao = ("JetBrains Mono", 16)
        
        #* Configurar todos os widgets da página

        #* Informação Nome
        self.label_nome = tk.Label(root, text="Nome: ", font=fonte_padrao)
        self.label_nome.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        #* Input do nome
        self.entry_nome = tk.Entry(root, font=fonte_padrao)
        self.entry_nome.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        #* Informação telefone
        self.label_telefone = tk.Label(root, text="Telefone: ", font=fonte_padrao)
        self.label_telefone.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        # Input Telefone
        self.entry_telefone = tk.Entry(root, font=fonte_padrao)
        self.entry_telefone.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        #* Informação email
        self.label_email = tk.Label(root, text="Email: ", font=fonte_padrao)
        self.label_email.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        #* Input Email
        self.entry_email = tk.Entry(root, font=fonte_padrao)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        
        #* Botões
        #* Botão de adicionar contato
        self.botao_add = tk.Button(root, text="Adicionar Contato", font=fonte_padrao, command=self.adicionar_contato)
        self.botao_add.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        #* Botão de listar contatos
        self.botao_list = tk.Button(root, text="Listar Contatos", font=fonte_padrao, command=self.listar_contatos)
        self.botao_list.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
         #* Botão de editar
        self.botao_edit = tk.Button(root, text="Editar Contato", font=fonte_padrao, command=self.editar_contato)
        self.botao_edit.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        #* Botão de deletar
        self.botao_del = tk.Button(root, text="Excluir Contato", font=fonte_padrao, command=self.excluir_contato)
        self.botao_del.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        for i in range(6):
            root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=2)
        
    def adicionar_contato(self):
        nome = self.entry_nome.get()
        telefone = self.entry_telefone.get()
        email = self.entry_email.get()
        
        # Verificar se os campos não estão vazios
        if nome and telefone and email:
            contato_id = len(self.contatos) + 1  # Gerar um ID único para o contato
            contato = Contato(contato_id, nome, telefone, email)
            self.contatos.append(contato)
            self.save_contatos()
            messagebox.showinfo("Sucesso!", f"O contato {nome} foi adicionado com sucesso!")
            self.limpa_entradas()
        else:
            messagebox.showerror("Error!", "Todos os campos são obrigatórios.")
    
    def listar_contatos(self):
        if not self.contatos:
            messagebox.showinfo("Sem contatos", "Não existem contatos cadastrados na agenda.")
            return
    
        #* Criar uma string com as infos
        info_contatos = ""
        for i, contato in enumerate(self.contatos):
            info_contatos += f"Contato: {i + 1}\nNome: {contato.nome}\nTelefone: {contato.telefone}\nEmail: {contato.email}\n\n"
        messagebox.showinfo("Lista de contatos:", info_contatos)
        
    def editar_contato(self):
            if not self.contatos:
                messagebox.showwarning("Sem contatos", "Não há contatos para editar")
                return
            
            indice_contato = simpledialog.askinteger("Editar Contato", f"Digite o ID do contato para editar (1 a {len(self.contatos)})")
            if indice_contato and 1 <= indice_contato <= len(self.contatos):
                contato = self.contatos[indice_contato - 1]
                novo_nome = simpledialog.askstring("Editar Nome", "Digite o novo nome:", initialvalue=contato.nome)
                novo_telefone = simpledialog.askstring("Editar Telefone", "Digite o novo telefone:", initialvalue=contato.telefone)
                novo_email = simpledialog.askstring("Editar Email", "Digite o novo email:", initialvalue=contato.email)
                
                if novo_nome and novo_telefone and novo_email:
                    contato.nome = novo_nome
                    contato.telefone = novo_telefone
                    contato.email = novo_email
                    self.save_contatos()
                    messagebox.showinfo("Sucesso!", "Contato editado com sucesso.")
                else:
                    messagebox.showerror("Error!", "Todos os campos são obrigatórios.")
            else:
                messagebox.showerror("ERROR!", "ID do contato inválido.")
        
    def excluir_contato(self):
        if not self.contatos:
            messagebox.showwarning("Sem contatos", "Não há contatos para excluir")
            return
        
        indice_contato = simpledialog.askinteger("Excluir Contato", f"Digite o ID do contato para excluir (1 a {len(self.contatos)})")
        if indice_contato and 1 <= indice_contato <= len(self.contatos):
            self.contatos.pop(indice_contato - 1)
            self.save_contatos()
            messagebox.showinfo("Sucesso!", "Contato excluído com sucesso.")
        else:
            messagebox.showerror("ERROR!", "ID do contato inválido.")
            
    def limpa_entradas(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        
    def save_contatos(self):
        with open("contatos.json", "w") as f:
            json.dump([contato.__dict__ for contato in self.contatos], f)
    
    def load_contatos(self):
        if os.path.exists("contatos.json"):
            with open("contatos.json", "r") as f:
                contatos_data = json.load(f)
                self.contatos = [Contato(**data) for data in contatos_data]
                
if __name__ == "__main__":
    root = tk.Tk()
    app = Agenda(root)
    root.mainloop()
