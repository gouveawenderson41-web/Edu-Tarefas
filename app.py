from flask import Flask, render_template, request, redirect, url_for, flash
from dados import (
    carregar, contar_concluidas, adicionar_tarefa, remover_tarefa,
    buscar_tarefas, indexar, alternar_conclusao, atualizar_status,
    obter_pendentes, obter_concluidas, obter_vencidas
)

app = Flask(__name__)
app.secret_key = "eduagendafacil_local_2026"


def preparar_tela(tarefas, filtro="todos", termo_busca=""):
    todas = indexar(atualizar_status(carregar()))
    return render_template(
        "index.html", tarefas=tarefas, total=len(todas),
        concluidas=contar_concluidas(todas), pendentes=len(obter_pendentes(todas)),
        vencidas=len(obter_vencidas(todas)), filtro=filtro, termo_busca=termo_busca
    )


@app.route("/")
def index():
    return preparar_tela(indexar(atualizar_status(carregar())))


@app.route("/adicionar", methods=["POST"])
def adicionar():
    sucesso, mensagem = adicionar_tarefa(
        request.form.get("titulo", ""), request.form.get("prazo", "")
    )
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(url_for("index"))


@app.route("/alternar/<int:indice>", methods=["POST"])
def alternar(indice):
    sucesso, mensagem = alternar_conclusao(indice)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(request.referrer or url_for("index"))


@app.route("/excluir/<int:indice>", methods=["POST"])
def excluir(indice):
    sucesso, mensagem = remover_tarefa(indice)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(request.referrer or url_for("index"))


@app.route("/pendentes")
def filtro_pendentes():
    tarefas = indexar(atualizar_status(carregar()))
    return preparar_tela(obter_pendentes(tarefas), "pendentes")


@app.route("/concluidas")
def filtro_concluidas():
    tarefas = indexar(atualizar_status(carregar()))
    return preparar_tela(obter_concluidas(tarefas), "concluidas")


@app.route("/vencidas")
def filtro_vencidas():
    tarefas = indexar(atualizar_status(carregar()))
    return preparar_tela(obter_vencidas(tarefas), "vencidas")


@app.route("/buscar")
def buscar():
    termo = request.args.get("termo", "").strip()
    if not termo:
        return redirect(url_for("index"))
    return preparar_tela(buscar_tarefas(termo), "busca", termo)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
