import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import urllib.parse
import streamlit.components.v1 as components
from datetime import datetime
import requests
import hmac

# ── CONFIG ────────────────────────────────────────────────────────────────────
SHEET_ID = "1ZSr8xN17_e7X0DiSyJaTcwOA-eETx66--ZBUjBsjUDs"
URL_CADASTRO  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote('Cadastro')}"
URL_HISTORICO = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote('Histórico MSG')}"

# ── EVOLUTION API ─────────────────────────────────────────────────────────────
EVOLUTION_URL      = "https://n8n-evolution-api.yypjz6.easypanel.host"
EVOLUTION_API_KEY  = "SUA_NOVA_API_KEY_AQUI"
EVOLUTION_INSTANCE = "teste n8n"

def send_whatsapp(remote_jid: str, text: str) -> dict:
    number = remote_jid.replace("@s.whatsapp.net", "").replace("@c.us", "").strip()
    url = f"{EVOLUTION_URL}/message/sendText/{urllib.parse.quote(EVOLUTION_INSTANCE)}"
    headers = {"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"}
    payload = {"number": number, "text": text}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return {"ok": r.status_code in (200, 201), "status": r.status_code, "body": r.json()}
    except Exception as e:
        return {"ok": False, "status": 0, "body": str(e)}

