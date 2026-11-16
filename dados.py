"""Funções de dados do EduTarefas. Os registros são persistidos em JSON."""
import json
from datetime import date, datetime
from pathlib import Path
import unicodedata

ARQUIVO = Path(__file__).resolve().parent / "tarefas.json"


def normalizar(texto):
    """Padroniza texto para buscas sem diferença entre maiúsculas/acentos."""
    texto = unicodedata.normalize("NFD", str(texto))
    return "".join(c for c in texto if unicodedata.category(c) != "Mn").lower().strip()


def carregar():
    """Lê a lista JSON; cria uma lista vazia se o arquivo não existir."""
    try:
        if not ARQUIVO.exists():
            return []
        with ARQUIVO.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, list) else []
    except (OSError, json.JSONDecodeError) as erro:
        print(f"Aviso: não foi possível ler {ARQUIVO.name}: {erro}")
        return []


def salvar(tarefas):
    """Grava a lista de dicionários no arquivo JSON."""
    try:
        with ARQUIVO.open("w", encoding="utf-8") as arquivo:
            json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
        return True
    except OSError as erro:
        print(f"Erro ao salvar tarefas: {erro}")
        return False


def obter_status(tarefa):
    """Calcula o status usando a data local de hoje."""
    if tarefa.get("concluida", False):
        return "Concluída"
    prazo = date.fromisoformat(tarefa["prazo"])
    return "Vencida" if prazo < date.today() else "Pendente"


def listar():
    """Devolve tarefas com posição e status calculado."""
    resultado = []
    for indice, tarefa in enumerate(carregar()):
        item = dict(tarefa)
        item["indice"] = indice
        item["status"] = obter_status(item)
        resultado.append(item)
    return resultado


def adicionar_tarefa(titulo, prazo):
    """Valida e cadastra tarefa; cada registro recebe data/hora de criação."""
    titulo = str(titulo).strip()
    if not titulo:
        return False, "Informe o título da tarefa."
    if len(titulo) > 150:
        return False, "O título deve ter até 150 caracteres."
    try:
        data = datetime.strptime(prazo.strip(), "%d/%m/%Y").date()
        if data.strftime("%d/%m/%Y") != prazo.strip():
            raise ValueError("data inválida")
    except (ValueError, AttributeError):
        return False, "Informe um prazo válido no formato DD/MM/AAAA."
    tarefas = carregar()
    tarefas.append({"titulo": titulo, "prazo": data.isoformat(), "concluida": False,
                    "criada_em": datetime.now().astimezone().isoformat(timespec="seconds")})
    return (True, "Tarefa adicionada com sucesso.") if salvar(tarefas) else (False, "Não foi possível gravar os dados.")


def alternar_conclusao(indice):
    tarefas = carregar()
    if not isinstance(indice, int) or not 0 <= indice < len(tarefas):
        return False, "Tarefa não encontrada."
    tarefas[indice]["concluida"] = not tarefas[indice].get("concluida", False)
    tarefas[indice]["atualizada_em"] = datetime.now().astimezone().isoformat(timespec="seconds")
    return (True, "Status atualizado.") if salvar(tarefas) else (False, "Não foi possível gravar os dados.")


def remover_tarefa(indice):
    tarefas = carregar()
    if not isinstance(indice, int) or not 0 <= indice < len(tarefas):
        return False, "Tarefa não encontrada."
    tarefas.pop(indice)
    return (True, "Tarefa removida.") if salvar(tarefas) else (False, "Não foi possível gravar os dados.")


def buscar_tarefas(termo):
    termo = normalizar(termo)
    return [t for t in listar() if termo in normalizar(t["titulo"])]


def filtrar_tarefas(filtro):
    return [t for t in listar() if t["status"].casefold() == filtro.casefold()]


def estatisticas():
    tarefas = listar()
    return {"total": len(tarefas), "concluidas": sum(t["concluida"] for t in tarefas),
            "pendentes": sum(t["status"] == "Pendente" for t in tarefas),
            "vencidas": sum(t["status"] == "Vencida" for t in tarefas)}
