"""Interface desktop Tkinter do EduTarefas. Execute com: python desktop.py"""
import tkinter as tk
from tkinter import ttk, messagebox
import dados


class EduTarefasApp:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("EduTarefas - Controle de prazos")
        raiz.geometry("850x600")
        raiz.minsize(650, 480)
        self.fundo = "#F7FAFF"
        raiz.configure(bg=self.fundo)
        topo = tk.Frame(raiz, bg="#155EEF", padx=18, pady=14)
        topo.pack(fill="x")
        tk.Label(topo, text="EduTarefas", font=("Arial", 20, "bold"), bg="#155EEF", fg="white").pack(anchor="w")
        self.resumo = tk.Label(topo, bg="#155EEF", fg="white", font=("Arial", 10))
        self.resumo.pack(anchor="w", pady=(4, 0))
        form = tk.LabelFrame(raiz, text="Nova tarefa", padx=12, pady=10, bg=self.fundo)
        form.pack(fill="x", padx=14, pady=12)
        tk.Label(form, text="Título:", bg=self.fundo).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.titulo = tk.Entry(form, width=42)
        self.titulo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(form, text="Prazo (DD/MM/AAAA):", bg=self.fundo).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.prazo = tk.Entry(form, width=18)
        self.prazo.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        tk.Button(form, text="Adicionar tarefa", command=self.adicionar, bg="#2563EB", fg="white").grid(row=0, column=2, rowspan=2, padx=10)
        form.columnconfigure(1, weight=1)
        area = tk.Frame(raiz, bg=self.fundo)
        area.pack(fill="both", expand=True, padx=14, pady=4)
        self.tabela = ttk.Treeview(area, columns=("titulo", "prazo", "status"), show="headings")
        for col, titulo, largura in [("titulo", "Título", 440), ("prazo", "Prazo", 120), ("status", "Status", 130)]:
            self.tabela.heading(col, text=titulo)
            self.tabela.column(col, width=largura, anchor="w")
        barra = ttk.Scrollbar(area, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=barra.set)
        self.tabela.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        controles = tk.Frame(raiz, bg=self.fundo)
        controles.pack(fill="x", padx=14, pady=10)
        for texto, comando in [("Todas", lambda: self.atualizar()), ("Pendentes", lambda: self.atualizar("Pendente")), ("Concluídas", lambda: self.atualizar("Concluída")), ("Vencidas", lambda: self.atualizar("Vencida")), ("Concluir / desfazer", self.alternar), ("Excluir", self.excluir)]:
            tk.Button(controles, text=texto, command=comando).pack(side="left", padx=3, pady=3)
        tk.Label(controles, text="Buscar:", bg=self.fundo).pack(side="left", padx=(12, 3))
        self.termo = tk.Entry(controles, width=20)
        self.termo.pack(side="left", padx=3)
        tk.Button(controles, text="Buscar", command=self.buscar).pack(side="left", padx=3)
        self.atualizar()

    def atualizar(self, filtro=None, tarefas=None):
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        todas = dados.listar()
        exibidas = tarefas if tarefas is not None else [t for t in todas if filtro is None or t["status"] == filtro]
        for t in exibidas:
            prazo = f"{t['prazo'][8:10]}/{t['prazo'][5:7]}/{t['prazo'][:4]}"
            self.tabela.insert("", "end", iid=str(t["indice"]), values=(t["titulo"], prazo, t["status"]))
        stats = dados.estatisticas()
        self.resumo.config(text=f"Tarefas: {stats['total']}    Concluídas: {stats['concluidas']}    Pendentes: {stats['pendentes']}    Vencidas: {stats['vencidas']}")

    def adicionar(self):
        ok, mensagem = dados.adicionar_tarefa(self.titulo.get(), self.prazo.get())
        (messagebox.showinfo if ok else messagebox.showerror)("EduTarefas", mensagem)
        if ok:
            self.titulo.delete(0, "end")
            self.prazo.delete(0, "end")
            self.atualizar()

    def indice_selecionado(self):
        selecao = self.tabela.selection()
        if not selecao:
            messagebox.showwarning("Atenção", "Selecione uma tarefa na lista.")
            return None
        return int(selecao[0])

    def alternar(self):
        indice = self.indice_selecionado()
        if indice is not None:
            ok, msg = dados.alternar_conclusao(indice)
            if not ok: messagebox.showerror("Erro", msg)
            self.atualizar()

    def excluir(self):
        indice = self.indice_selecionado()
        if indice is not None and messagebox.askyesno("Confirmar", "Excluir a tarefa selecionada?"):
            ok, msg = dados.remover_tarefa(indice)
            if not ok: messagebox.showerror("Erro", msg)
            self.atualizar()

    def buscar(self):
        termo = self.termo.get().strip()
        if not termo:
            messagebox.showwarning("Busca", "Digite um título para buscar.")
            return
        self.atualizar(tarefas=dados.buscar_tarefas(termo))


if __name__ == "__main__":
    janela = tk.Tk()
    EduTarefasApp(janela)
    janela.mainloop()
