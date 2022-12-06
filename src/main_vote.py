import tkinter as tk
from tkinter import ttk
from geradorVotos import vote_app
from PIL import Image
LARGEFONT = ("Verdana", 35)

# Parametos do sistema
i = 0
qtd = 2
votos = []
nome_eleicao = "Teste"
optList1 = [
    'Selecione o cargo',
    "Cargo 1",
    "Cargo 2",
    "Cargo 3"
]

# Classe principal
class tkinterApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        # Define parametros do sistema
        self.i = 1
        self.contador = 2
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Cria os containers para cada classe
        for F in (StartPage, Votacao, Confirm):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
            frame['background'] = 'white'

        self.show_frame(StartPage)

    # Controla a ordem das paginas
    def show_frame(self, cont, test=None):
        if self.contador == 4:
            vote_app(votos)
        if test and self.contador < test:
            self.contador += 1

            frame = self.frames[Votacao]
            frame.tkraise()
        else:
            frame = self.frames[cont]
            frame.tkraise()


# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0, padx=50)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=1, padx=0)

        s = ttk.Style()
        s.configure('my.TButton', font=('Helvetica', 15))

        button1 = ttk.Button(self, text="Votar", command=lambda: controller.show_frame(Votacao), padding=22,
                             style='my.TButton')
        button1['width'] = 20
        button1.grid(row=1, column=1, pady=200)


# Pagina de votos
class Votacao(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.voto = ''
        self.digito = 2
        self.fontePadrao = ("Arial", "10")

        # configura o cabeçalho
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=3)

        # Menu de opções para votação
        self.labe = tk.StringVar()
        self.labe.set(optList1[0])
        self.someStyle = ttk.Style()
        self.someStyle.configure('my.TMenubutton', font=('Futura', 20))
        self.drop = ttk.OptionMenu(self, self.labe, optList1[0], *optList1, style='my.TMenubutton')
        self.drop.configure(width=15, padding=10)
        self.drop.grid(row=2, column=0, padx=40, sticky=tk.W)

        but = ttk.Style()
        but.configure('my.TButton', font=('Verdana', 20))

        # Botes dos numeros
        self.numero1 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero1["text"] = '1'
        self.numero1.bind("<Button-1>", self.add1)
        self.numero1.grid(row=3, column=1, padx=22, pady=22)

        self.numero2 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero2["text"] = '2'
        self.numero2.bind("<Button-1>", self.add2)
        self.numero2.grid(row=3, column=2, padx=22, pady=22)

        self.numero3 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero3["text"] = '3'
        self.numero3.bind("<Button-1>", self.add3)
        self.numero3.grid(row=3, column=3, padx=22, pady=22)

        self.numero4 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero4["text"] = '4'
        self.numero4.bind("<Button-1>", self.add4)
        self.numero4.grid(row=4, column=1, padx=22, pady=22)

        self.numero5 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero5["text"] = '5'
        self.numero5.bind("<Button-1>", self.add5)
        self.numero5.grid(row=4, column=2, padx=22, pady=22)

        self.numero6 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero6["text"] = '6'
        self.numero6.bind("<Button-1>", self.add6)
        self.numero6.grid(row=4, column=3, padx=22, pady=22)

        self.numero7 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero7["text"] = '7'
        self.numero7.bind("<Button-1>", self.add7)
        self.numero7.grid(row=5, column=1, padx=22, pady=22)

        self.numero8 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero8["text"] = '8'
        self.numero8.bind("<Button-1>", self.add8)
        self.numero8.grid(row=5, column=2, padx=22, pady=22)

        self.numero9 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero9["text"] = '9'
        self.numero9.bind("<Button-1>", self.add9)
        self.numero9.grid(row=5, column=3, padx=22, pady=22)

        self.numero0 = ttk.Button(self, width=4, style='my.TButton', padding=20)
        self.numero0["text"] = '0'
        self.numero0.bind("<Button-1>", self.add0)
        self.numero0.grid(row=6, column=2, padx=22, pady=22)

        # Digitos
        self.resultado = ttk.Label(self, width=12)
        self.resultado["background"] = '#EEEEEE'
        self.resultado["font"] = ("Verdana", "25")
        self.resultado.grid(row=4, column=6, padx=122, pady=40)

        # Confirma
        self.confirmar = ttk.Button(self, width=12, style='my.TButton', padding=20,
                                    command=lambda: controller.show_frame(Page4, len(optList1)))
        self.confirmar["text"] = 'Confirma'
        self.confirmar.bind("<Button-1>", self.confirma)
        self.confirmar.grid(row=6, column=6, padx=122, pady=40)

        # Apaga
        self.apagar = ttk.Button(self, width=12, style='my.TButton', padding=20)
        self.apagar["text"] = 'Apaga'
        self.apagar.bind("<Button-1>", self.apaga)
        self.apagar.grid(row=6, column=0, sticky=tk.W, padx=20)

    # Funções que adicionam o digito
    def add1(self, event):
        self.voto += str(1)
        self.resultado['text'] = self.voto

    def add2(self, event):
        self.voto += str(2)
        self.resultado['text'] = self.voto

    def add3(self, event):
        self.voto += str(3)
        self.resultado['text'] = self.voto

    def add4(self, event):
        self.voto += str(4)
        self.resultado['text'] = self.voto

    def add5(self, event):
        self.voto += str(5)
        self.resultado['text'] = self.voto

    def add6(self, event):
        self.voto += str(6)
        self.resultado['text'] = self.voto

    def add7(self, event):
        self.voto += str(7)
        self.resultado['text'] = self.voto

    def add8(self, event):
        self.voto += str(8)
        self.resultado['text'] = self.voto

    def add9(self, event):
        self.voto += str(9)
        self.resultado['text'] = self.voto

    def add0(self, event):
        self.voto += str(0)
        self.resultado['text'] = self.voto

    # Apaga o ultimo digito
    def apaga(self, event):
        self.voto = str(self.voto)[:-1]
        self.resultado['text'] = str(self.voto)

    # Confirma o voto
    def confirma(self, event):
        votos.append(str(self.voto))
        self.resultado['text'] = ''
        self.voto = ''


