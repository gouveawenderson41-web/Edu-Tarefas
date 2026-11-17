import tkinter as tk
from tkinter import ttk, messagebox
from dados import (
    carregar, contar_concluidas, adicionar_tarefa, remover_tarefa,
    buscar_tarefas, indexar, alternar_conclusao, atualizar_status,
    obter_pendentes, obter_concluidas, obter_vencidas
)


class EduAgendaFacilApp:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("EduAgendaFácil - Gestão de Tarefas")
        self.raiz.geometry("900x700")
        self.raiz.minsize(760, 600)
        self.azul = "#1769aa"
        self.azul_escuro = "#104b7a"
        self.fundo = "#f3f7fc"
        self.raiz.configure(bg=self.fundo)
        self._estilo()
        self._cabecalho()
        self._formulario()
        self._lista()
        self._filtros()
        self._atualizar_lista()

    def _estilo(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"),
                        background="#dcecff", foreground=self.azul_escuro)

    def _cabecalho(self):
        frame = tk.Frame(self.raiz, bg=self.azul, pady=14)
        frame.pack(fill=tk.X)
        tk.Label(frame, text="EduAgendaFácil", font=("Arial", 22, "bold"),
                 bg=self.azul, fg="white").pack()
        tk.Label(frame, text="Organize suas tarefas e não perca nenhum prazo",
                 font=("Arial", 10), bg=self.azul, fg="#eaf4ff").pack(pady=(3, 8))
        linha = tk.Frame(frame, bg=self.azul)
        linha.pack()
        self.label_total = tk.Label(linha, text="Total: 0", bg=self.azul,
                                    fg="white", font=("Arial", 10, "bold"))
        self.label_total.pack(side=tk.LEFT, padx=12)
        self.label_concluidas = tk.Label(linha, text="Concluídas: 0", bg=self.azul,
                                         fg="white", font=("Arial", 10, "bold"))
        self.label_concluidas.pack(side=tk.LEFT, padx=12)

    def _formulario(self):
        frame = tk.LabelFrame(self.raiz, text="Adicionar nova tarefa",
                              bg=self.fundo, fg=self.azul_escuro,
                              font=("Arial", 11, "bold"), padx=12, pady=10)
        frame.pack(fill=tk.X, padx=14, pady=12)
        tk.Label(frame, text="Título:", bg=self.fundo).grid(row=0, column=0, sticky="w")
        self.entry_titulo = tk.Entry(frame, width=42, font=("Arial", 10))
        self.entry_titulo.grid(row=0, column=1, padx=8, pady=5, sticky="ew")
        tk.Label(frame, text="Prazo (DD/MM/AAAA):", bg=self.fundo).grid(row=1, column=0, sticky="w")
        self.entry_prazo = tk.Entry(frame, width=18, font=("Arial", 10))
        self.entry_prazo.grid(row=1, column=1, padx=8, pady=5, sticky="w")
        tk.Button(frame, text="Adicionar tarefa", command=self._adicionar,
                  bg=self.azul, fg="white", activebackground=self.azul_escuro,
                  relief=tk.FLAT, padx=14, pady=8).grid(row=0, column=2, rowspan=2, padx=12)
        frame.columnconfigure(1, weight=1)

    def _lista(self):
        frame = tk.LabelFrame(self.raiz, text="Minhas tarefas", bg=self.fundo,
                              fg=self.azul_escuro, font=("Arial", 11, "bold"),
                              padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=5)
        colunas = ("Título", "Prazo", "Status", "Concluída")
        self.tree = ttk.Treeview(frame, columns=colunas, show="headings")
        for c in colunas:
            self.tree.heading(c, text=c)
        self.tree.column("Título", width=420)
        self.tree.column("Prazo", width=120, anchor="center")
        self.tree.column("Status", width=140, anchor="center")
        self.tree.column("Concluída", width=100, anchor="center")
        scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _filtros(self):
        frame = tk.Frame(self.raiz, bg=self.fundo)
        frame.pack(fill=tk.X, padx=14, pady=10)
        botoes = [
            ("Todas", self._ver_todas), ("Pendentes", self._pendentes),
            ("Concluídas", self._concluidas), ("Vencidas", self._vencidas),
            ("Concluir / desfazer", self._alternar), ("Remover", self._remover)
        ]
        for texto, comando in botoes:
            tk.Button(frame, text=texto, command=comando, bg=self.azul,
                      fg="white", relief=tk.FLAT, padx=8, pady=6).pack(side=tk.LEFT, padx=3)
        busca = tk.Frame(self.raiz, bg=self.fundo)
        busca.pack(fill=tk.X, padx=18, pady=(0, 12))
        tk.Label(busca, text="Buscar:", bg=self.fundo).pack(side=tk.LEFT)
        self.entry_busca = tk.Entry(busca, font=("Arial", 10))
        self.entry_busca.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)
        self.entry_busca.bind("<Return>", lambda event: self._buscar())
        tk.Button(busca, text="Pesquisar", command=self._buscar, bg="#2d86d5",
                  fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT)
        tk.Button(busca, text="Limpar", command=self._ver_todas, bg="#718096",
                  fg="white", relief=tk.FLAT, padx=10).pack(side=tk.LEFT, padx=5)

    def _adicionar(self):
        ok, msg = adicionar_tarefa(self.entry_titulo.get(), self.entry_prazo.get())
        (messagebox.showinfo if ok else messagebox.showerror)("EduAgendaFácil", msg)
        if ok:
            self.entry_titulo.delete(0, tk.END)
            self.entry_prazo.delete(0, tk.END)
            self._ver_todas()

    def _selecionado(self):
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma tarefa.")
            return None
        return int(selecao[0])

    def _alternar(self):
        indice = self._selecionado()
        if indice is not None:
            ok, msg = alternar_conclusao(indice)
            if not ok:
                messagebox.showerror("Erro", msg)
            self._atualizar_lista()

    def _remover(self):
        indice = self._selecionado()
        if indice is not None and messagebox.askyesno("Confirmar", "Deseja remover esta tarefa?"):
            ok, msg = remover_tarefa(indice)
            (messagebox.showinfo if ok else messagebox.showerror)("EduAgendaFácil", msg)
            self._atualizar_lista()

    def _atualizar_lista(self, tarefas=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        todas = indexar(atualizar_status(carregar()))
        for t in (tarefas if tarefas is not None else todas):
            feita = t.get("concluida", False)
            self.tree.insert("", "end", iid=str(t["indice"]),
                             values=(t.get("titulo", ""), t.get("prazo", ""),
                                     "Concluída" if feita else t.get("status", ""),
                                     "Sim" if feita else "Não"))
        self.label_total.config(text=f"Total: {len(todas)}")
        self.label_concluidas.config(text=f"Concluídas: {contar_concluidas(todas)}")

    def _ver_todas(self):
        self.entry_busca.delete(0, tk.END)
        self._atualizar_lista()

    def _pendentes(self):
        t = indexar(atualizar_status(carregar()))
        self._atualizar_lista(obter_pendentes(t))

    def _concluidas(self):
        t = indexar(atualizar_status(carregar()))
        self._atualizar_lista(obter_concluidas(t))

    def _vencidas(self):
        t = indexar(atualizar_status(carregar()))
        self._atualizar_lista(obter_vencidas(t))

    def _buscar(self):
        termo = self.entry_busca.get().strip()
        if not termo:
            messagebox.showwarning("Atenção", "Digite algo para pesquisar.")
            return
        self._atualizar_lista(buscar_tarefas(termo))


if __name__ == "__main__":
    raiz = tk.Tk()
    EduAgendaFacilApp(raiz)
    raiz.mainloop()
