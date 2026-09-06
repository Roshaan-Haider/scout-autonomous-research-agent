import streamlit as st
from graph.agent_graph import app as agent_app
import uuid
import re

st.set_page_config(page_title="Scout — AI Company Research", page_icon="◈", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

theme = st.session_state.theme

if theme == "dark":
    bg_gradient = "linear-gradient(160deg, #0B0D10 0%, #101319 45%, #0B0D10 100%)"
    sidebar_bg = "#111418"
    card_bg = "#15191E"
    border_col = "rgba(255,255,255,0.08)"
    text_primary = "#F5F5F5"
    text_secondary = "#9CA3AF"
    input_bg = "#15191E"
else:
    bg_gradient = "linear-gradient(160deg, #FAFAFA 0%, #F0F2F5 45%, #FAFAFA 100%)"
    sidebar_bg = "#FFFFFF"
    card_bg = "#F5F6F8"
    border_col = "rgba(0,0,0,0.08)"
    text_primary = "#1A1D21"
    text_secondary = "#6B7280"
    input_bg = "#F5F6F8"

accent = "#5B8CFF"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

    .stApp {{ background: {bg_gradient}; }}

    .main .block-container {{
        max-width: 880px;
        padding-top: 2rem;
        padding-bottom: 9rem;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        border-right: 1px solid {border_col};
        width: 270px !important;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background: transparent;
        border: 1px solid {border_col};
        color: {text_primary};
        border-radius: 8px;
        text-align: left;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: rgba(91, 140, 255, 0.1);
        border: 1px solid rgba(91, 140, 255, 0.35);
    }}

    .sidebar-brand {{
        display: flex; align-items: center; gap: 10px;
        font-size: 18px; font-weight: 700; color: {text_primary};
        margin: 4px 0 20px 0;
    }}
    .sidebar-brand-icon {{ font-size: 20px; color: {accent}; }}
    .sidebar-section-label {{
        font-size: 11px; font-weight: 600; letter-spacing: 0.08em;
        color: {text_secondary}; text-transform: uppercase;
        margin: 20px 0 8px 4px;
    }}

    /* Bottom-left profile cluster */
    .sidebar-footer-row {{
        position: fixed;
        bottom: 16px;
        left: 16px;
        width: 238px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-top: 12px;
        border-top: 1px solid {border_col};
    }}
    .profile-cluster {{ display: flex; align-items: center; gap: 10px; }}
    .avatar-circle {{
        width: 30px; height: 30px; border-radius: 50%;
        background: {accent};
        color: white; font-size: 13px; font-weight: 600;
        display: flex; align-items: center; justify-content: center;
    }}
    .profile-name {{ font-size: 13px; font-weight: 500; color: {text_primary}; }}
    .footer-icons {{ display: flex; gap: 4px; }}

    /* Empty state */
    .hero-wrap {{ text-align: center; margin-top: 8%; }}
    .hero-icon {{ font-size: 32px; color: {accent}; margin-bottom: 16px; }}
    .hero-title {{ font-size: 34px; font-weight: 700; color: {text_primary}; margin-bottom: 12px; }}
    .hero-sub {{
        font-size: 15px; color: {text_secondary};
        max-width: 520px; margin: 0 auto 40px auto; line-height: 1.6;
    }}

    .suggestion-card {{
        background: {card_bg};
        border: 1px solid {border_col};
        border-radius: 14px;
        padding: 18px;
        transition: all 0.2s ease;
        height: 118px;
    }}
    .suggestion-card:hover {{
        border: 1px solid rgba(91,140,255,0.4);
        transform: translateY(-2px);
    }}
    .suggestion-icon {{ color: {accent}; font-size: 15px; margin-bottom: 8px; }}
    .suggestion-title {{ font-size: 14px; font-weight: 600; color: {text_primary}; margin-bottom: 6px; }}
    .suggestion-sub {{ font-size: 12.5px; color: {text_secondary}; line-height: 1.4; }}

    .role-label {{ font-size: 13px; font-weight: 600; color: {text_secondary}; margin: 24px 0 8px 0; }}
    .role-label.assistant {{ color: {accent}; }}
    .user-message {{
        background: {card_bg};
        border-radius: 12px; padding: 14px 18px; max-width: 80%;
        color: {text_primary}; font-size: 15px; line-height: 1.6;
    }}
    .assistant-message {{
        color: {text_primary}; font-size: 15px; line-height: 1.7; padding: 4px 0 12px 0;
    }}
    .assistant-message h2 {{ font-size: 20px; margin-top: 20px; color: {text_primary}; }}
    .assistant-message h3 {{ font-size: 16px; margin-top: 16px; color: {text_primary}; }}
    .assistant-message code {{ background: {card_bg}; padding: 2px 6px; border-radius: 4px; font-size: 13px; }}

    .status-box {{
        border: 1px solid {border_col}; background: {card_bg};
        border-radius: 10px; padding: 14px 18px; color: {text_secondary};
        font-size: 14px; margin: 12px 0;
    }}
    .status-box .dot {{
        display: inline-block; width: 7px; height: 7px; border-radius: 50%;
        background: {accent}; margin-right: 8px; animation: pulse 1.4s infinite ease-in-out;
    }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 0.3; }} 50% {{ opacity: 1; }} }}

    /* Chat input — pushed lower, floating feel */
    div[data-testid="stChatInput"] {{
        background: {input_bg};
        border: 1px solid {border_col};
        border-radius: 14px;
        box-shadow: 0 6px 24px rgba(0,0,0,0.15);
        margin-bottom: 28px;
    }}
    div[data-testid="stChatInput"] textarea {{ color: {text_primary} !important; }}

    hr {{ border-color: {border_col}; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# STATE
# ============================================================
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {"title": "New research", "messages": []}
    st.session_state.current_chat_id = new_id


def new_chat():
    new_id = str(uuid.uuid4())
    st.session_state.chats[new_id] = {"title": "New research", "messages": []}
    st.session_state.current_chat_id = new_id


def switch_chat(chat_id):
    st.session_state.current_chat_id = chat_id


def generate_title(question: str) -> str:
    filler_starts = [
        "compare", "what does", "what is", "summarize", "search for",
        "find", "tell me", "give me", "explain", "according to"
    ]
    cleaned = question.strip()
    lowered = cleaned.lower()
    for phrase in filler_starts:
        if lowered.startswith(phrase):
            cleaned = cleaned[len(phrase):].strip(" ?,.:")
            break
    cleaned = re.split(r"[,.;]| and | focusing ", cleaned, maxsplit=1)[0]
    words = cleaned.split()
    short = " ".join(words[:6])
    return short[:1].upper() + short[1:] if short else question[:30]


def ask(question: str):
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    current_chat["messages"].append({"role": "user", "content": question})
    if current_chat["title"] == "New research":
        current_chat["title"] = generate_title(question)

    result = agent_app.invoke(
        {"messages": [("user", question)], "tool_calls_made": 0, "call_history": []},
        config={"recursion_limit": 15}
    )
    answer = result["messages"][-1].content
    current_chat["messages"].append({"role": "assistant", "content": answer})


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    with st.sidebar:
        st.markdown(
            '<div class="sidebar-brand"><span class="sidebar-brand-icon">◈</span> Scout</div>',
            unsafe_allow_html=True
        )
        st.button("+  New research", on_click=new_chat, use_container_width=True)

        st.markdown('<div class="sidebar-section-label">Recent</div>', unsafe_allow_html=True)
        for chat_id, chat in reversed(list(st.session_state.chats.items())):
            if st.button(chat["title"], key=chat_id, use_container_width=True):
                switch_chat(chat_id)

        # Bottom-left profile cluster
        st.markdown("""
        <div class="sidebar-footer-row">
            <div class="profile-cluster">
                <div class="avatar-circle">RH</div>
                <div class="profile-name">Roshaan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col2:
            st.button("🔍", key="search_btn", help="Search chats")
        with col3:
            if st.button("⋯", key="menu_btn", help="Settings"):
                toggle_theme()
                st.rerun()


# ============================================================
# EMPTY STATE
# ============================================================
def render_empty_state():
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-icon">◈</div>
        <div class="hero-title">What would you like to research?</div>
        <div class="hero-sub">
            Scout researches companies using SEC filings and live web sources
            to produce evidence-backed answers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        ("⌁", "Compare risk factors", "Compare NVIDIA and AMD's risk factors, focusing on AI hardware competition"),
        ("◷", "Recent earnings", "Summarize Tesla's most recent 8-K in one paragraph"),
        ("⇄", "Filings + live news", "What does Apple's 10-K say about supply chain risk, and search for recent related news"),
    ]
    cols = st.columns(3)
    for col, (icon, title, prompt) in zip(cols, suggestions):
        with col:
            st.markdown(f"""
            <div class="suggestion-card">
                <div class="suggestion-icon">{icon}</div>
                <div class="suggestion-title">{title}</div>
                <div class="suggestion-sub">{prompt}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Ask", key=title, use_container_width=True):
                status_placeholder = st.empty()
                render_research_status(status_placeholder)
                ask(prompt)
                status_placeholder.empty()
                st.rerun()


# ============================================================
# MESSAGES
# ============================================================
def render_message(msg):
    if msg["role"] == "user":
        st.markdown('<div class="role-label">You</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="role-label assistant">Scout</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)


def render_research_status(placeholder):
    placeholder.markdown("""
    <div class="status-box"><span class="dot"></span> Scout is researching — searching filings and relevant sources...</div>
    """, unsafe_allow_html=True)


# ============================================================
# MAIN
# ============================================================
render_sidebar()

current_chat = st.session_state.chats[st.session_state.current_chat_id]

if not current_chat["messages"]:
    render_empty_state()
else:
    for msg in current_chat["messages"]:
        render_message(msg)

user_input = st.chat_input("Ask Scout a research question...")
if user_input:
    render_message({"role": "user", "content": user_input})
    status_placeholder = st.empty()
    render_research_status(status_placeholder)
    ask(user_input)
    status_placeholder.empty()
    st.rerun()