import tkinter as tk


class ConfigList(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        entry_frame = tk.Frame(self, bg='White')

        cargo = tk.Label(entry_frame, text="Cargos:", bg='White')
        digito = tk.Label(entry_frame, text="Digitos:", bg='White')
        cargo["font"] = ("Verdana", "15")
        digito["font"] = ("Verdana", "15")

        # alterando para colocar uma lista de classes

        self.cargo_var = tk.StringVar(self)  # sera que é self msm?
        self.digito_var = tk.StringVar()

        cargo_entry = tk.Entry(entry_frame, textvariable=self.digito_var, validate='key')
        cargo_entry["font"] = ("Verdana", "15")
        digito_entry = tk.Entry(entry_frame, textvariable=self.cargo_var, validate='key')
        digito_entry["font"] = ("Verdana", "15")

        digito_entry.bind('<Return>', lambda e: cargo_entry.focus_set())
        cargo_entry.bind('<Return>', lambda e: self.add_item() and digito_entry.focus_set())

        cargo.grid(row=0, column=0, sticky=tk.W, pady=25)
        cargo_entry.grid(row=2, column=1)
        digito.grid(row=2, column=0, sticky=tk.W)
        digito_entry.grid(row=0, column=1)

        buttons_frame = tk.Frame(self, bg='White')

        add_button = tk.ttk.Button(buttons_frame, text="Adiciona", command=lambda: self.add_classe())
        remove_button = tk.ttk.Button(buttons_frame, text="Remove", command=lambda: self.remove_item())

        add_button.grid(row=0, column=0, pady=10, padx=10)
        remove_button.grid(row=0, column=1)

        self.listbox = tk.Listbox(self, width=20, height=6)
        self.listbox["font"] = ("Verdana", "14")

        entry_frame.grid(row=0, column=0, sticky=tk.EW)
        buttons_frame.grid(row=1, column=0, sticky=tk.EW)
        self.listbox.grid(row=2, column=0, sticky=tk.EW)

    def add_classe(self):
        classe = self.cargo_var.get()
        nivel = self.digito_var.get()
        if not nivel:
            return False

        self.listbox.insert(tk.END, f"{classe} - {nivel}")
        self.digito_var.set('')
        self.cargo_var.set('')

    def add_item(self):

        classe = self.cargo_var.get()
        nivel = self.digito_var.get()

        if not classe or not nivel:
            return False

        self.listbox.insert(tk.END, f"{classe} - {nivel}")

        self.cargo_var.set('')
        self.digito_var.set('')

        return True

    def remove_item(self):
        self.listbox.delete(tk.ANCHOR)

    def insert(self, classe, nivel):
        self.cargo_var.set(classe)
        self.digito_var.set(nivel)
        return self.add_item()

    def clear(self):
        self.listbox.delete(0, tk.END)

    def get(self):
        def split(value):
            classe, nivel = value.split('-')
            classe = classe.strip()
            nivel = (nivel.strip())

            return classe, nivel

        values = list(map(split, self.listbox.get(0, tk.END)))

        return values


class VoteList(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        entry_frame = tk.Frame(self, bg='White')

        cargo = tk.Label(entry_frame, text="Nome da eleição", bg='White')
        cargo["font"] = ("Verdana", "15")

        # alterando para colocar uma lista de classes

        self.cargo_var = tk.StringVar(self)  # sera que é self msm?

        cargo_entry = tk.Entry(entry_frame, textvariable=self.cargo_var, validate='key')
        cargo_entry["font"] = ("Verdana", "15")

        cargo_entry.bind('<Return>', lambda e: self.add_item() and cargo_entry.focus_set())

        cargo.grid(row=0, column=0, sticky=tk.W, pady=25)
        cargo_entry.grid(row=0, column=1)

        buttons_frame = tk.Frame(self, bg='White')

        add_button = tk.Button(buttons_frame, text="Pesquisa", command=lambda: self.pesquisa())
        add_button["font"] = ("Verdana", "13")

        add_button.grid(row=0, column=0, pady=10, padx=10)

        self.listbox = tk.Listbox(self, width=20, height=12)
        self.listbox["font"] = ("Verdana", "14")

        entry_frame.grid(row=0, column=0, sticky=tk.EW)
        buttons_frame.grid(row=1, column=0, sticky=tk.EW)
        self.listbox.grid(row=2, column=0, sticky=tk.EW)

    def clear(self):
        self.listbox.delete(0, tk.END)

    def add_item(self):

        classe = self.cargo_var.get()
        if not classe:
            return False

        self.listbox.insert(tk.END, f"{classe}")
        self.cargo_var.set('')

        return True

    def remove_item(self):
        self.listbox.delete(tk.ANCHOR)

    def insert(self, classe):
        self.cargo_var.set(classe)
        return self.add_item()

