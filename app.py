"""Aplicação web Flask do EduTarefas. Execute com: python app.py"""
from flask import Flask, flash, redirect, render_template, request, url_for
from dados import adicionar_tarefa, alternar_conclusao, buscar_tarefas, estatisticas, filtrar_tarefas, listar, remover_tarefa

app = Flask(__name__)
app.secret_key = "edu-tarefas-chave-local"


def renderizar(tarefas=None, filtro="todas", termo_busca=""):
    dados = estatisticas()
    return render_template("index.html", tarefas=listar() if tarefas is None else tarefas,
                           filtro=filtro, termo_busca=termo_busca,
                           total=dados["total"], concluidas=dados["concluidas"])


@app.get("/")
def index():
    return renderizar()


@app.post("/adicionar")
def adicionar():
    sucesso, mensagem = adicionar_tarefa(request.form.get("titulo", ""), request.form.get("prazo", ""))
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(url_for("index"))


@app.post("/alternar/<int:indice>")
def alternar(indice):
    sucesso, mensagem = alternar_conclusao(indice)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(request.referrer or url_for("index"))


@app.post("/excluir/<int:indice>")
def excluir(indice):
    sucesso, mensagem = remover_tarefa(indice)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(request.referrer or url_for("index"))


@app.get("/filtro/<categoria>")
def filtro(categoria):
    mapa = {"pendentes": "Pendente", "concluidas": "Concluída", "vencidas": "Vencida"}
    if categoria not in mapa:
        return redirect(url_for("index"))
    return renderizar(filtrar_tarefas(mapa[categoria]), categoria)


@app.get("/buscar")
def buscar():
    termo = request.args.get("termo", "").strip()
    return renderizar(buscar_tarefas(termo), "busca", termo)


if __name__ == "__main__":
    # Para abrir pelo celular na mesma rede Wi-Fi, use o IP do computador e a porta 5000.
    app.run(host="0.0.0.0", port=5000, debug=False)
