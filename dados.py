import json
import os
import unicodedata
from datetime import datetime

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tarefas.json")


def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto))
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower().strip()


def indexar(tarefas):
    for i, tarefa in enumerate(tarefas):
        tarefa["indice"] = i
    return tarefas


def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return []


def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def calcular_status_prazo(prazo):
    try:
        data_prazo = datetime.strptime(prazo, "%d/%m/%Y").date()
        return "Vencida" if data_prazo < datetime.now().date() else "No Prazo"
    except (ValueError, TypeError):
        return "Pendente"


def atualizar_status(tarefas):
    for tarefa in tarefas:
        tarefa["status"] = calcular_status_prazo(tarefa.get("prazo", ""))
    return tarefas


def contar_concluidas(tarefas):
    return sum(1 for tarefa in tarefas if tarefa.get("concluida", False))


def adicionar_tarefa(titulo, prazo):
    titulo = titulo.strip() if isinstance(titulo, str) else ""
    prazo = prazo.strip() if isinstance(prazo, str) else ""
    if not titulo:
        return False, "Informe o título da tarefa."
    if not prazo:
        return False, "Informe o prazo da tarefa."
    try:
        datetime.strptime(prazo, "%d/%m/%Y")
    except ValueError:
        return False, "Data inválida. Use DD/MM/AAAA."

    tarefas = carregar()
    tarefas.append({
        "titulo": titulo,
        "prazo": prazo,
        "concluida": False,
        "status": calcular_status_prazo(prazo),
        "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })
    salvar(tarefas)
    return True, f"Tarefa '{titulo}' adicionada com sucesso!"


def alternar_conclusao(indice):
    tarefas = carregar()
    if not isinstance(indice, int) or not 0 <= indice < len(tarefas):
        return False, "Tarefa não encontrada."
    tarefas[indice]["concluida"] = not tarefas[indice].get("concluida", False)
    salvar(tarefas)
    return True, "Status alterado com sucesso!"


def remover_tarefa(indice):
    tarefas = carregar()
    if not isinstance(indice, int) or not 0 <= indice < len(tarefas):
        return False, "Tarefa não encontrada."
    removida = tarefas.pop(indice)
    salvar(tarefas)
    return True, f"Tarefa '{removida.get('titulo', 'Tarefa')}' removida com sucesso!"


def buscar_tarefas(termo):
    tarefas = indexar(atualizar_status(carregar()))
    termo = normalizar(termo)
    if not termo:
        return tarefas
    return [t for t in tarefas if termo in normalizar(t.get("titulo", ""))]


def obter_pendentes(tarefas):
    return [t for t in tarefas if not t.get("concluida", False)]


def obter_concluidas(tarefas):
    return [t for t in tarefas if t.get("concluida", False)]


def obter_vencidas(tarefas):
    return [t for t in tarefas if t.get("status") == "Vencida" and not t.get("concluida", False)]
