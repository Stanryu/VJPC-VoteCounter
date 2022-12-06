import tkinter
from tkinter.messagebox import *
import tkinter as tk
from tkinter import ttk
from src.base import VoteList, ConfigList
from electionConfiguration import configElection_app

LARGEFONT = ("Verdana", 35)


#  Classe principal
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Cria os containers para cada classe
        for F in (StartPage, Configuracao, Votacao):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame['bg'] = 'white'

        self.show_frame(StartPage)

    #  função que controla a ordem dos frames
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Pagina inicial
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Define o cabeçalho
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0, padx=50)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=1, padx=50)

        # Configuração para o botão
        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 15))

        # Cria os dois botoes
        button1 = ttk.Button(self, text="Criar uma eleição", command=lambda: controller.show_frame(Configuracao), padding=22,
                             style='my.TButton')
        button1['width'] = 30
        button1.grid(row=1, column=1, pady=100)

        button2 = ttk.Button(self, text="Resultado de uma eleição", command=lambda: controller.show_frame(Votacao),
                             style='my.TButton', padding=22)
        button2['width'] = 30
        button2.grid(row=2, column=1, padx=10)


# Primeira pagina
class Configuracao(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.fontePadrao = ("Arial", "10")

        # Define o cabeçalho
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0, sticky=tk.W)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=1)

        # Aqui começa a definição dos campois
        # O label é o titulo do nome
        # O entry é a caixa em que o usuario digita
        self.nome_eleicao = ttk.Label(self)
        self.nome_eleicao["text"] = "Nome da eleição:"
        self.nome_eleicao["font"] = ("Verdana", "15")
        self.nome_eleicao["background"] = '#FFFFFF'
        self.nome_eleicao.grid(row=3, column=0, padx=20, sticky=tk.W)

        self.nome_eleicao_entry = ttk.Entry(self)
        self.nome_eleicao_entry["background"] = '#FFFFFF'
        self.nome_eleicao_entry["font"] = ("Verdana", "15")
        self.nome_eleicao_entry.grid(row=3, column=0, )

        self.descricao = ttk.Label(self)
        self.descricao["text"] = "Descrição:"
        self.descricao["font"] = ("Verdana", "15")
        self.descricao["background"] = '#FFFFFF'
        self.descricao.grid(row=4, column=0, padx=20, sticky=tk.W)

        self.descricao_entry = ttk.Entry(self)
        self.descricao_entry["background"] = '#FFFFFF'
        self.descricao_entry["font"] = ("Verdana", "15")
        self.descricao_entry.grid(row=4, column=0, )

        self.qtd = ttk.Label(self)
        self.qtd["text"] = "Número de cargos:"
        self.qtd["font"] = ("Verdana", "15")
        self.qtd["background"] = '#FFFFFF'
        self.qtd.grid(row=5, column=0, padx=20, sticky=tk.W, pady=10)

        self.qtd_entry = ttk.Entry(self)
        self.qtd_entry["background"] = '#FFFFFF'
        self.qtd_entry["font"] = ("Verdana", "15")
        self.qtd_entry.grid(row=5, column=0, padx=233)

        self.data_inicio = ttk.Label(self)
        self.data_inicio["text"] = "Data inicio:"
        self.data_inicio["font"] = ("Verdana", "15")
        self.data_inicio["background"] = '#FFFFFF'
        self.data_inicio.grid(row=6, column=0, padx=20, sticky=tk.W, pady=10)

        self.data_inicio_entry = ttk.Entry(self)
        self.data_inicio_entry["background"] = '#FFFFFF'
        self.data_inicio_entry["font"] = ("Verdana", "15")
        self.data_inicio_entry.grid(row=6, column=0, padx=233)

        self.hora_inicio = ttk.Label(self)
        self.hora_inicio["text"] = "Hora inicio:"
        self.hora_inicio["font"] = ("Verdana", "15")
        self.hora_inicio["background"] = '#FFFFFF'
        self.hora_inicio.grid(row=7, column=0, padx=20, sticky=tk.W, pady=10)

        self.hora_inicio_entry = ttk.Entry(self)
        self.hora_inicio_entry["background"] = '#FFFFFF'
        self.hora_inicio_entry["font"] = ("Verdana", "15")
        self.hora_inicio_entry.grid(row=7, column=0, padx=233)

        self.data_fim = ttk.Label(self)
        self.data_fim["text"] = "Data inicio:"
        self.data_fim["font"] = ("Verdana", "15")
        self.data_fim["background"] = '#FFFFFF'
        self.data_fim.grid(row=3, column=1, padx=20, sticky=tk.W, pady=10)

        self.data_fim_entry = ttk.Entry(self)
        self.data_fim_entry["background"] = '#FFFFFF'
        self.data_fim_entry["font"] = ("Verdana", "15")
        self.data_fim_entry.grid(row=3, column=1, padx=233)

        self.hora_fim = ttk.Label(self)
        self.hora_fim["text"] = "Hora fim:"
        self.hora_fim["font"] = ("Verdana", "15")
        self.hora_fim["background"] = '#FFFFFF'
        self.hora_fim.grid(row=4, column=1, padx=20, sticky=tk.W, pady=10)

        self.hora_fim_entry = ttk.Entry(self)
        self.hora_fim_entry["background"] = '#FFFFFF'
        self.hora_fim_entry["font"] = ("Verdana", "15")
        self.hora_fim_entry.grid(row=4, column=1, padx=233)

        self.arqivo_candidato = ttk.Label(self)
        self.arqivo_candidato["text"] = "Arquivo de candidatos:"
        self.arqivo_candidato["font"] = ("Verdana", "15")
        self.arqivo_candidato["background"] = '#FFFFFF'
        self.arqivo_candidato.grid(row=5, column=1, padx=20, sticky=tk.W, pady=10)

        self.arqivo_candidato_entry = ttk.Entry(self)
        self.arqivo_candidato_entry["background"] = '#FFFFFF'
        self.arqivo_candidato_entry["font"] = ("Verdana", "15")
        self.arqivo_candidato_entry.grid(row=5, column=1, padx=263)

        self.arqivo_eleitor = ttk.Label(self)
        self.arqivo_eleitor["text"] = "Arquivop de eleitores:"
        self.arqivo_eleitor["font"] = ("Verdana", "15")
        self.arqivo_eleitor["background"] = '#FFFFFF'
        self.arqivo_eleitor.grid(row=6, column=1, padx=20, sticky=tk.W, pady=10)

        self.arqivo_eleitor_entry = ttk.Entry(self)
        self.arqivo_eleitor_entry["background"] = '#FFFFFF'
        self.arqivo_eleitor_entry["font"] = ("Verdana", "15")
        self.arqivo_eleitor_entry.grid(row=6, column=1, padx=233)

        #
        #

        """self.class_list = ConfigList(self)
        self.class_list.grid(row=4, column=2)"""

        self.criar = ttk.Button(self, padding=20, width=30)
        self.criar["text"] = 'Confirma'
        self.criar.bind("<Button-1>", self.save_relatorio)
        self.criar.grid(row=7, column=1)

        self.button2 = ttk.Button(self, text="Retornar", command=lambda: controller.show_frame(StartPage), padding=22)
        self.button2['width'] = 30
        self.button2.grid(row=8, column=1)

        self.class_list = ConfigList(self)
        self.class_list.grid(row=8, column=0, sticky=tk.W, padx=20)

    # Função que salva o relatorio
    def save_relatorio(self, event):
        try:
            configElection_app(str(self.nome_eleicao_entry.get()), str(self.descricao_entry.get()), str(self.qtd_entry.get()),
                               str(self.data_inicio_entry.get()),str(self.hora_inicio_entry.get()),
                               str(self.data_fim_entry.get()), str(self.hora_fim_entry.get()), self.class_list.get(),
                               str(self.arqivo_candidato_entry.get()), str(self.arqivo_eleitor_entry.get()))
            showinfo("showerror", "Boleta criada com sucesso")
        except:
            #  Caso acontece algum erro plota a menssagem
            showerror("showerror", "Error")

        # Limpa todos os campos
        self.nome_eleicao_entry.delete(0, 'end')
        self.qtd_entry.delete(0, 'end')
        self.descricao_entry.delete(0, 'end')
        self.data_fim_entry.delete(0, 'end')
        self.data_inicio_entry.delete(0, 'end')
        self.hora_fim_entry.delete(0, 'end')
        self.hora_inicio_entry.delete(0, 'end')
        self.class_list.clear()
        self.arqivo_eleitor_entry.delete(0, 'end')
        self.arqivo_candidato_entry.delete(0, 'end')


# Sehunda pagina, a que mostra o resultado
class Votacao(tk.Frame):
    def __init__(self, parent, controller):
        # Define o cabeçalho
        tk.Frame.__init__(self, parent)
        self.fontePadrao = ("Arial", "10")
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0, padx=50)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=2, padx=50)

        # Importa do base a lista ja pronta
        self.class_list = VoteList(self)
        self.class_list.grid(row=2, column=2, padx=50)

        button2 = ttk.Button(self, text="Retornar", command=lambda: controller.show_frame(StartPage), padding=22)
        button2['width'] = 30
        button2.grid(row=3, column=0)


# Inicia o codigo
app = tkinterApp()
app.attributes('-fullscreen', True)
app.mainloop()