def _favicon():
    from PIL import Image, ImageDraw, ImageFont
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    def rr(d, xy, r, fill):
        x0,y0,x1,y1 = xy
        d.rectangle([x0+r,y0,x1-r,y1],fill=fill); d.rectangle([x0,y0+r,x1,y1-r],fill=fill)
        d.ellipse([x0,y0,x0+2*r,y0+2*r],fill=fill); d.ellipse([x1-2*r,y0,x1,y0+2*r],fill=fill)
        d.ellipse([x0,y1-2*r,x0+2*r,y1],fill=fill); d.ellipse([x1-2*r,y1-2*r,x1,y1],fill=fill)
    rr(draw, (0,0,63,63), 14, (107,200,149,255))
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), "H", font=font)
    w,h = bbox[2]-bbox[0], bbox[3]-bbox[1]
    draw.text(((size-w)//2 - bbox[0], (size-h)//2 - bbox[1] - 2), "H", fill=(10,12,16,255), font=font)
    return img


# ── LOGIN ─────────────────────────────────────────────────────────────────────
def _check_password():

    def _login_form():
        st.set_page_config(
            page_title="HUIT AI — Login",
            layout="centered",
            page_icon=_favicon(),
            initial_sidebar_state="collapsed"
        )
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Outfit:wght@400;500;600&display=swap');
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
        html, body, [data-testid="stAppViewContainer"], .main {
            background-color: #0a0c10 !important;
            font-family: 'Outfit', sans-serif !important;
            color: #f1f5f9 !important;
        }
        [data-testid="stHeader"]  { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        section.main > div { padding-top: 0 !important; }

        [data-testid="stTextInput"] input {
            background: #151b24 !important;
            border: 1px solid rgba(148,163,184,0.12) !important;
            border-radius: 10px !important;
            color: #f1f5f9 !important;
            font-family: 'Outfit', sans-serif !important;
            font-size: 14px !important;
            padding: 10px 14px !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: rgba(107,200,149,0.4) !important;
            box-shadow: 0 0 0 3px rgba(107,200,149,0.08) !important;
        }
        [data-testid="stTextInput"] label { display: none !important; }

        .stButton > button {
            background: linear-gradient(135deg, #6bc895, #4aab77) !important;
            border: none !important;
            border-radius: 12px !important;
            color: #0a0c10 !important;
            font-weight: 800 !important;
            font-size: 13px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            width: 100% !important;
            height: 46px !important;
            letter-spacing: 0.3px !important;
            transition: opacity 0.15s ease !important;
            margin-top: 4px !important;
        }
        .stButton > button:hover { opacity: 0.88 !important; }

        @keyframes pulse-lime {
            0%, 100% { box-shadow: 0 0 0 0 rgba(107,200,149,0.4); }
            50%       { box-shadow: 0 0 0 5px rgba(107,200,149,0); }
        }
        </style>
        """, unsafe_allow_html=True)

        _, col, _ = st.columns([1, 1.6, 1])
        with col:
            st.markdown("""
            <div style="min-height:100vh;display:flex;align-items:center;
                        justify-content:center;padding:60px 0 40px;">
            <div style="width:100%;">
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:36px;">
                    <div style="width:44px;height:44px;border-radius:12px;background:#6bc895;
                                display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                                  stroke="#0a0c10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div>
                        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;
                                    font-size:18px;color:#f1f5f9;letter-spacing:-0.3px;">HUIT AI</div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
                                    color:#6bc895;letter-spacing:1.5px;">AGENT PANEL</div>
                    </div>
                </div>
                <div style="margin-bottom:28px;">
                    <h2 style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;
                               font-weight:800;color:#f1f5f9;letter-spacing:-0.5px;margin-bottom:6px;">
                        Bem-vindo de volta
                    </h2>
                    <p style="font-family:'Outfit',sans-serif;font-size:13px;color:#475569;">
                        Digite a senha para acessar o painel.
                    </p>
                </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

            st.text_input(
                "Senha", type="password", key="_login_pwd",
                placeholder="••••••••••••",
                on_change=_submit_password
            )

            if st.session_state.get("_login_error"):
                st.markdown("""
                <div style="background:rgba(255,107,107,0.08);border:1px solid rgba(255,107,107,0.2);
                            border-radius:10px;padding:10px 14px;margin:8px 0 12px;
                            font-family:'Outfit',sans-serif;font-size:12px;color:#ff6b6b;">
                    ✗ Senha incorreta. Tente novamente.
                </div>
                """, unsafe_allow_html=True)

            st.button("Entrar no Painel →", on_click=_submit_password)

            st.markdown("""
            <div style="margin-top:24px;text-align:center;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:9px;
                             color:#334155;letter-spacing:1px;">ACESSO RESTRITO · HUIT AI</span>
            </div>
            """, unsafe_allow_html=True)

    def _submit_password():
        pwd     = st.session_state.get("_login_pwd", "")
        correct = st.secrets.get("APP_PASSWORD", "")
        if hmac.compare_digest(pwd, correct):
            st.session_state["_authenticated"] = True
            st.session_state["_login_error"]   = False
        else:
            st.session_state["_authenticated"] = False
            st.session_state["_login_error"]   = True

    if st.session_state.get("_authenticated"):
        return True

    _login_form()
    st.stop()
    return False


if not _check_password():
    st.stop()


# ── APP (tudo igual ao original a partir daqui) ───────────────────────────────

st.set_page_config(page_title="HUIT AI", layout="wide", page_icon=_favicon(), initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body {
    background-color: #0a0c10 !important;
    font-family: 'Outfit', sans-serif !important;
    color: #f1f5f9 !important;
}
[data-testid="stAppViewContainer"], .main, section.main {
    background-color: #0a0c10 !important;
}
[data-testid="stHeader"] {
    background: rgba(10,12,16,0.9) !important;
    border-bottom: 1px solid rgba(148,163,184,0.06) !important;
    height: 0px !important;
}
[data-testid="stSidebar"] {
    background-color: #0f1318 !important;
    border-right: 1px solid rgba(148,163,184,0.06) !important;
    width: 260px !important;
}
[data-testid="stSidebarContent"] {
    background-color: #0f1318 !important;
    padding: 0 !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    background: transparent !important;
    border-bottom: 1px solid rgba(148,163,184,0.1) !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    height: 44px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: #64748b !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    padding: 0 22px !important;
    transition: all 0.15s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #e2e8f0 !important;
    background: rgba(255,255,255,0.02) !important;
}
.stTabs [aria-selected="true"],
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #6bc895 !important;
    border-bottom-color: #6bc895 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 28px !important; }
[data-testid="stTabContent"] { padding: 0 !important; }

/* METRICS */
div[data-testid="stMetric"] {
    background: #0f1318 !important;
    border: 1px solid rgba(148,163,184,0.07) !important;
    border-radius: 14px !important;
    padding: 24px !important;
    transition: all 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="stMetric"]:hover {
    border-color: rgba(107,200,149,0.2) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #6bc895, transparent);
    opacity: 0.6;
}
[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    font-weight: 700 !important;
    color: #94a3b8 !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
[data-testid="stMetricValue"] {
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -1.5px !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] > div {
    background: #0f1318 !important;
    border: 1px solid rgba(148,163,184,0.07) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* SELECTBOX geral */
[data-testid="stSelectbox"] > div > div {
    background: #151b24 !important;
    border: 1px solid rgba(148,163,184,0.11) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* LEAD CARD — wrapper com botão sobreposto */
.card-btn-wrap { position: relative; margin-bottom: 6px; }
.card-btn-wrap div[data-testid="stButton"] {
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    right: 0 !important; bottom: 0 !important;
    margin: 0 !important; padding: 0 !important;
    height: 100% !important;
    z-index: 10 !important;
}
.card-btn-wrap div[data-testid="stButton"] button {
    width: 100% !important; height: 100% !important;
    background: transparent !important;
    border: none !important; color: transparent !important;
    font-size: 0 !important; box-shadow: none !important;
    cursor: pointer !important; border-radius: 12px !important;
    padding: 0 !important; min-height: unset !important;
}
.card-btn-wrap div[data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.04) !important;
    border: none !important; box-shadow: none !important;
}
.card-btn-wrap div[data-testid="stButton"] button:focus {
    outline: none !important; box-shadow: none !important;
    border: none !important;
}

/* BUTTONS */
.stButton > button {
    background: #151b24 !important;
    border: 1px solid rgba(148,163,184,0.11) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.4px !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background: #1a2130 !important;
    border-color: rgba(107,200,149,0.3) !important;
    color: #6bc895 !important;
}
.sync-btn > button {
    background: rgba(107,200,149,0.08) !important;
    border: 1px solid rgba(107,200,149,0.2) !important;
    color: #6bc895 !important;
    width: 100% !important;
}
.sync-btn > button:hover { background: rgba(107,200,149,0.15) !important; }

/* SEND BUTTON */
.send-btn > div > button {
    background: linear-gradient(135deg, #6bc895, #4aab77) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #0a0c10 !important;
    font-weight: 800 !important;
    font-size: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: 0.3px !important;
    height: 42px !important;
    transition: all 0.15s ease !important;
}
.send-btn > div > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(148,163,184,0.12); border-radius: 99px; }

@keyframes pulse-lime {
    0%, 100% { box-shadow: 0 0 0 0 rgba(107,200,149,0.4); }
    50%       { box-shadow: 0 0 0 5px rgba(107,200,149,0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
.shimmer {
    background: linear-gradient(90deg, transparent, rgba(107,200,149,0.12), transparent);
    background-size: 200%;
    animation: shimmer 1.8s infinite;
}
</style>
""", unsafe_allow_html=True)


# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip().lower() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df_leads = load_data(URL_CADASTRO)
df_msgs  = load_data(URL_HISTORICO)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:28px 24px 18px;">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
            <div style="width:38px;height:38px;border-radius:10px;background:#6bc895;
                        display:flex;align-items:center;justify-content:center;flex-shrink:0;">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                          stroke="#0a0c10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </div>
            <div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-weight:800;font-size:16px;
                            color:#f1f5f9;letter-spacing:-0.3px;">HUIT AI</div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
                            color:#6bc895;letter-spacing:1.5px;margin-top:1px;">AGENT PANEL</div>
            </div>
        </div>
        <div style="display:inline-flex;align-items:center;gap:7px;
                    background:rgba(107,200,149,0.08);border:1px solid rgba(107,200,149,0.2);
                    border-radius:8px;padding:6px 12px;">
            <div style="width:7px;height:7px;border-radius:50%;background:#6bc895;
                        animation:pulse-lime 2s infinite;flex-shrink:0;"></div>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;
                         font-weight:500;color:#6bc895;letter-spacing:1px;">ONLINE</span>
        </div>
    </div>
    <div style="height:1px;background:rgba(148,163,184,0.06);margin:0 24px 20px;"></div>
    """, unsafe_allow_html=True)

    total_leads = len(df_leads) if not df_leads.empty else 0
    total_bot = 0
    if not df_msgs.empty and 'message_from' in df_msgs.columns:
        total_bot = len(df_msgs[df_msgs['message_from'].str.lower() == 'agent'])

    st.markdown(f"""
    <div style="padding:0 24px 20px;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:9px;font-weight:700;
                    color:#64748b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;">
            Visão Geral
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            <div style="background:#151b24;border:1px solid rgba(148,163,184,0.07);
                        border-radius:10px;padding:14px 12px;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#64748b;
                            letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px;">Leads</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;
                            color:#f1f5f9;letter-spacing:-1px;line-height:1;">{total_leads}</div>
            </div>
            <div style="background:#151b24;border:1px solid rgba(148,163,184,0.07);
                        border-radius:10px;padding:14px 12px;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#64748b;
                            letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px;">Msg IA</div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;
                            color:#f1f5f9;letter-spacing:-1px;line-height:1;">{total_bot}</div>
            </div>
        </div>
    </div>
    <div style="height:1px;background:rgba(148,163,184,0.06);margin:0 24px 20px;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sync-btn">', unsafe_allow_html=True)
    if st.button("↻  Sincronizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Botão de Sair ──────────────────────────────────────────────────────────
    st.markdown('<div style="padding: 0 24px 8px;">', unsafe_allow_html=True)
    if st.button("⎋  Sair", use_container_width=True):
        st.session_state["_authenticated"] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    now = datetime.now().strftime("%d/%m  %H:%M")
    st.markdown(f"""
    <div style="padding:14px 24px 28px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-family:'JetBrains Mono',monospace;font-size:9px;
                         color:#64748b;letter-spacing:0.5px;">ULTIMA SYNC</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#475569;">{now}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── LOADING STATE ─────────────────────────────────────────────────────────────
if df_leads.empty:
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;
                justify-content:center;height:70vh;gap:20px;">
        <div style="width:64px;height:64px;border-radius:16px;background:#6bc895;
                    display:flex;align-items:center;justify-content:center;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                      stroke="#0a0c10" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </div>
        <div>
            <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;
                        color:#f1f5f9;text-align:center;">Conectando</div>
            <div style="font-family:'Outfit',sans-serif;font-size:13px;color:#475569;
                        text-align:center;margin-top:6px;">Verificando Google Sheets...</div>
        </div>
        <div style="width:220px;height:2px;background:#151b24;border-radius:2px;overflow:hidden;">
            <div class="shimmer" style="height:100%;width:100%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:4px 0 28px;">
    <div style="display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;">
        <h1 style="font-family:'Plus Jakarta Sans',sans-serif;font-size:26px;font-weight:800;
                   color:#f1f5f9;letter-spacing:-1px;margin:0;">Painel de Controle</h1>
        <span style="font-family:'JetBrains Mono',monospace;font-size:9px;
                     color:#64748b;letter-spacing:1px;">MONITORAMENTO EM TEMPO REAL</span>
    </div>
    <p style="font-family:'Outfit',sans-serif;font-size:13px;color:#475569;margin:6px 0 0;">
        Leads, conversas e performance do agente de inteligência artificial.
    </p>
</div>
""", unsafe_allow_html=True)

tab_dash, tab_leads, tab_chat, tab_kanban, tab_conv = st.tabs(["Dashboard", "Base de Leads", "Chat", "Pipeline", "Conversões"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab_dash:

    total_bot_msgs = 0
    total_human_msgs = 0
    total_lead_msgs  = 0
    if 'message_from' in df_msgs.columns:
        total_bot_msgs   = len(df_msgs[df_msgs['message_from'].str.lower() == 'agent'])
        total_human_msgs = len(df_msgs[df_msgs['message_from'].str.lower() == 'human_agent'])
        total_lead_msgs  = len(df_msgs[df_msgs['message_from'].str.lower() == 'lead'])

    total_leads = len(df_leads)

    dfu_col_dash = next(
        (c for c in df_leads.columns
         if df_leads[c].dropna().astype(str).str.strip().str.upper()
            .isin({'RECUSA_EXPLICITA','JA_FECHOU','CONVERSA_ENCERRADA','INTERESSE_FRACO',
                   'CONVERSA_ATIVA','INTERESSE_FORTE_SEM_RESPOSTA',
                   'NEGOCIACAO_INTERROMPIDA','PROPOSTA_ENVIADA_SEM_RETORNO'}).any()),
        None
    )
    leads_quentes = 0
    if dfu_col_dash:
        leads_quentes = len(df_leads[df_leads[dfu_col_dash].astype(str).str.strip().str.upper()
                            .isin({'INTERESSE_FORTE_SEM_RESPOSTA','NEGOCIACAO_INTERROMPIDA',
                                   'PROPOSTA_ENVIADA_SEM_RETORNO'})])

    aguardando = len(df_leads[df_leads['status'].astype(str).str.upper() == 'AGUARDANDO_LEAD']) if 'status' in df_leads.columns else 0

    tel_to_nome_dash = {}
    if 'telefone do lead' in df_leads.columns and 'nome do lead' in df_leads.columns:
        tel_to_nome_dash = dict(zip(df_leads['telefone do lead'].astype(str), df_leads['nome do lead']))

    kpi_html = f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px;">

  <div style="background:linear-gradient(135deg,#0f1318 60%,rgba(107,200,149,0.04));
              border:1px solid rgba(107,200,149,0.15);border-radius:16px;padding:20px 22px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-18px;right:-18px;width:72px;height:72px;
                border-radius:50%;background:rgba(107,200,149,0.06);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#475569;
                letter-spacing:1.4px;text-transform:uppercase;margin-bottom:10px;">Total de Leads</div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:32px;font-weight:800;
                color:#f1f5f9;line-height:1;">{total_leads}</div>
    <div style="margin-top:8px;font-family:'Outfit',sans-serif;font-size:11px;color:#6bc895;">
      ● Cadastros ativos
    </div>
  </div>

  <div style="background:linear-gradient(135deg,#0f1318 60%,rgba(251,191,36,0.04));
              border:1px solid rgba(251,191,36,0.15);border-radius:16px;padding:20px 22px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-18px;right:-18px;width:72px;height:72px;
                border-radius:50%;background:rgba(251,191,36,0.06);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#475569;
                letter-spacing:1.4px;text-transform:uppercase;margin-bottom:10px;">Aguardando Lead</div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:32px;font-weight:800;
                color:#f1f5f9;line-height:1;">{aguardando}</div>
    <div style="margin-top:8px;font-family:'Outfit',sans-serif;font-size:11px;color:#fbbf24;">
      ● Bot aguardando resposta
    </div>
  </div>

  <div style="background:linear-gradient(135deg,#0f1318 60%,rgba(251,113,133,0.04));
              border:1px solid rgba(251,113,133,0.15);border-radius:16px;padding:20px 22px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-18px;right:-18px;width:72px;height:72px;
                border-radius:50%;background:rgba(251,113,133,0.06);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#475569;
                letter-spacing:1.4px;text-transform:uppercase;margin-bottom:10px;">Leads Quentes</div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:32px;font-weight:800;
                color:#f1f5f9;line-height:1;">{leads_quentes}</div>
    <div style="margin-top:8px;font-family:'Outfit',sans-serif;font-size:11px;color:#fb7185;">
      ● Requerem atenção
    </div>
  </div>

  <div style="background:linear-gradient(135deg,#0f1318 60%,rgba(56,189,248,0.04));
              border:1px solid rgba(56,189,248,0.15);border-radius:16px;padding:20px 22px;position:relative;overflow:hidden;">
    <div style="position:absolute;top:-18px;right:-18px;width:72px;height:72px;
                border-radius:50%;background:rgba(56,189,248,0.06);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#475569;
                letter-spacing:1.4px;text-transform:uppercase;margin-bottom:10px;">Msgs do Agente IA</div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:32px;font-weight:800;
                color:#f1f5f9;line-height:1;">{total_bot_msgs}</div>
    <div style="margin-top:8px;font-family:'Outfit',sans-serif;font-size:11px;color:#38bdf8;">
      ● Enviadas pela IA
    </div>
  </div>

</div>
"""
    components.html(f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Outfit:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>* {{box-sizing:border-box;margin:0;padding:0;}}</style>
</head><body style="background:transparent;padding:4px 2px;">{kpi_html}</body></html>""", height=148)

    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:3px;height:16px;background:#6bc895;border-radius:2px;flex-shrink:0;"></div>
            <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                         color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">
                Qualificação dos Leads
            </span>
        </div>
        """, unsafe_allow_html=True)

        DFU_META = {
            'CONVERSA_ATIVA':              {'color':'#38bdf8', 'label':'Conversa Ativa'},
            'INTERESSE_FORTE_SEM_RESPOSTA':{'color':'#a78bfa', 'label':'Interesse Forte'},
            'NEGOCIACAO_INTERROMPIDA':     {'color':'#fb923c', 'label':'Negociação Parada'},
            'PROPOSTA_ENVIADA_SEM_RETORNO':{'color':'#e879f9', 'label':'Proposta Enviada'},
            'INTERESSE_FRACO':             {'color':'#fbbf24', 'label':'Interesse Fraco'},
            'CONVERSA_ENCERRADA':          {'color':'#94a3b8', 'label':'Encerrada'},
            'RECUSA_EXPLICITA':            {'color':'#ff6b6b', 'label':'Recusa'},
            'JA_FECHOU':                   {'color':'#6bc895', 'label':'Fechou'},
        }

        if dfu_col_dash and not df_leads.empty:
            dfu_counts = df_leads[dfu_col_dash].astype(str).str.strip().str.upper().value_counts()
            total_dfu  = dfu_counts.sum()

            bars_html = ""
            for tag, meta in DFU_META.items():
                count = dfu_counts.get(tag, 0)
                if count == 0:
                    continue
                pct = round((count / total_dfu) * 100)
                bars_html += f"""
<div style="margin-bottom:14px;">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
    <div style="display:flex;align-items:center;gap:8px;">
      <div style="width:8px;height:8px;border-radius:50%;background:{meta['color']};flex-shrink:0;"></div>
      <span style="font-family:'Outfit',sans-serif;font-size:12px;color:#cbd5e1;font-weight:500;">{meta['label']}</span>
    </div>
    <div style="display:flex;align-items:center;gap:10px;">
      <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#475569;">{pct}%</span>
      <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:{meta['color']};
                   background:{meta['color']}18;border-radius:4px;padding:1px 7px;">{count}</span>
    </div>
  </div>
  <div style="height:5px;background:rgba(255,255,255,0.04);border-radius:99px;overflow:hidden;">
    <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,{meta['color']}cc,{meta['color']}66);
                border-radius:99px;transition:width 0.4s ease;"></div>
  </div>
</div>"""

            components.html(f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>* {{box-sizing:border-box;margin:0;padding:0;}}</style>
</head><body style="background:transparent;padding:2px 4px 8px;">{bars_html}</body></html>""", height=320, scrolling=True)
        else:
            st.markdown('<p style="color:#475569;font-size:13px;padding:40px 0;text-align:center;">Sem dados de qualificação ainda.</p>', unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:3px;height:16px;background:#38bdf8;border-radius:2px;flex-shrink:0;"></div>
            <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                         color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">
                Feed de Atividade
            </span>
        </div>
        """, unsafe_allow_html=True)

        if not df_msgs.empty and 'message_from' in df_msgs.columns:
            ultimas = df_msgs.tail(14).iloc[::-1]

            items_html = ""
            for _, row in ultimas.iterrows():
                sender = str(row['message_from']).lower()
                is_bot   = sender == 'agent'
                is_human = sender == 'human_agent'
                if is_bot:
                    nome_display = "Agente IA"
                    tag_bg    = "rgba(107,200,149,0.1)"
                    tag_color = "#6bc895"
                    tag_text  = "RESPOSTA IA"
                    icon_bg   = "#6bc895"
                    icon_c    = "#0a0c10"
                    icon_txt  = "AI"
                elif is_human:
                    nome_display = "Atendente"
                    tag_bg    = "rgba(56,189,248,0.1)"
                    tag_color = "#38bdf8"
                    tag_text  = "HUMANO"
                    icon_bg   = "#38bdf8"
                    icon_c    = "#0a0c10"
                    icon_txt  = "HU"
                else:
                    tel = str(row.iloc[1])
                    nome_display = tel_to_nome_dash.get(tel, "..." + tel[-4:] if len(tel) >= 4 else "Cliente")
                    tag_bg    = "rgba(148,163,184,0.1)"
                    tag_color = "#94a3b8"
                    tag_text  = "MENSAGEM"
                    icon_bg   = "#1e293b"
                    icon_c    = "#94a3b8"
                    icon_txt  = nome_display[:2].upper() if nome_display else "??"

                hora_raw = str(row.iloc[3])
                hora = hora_raw.split(" ")[-1][:5] if " " in hora_raw else hora_raw[:5]

                items_html += f"""
<div style="display:flex;align-items:center;gap:10px;
            padding:9px 0;border-bottom:1px solid rgba(148,163,184,0.05);">
    <div style="width:32px;height:32px;border-radius:8px;background:{icon_bg};
                display:flex;align-items:center;justify-content:center;
                font-size:10px;font-weight:700;flex-shrink:0;color:{icon_c};
                font-family:'Outfit',sans-serif;letter-spacing:0.5px;">
        {icon_txt}
    </div>
    <div style="flex:1;min-width:0;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-family:'Outfit',sans-serif;color:#f1f5f9;font-size:12px;
                         font-weight:600;white-space:nowrap;overflow:hidden;
                         text-overflow:ellipsis;max-width:130px;">{nome_display}</span>
            <span style="font-family:'JetBrains Mono',monospace;color:#475569;
                         font-size:10px;flex-shrink:0;margin-left:8px;">{hora}</span>
        </div>
        <div style="margin-top:3px;">
            <span style="background:{tag_bg};color:{tag_color};
                          font-family:'JetBrains Mono',monospace;font-size:9px;
                          font-weight:500;letter-spacing:0.8px;
                          padding:2px 7px;border-radius:4px;">{tag_text}</span>
        </div>
    </div>
</div>"""

            components.html(f"""<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&family=Outfit:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:#0a0c10; font-family:'Outfit',sans-serif; padding:0 4px 8px; }}
  ::-webkit-scrollbar {{ width:2px; }}
  ::-webkit-scrollbar-thumb {{ background:rgba(148,163,184,0.1); border-radius:99px; }}
</style>
</head><body>{items_html}</body></html>""", height=330, scrolling=True)

        else:
            st.markdown('<p style="color:#475569;font-size:13px;padding:40px 0;">Sem dados de atividade.</p>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LEADS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_leads:

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:3px;height:18px;background:#6bc895;border-radius:2px;"></div>
            <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:15px;font-weight:800;
                         color:#f1f5f9;letter-spacing:-0.3px;">Base de Leads</span>
        </div>
        <span style="background:rgba(107,200,149,0.08);border:1px solid rgba(107,200,149,0.2);
                     color:#6bc895;font-family:'JetBrains Mono',monospace;
                     font-size:10px;font-weight:500;padding:3px 10px;
                     border-radius:6px;letter-spacing:0.5px;">
            {len(df_leads)} registros
        </span>
    </div>
    """, unsafe_allow_html=True)

    if 'status' in df_leads.columns:
        status_list = df_leads['status'].value_counts()
        PALETTE = ['#6bc895', '#38bdf8', '#4ade80', '#fb7185', '#fbbf24']
        pills_html = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:20px;">'
        for i, (status, count) in enumerate(status_list.items()):
            c = PALETTE[i % len(PALETTE)]
            pills_html += f"""<span style="background:rgba(255,255,255,0.03);
                border:1px solid rgba(255,255,255,0.07);border-radius:6px;padding:5px 12px;
                font-family:'Outfit',sans-serif;font-size:12px;color:{c};font-weight:500;">
                {status}&nbsp;&nbsp;&middot;&nbsp;&nbsp;<b style="font-family:'JetBrains Mono',monospace;">{count}</b>
            </span>"""
        pills_html += '</div>'
        st.markdown(pills_html, unsafe_allow_html=True)

    DFU_TAGS = {'RECUSA_EXPLICITA', 'JA_FECHOU', 'CONVERSA_ENCERRADA', 'INTERESSE_FRACO', 'CONVERSA_ATIVA'}
    DFU_COL = next(
        (c for c in df_leads.columns
         if df_leads[c].dropna().astype(str).str.strip().str.upper().isin(DFU_TAGS).any()),
        None
    )
    if DFU_COL:
        DFU_COLORS = {
            'RECUSA_EXPLICITA':   ('#ff6b6b', 'rgba(255,107,107,0.08)', 'rgba(255,107,107,0.2)'),
            'JA_FECHOU':          ('#6bc895', 'rgba(107,200,149,0.08)', 'rgba(107,200,149,0.2)'),
            'CONVERSA_ENCERRADA': ('#94a3b8', 'rgba(148,163,184,0.08)', 'rgba(148,163,184,0.2)'),
            'INTERESSE_FRACO':    ('#fbbf24', 'rgba(251,191,36,0.08)',  'rgba(251,191,36,0.2)'),
            'CONVERSA_ATIVA':     ('#38bdf8', 'rgba(56,189,248,0.08)',  'rgba(56,189,248,0.2)'),
        }
        dfu_counts = df_leads[DFU_COL].value_counts()
        dfu_html = '''<div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;margin-top:6px;">
            <div style="width:3px;height:14px;background:#94a3b8;border-radius:2px;flex-shrink:0;"></div>
            <span style="font-family:\'Plus Jakarta Sans\',sans-serif;font-size:10px;font-weight:700;
                         color:#64748b;letter-spacing:1.2px;text-transform:uppercase;">Decision Follow Up</span>
        </div>'''
        dfu_html += '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:24px;">'
        for tag, count in dfu_counts.items():
            color, bg, border = DFU_COLORS.get(str(tag).strip().upper(), ('#94a3b8', 'rgba(148,163,184,0.08)', 'rgba(148,163,184,0.2)'))
            dfu_html += f"""<span style="background:{bg};border:1px solid {border};border-radius:6px;
                padding:5px 12px;font-family:'JetBrains Mono',monospace;font-size:10px;
                color:{color};font-weight:500;letter-spacing:0.5px;">
                {tag}&nbsp;&nbsp;&middot;&nbsp;&nbsp;<b>{count}</b>
            </span>"""
        dfu_html += '</div>'
        st.markdown(dfu_html, unsafe_allow_html=True)

    st.dataframe(
        df_leads,
        use_container_width=True,
        hide_index=True,
        height=500,
        column_config={col: st.column_config.TextColumn(col.title()) for col in df_leads.columns}
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CHAT
# ═══════════════════════════════════════════════════════════════════════════════

@st.fragment(run_every=60)
def _render_chat(tel_lead, nome_sel):
    df_msgs_live = pd.DataFrame()
    try:
        df_msgs_live = pd.read_csv(URL_HISTORICO)
    except Exception:
        pass
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
        <div style="width:3px;height:16px;background:#6bc895;border-radius:2px;flex-shrink:0;"></div>
        <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                     color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">
            Historico da Conversa
        </span>
    </div>
    """, unsafe_allow_html=True)

    if tel_lead and not df_msgs_live.empty:
        tel_clean = str(tel_lead).replace("@s.whatsapp.net", "").replace("@c.us", "")
        conversa = df_msgs_live[df_msgs_live.iloc[:, 1].astype(str).str.replace("@s.whatsapp.net","").str.replace("@c.us","") == tel_clean].copy()
        conversa = conversa.sort_values(by=conversa.columns[3])

        if conversa.empty:
            st.markdown('<p style="color:#475569;font-size:13px;padding:60px 0;text-align:center;">Nenhuma mensagem encontrada.</p>', unsafe_allow_html=True)
        else:
            chat_html = ""
            for _, m in conversa.iterrows():
                sender = str(m['message_from']).lower()
                is_bot   = sender == 'agent'
                is_human = sender == 'human_agent'

                if is_bot:
                    row_dir       = "row-reverse"
                    header_dir    = "row-reverse"
                    bubble_bg     = "rgba(107,200,149,0.08)"
                    bubble_border = "rgba(107,200,149,0.15)"
                    lbl           = "Agente IA"
                    lbl_c         = "#6bc895"
                    avatar_bg     = "#6bc895"
                    avatar_c      = "#0a0c10"
                    avatar_txt    = "AI"
                elif is_human:
                    row_dir       = "row-reverse"
                    header_dir    = "row-reverse"
                    bubble_bg     = "rgba(56,189,248,0.08)"
                    bubble_border = "rgba(56,189,248,0.2)"
                    lbl           = "Atendente"
                    lbl_c         = "#38bdf8"
                    avatar_bg     = "#38bdf8"
                    avatar_c      = "#0a0c10"
                    avatar_txt    = "HU"
                else:
                    row_dir       = "row"
                    header_dir    = "row"
                    bubble_bg     = "rgba(255,255,255,0.03)"
                    bubble_border = "rgba(255,255,255,0.07)"
                    lbl           = str(nome_sel)
                    lbl_c         = "#94a3b8"
                    avatar_bg     = "#1e293b"
                    avatar_c      = "#94a3b8"
                    avatar_txt    = ''.join([p[0].upper() for p in str(nome_sel).split()[:2]])

                msg_txt  = str(m.iloc[4]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                hora_raw = str(m.iloc[3])
                try:
                    dt   = pd.to_datetime(hora_raw, dayfirst=True)
                    hora = dt.strftime("%d/%m/%Y %H:%M")
                except Exception:
                    hora = hora_raw[:16]

                chat_html += f"""
    <div style="display:flex;flex-direction:{row_dir};align-items:flex-start;gap:10px;margin-bottom:16px;">
    <div style="width:30px;height:30px;border-radius:9px;background:{avatar_bg};flex-shrink:0;
            display:flex;align-items:center;justify-content:center;font-size:10px;
            color:{avatar_c};font-weight:700;margin-top:2px;
            font-family:'Outfit',sans-serif;letter-spacing:0.3px;">
    {avatar_txt}
    </div>
    <div style="max-width:78%;">
    <div style="display:flex;flex-direction:{header_dir};align-items:center;gap:8px;margin-bottom:5px;">
        <span style="font-family:'Outfit',sans-serif;font-size:11px;font-weight:700;color:{lbl_c};">{lbl}</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:9px;color:#64748b;">{hora}</span>
    </div>
    <div style="background:{bubble_bg};border:1px solid {bubble_border};border-radius:12px;padding:11px 15px;">
        <div style="font-family:'Outfit',sans-serif;font-size:13px;line-height:1.65;color:#cbd5e1;font-weight:400;">
            {msg_txt}
        </div>
    </div>
    </div>
    </div>"""

            components.html(f"""<!DOCTYPE html>
    <html><head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&family=Outfit:wght@400;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
    <style>
      * {{ box-sizing:border-box; margin:0; padding:0; }}
      body {{ background:#0a0c10; font-family:'Outfit',sans-serif; padding:8px 6px 12px; }}
      ::-webkit-scrollbar {{ width:2px; }}
      ::-webkit-scrollbar-thumb {{ background:rgba(255,255,255,0.07); border-radius:99px; }}
    </style>
    </head><body>{chat_html}<script>window.scrollTo(0, document.body.scrollHeight);</script></body></html>""", height=480, scrolling=True)

        # ── INPUT DE MENSAGEM ──────────────────────────────────────
        if tel_lead:
            st.markdown("""
            <div style="margin-top:16px;">
                <div style="background:#0f1318;border:1px solid rgba(148,163,184,0.1);
                            border-radius:16px;padding:12px 14px 10px;
                            box-shadow:0 4px 24px rgba(0,0,0,0.3);">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <div style="width:6px;height:6px;border-radius:50%;background:#6bc895;
                                    animation:pulse-lime 2s infinite;flex-shrink:0;"></div>
                        <span style="font-family:'JetBrains Mono',monospace;font-size:9px;
                                     color:#64748b;letter-spacing:1px;text-transform:uppercase;">
                            Chat do WhatsApp
                        </span>
                        <span style="margin-left:auto;background:rgba(251,191,36,0.08);
                                     border:1px solid rgba(251,191,36,0.18);border-radius:4px;
                                     padding:2px 7px;font-family:'JetBrains Mono',monospace;
                                     font-size:9px;color:#fbbf24;letter-spacing:0.5px;">
                            PAUSA AUTOMAÇÃO
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            msg_input = st.text_area(
                "msg",
                placeholder="  Digite sua mensagem...",
                label_visibility="collapsed",
                height=80,
                key=f"msg_input_{nome_sel}"
            )

            send_col, info_col2 = st.columns([2, 3], gap="small")
            with send_col:
                st.markdown('<div class="send-btn">', unsafe_allow_html=True)
                send_clicked = st.button(
                    "⬆  Enviar mensagem",
                    key=f"send_{nome_sel}",
                    use_container_width=True,
                    help="Enviar via WhatsApp — pausa o follow-up automático"
                )
                st.markdown('</div>', unsafe_allow_html=True)
            with info_col2:
                st.markdown("""
                <div style="display:flex;align-items:center;height:38px;gap:6px;padding-left:4px;">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
                        <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z"
                              stroke="#475569" stroke-width="2"/>
                        <path d="M12 8V12M12 16H12.01" stroke="#475569" stroke-width="2"
                              stroke-linecap="round"/>
                    </svg>
                    <span style="font-family:'Outfit',sans-serif;font-size:11px;color:#475569;">
                        Enviado como mensagem do atendente humano
                    </span>
                </div>
                """, unsafe_allow_html=True)

            if send_clicked:
                if msg_input.strip():
                    result = send_whatsapp(str(tel_lead), msg_input.strip())
                    if result["ok"]:
                        st.success("✓ Mensagem enviada com sucesso")
                        st.cache_data.clear()
                    else:
                        st.error(f"Erro {result['status']}: {result['body']}")
                else:
                    st.warning("Digite uma mensagem antes de enviar.")

    else:
        st.markdown('<p style="color:#475569;font-size:13px;padding:60px 0;text-align:center;">Selecione um contato para ver o historico.</p>', unsafe_allow_html=True)


with tab_chat:

    if 'chat_lead_sel' not in st.session_state:
        st.session_state['chat_lead_sel'] = None

    sel_col, info_col = st.columns([1, 2.2], gap="large")

    with sel_col:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:3px;height:16px;background:#6bc895;border-radius:2px;flex-shrink:0;"></div>
            <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                         color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">
                Conversas
            </span>
        </div>
        """, unsafe_allow_html=True)

        if 'nome do lead' not in df_leads.columns:
            st.warning("Coluna 'nome do lead' nao encontrada.")
            st.stop()

        leads_unicos = df_leads['nome do lead'].unique().tolist()

        dfu_col_chat2 = next(
            (c for c in df_leads.columns
             if df_leads[c].dropna().astype(str).str.strip().str.upper()
                .isin({'RECUSA_EXPLICITA','JA_FECHOU','CONVERSA_ENCERRADA','INTERESSE_FRACO',
                       'CONVERSA_ATIVA','INTERESSE_FORTE_SEM_RESPOSTA',
                       'NEGOCIACAO_INTERROMPIDA','PROPOSTA_ENVIADA_SEM_RETORNO'}).any()),
            None
        )
        DFU_DOT = {
            'CONVERSA_ATIVA':               '#38bdf8',
            'INTERESSE_FORTE_SEM_RESPOSTA': '#a78bfa',
            'NEGOCIACAO_INTERROMPIDA':      '#fb923c',
            'PROPOSTA_ENVIADA_SEM_RETORNO': '#e879f9',
            'INTERESSE_FRACO':              '#fbbf24',
            'CONVERSA_ENCERRADA':           '#475569',
            'RECUSA_EXPLICITA':             '#ff6b6b',
            'JA_FECHOU':                    '#6bc895',
        }

        nome_sel = st.session_state.get('chat_lead_sel', None)

        lead_data = []
        for nome_item in leads_unicos:
            lead_row_item = df_leads[df_leads['nome do lead'] == nome_item].iloc[0]
            initials_item = ''.join([p[0].upper() for p in str(nome_item).split()[:2]])
            status_item   = str(lead_row_item.get('status', '')).strip()
            dfu_item      = str(lead_row_item[dfu_col_chat2]).strip().upper() if dfu_col_chat2 and dfu_col_chat2 in lead_row_item.index else ''
            dot_color     = DFU_DOT.get(dfu_item, '#475569')
            last_msg = ''
            if not df_msgs.empty and 'telefone do lead' in df_leads.columns:
                tel_item = str(lead_row_item.get('telefone do lead', ''))
                msgs_item = df_msgs[df_msgs.iloc[:, 1].astype(str) == tel_item]
                if not msgs_item.empty:
                    raw = str(msgs_item.iloc[-1].iloc[4])
                    last_msg = raw[:40] + ('…' if len(raw) > 40 else '')
            lead_data.append({
                'nome': nome_item,
                'initials': initials_item,
                'dot': dot_color,
                'preview': last_msg if last_msg else status_item,
            })

        opcoes = ["— selecione um contato —"] + [ld["nome"] for ld in lead_data]
        idx_atual = 0
        if nome_sel in leads_unicos:
            idx_atual = leads_unicos.index(nome_sel) + 1

        escolha = st.selectbox(
            "Contato",
            opcoes,
            index=idx_atual,
            label_visibility="collapsed",
            key="sel_lead"
        )
        if escolha != "— selecione um contato —":
            if escolha != nome_sel:
                st.session_state["chat_lead_sel"] = escolha
                st.rerun()
            nome_sel = escolha
        else:
            st.session_state["chat_lead_sel"] = None
            nome_sel = None

        if nome_sel:
            lead_row_sel = df_leads[df_leads["nome do lead"] == nome_sel].iloc[0]
            tel_display  = str(lead_row_sel.get("telefone do lead", "—")).replace("@s.whatsapp.net","").replace("@c.us","")
            status_val   = str(lead_row_sel.get("status", "—")).strip()
            dfu_val      = str(lead_row_sel[dfu_col_chat2]).strip().upper() if dfu_col_chat2 and dfu_col_chat2 in lead_row_sel.index else ""
            initials_sel = "".join([p[0].upper() for p in nome_sel.split()[:2]])

            DFU_COLORS_MAP = {
                "CONVERSA_ATIVA":               ("#38bdf8", "rgba(56,189,248,0.08)",  "rgba(56,189,248,0.2)"),
                "INTERESSE_FORTE_SEM_RESPOSTA": ("#a78bfa", "rgba(167,139,250,0.08)", "rgba(167,139,250,0.2)"),
                "NEGOCIACAO_INTERROMPIDA":      ("#fb923c", "rgba(251,146,60,0.08)",  "rgba(251,146,60,0.2)"),
                "PROPOSTA_ENVIADA_SEM_RETORNO": ("#e879f9", "rgba(232,121,249,0.08)", "rgba(232,121,249,0.2)"),
                "INTERESSE_FRACO":              ("#fbbf24", "rgba(251,191,36,0.08)",  "rgba(251,191,36,0.2)"),
                "CONVERSA_ENCERRADA":           ("#94a3b8", "rgba(148,163,184,0.08)", "rgba(148,163,184,0.2)"),
                "RECUSA_EXPLICITA":             ("#ff6b6b", "rgba(255,107,107,0.08)", "rgba(255,107,107,0.2)"),
                "JA_FECHOU":                    ("#6bc895", "rgba(107,200,149,0.08)", "rgba(107,200,149,0.2)"),
            }
            STATUS_COLORS = {
                "AGUARDANDO_LEAD": ("#fbbf24", "rgba(251,191,36,0.08)",  "rgba(251,191,36,0.2)"),
                "CONVERSA_ATIVA":  ("#38bdf8", "rgba(56,189,248,0.08)",  "rgba(56,189,248,0.2)"),
                "ENCERRADO":       ("#94a3b8", "rgba(148,163,184,0.08)", "rgba(148,163,184,0.2)"),
            }

            dfu_color, dfu_bg, dfu_border = DFU_COLORS_MAP.get(dfu_val, ("#94a3b8", "rgba(148,163,184,0.08)", "rgba(148,163,184,0.2)"))
            st_color,  st_bg,  st_border  = STATUS_COLORS.get(status_val.upper(), ("#94a3b8", "rgba(148,163,184,0.08)", "rgba(148,163,184,0.2)"))

            last_msg_txt = ""
            last_msg_de  = ""
            if not df_msgs.empty and "telefone do lead" in df_leads.columns:
                tel_raw  = str(lead_row_sel.get("telefone do lead", ""))
                msgs_sel = df_msgs[df_msgs.iloc[:, 1].astype(str) == tel_raw]
                if not msgs_sel.empty:
                    last_row    = msgs_sel.iloc[-1]
                    last_msg_txt = str(last_row.iloc[4])[:80]
                    sender       = str(last_row["message_from"]).lower()
                    last_msg_de  = "Agente IA" if sender == "agent" else ("Atendente" if sender == "human_agent" else nome_sel)

            n_msgs = 0
            if not df_msgs.empty and "telefone do lead" in df_leads.columns:
                tel_raw = str(lead_row_sel.get("telefone do lead", ""))
                n_msgs  = len(df_msgs[df_msgs.iloc[:, 1].astype(str) == tel_raw])

            dfu_badge  = f'<span style="background:{dfu_bg};border:1px solid {dfu_border};border-radius:6px;padding:3px 9px;font-family:JetBrains Mono,monospace;font-size:10px;color:{dfu_color};font-weight:600;letter-spacing:0.4px;">{dfu_val if dfu_val else "—"}</span>' if dfu_val else ""
            st_badge   = f'<span style="background:{st_bg};border:1px solid {st_border};border-radius:6px;padding:3px 9px;font-family:JetBrains Mono,monospace;font-size:10px;color:{st_color};font-weight:600;letter-spacing:0.4px;">{status_val}</span>'

            panel_html = f"""
<div style="background:#0f1318;border:1px solid rgba(107,200,149,0.15);border-radius:16px;
            padding:18px;margin-top:4px;position:relative;overflow:hidden;">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,#6bc895,transparent);opacity:0.6;"></div>
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
    <div style="width:48px;height:48px;border-radius:14px;flex-shrink:0;
                background:rgba(107,200,149,0.12);border:1px solid rgba(107,200,149,0.25);
                display:flex;align-items:center;justify-content:center;
                font-family:Plus Jakarta Sans,sans-serif;font-size:15px;
                font-weight:700;color:#6bc895;">{initials_sel}</div>
    <div>
      <div style="font-family:Plus Jakarta Sans,sans-serif;font-size:15px;
                  font-weight:700;color:#f1f5f9;line-height:1.2;">{nome_sel}</div>
      <div style="font-family:JetBrains Mono,monospace;font-size:11px;
                  color:#475569;margin-top:3px;">{tel_display}</div>
    </div>
  </div>
  <div style="height:1px;background:rgba(148,163,184,0.07);margin-bottom:14px;"></div>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;">
    {st_badge}
    {dfu_badge}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:{'14px' if last_msg_txt else '0'};">
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(148,163,184,0.07);
                border-radius:10px;padding:10px 12px;">
      <div style="font-family:JetBrains Mono,monospace;font-size:9px;color:#475569;
                  letter-spacing:0.8px;text-transform:uppercase;margin-bottom:4px;">Mensagens</div>
      <div style="font-family:Plus Jakarta Sans,sans-serif;font-size:20px;font-weight:800;
                  color:#f1f5f9;line-height:1;">{n_msgs}</div>
    </div>
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(148,163,184,0.07);
                border-radius:10px;padding:10px 12px;">
      <div style="font-family:JetBrains Mono,monospace;font-size:9px;color:#475569;
                  letter-spacing:0.8px;text-transform:uppercase;margin-bottom:4px;">Follow-up</div>
      <div style="font-family:Plus Jakarta Sans,sans-serif;font-size:11px;font-weight:600;
                  color:{dfu_color};line-height:1.3;margin-top:2px;">{dfu_val.replace("_"," ") if dfu_val else "—"}</div>
    </div>
  </div>
  {'<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(148,163,184,0.07);border-radius:10px;padding:10px 12px;"><div style="font-family:JetBrains Mono,monospace;font-size:9px;color:#475569;letter-spacing:0.8px;text-transform:uppercase;margin-bottom:6px;">Última mensagem · ' + last_msg_de + '</div><div style="font-family:Outfit,sans-serif;font-size:12px;color:#94a3b8;line-height:1.5;">' + last_msg_txt + '</div></div>' if last_msg_txt else ""}
</div>"""

            components.html(f'''<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Outfit:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>* {{box-sizing:border-box;margin:0;padding:0;}}</style>
</head><body style="background:transparent;padding:2px 2px 4px;">{panel_html}</body></html>''',
                height=320)
        else:
            st.markdown("""
<div style="background:rgba(255,255,255,0.02);border:1px dashed rgba(148,163,184,0.1);
            border-radius:16px;padding:32px 16px;text-align:center;margin-top:8px;">
  <div style="font-family:'Outfit',sans-serif;font-size:13px;color:#334155;">
    Selecione um contato acima
  </div>
</div>""", unsafe_allow_html=True)

        tel_lead = None
        if nome_sel and 'telefone do lead' in df_leads.columns:
            tel_map  = dict(zip(df_leads['nome do lead'], df_leads['telefone do lead']))
            tel_lead = tel_map.get(nome_sel)

    with info_col:
        if nome_sel is None:
            st.markdown("""
            <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                        height:560px;text-align:center;gap:16px;">
                <div style="width:64px;height:64px;border-radius:20px;
                            background:rgba(107,200,149,0.08);border:1px solid rgba(107,200,149,0.15);
                            display:flex;align-items:center;justify-content:center;margin-bottom:8px;">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                        <path d="M21 15C21 15.5304 20.7893 16.0391 20.4142 16.4142C20.0391 16.7893 19.5304 17 19 17H7L3 21V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V15Z"
                              stroke="#6bc895" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:18px;font-weight:700;
                            color:#f1f5f9;">Bem-vindo ao Chat</div>
                <div style="font-family:'Outfit',sans-serif;font-size:13px;color:#475569;
                            max-width:280px;line-height:1.6;">
                    Selecione um contato ao lado para visualizar a conversa e enviar mensagens via WhatsApp.
                </div>
                <div style="margin-top:8px;display:flex;align-items:center;gap:6px;">
                    <div style="width:5px;height:5px;border-radius:50%;background:#6bc895;"></div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:10px;color:#475569;
                                 letter-spacing:0.8px;">ATUALIZA A CADA 60S</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            _render_chat(tel_lead, nome_sel)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — KANBAN
# ═══════════════════════════════════════════════════════════════════════════════
with tab_kanban:

    SECTION_HEADER = """
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;">
        <div style="width:3px;height:16px;background:{color};border-radius:2px;flex-shrink:0;"></div>
        <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                     color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">{title}</span>
        <span style="margin-left:auto;background:{badge_bg};border:1px solid {badge_border};
                     border-radius:6px;padding:2px 9px;font-family:'JetBrains Mono',monospace;
                     font-size:10px;color:{badge_color};font-weight:600;">{count}</span>
    </div>
    """

    KANBAN_STATUS_MAP = {
        "CONVERSA_ATIVA":  {"color": "#38bdf8", "badge_bg": "rgba(56,189,248,0.08)",  "badge_border": "rgba(56,189,248,0.2)",  "badge_color": "#38bdf8",  "label": "CONVERSA ATIVA"},
        "AGUARDANDO_LEAD": {"color": "#fbbf24", "badge_bg": "rgba(251,191,36,0.08)",  "badge_border": "rgba(251,191,36,0.2)",  "badge_color": "#fbbf24",  "label": "AGUARDANDO LEAD"},
        "ENCERRADO":       {"color": "#94a3b8", "badge_bg": "rgba(148,163,184,0.08)", "badge_border": "rgba(148,163,184,0.2)", "badge_color": "#94a3b8",  "label": "ENCERRADO"},
    }

    TAGS_ENCERRADO = {'JA_FECHOU', 'RECUSA_EXPLICITA', 'CONVERSA_ENCERRADA'}

    if 'status' not in df_leads.columns:
        st.warning("Coluna 'status' não encontrada.")
    else:
        col_ativa, col_aguard, col_enc = st.columns(3, gap="medium")

        for col_ui, status_key in zip(
            [col_ativa, col_aguard, col_enc],
            ["CONVERSA_ATIVA", "AGUARDANDO_LEAD", "ENCERRADO"]
        ):
            cfg = KANBAN_STATUS_MAP[status_key]

            dfu_col = next((c for c in df_leads.columns if df_leads[c].dropna().astype(str).str.strip().str.upper().isin(TAGS_ENCERRADO).any()), None)
            encerrados_idx = df_leads[df_leads[dfu_col].astype(str).str.strip().str.upper().isin(TAGS_ENCERRADO)].index if dfu_col else pd.Index([])

            if status_key == "ENCERRADO":
                grupo = df_leads.loc[encerrados_idx] if len(encerrados_idx) > 0 else df_leads.iloc[0:0]
            else:
                grupo = df_leads[df_leads['status'].astype(str).str.upper() == status_key]
                grupo = grupo[~grupo.index.isin(encerrados_idx)]

            with col_ui:
                st.markdown(SECTION_HEADER.format(
                    color=cfg["color"], title=cfg['label'],
                    badge_bg=cfg["badge_bg"], badge_border=cfg["badge_border"],
                    badge_color=cfg["badge_color"], count=len(grupo)
                ), unsafe_allow_html=True)

                if grupo.empty:
                    st.markdown(f"""
                    <div style="border:1px dashed rgba(148,163,184,0.1);border-radius:12px;
                                padding:32px 16px;text-align:center;color:#334155;
                                font-family:'Outfit',sans-serif;font-size:12px;">
                        Nenhum lead
                    </div>""", unsafe_allow_html=True)
                else:
                    for _, lead in grupo.iterrows():
                        nome = str(lead.get('nome do lead', '—'))
                        tel  = str(lead.get('telefone do lead', '')).replace('@s.whatsapp.net','').replace('@c.us','')
                        dfu  = str(lead.get('decision_follow_up', '')).strip() if 'decision_follow_up' in lead else ''
                        msgs = ''
                        if not df_msgs.empty and 'telefone do lead' in df_msgs.columns:
                            n = len(df_msgs[df_msgs['telefone do lead'].astype(str) == str(lead.get('telefone do lead',''))])
                            msgs = f'<span style="font-size:10px;color:#475569;font-family:JetBrains Mono,monospace;">{n} msgs</span>'

                        dfu_html = ''
                        if dfu and dfu.lower() not in ('nan','none',''):
                            DFU_COLORS = {
                                'RECUSA_EXPLICITA':            '#ff6b6b',
                                'JA_FECHOU':                   '#6bc895',
                                'CONVERSA_ENCERRADA':          '#94a3b8',
                                'INTERESSE_FRACO':             '#fbbf24',
                                'CONVERSA_ATIVA':              '#38bdf8',
                                'INTERESSE_FORTE_SEM_RESPOSTA':'#a78bfa',
                                'NEGOCIACAO_INTERROMPIDA':     '#fb923c',
                                'PROPOSTA_ENVIADA_SEM_RETORNO':'#e879f9',
                            }
                            dc = DFU_COLORS.get(dfu.upper(), '#94a3b8')
                            dfu_html = f'<span style="background:rgba(0,0,0,0.3);border:1px solid {dc}33;border-radius:4px;padding:2px 6px;font-family:JetBrains Mono,monospace;font-size:9px;color:{dc};letter-spacing:0.4px;">{dfu}</span>'

                        initials = ''.join([p[0].upper() for p in nome.split()[:2]])
                        st.markdown(f"""
                        <div style="background:#0f1318;border:1px solid rgba(148,163,184,0.08);
                                    border-radius:12px;padding:13px 14px;margin-bottom:8px;
                                    transition:border-color 0.2s;"
                             onmouseover="this.style.borderColor='rgba(148,163,184,0.2)'"
                             onmouseout="this.style.borderColor='rgba(148,163,184,0.08)'">
                            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
                                <div style="width:28px;height:28px;border-radius:8px;
                                            background:{cfg['color']}22;flex-shrink:0;
                                            display:flex;align-items:center;justify-content:center;
                                            font-size:10px;font-weight:700;color:{cfg['color']};
                                            font-family:'Outfit',sans-serif;">{initials}</div>
                                <div style="flex:1;min-width:0;">
                                    <div style="font-family:'Outfit',sans-serif;font-size:12px;
                                                font-weight:600;color:#f1f5f9;white-space:nowrap;
                                                overflow:hidden;text-overflow:ellipsis;">{nome}</div>
                                    <div style="font-family:'JetBrains Mono',monospace;font-size:10px;
                                                color:#475569;margin-top:1px;">{tel[-11:] if len(tel)>=11 else tel}</div>
                                </div>
                                {msgs}
                            </div>
                            {('<div>' + dfu_html + '</div>') if dfu_html else ''}
                        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — CONVERSÕES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_conv:

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;">
        <div style="width:3px;height:16px;background:#6bc895;border-radius:2px;flex-shrink:0;"></div>
        <span style="font-family:'Plus Jakarta Sans',sans-serif;font-size:11px;font-weight:700;
                     color:#94a3b8;letter-spacing:1.2px;text-transform:uppercase;">
            Conversões por Semana
        </span>
    </div>
    """, unsafe_allow_html=True)

    date_col = None
    for c in df_leads.columns:
        if 'data' in c.lower() or 'created' in c.lower() or 'entrada' in c.lower() or 'cadastro' in c.lower():
            date_col = c
            break
    if date_col is None and 'last_message_at' in df_leads.columns:
        date_col = 'last_message_at'

    if date_col is None:
        st.info("Nenhuma coluna de data encontrada no Cadastro (ex: 'data_cadastro', 'created_at'). Adicione uma coluna de data de entrada para ver o gráfico.")
    else:
        df_conv = df_leads.copy()
        df_conv['_date'] = pd.to_datetime(df_conv[date_col], errors='coerce', dayfirst=True)
        df_conv = df_conv.dropna(subset=['_date'])

        if df_conv.empty:
            st.info("Sem dados de data válidos para gerar o gráfico.")
        else:
            df_conv['_week'] = df_conv['_date'].dt.to_period('W').apply(lambda r: r.start_time)

            leads_por_semana = df_conv.groupby('_week').size().reset_index(name='Leads')

            fechados_por_semana = pd.DataFrame(columns=['_week','Fechados'])
            if 'status' in df_conv.columns:
                df_fechados = df_conv[df_conv['status'].astype(str).str.upper() == 'FECHADO']
                fechados_por_semana = df_fechados.groupby('_week').size().reset_index(name='Fechados')

            df_chart = leads_por_semana.merge(fechados_por_semana, on='_week', how='left').fillna(0)
            df_chart['Fechados'] = df_chart['Fechados'].astype(int)
            df_chart['_week_str'] = df_chart['_week'].dt.strftime('%d/%m')

            total_leads_conv = len(df_conv)
            total_fechados = int(df_chart['Fechados'].sum())
            taxa = round((total_fechados / total_leads_conv) * 100, 1) if total_leads_conv > 0 else 0

            m1, m2, m3 = st.columns(3)
            m1.metric("Total de Leads", total_leads_conv)
            m2.metric("Fechados", total_fechados)
            m3.metric("Taxa de Conversão", f"{taxa}%")

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            fig2 = go.Figure()

            fig2.add_trace(go.Scatter(
                x=df_chart['_week_str'],
                y=df_chart['Leads'],
                name='Leads Entraram',
                mode='lines+markers',
                line=dict(color='#38bdf8', width=2.5, shape='spline', smoothing=0.8),
                fill='tozeroy',
                fillcolor='rgba(56,189,248,0.08)',
                marker=dict(size=7, color='#38bdf8', line=dict(color='#0a0c10', width=2)),
                hovertemplate='<b>%{x}</b><br>Leads: %{y}<extra></extra>',
            ))

            fig2.add_trace(go.Scatter(
                x=df_chart['_week_str'],
                y=df_chart['Fechados'],
                name='Fechados',
                mode='lines+markers',
                line=dict(color='#6bc895', width=2.5, shape='spline', smoothing=0.8),
                fill='tozeroy',
                fillcolor='rgba(107,200,149,0.08)',
                marker=dict(size=7, color='#6bc895', line=dict(color='#0a0c10', width=2)),
                hovertemplate='<b>%{x}</b><br>Fechados: %{y}<extra></extra>',
            ))

            fig2.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#94a3b8', family='Outfit'),
                height=380,
                margin=dict(t=20, b=20, l=0, r=0),
                hovermode='x unified',
                xaxis=dict(
                    showgrid=False, zeroline=False,
                    tickfont=dict(family='JetBrains Mono', size=11, color='#475569'),
                    showline=False,
                ),
                yaxis=dict(
                    showgrid=True, zeroline=False,
                    gridcolor='rgba(148,163,184,0.05)',
                    tickfont=dict(family='JetBrains Mono', size=11, color='#475569'),
                    showline=False,
                    rangemode='tozero',
                    dtick=1,
                ),
                legend=dict(
                    orientation='h', x=0, y=1.06,
                    font=dict(size=12, color='#94a3b8', family='Outfit'),
                    bgcolor='rgba(0,0,0,0)',
                    itemsizing='constant',
                ),
                hoverlabel=dict(
                    bgcolor='#0f1318', font_size=12,
                    font_family='Outfit',
                    bordercolor='rgba(148,163,184,0.12)',
                    font_color='#f1f5f9',
                ),
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})