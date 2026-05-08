LOCAL_MODEL_PATH = "./models/bertimbau"
TRAINING_DATA = [

    # CREATE
    {
        "text": "criar cliente com nome lucas idade 21",
        "intent": "CREATE"
    },

    {
        "text": "adicionar funcionario marcos matricula 1234",
        "intent": "CREATE"
    },

    {
        "text": "inserir produto caderno cor verde",
        "intent": "CREATE"
    },

    # READ
    {
        "text": "buscar cliente lucas",
        "intent": "READ"
    },

    {
        "text": "consultar funcionario matricula 1234",
        "intent": "READ"
    },

    {
        "text": "listar produtos ativos",
        "intent": "READ"
    },

    # UPDATE
    {
        "text": "atualizar idade do cliente lucas",
        "intent": "UPDATE"
    },

    {
        "text": "editar setor do funcionario marcos",
        "intent": "UPDATE"
    },

    {
        "text": "alterar status do pedido 123",
        "intent": "UPDATE"
    },

    # DELETE
    {
        "text": "deletar cliente lucas",
        "intent": "DELETE"
    },

    {
        "text": "remover funcionario matricula 1234",
        "intent": "DELETE"
    },

    {
        "text": "apagar produto caderno",
        "intent": "DELETE"
    }
]

INTENT_MAP = {
    0: "CREATE",
    1: "READ",
    2: "UPDATE",
    3: "DELETE"
}

LABEL_TO_ID = {
    "CREATE": 0,
    "READ": 1,
    "UPDATE": 2,
    "DELETE": 3
}

# =========================================================
# FALLBACK CONFIG
# =========================================================

INTENT_FALLBACK = {

    "CREATE": [
        "criar",
        "adicionar",
        "inserir",
        "cadastrar",
        "novo"
    ],

    "READ": [
        "buscar",
        "consultar",
        "listar",
        "mostrar"
    ],

    "UPDATE": [
        "editar",
        "alterar",
        "atualizar",
        "modificar"
    ],

    "DELETE": [
        "deletar",
        "apagar",
        "remover",
        "excluir"
    ]
}