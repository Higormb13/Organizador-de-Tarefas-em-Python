import json
from datetime import datetime, timedelta
from typing import Optional

# ==========================================================
# VARIÁVEIS GLOBAIS
# ==========================================================
# Aqui eu guardo a lista de tarefas. Como todo o sistema usa isso,
# faz sentido ficar como variável global.
tarefas = []

# Esse controle_id vai garantir que cada nova tarefa tenha um ID único.
controle_id = 1

# Arquivo onde vou salvar tudo em formato JSON.
ARQUIVO_JSON = "tarefas.json"

# Listas fixas do sistema — eu uso para validação.
PRIORIDADES = ["Urgente", "Alta", "Média", "Baixa"]
STATUS_VALIDOS = ["Pendente", "Fazendo", "Concluída", "Arquivado", "Excluída"]
ORIGENS = ["E-mail", "Telefone", "Chamado do Sistema"]


# ==========================================================
# Função auxiliar para manter o padrão de prints de debug
# ==========================================================
def print_executando(nome: str):
    print(f"Executando a função {nome}")


# ==========================================================
# Funções de validação
# ==========================================================
def validar_prioridade(prio: str) -> Optional[str]:
    """
    Aqui eu comparo a prioridade digitada com as prioridades oficiais.
    Se encontrar uma igual (ignoro maiúsculas/minúsculas), retorno a versão correta.
    """
    for p in PRIORIDADES:
        if prio.strip().lower() == p.lower():
            return p
    return None

def validar_origem(orig: str) -> Optional[str]:
    """
    Mesma lógica da prioridade, mas agora para a origem da tarefa.
    """
    for o in ORIGENS:
        if orig.strip().lower() == o.lower():
            return o
    return None

def buscar_tarefa_por_id(id_busca: int) -> Optional[dict]:
    """
    Eu percorro todas as tarefas procurando pelo ID informado.
    Se achar, retorno a tarefa inteira.
    """
    for t in tarefas:
        if t.get("id") == id_busca:
            return t
    return None


