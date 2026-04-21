import streamlit as st
import threading
import time
from datetime import datetime
from capture import ScreenCapture, take_screenshots, image_to_bytes
from ai_engine import describe_screen, ask_for_help, chat_with_ai, check_ollama_running
from context import ContextBuffer

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="Screen AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0a0f !important;
    color: #e2e8f0;
    font-family: 'Syne', sans-serif;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Layout ── */
.main-grid {
    display: grid;
    grid-template-columns: 340px 1fr;
    grid-template-rows: 64px 1fr;
    height: 100vh;
    gap: 0;
}

/* ── Top Bar ── */
.topbar {
    grid-column: 1 / -1;
    background: #0d0d14;
    border-bottom: 1px solid #1e1e2e;
    display: flex;
    align-items: center;
    padding: 0 24px;
    gap: 16px;
}
.topbar-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 18px;
    color: #a78bfa;
    letter-spacing: -0.5px;
}
.topbar-logo span { color: #e2e8f0; }
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 8px #22c55e;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
}
.status-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #64748b;
}
.topbar-spacer { flex: 1; }
.hotkey-badge {
    background: #1e1e2e;
    border: 1px solid #2d2d3d;
    border-radius: 6px;
    padding: 4px 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #a78bfa;
}

/* ── Sidebar: Activity Feed ── */
.sidebar-panel {
    background: #0d0d14;
    border-right: 1px solid #1e1e2e;
    overflow-y: auto;
    padding: 16px;
}
.sidebar-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e1e2e;
}
.activity-entry {
    padding: 10px 12px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: #12121a;
    border: 1px solid #1e1e2e;
    transition: border-color 0.2s;
}
.activity-entry:hover { border-color: #2d2d4d; }
.activity-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #475569;
    margin-bottom: 4px;
}
.activity-desc {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.5;
}
.activity-desc.error { color: #f87171; }
.no-activity {
    text-align: center;
    color: #334155;
    font-size: 12px;
    margin-top: 40px;
    line-height: 1.8;
}

/* ── Main Chat Panel ── */
.chat-panel {
    display: flex;
    flex-direction: column;
    height: calc(100vh - 64px);
    background: #0a0a0f;
}
.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 24px 32px;
}
.chat-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #1e1e2e;
    gap: 12px;
}
.chat-empty-icon { font-size: 48px; opacity: 0.5; }
.chat-empty-text {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    color: #334155;
    text-align: center;
    line-height: 1.8;
}

