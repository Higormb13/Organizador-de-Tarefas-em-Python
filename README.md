#  **Gerenciador de Tarefas em Python (CLI + JSON)**

Um gerenciador de tarefas simples, direto e funcional, rodando no
terminal e salvando tudo em **JSON**.\
Ideal para estudos de lógica, modularização, manipulação de arquivos e
boas práticas em Python.

------------------------------------------------------------------------

##  **Sobre o Projeto**

Este sistema permite criar, listar, atualizar e concluir tarefas, sempre
preservando tudo em um arquivo `tarefas.json`.\
A ideia é entregar um fluxo completo de gerenciamento com prioridade,
origem, status, arquivamento automático e relatórios.

------------------------------------------------------------------------

##  **Funcionalidades**

-   Criar tarefas com título, descrição, prioridade e origem
-   Seleção automática da tarefa mais urgente
-   Atualizar prioridade
-   Marcar como concluída
-   Arquivar tarefas antigas (7+ dias)
-   Exclusão lógica
-   Relatórios completos e de arquivados
-   Persistência total em JSON

------------------------------------------------------------------------

##  **Estrutura do JSON**

``` json
{
    "controle_id": 5,
    "tarefas": [
        {
            "id": 1,
            "titulo": "Exemplo",
            "descricao": "Minha tarefa",
            "prioridade": "Alta",
            "status": "Pendente",
            "origem": "E-mail",
            "data_criacao": "2025-11-10T14:30:05",
            "data_conclusao": null
        }
    ]
}
```

------------------------------------------------------------------------

## Como Usar

1.  Clone o repositório:

``` bash
git clone https://github.com/Higormb13/Organizador-de-Tarefas-em-Python.git
```

2.  Entre na pasta:

``` bash
cd Organizador-de-Tarefas-em-Python
```

3.  Execute:

``` bash
python tarefas.py
```


------------------------------------------------------------------------

##  **Tecnologias Usadas**

-   Python 3\
-   json\
-   datetime

------------------------------------------------------------------------

##  **Objetivo Educacional**

Dominar: - Organização lógica
- Persistência de dados
- Serialização/desserialização
- Funções e modularização
