import os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "Segurança": True,
    "Porta": 5000,
    "Proprietario": "Administrador"
}


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    lower_value = value.lower()
    if lower_value in {"true", "false"}:
        return lower_value == "true"
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def _build_yaml_text(config: Dict[str, Any]) -> str:
    lines = []
    for key, value in config.items():
        if isinstance(value, bool):
            value_text = "true" if value else "false"
        elif isinstance(value, int) or isinstance(value, float):
            value_text = str(value)
        else:
            value_text = str(value)
            if " " in value_text or value_text == "":
                value_text = f'"{value_text}"'
        lines.append(f"{key}: {value_text}")
    return "\n".join(lines) + "\n"


def create_config_yaml(path: str = "Deteflect.yaml", config: Dict[str, Any] | None = None) -> str:
    config = config or DEFAULT_CONFIG
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    yaml_text = _build_yaml_text(config)
    with open(path, "w", encoding="utf-8") as file:
        file.write(yaml_text)
    return yaml_text


def load_config_yaml(path: str = "Deteflect.yaml") -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as file:
        config: Dict[str, Any] = {}
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            config[key.strip()] = _parse_scalar(value)
    return config


def ensure_config_yaml(path: str = "Deteflect.yaml", config: Dict[str, Any] | None = None) -> Dict[str, Any]:
    config = config or DEFAULT_CONFIG
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        create_config_yaml(path, config)
        return config
    loaded = load_config_yaml(path)
    if not loaded:
        create_config_yaml(path, config)
        return config
    return loaded
