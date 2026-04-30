import os
from rules.RulesUser import RulesSintaxe
from config_generator import DEFAULT_CONFIG, ensure_config_yaml

Rule_data = RulesSintaxe()

config_path = os.path.join(os.path.dirname(__file__), "Deteflect.yaml")
config = ensure_config_yaml(config_path)

security_enabled = config.get("Segurança", True)
DataFlectApi = {
    "Seguranca": security_enabled,
    "Porta": config.get("Porta", 5000),
    "Proprietario": config.get("Proprietario", "Administrador"),
    "Secuty_by_pass": not security_enabled
}

Rule_data.AddIntents({"cadastrar processo": "JURI_PROCESSO"}, ("process", "JURI_PROCESSO"))

# Your data project here, all rules of your project added here
list_mercado = ["pera, maca, banana,limao"]


def Mostrar_list():
    return f" Esses são os itens que preciso comprar no mercado {list_mercado}"


def FeedBackNegativo():
    return f"Obrigado pelo feedback negativo, vamos melhorar"


def RemoverItem():
    list_mercado.remove("pera")

Rule_data.NewRule(("comprar", "produtos"), "READ", Mostrar_list)
Rule_data.NewRule(("compras", "produtos"), "READ", Mostrar_list)
Rule_data.NewRule(("compras", "produtos"), "DELETE", Mostrar_list)
Rule_data.NewRule(("consultar", "feedback"), "READ", FeedBackNegativo, "NEGATIVE")
Rule_data.NewRule(("consultar", "feedback"), "READ", FeedBackNegativo, "NEGATIVE")


