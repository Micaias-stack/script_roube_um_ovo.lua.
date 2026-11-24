import streamlit as st

st.set_page_config(page_title="Gerador de Script - Roube um Ovo", page_icon="🥚", layout="centered")

st.title("🥚 Painel de Controle: Roube um Ovo")
st.write("Configure as funções abaixo e copie o código pronto para usar no seu executor do Roblox.")

st.markdown("---")

# Link RAW configurado para o seu repositório no GitHub
raw_url = st.text_input(
    "Link RAW do seu script .lua no GitHub:",
    value="https://raw.githubusercontent.com/Micaias-stack/script_roube_um_ovo.lua./main/script_roube_um_ovo.lua",
    help="URL RAW gerada pelo arquivo script_roube_um_ovo.lua no seu GitHub."
)

st.markdown("### ⚙️ Opções do Auto-Farm")

col1, col2 = st.columns(2)

with col1:
    auto_farm = st.checkbox("Auto Farm Ovos", value=True)
    auto_missoes = st.checkbox("Auto Missões / Quests", value=True)
    distancia = st.slider("Distância de Coleta (Studs)", min_value=10, max_value=200, value=100, step=5)

with col2:
    auto_hatch = st.checkbox("Auto Chocar Ovos", value=False)
    ovo_selecionado = st.selectbox(
        "Tipo de Ovo para Chocar",
        ["Ovo Comum", "Ovo Raro", "Ovo Épico", "Ovo Lendário"]
    )
    auto_rebirth = st.checkbox("Auto Rebirth", value=False)

# Código Luau gerado dinamicamente
lua_script = f"""-- Script Gerado via Painel Web Streamlit
_G.AutoFarmOvos = {str(auto_farm).lower()}
_G.AutoMissoes = {str(auto_missoes).lower()}
_G.AutoChocarOvos = {str(auto_hatch).lower()}
_G.AutoRebirth = {str(auto_rebirth).lower()}
_G.DistanciaColeta = {distancia}
_G.NomeOvoParaChocar = "{ovo_selecionado}"

loadstring(game:HttpGet("{raw_url}"))()
"""

st.markdown("---")
st.markdown("### 📜 Código para Colar no Executor")
st.code(lua_script, language="lua")

st.success("Copie o bloco de código acima e cole direto no seu executor (Delta, Fluxus, etc.).")
