"""
main.py — Screen AI ka entry point
Yeh file sab kuch shuru karti hai:
  1. Ollama + models check
  2. Context buffer ready
  3. Streamlit app launch (subprocess mein)
  4. Hotkey listener background mein
"""

import sys
import os
import time
import threading
import subprocess
import signal
from datetime import datetime

# ── Try imports — helpful error agar koi library missing hai ──
try:
    import keyboard
except ImportError:
    print("❌ 'keyboard' library nahi mili. Run karo: pip install keyboard")
    sys.exit(1)

try:
    from capture import take_screenshots, image_to_bytes
    from ai_engine import check_ollama_running, ask_for_help, describe_screen
    from context import ContextBuffer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("   Make sure capture.py, ai_engine.py, context.py isi folder mein hain.")
    sys.exit(1)


# ── Settings ──────────────────────────────────────────────────
STREAMLIT_PORT  = 8501
HOTKEY          = "ctrl+shift+h"
DB_PATH         = "screen_ai_context.db"
APP_FILE        = "app.py"


# ── Banner ────────────────────────────────────────────────────
def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    👁️   S C R E E N   A I   —   Starting Up...             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")


# ── Step 1: Check Ollama ──────────────────────────────────────
def step_check_ollama() -> bool:
    print("🔍 Step 1: Ollama aur models check kar raha hoon...")
    ok = check_ollama_running()
    if not ok:
        print("""
❌ Ollama ready nahi hai. Yeh karo:

   1. Ollama install karo  → https://ollama.com
   2. CMD mein run karo:
        ollama pull moondream
        ollama pull llama3.1:8b
   3. Phir main.py dobara chalao.
""")
    return ok


# ── Step 2: Context Buffer ────────────────────────────────────
def step_init_buffer() -> ContextBuffer:
    print("\n💾 Step 2: Context buffer load kar raha hoon...")
    buf = ContextBuffer(db_path=DB_PATH)
    stats = buf.stats()
    print(f"   → {stats['total_entries']} existing entries mili")
    return buf


# ── Step 3: Pehla Screenshot ─────────────────────────────────
def step_first_screenshot() -> bytes | None:
    print("\n📸 Step 3: Pehla screenshot le raha hoon...")
    try:
        img = take_screenshots()
        img_bytes = image_to_bytes(img)
        print(f"   ✅ Screenshot ready! ({len(img_bytes) / 1024:.1f} KB)")
        return img_bytes
    except Exception as e:
        print(f"   ⚠️  Screenshot nahi aayi: {e}")
        return None


# ── Step 4: Background Capture Thread ────────────────────────
def step_start_capture_thread(buf: ContextBuffer):
    """
    Background mein ek thread chalao jo:
      - Har 5 second mein screenshot le
      - Change detect kare
      - Moondream se describe karwaye
      - SQLite mein save kare
    """
    print("\n🚀 Step 4: Capture thread shuru kar raha hoon...")

    from capture import ScreenCapture

    def on_frame(img_bytes: bytes):
        desc = describe_screen(img_bytes)
        if desc:
            buf.save(desc)

    def run():
        cap = ScreenCapture()
        try:
            cap.capture_loop(on_new_frame=on_frame)
        except Exception as e:
            print(f"\n⚠️  Capture thread error: {e}")

    t = threading.Thread(target=run, daemon=True, name="CaptureThread")
    t.start()
    print("   ✅ Capture thread background mein chal raha hai!")
    return t


# ── Step 5: Hotkey Listener ───────────────────────────────────
def step_start_hotkey_listener(buf: ContextBuffer):
    """
    Ctrl+Shift+H sunne ke liye background listener.
    Jab dabaya — latest context padh ke terminal mein print karo.
    (Streamlit UI mein bhi dikhega kyunki woh SQLite se read karta hai)
    """
    print(f"\n⌨️  Step 5: Hotkey listener start kar raha hoon ({HOTKEY})...")

    _busy = threading.Event()

    def on_hotkey():
        if _busy.is_set():
            print("\n⏳ Pehli request abhi chal rahi hai, thoda ruko...")
            return

        _busy.set()
        print(f"\n{'─' * 60}")
        print(f"🆘 Help request — {datetime.now().strftime('%I:%M:%S %p')}")
        print(f"{'─' * 60}")

        try:
            screenshot = take_screenshots()
            img_bytes  = image_to_bytes(screenshot)
            recent     = buf.get_recent(20)

            print("   🧠 Context padh raha hoon aur response bana raha hoon...")
            response = ask_for_help(img_bytes, recent)

            print(f"\n🤖 AI Response:\n{'─' * 40}")
            print(response)
            print(f"{'─' * 40}")
            print("💡 Streamlit UI mein bhi chat kar sakte ho!\n")

        except Exception as e:
            print(f"❌ Help error: {e}")
        finally:
            _busy.clear()

    keyboard.add_hotkey(HOTKEY, on_hotkey)
    print(f"   ✅ Hotkey active! '{HOTKEY}' dabao help ke liye.")