# Pagina de confirmação
class Confirm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.fontePadrao = ("Arial", "10")
        # configura cabeçalho
        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Imgs/download-removebg-preview.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=0, column=0)

        self.titulo = ttk.Label(self, text="Vote")
        self.titulo["font"] = ("Arial", "50", "bold")
        self.titulo["foreground"] = '#c2393e'
        self.titulo['background'] = 'white'
        self.titulo.grid(row=0, column=2)

        self.criar = ttk.Label(self)
        self.criar["text"] = f"Nome da eleição: {nome_eleicao}"
        self.criar["font"] = ("Verdana", "15")
        self.criar["background"] = '#FFFFFF'
        self.criar.grid(row=2, column=0, padx=20, sticky=tk.W, pady=20)

        self.imagem = tk.PhotoImage(file=r"../election_data/Static/Novas Boletas/atual.png")
        self.imagem_side = ttk.Label(self, image=self.imagem)
        self.imagem_side.image = self.imagem
        self.imagem_side['background'] = 'white'
        self.imagem_side.grid(row=3, column=0)

        # Digitos
        self.resultado = ttk.Button(self, width=12, padding=22, style='my.TButton')
        self.resultado["text"] = 'Reinicia'
        self.resultado.grid(row=3, column=3, padx=40)

        # Confirma
        self.resultado = ttk.Button(self, width=12, padding=22, style='my.TButton')
        self.resultado["text"] = 'Confirma'
        self.resultado.grid(row=3, column=2, padx=40)

        img = Image.open(r"../election_data/Static/Novas Boletas/atual.png")
        width = 500
        height = 500
        img_resized = img.resize((width, height))
        img_resized.save(r"../election_data/Static/Novas Boletas/atual.png")


# Inicia o codigo
app = tkinterApp()
app.attributes('-fullscreen', True)
app.mainloop()