/* ── Chat Bubbles ── */
.msg-row {
    display: flex;
    margin-bottom: 20px;
    gap: 12px;
}
.msg-row.user { flex-direction: row-reverse; }
.msg-avatar {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.msg-avatar.ai { background: #1e1030; border: 1px solid #3730a3; }
.msg-avatar.user-av { background: #0f2720; border: 1px solid #065f46; }
.msg-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.7;
}
.msg-bubble.ai {
    background: #12121a;
    border: 1px solid #1e1e2e;
    color: #cbd5e1;
    border-top-left-radius: 4px;
}
.msg-bubble.user {
    background: #1e1030;
    border: 1px solid #3730a3;
    color: #c4b5fd;
    border-top-right-radius: 4px;
}
.msg-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #334155;
    margin-top: 4px;
}

/* ── Chat Input Area ── */
.chat-input-area {
    padding: 16px 32px 24px;
    border-top: 1px solid #1e1e2e;
    background: #0d0d14;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #12121a !important;
    border: 1px solid #2d2d3d !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    padding: 12px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.15) !important;
}
.stButton > button {
    background: #7c3aed !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 12px 20px !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #6d28d9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:disabled {
    background: #1e1e2e !important;
    color: #475569 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e1e2e; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #2d2d4d; }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ─────────────────────────────────────
def init_state():
    defaults = {
        "buf":              None,
        "capture_running":  False,
        "chat_history":     [],       # [{"role": ..., "content": ..., "time": ...}]
        "session_id":       None,
        "ollama_ok":        False,
        "frame_count":      0,
        "processed_count":  0,
        "help_loading":     False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Context Buffer (singleton) ────────────────────────────
@st.cache_resource
def get_buffer():
    return ContextBuffer(db_path="screen_ai_context.db")

buf = get_buffer()
st.session_state.buf = buf


# ── Background Capture Thread ─────────────────────────────
@st.cache_resource
def get_capture_controller():
    return {"running": False, "thread": None}

ctrl = get_capture_controller()

def _capture_loop(buf: ContextBuffer, ctrl: dict):
    cap = ScreenCapture()
    def on_frame(img_bytes):
        desc = describe_screen(img_bytes)
        if desc:
            buf.save(desc)
            ctrl["processed"] = ctrl.get("processed", 0) + 1
        ctrl["frames"] = ctrl.get("frames", 0) + 1

    cap.capture_loop(on_new_frame=on_frame)

def start_capture(buf):
    if not ctrl["running"]:
        ctrl["running"] = True
        ctrl["frames"] = 0
        ctrl["processed"] = 0
        t = threading.Thread(
            target=_capture_loop,
            args=(buf, ctrl),
            daemon=True,
            name="CaptureThread"
        )
        t.start()
        ctrl["thread"] = t


# ── Helper: Add chat message ──────────────────────────────
def add_message(role: str, content: str):
    st.session_state.chat_history.append({
        "role":    role,
        "content": content,
        "time":    datetime.now().strftime("%I:%M %p"),
    })
    # Save to SQLite
    if st.session_state.session_id:
        buf.save_chat(st.session_state.session_id, role, content)


# ── Helper: Trigger Help ──────────────────────────────────
def trigger_help():
    """Ctrl+Shift+H ki tarah kaam karta hai — context padh ke help deta hai."""
    # Naya session banao
    st.session_state.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.chat_history = []
    st.session_state.help_loading = True

    screenshot = take_screenshots()
    img_bytes  = image_to_bytes(screenshot)
    recent     = buf.get_recent(20)

    response = ask_for_help(img_bytes, recent)
    add_message("assistant", response)
    st.session_state.help_loading = False


# ── UI: Top Bar ───────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">👁️ Screen<span>AI</span></div>
    <div class="status-dot"></div>
    <div class="status-text">WATCHING</div>
    <div class="topbar-spacer"></div>
    <div class="hotkey-badge">Ctrl+Shift+H → Help</div>
</div>
""", unsafe_allow_html=True)


# ── UI: Two Column Layout ─────────────────────────────────
left_col, right_col = st.columns([1.1, 3], gap="small")


# ── LEFT: Activity Feed ───────────────────────────────────
with left_col:
    st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📡 Live Activity</div>', unsafe_allow_html=True)

    # Ollama check + capture start
    if not st.session_state.ollama_ok:
        if check_ollama_running():
            st.session_state.ollama_ok = True
            start_capture(buf)

    # Activity entries
    recent_entries = buf.get_recent(30)

    if not recent_entries:
        st.markdown("""
        <div class="no-activity">
            👁️<br>
            Screen watch kar raha hoon...<br>
            Thoda kaam karo, entries<br>
            yahan dikhne lagegi!
        </div>
        """, unsafe_allow_html=True)
    else:
        for entry in recent_entries:
            desc = entry["description"]
            is_error = any(w in desc.lower() for w in ["error", "exception", "failed", "warning"])
            desc_class = "activity-desc error" if is_error else "activity-desc"
            st.markdown(f"""
            <div class="activity-entry">
                <div class="activity-time">{entry['timestamp']}</div>
                <div class="{desc_class}">{desc[:120]}{'...' if len(desc) > 120 else ''}</div>
            </div>
            """, unsafe_allow_html=True)

    # Stats
    stats = buf.stats()
    st.markdown(f"""
    <div style="margin-top:16px; padding-top:12px; border-top:1px solid #1e1e2e;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:10px; color:#334155; line-height:2;">
            ENTRIES: {stats['total_entries']} / 200<br>
            DB: {stats['db_size_kb']} KB<br>
            FRAMES: {ctrl.get('frames', 0)} | PROCESSED: {ctrl.get('processed', 0)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Help button (sidebar mein bhi)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🆘 Ask for Help", key="help_sidebar", disabled=st.session_state.help_loading):
        with st.spinner("Context padh raha hoon..."):
            trigger_help()
        st.rerun()

    if st.button("🗑️ Clear Context", key="clear_ctx"):
        buf.clear()
        st.session_state.chat_history = []
        st.rerun()


# ── RIGHT: Chat Window ────────────────────────────────────
with right_col:

    # Chat messages area
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="chat-empty">
            <div class="chat-empty-icon">👁️</div>
            <div class="chat-empty-text">
                Main teri screen dekh raha hoon...<br>
                Jab problem aaye — <strong style="color:#7c3aed">Ctrl+Shift+H</strong> dabao<br>
                ya neeche ka Help button use karo
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            time_str = msg.get("time", "")

            if role == "assistant":
                st.markdown(f"""
                <div class="msg-row">
                    <div class="msg-avatar ai">🤖</div>
                    <div>
                        <div class="msg-bubble ai">{content}</div>
                        <div class="msg-time">{time_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="msg-row user">
                    <div class="msg-avatar user-av">👤</div>
                    <div>
                        <div class="msg-bubble user">{content}</div>
                        <div class="msg-time">{time_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.help_loading:
        st.markdown("""
        <div class="msg-row">
            <div class="msg-avatar ai">🤖</div>
            <div class="msg-bubble ai">
                <span style="color:#7c3aed">⠋</span> Context padh raha hoon...
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chat Input ─────────────────────────────────────────
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)

    has_chat = bool(st.session_state.chat_history)

    input_col, btn_col = st.columns([5, 1])

    with input_col:
        user_input = st.text_input(
            label="message",
            placeholder="Koi bhi sawaal poochho... (pehle Help button dabao)" if not has_chat
                        else "Aur kuch poochho is error ke baare mein...",
            label_visibility="collapsed",
            key="chat_input",
            disabled=not has_chat,
        )

    with btn_col:
        send_clicked = st.button(
            "Send ↑",
            key="send_btn",
            disabled=not has_chat or not user_input.strip(),
        )

    # Help button (chat area mein bhi)
    if not has_chat:
        if st.button(
            "🆘 Ctrl+Shift+H — Help Maango",
            key="help_main",
            disabled=st.session_state.help_loading
        ):
            with st.spinner("Screen dekh raha hoon aur context padh raha hoon..."):
                trigger_help()
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Handle Send ───────────────────────────────────────
    if send_clicked and user_input.strip():
        add_message("user", user_input)

        # Chat history banao AI ke liye
        history_for_ai = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.chat_history[:-1]  # naya message already add ho gaya
        ]

        with st.spinner("Soch raha hoon..."):
            reply = chat_with_ai(user_input, history_for_ai)

        add_message("assistant", reply)
        st.rerun()


# ── Auto Refresh (activity feed update ke liye) ───────────
time.sleep(0.5)
st.rerun()