# ── Step 6: Launch Streamlit ──────────────────────────────────
def step_launch_streamlit() -> subprocess.Popen | None:
    """
    app.py ko streamlit se launch karo — browser mein khulega.
    """
    print(f"\n🌐 Step 6: Streamlit UI launch kar raha hoon...")

    # app.py exist karta hai?
    if not os.path.exists(APP_FILE):
        print(f"   ⚠️  '{APP_FILE}' nahi mila — Streamlit UI skip kar raha hoon.")
        print(f"   Terminal aur hotkey still kaam karenge!")
        return None

    try:
        proc = subprocess.Popen(
            [
                sys.executable, "-m", "streamlit", "run", APP_FILE,
                "--server.port", str(STREAMLIT_PORT),
                "--server.headless", "false",
                "--browser.gatherUsageStats", "false",
            ],
            # stdout/stderr inherit karo taaki errors dikh sakein
        )
        print(f"   ✅ Streamlit shuru ho gaya!")
        print(f"   🌐 Browser mein kholo: http://localhost:{STREAMLIT_PORT}")
        return proc

    except FileNotFoundError:
        print("   ❌ Streamlit install nahi hai. Run karo: pip install streamlit")
        return None
    except Exception as e:
        print(f"   ❌ Streamlit launch nahi hua: {e}")
        return None


# ── Clean Shutdown ────────────────────────────────────────────
def setup_shutdown(streamlit_proc: subprocess.Popen | None):
    """Ctrl+C ya SIGTERM par sab kuch cleanly band karo."""

    def shutdown(sig=None, frame=None):
        print("\n\n🛑 Screen AI band ho raha hai...")
        keyboard.unhook_all()

        if streamlit_proc and streamlit_proc.poll() is None:
            print("   → Streamlit band kar raha hoon...")
            streamlit_proc.terminate()
            try:
                streamlit_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                streamlit_proc.kill()

        print("   ✅ Sab kuch cleanly band ho gaya. Bye! 👋\n")
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    return shutdown


# ── Main ──────────────────────────────────────────────────────
def main():
    print_banner()

    # ── 1. Ollama check
    if not step_check_ollama():
        sys.exit(1)

    # ── 2. Context buffer
    buf = step_init_buffer()

    # ── 3. Pehla screenshot (warm-up)
    step_first_screenshot()

    # ── 4. Capture thread (background)
    step_start_capture_thread(buf)

    # ── 5. Hotkey listener (background)
    step_start_hotkey_listener(buf)

    # ── 6. Streamlit launch
    streamlit_proc = step_launch_streamlit()

    # ── Shutdown handler register karo
    shutdown_fn = setup_shutdown(streamlit_proc)

    # ── Ready!
    print(f"""
{'═' * 62}
  ✅  Screen AI fully ready hai!

  👁️   Screen watch ho rahi hai (har 5 sec)
  ⌨️   Hotkey: {HOTKEY} → terminal mein help
  🌐  Streamlit UI: http://localhost:{STREAMLIT_PORT}

  Ctrl+C dabao band karne ke liye
{'═' * 62}
""")

    # ── Keep alive loop
    try:
        while True:
            # Streamlit crash ho gayi toh batao
            if streamlit_proc and streamlit_proc.poll() is not None:
                print("⚠️  Streamlit band ho gayi! Dobara start kar raha hoon...")
                streamlit_proc = step_launch_streamlit()
                setup_shutdown(streamlit_proc)  # naye proc ke liye handler update karo

            time.sleep(5)

    except KeyboardInterrupt:
        shutdown_fn()


if __name__ == "__main__":
    main()