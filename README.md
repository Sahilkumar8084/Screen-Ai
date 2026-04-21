<div align="center">

# 👁️ ScreenAI

### An ambient AI that watches your screen and helps you debug in real-time

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-black?style=for-the-badge&logo=ollama)](https://ollama.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![100% Local](https://img.shields.io/badge/100%25-Local%20%26%20Private-purple?style=for-the-badge)]()

<br/>

**ScreenAI** continuously watches your screen, builds context of everything you do, and when you hit a problem — press `Ctrl+Shift+H` and it already knows what went wrong.

<br/>

![ScreenAI Demo](https://placehold.co/900x500/0a0a0f/a78bfa?text=👁️+ScreenAI+—+Your+AI+Pair+Programmer)

</div>

---

## ✨ What It Does

- 📸 **Captures your screen** every 5 seconds with smart change detection (no unnecessary processing)
- 🧠 **Builds context** — a rolling log of everything you've been doing, stored locally in SQLite
- 🆘 **Instant help** — press `Ctrl+Shift+H` anytime and the AI analyzes your full activity history + current screen
- 💬 **Continue the conversation** — chat back and forth to fully resolve the issue
- 🔒 **100% local & private** — everything runs on your machine, nothing sent to the cloud
- 🌐 **Beautiful Streamlit UI** — live activity feed on the left, chat window on the right

---

## 🖥️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Windows 10 | Windows 11 |
| Python | 3.10 | 3.11+ |
| RAM | 8 GB | 16 GB |
| GPU | Any NVIDIA | NVIDIA 6GB+ VRAM |
| Storage | 10 GB free | 20 GB free |
| Ollama | Latest | Latest |

> **GPU is strongly recommended.** Moondream runs in ~1–3 seconds with a GPU. Without one, it may take 15–30 seconds per frame.

---

## 📁 Project Structure

```
ScreenAI/
│
├── 📄 main.py          # Entry point — starts everything
├── 📄 app.py           # Streamlit UI (browser interface)
├── 📄 capture.py       # Screen capture + change detection
├── 📄 ai_engine.py     # Vision AI (Moondream) + Chat AI (LLaMA)
├── 📄 context.py       # SQLite rolling context buffer + chat history
├── 📄 query.py         # Hotkey listener (Ctrl+Shift+H)
│
├── 📂 screenshots/     # Auto-created — processed frames saved here
├── 🗄️ screen_ai_context.db  # Auto-created — SQLite database
│
├── 📄 requirements.txt
└── 📄 README.md
```

---

## ⚙️ Installation — Step by Step

### Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ScreenAI.git
cd ScreenAI
```

### Step 2 — Install Python

Make sure Python 3.10 or higher is installed.

```bash
python --version
# Should show: Python 3.10.x or higher
```

Download Python from [python.org](https://python.org) if needed. ✅ Check **"Add to PATH"** during installation.

### Step 3 — Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 4 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install streamlit mss pillow ollama keyboard pyautogui
```

### Step 5 — Install Ollama

Ollama runs AI models locally on your machine.

1. Go to **[ollama.com](https://ollama.com)**
2. Click **Download for Windows**
3. Run the `.exe` installer
4. Verify installation:

```bash
ollama --version
```

### Step 6 — Download AI Models

ScreenAI uses two models:

| Model | Purpose | Size |
|-------|---------|------|
| `moondream` | Vision — reads your screen | ~1.7 GB |
| `llama3.1:8b` | Chat — understands context & helps | ~4.7 GB |

Download both (one-time, takes a few minutes):

```bash
ollama pull moondream
ollama pull llama3.1:8b
```

Verify models are ready:

```bash
ollama list
# Should show both models
```

---

## 🚀 Running ScreenAI

Make sure your virtual environment is active, then:

```bash
python main.py
```

On first launch you'll see:

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    👁️   S C R E E N   A I   —   Starting Up...             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🔍 Step 1: Ollama aur models check kar raha hoon...
✅ Vision model 'moondream' ready!
✅ Chat model 'llama3.1:8b' ready!

💾 Step 2: Context buffer load kar raha hoon...
   → 0 existing entries mili

📸 Step 3: Pehla screenshot le raha hoon...
   ✅ Screenshot ready! (284.3 KB)

🚀 Step 4: Capture thread shuru kar raha hoon...
   ✅ Capture thread background mein chal raha hai!

⌨️  Step 5: Hotkey listener start kar raha hoon (ctrl+shift+h)...
   ✅ Hotkey active!

🌐 Step 6: Streamlit UI launch kar raha hoon...
   ✅ Streamlit shuru ho gaya!
   🌐 Browser mein kholo: http://localhost:8501
```

Your browser will automatically open `http://localhost:8501` with the ScreenAI interface.

> ⚠️ **Windows Note:** The `keyboard` library requires administrator privileges for hotkeys. Run your terminal as **Administrator** if `Ctrl+Shift+H` doesn't work.

---

## 🎮 How to Use

### Normal workflow

1. **Start ScreenAI** — `python main.py`
2. **Do your work** — code, browse, write, debug — ScreenAI watches silently in the background
3. **Hit a problem?** — press `Ctrl+Shift+H`
4. **AI responds** in the Streamlit chat with full context of what you were doing
5. **Continue chatting** to dig deeper into the solution

### Hotkeys

| Hotkey | Action |
|--------|--------|
| `Ctrl+Shift+H` | Ask for help — AI reads your full context + current screen |

### Streamlit UI

| Button | Action |
|--------|--------|
| `🆘 Ask for Help` | Same as `Ctrl+Shift+H` — triggers AI help |
| `🗑️ Clear Context` | Wipes the activity log and chat history |

---

## 🏗️ How It Works — Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        main.py                              │
│              (Orchestrates everything)                      │
└──────┬───────────────────┬────────────────────┬────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────┐   ┌────────────────┐   ┌───────────────────┐
│  capture.py │   │  ai_engine.py  │   │    context.py     │
│             │   │                │   │                   │
│ • mss       │──▶│ • moondream    │──▶│ • SQLite DB       │
│ • PIL       │   │   (vision)     │   │ • activity_log    │
│ • hash diff │   │ • llama3.1:8b  │   │ • chat_history    │
│ • 5s loop   │   │   (chat)       │   │ • rolling buffer  │
└─────────────┘   └────────────────┘   └───────────────────┘
                                                │
                                                ▼
                                       ┌────────────────┐
                                       │    app.py      │
                                       │                │
                                       │ • Streamlit UI │
                                       │ • Activity feed│
                                       │ • Chat window  │
                                       └────────────────┘
```

### Data Flow

```
Every 5 seconds:
  Screen → Hash check → Pixel diff → Moondream → SQLite

On Ctrl+Shift+H:
  Current screen + Last 20 activities → LLaMA 3.1 → Chat response

Follow-up messages:
  User message + Full chat history → LLaMA 3.1 → Reply
```

### Change Detection (saves ~80% API calls)

```
Screenshot taken
      │
      ▼
Hash check ──── Same hash? ──── YES ──▶ Skip (no change)
      │
      NO
      │
      ▼
Pixel diff ──── < 8% changed? ── YES ──▶ Skip (minor change)
      │
      NO
      │
      ▼
Send to Moondream ──▶ Save to SQLite
```

---

## 🔧 Configuration

All settings are at the top of each file. Common ones you might want to change:

**`capture.py`**
```python
CAPTURE_INTERVAL  = 5     # Seconds between screenshots (increase to save resources)
CAPTURE_THRESHOLD = 0.08  # 8% pixel change needed to process (increase to be less sensitive)
SAVE_SCREENSHOTS  = True  # Set False to not save frames to disk
```

**`ai_engine.py`**
```python
VISION_MODEL = "moondream"    # Change to "llava" for better quality
CHAT_MODEL   = "llama3.1:8b" # Change to "llama3.1:70b" for smarter responses
```

**`context.py`**
```python
MAX_ENTRIES     = 200  # Max activity entries to keep in DB
RECENT_FOR_HELP = 20   # How many recent entries to send with help request
```

**`main.py`**
```python
STREAMLIT_PORT = 8501  # Change if port is already in use
HOTKEY         = "ctrl+shift+h"  # Change hotkey if needed
```

---

## ❗ Troubleshooting

**`keyboard` hotkey not working**
> Run your terminal as Administrator (right-click → Run as administrator)

**`ollama` connection error**
> Make sure Ollama is running. Open a new terminal and run: `ollama serve`

**Moondream giving poor screen descriptions**
> Try `llava` instead — better quality at the cost of more VRAM:
> ```bash
> ollama pull llava
> ```
> Then change `VISION_MODEL = "llava"` in `ai_engine.py`

**App running slow / GPU not being used**
> Check CUDA is working:
> ```bash
> ollama run moondream "hello"
> ```
> Check GPU usage in Task Manager → Performance → GPU

**Port 8501 already in use**
> Change `STREAMLIT_PORT = 8502` in `main.py`

**`mss` screenshot error on multiple monitors**
> In `capture.py`, change `sct.monitors[1]` to `sct.monitors[0]` (captures all screens combined)

---

## 📦 requirements.txt

```
streamlit>=1.32.0
mss>=9.0.1
Pillow>=10.0.0
ollama>=0.2.0
keyboard>=0.13.5
pyautogui>=0.9.54
```

---

## 🗺️ Roadmap

- [ ] Auto-detect errors without needing `Ctrl+Shift+H`
- [ ] OCR support for better text extraction from screenshots  
- [ ] Export chat sessions as markdown
- [ ] Support for multiple monitors
- [ ] macOS & Linux hotkey support
- [ ] Faster local vision model options (e.g., Moondream2)
- [ ] Voice output for AI responses

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ using [Ollama](https://ollama.com) · [Streamlit](https://streamlit.io) · [Moondream](https://moondream.ai) · [LLaMA 3.1](https://llama.meta.com)

**Star ⭐ the repo if this helped you!**

</div>