# ==========================================================
# Funções para converter datas JSON <-> datetime
# ==========================================================
def serializar_data(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Tipo não serializável")

def desserializar_data(iso_str: Optional[str]) -> Optional[datetime]:
    if not iso_str:
        return None
    try:
        return datetime.fromisoformat(iso_str)
    except:
        return None


# ==========================================================
# PERSISTÊNCIA EM JSON
# ==========================================================
def salvar_json():
    """
    Aqui eu salvo todas as tarefas em um arquivo JSON, convertendo datas para strings.
    """
    print_executando("salvar_json")
    global tarefas, controle_id

    payload = {
        "controle_id": controle_id,
        "tarefas": []
    }

    # Aqui eu percorro tarefa por tarefa para converter datetimes para ISO
    for t in tarefas:
        copia = t.copy()
        if copia["data_criacao"]:
            copia["data_criacao"] = copia["data_criacao"].isoformat()
        if copia.get("data_conclusao"):
            copia["data_conclusao"] = copia["data_conclusao"].isoformat()
        payload["tarefas"].append(copia)

    try:
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        print("Dados salvos.")
    except Exception as e:
        print("Erro ao salvar:", e)


def carregar_json():
    """
    Quando inicio o sistema, eu tento carregar o JSON.
    Se não existir, sigo com lista vazia.
    """
    print_executando("carregar_json")
    global tarefas, controle_id

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            payload = json.load(f)

        controle_id = payload.get("controle_id", 1)
        tarefas = []

        for t in payload.get("tarefas", []):
            tarefa = t.copy()
            tarefa["data_criacao"] = desserializar_data(tarefa.get("data_criacao"))
            tarefa["data_conclusao"] = desserializar_data(tarefa.get("data_conclusao"))
            tarefas.append(tarefa)

    except FileNotFoundError:
        print("Nenhum arquivo encontrado — começando do zero.")
    except Exception as e:
        print("Erro ao carregar JSON:", e)


# ==========================================================
# CRIAÇÃO DE TAREFA
# ==========================================================
def criar_tarefa():
    """
    Aqui eu peço todas as infos da tarefa, valido prioridade/origem,
    e adiciono na lista global.
    """
    print_executando("criar_tarefa")
    global tarefas, controle_id

    titulo = input("Título (obrigatório): ").strip()
    if not titulo:
        print("Título é obrigatório.")
        return

    descricao = input("Descrição: ")

    print("Prioridades:", ", ".join(PRIORIDADES))
    prio = validar_prioridade(input("Prioridade: "))
    if not prio:
        print("Prioridade inválida.")
        return

    print("Origens:", ", ".join(ORIGENS))
    origem = validar_origem(input("Origem: "))
    if not origem:
        print("Origem inválida.")
        return

    tarefa = {
        "id": controle_id,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prio,
        "status": "Pendente",
        "origem": origem,
        "data_criacao": datetime.now(),
        "data_conclusao": None
    }

    tarefas.append(tarefa)
    print(f"Tarefa criada com ID {controle_id}")
    controle_id += 1


# ==========================================================
# SELEÇÃO POR URGÊNCIA
# ==========================================================
def verificar_urgencia():
    """
    Eu busco a tarefa mais prioritária que ainda está pendente,
    sempre seguindo a ordem: Urgente > Alta > Média > Baixa.
    """
    print_executando("verificar_urgencia")

    # Primeiro verifico se já tem tarefa em execução
    em_exec = [t for t in tarefas if t["status"] == "Fazendo"]
    if em_exec:
        print(f"Já existe tarefa sendo feita: ID {em_exec[0]['id']}")
        if input("Trocar tarefa em execução? (s/n): ").lower() != "s":
            return
        em_exec[0]["status"] = "Pendente"

    # Procuro a próxima pendente de maior prioridade
    selecionada = None
    for p in PRIORIDADES:
        for t in tarefas:
            if t["prioridade"] == p and t["status"] == "Pendente":
                selecionada = t
                break
        if selecionada:
            break

    if not selecionada:
        print("Nenhuma tarefa pendente encontrada.")
        return

    selecionada["status"] = "Fazendo"
    print(f"Tarefa selecionada: ID {selecionada['id']} - {selecionada['titulo']}")


# ==========================================================
# ATUALIZAÇÃO DE PRIORIDADE
# ==========================================================
def atualizar_prioridade():
    print_executando("atualizar_prioridade")

    try:
        id_tarefa = int(input("ID da tarefa: "))
    except:
        print("ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_tarefa)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    print("Prioridades:", ", ".join(PRIORIDADES))
    nova = validar_prioridade(input("Nova prioridade: "))
    if not nova:
        print("Prioridade inválida.")
        return

    tarefa["prioridade"] = nova
    print("Prioridade atualizada.")


# ==========================================================
# CONCLUSÃO DE TAREFA
# ==========================================================
def concluir_tarefa():
    print_executando("concluir_tarefa")

    try:
        id_tarefa = int(input("ID da tarefa: "))
    except:
        print("ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_tarefa)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    if tarefa["status"] == "Excluída":
        print("Não posso concluir tarefa excluída.")
        return

    tarefa["status"] = "Concluída"
    tarefa["data_conclusao"] = datetime.now()
    print("Tarefa concluída.")


# ==========================================================
# ARQUIVAMENTO AUTOMÁTICO
# ==========================================================
def arquivar_tarefas_antigas():
    print_executando("arquivar_tarefas_antigas")
    agora = datetime.now()
    count = 0

    for t in tarefas:
        if t["status"] == "Concluída" and t["data_conclusao"]:
            if agora - t["data_conclusao"] > timedelta(days=7):
                t["status"] = "Arquivado"
                count += 1

    print(f"{count} tarefa(s) arquivadas.")


# ==========================================================
# EXCLUSÃO LÓGICA
# ==========================================================
def excluir_tarefa():
    print_executando("excluir_tarefa")

    try:
        id_tarefa = int(input("ID da tarefa: "))
    except:
        print("ID inválido.")
        return

    tarefa = buscar_tarefa_por_id(id_tarefa)
    if not tarefa:
        print("Tarefa não encontrada.")
        return

    tarefa["status"] = "Excluída"
    print("Tarefa excluída logicamente.")


# ==========================================================
# RELATÓRIOS
# ==========================================================
def relatorio():
    print_executando("relatorio")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    for t in tarefas:
        print("-" * 40)
        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Prioridade: {t['prioridade']}")
        print(f"Status: {t['status']}")
        print(f"Origem: {t['origem']}")
        print(f"Criada em: {t['data_criacao']}")

        if t["data_conclusao"]:
            print(f"Concluída em: {t['data_conclusao']}")
            tempo = t["data_conclusao"] - t["data_criacao"]
            print(f"Tempo de execução: {tempo}")
        else:
            print("Concluída em: -")


def relatorio_arquivados():
    print_executando("relatorio_arquivados")

    arquivados = [t for t in tarefas if t["status"] == "Arquivado"]

    if not arquivados:
        print("Nenhuma tarefa arquivada.")
        return

    for t in arquivados:
        print("-" * 40)
        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Prioridade: {t['prioridade']}")
        print(f"Criada em: {t['data_criacao']}")
        print(f"Concluída em: {t['data_conclusao']}")


# ==========================================================
# MENU PRINCIPAL
# ==========================================================
def menu():
    print_executando("menu")
    carregar_json()  # Carrego o arquivo logo no início

    while True:
        print("""
1. Criar tarefa
2. Pegar tarefa por urgência
3. Atualizar prioridade
4. Concluir tarefa
5. Arquivar tarefas antigas
6. Excluir tarefa
7. Relatório completo
8. Relatório arquivados
9. Salvar agora
0. Sair
""")

        opc = input("Opção: ").strip()

        if not opc.isdigit():
            print("Digite um número válido.")
            continue

        opc = int(opc)

        if opc == 1: criar_tarefa()
        elif opc == 2: verificar_urgencia()
        elif opc == 3: atualizar_prioridade()
        elif opc == 4: concluir_tarefa()
        elif opc == 5: arquivar_tarefas_antigas()
        elif opc == 6: excluir_tarefa()
        elif opc == 7: relatorio()
        elif opc == 8: relatorio_arquivados()
        elif opc == 9: salvar_json()
        elif opc == 0:
            salvar_json()
            print("Saindo...")
            break
        else:
            print("Opção inválida.")


# ==========================================================
# EXECUÇÃO
# ==========================================================
if __name__ == "__main__":
    menu()
