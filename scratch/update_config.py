with open('memory/config_manager.py', 'r', encoding='utf-8') as f:
    text = f.read()

addition = """

def get_vrm_model() -> str:
    \"\"\"Nombre del archivo VRM activo en core/vrm/models (por defecto edithof.vrm).\"\"\"
    return str(load_api_keys().get("vrm_model", "edithof.vrm")).strip()


def save_vrm_model(model_name: str) -> None:
    _save_flag("vrm_model", str(model_name or "edithof.vrm").strip())
"""

target = 'def save_hud_style(style: str) -> None:\n    s = str(style or "").strip().lower()\n    _save_flag("hud_style", s if s in HUD_STYLES else "edith_live2d")'
if target not in text:
    target = 'def save_hud_style(style: str) -> None:\r\n    s = str(style or "").strip().lower()\r\n    _save_flag("hud_style", s if s in HUD_STYLES else "edith_live2d")'

assert target in text, 'target not found'
text = text.replace(target, target + addition)
with open('memory/config_manager.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated config_manager.py successfully!")
