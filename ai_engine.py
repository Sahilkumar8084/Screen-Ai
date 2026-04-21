# import ollama
# import base64
# import time
# from datetime import datetime

# # import mss
# # import time
# # from PIL import Image
# # import hashlib
# # import os
# # import io

# #__________Settings__________________

# MODEL_NAME= "llama3.1:8b"
# MAX_RETRIES = 3
# RETRY_DELAY = 2
# #___________________________________________



# DESCRIBE_PROMPT = """You are an AI assistant watching a user's screen.
# Describe what the user is currently doing in 2-3 short sentences.
# Focus on:
# - Which app or website is open
# - What the user is working on (code, writing, browsing, etc.)
# - Any visible errors, warnings, or important text
 
# Be concise and factual. Do not make assumptions beyond what's visible."""
 
# HELP_PROMPT_TEMPLATE = """You are an AI assistant that has been watching the user's screen.
 
# Here is the recent activity context (newest first):
# {context}
 
# Current screen description:
# {current}
 
# The user is asking for help. Based on everything you can see:
# 1. What is the user trying to do?
# 2. What might be the issue or error?
# 3. What should they do next?
 
# Give a clear, helpful response."""


# def image_bytes_to_base64(img_bytes: bytes)->str:
#     "Image Bytes ko Hum BAse 64 me convert kar rhe hia basically image ko text representation me convert karna"
    
#     return base64.b64encode(img_bytes).decode("utf-8")


# def describe_screen(img_bytes: bytes) -> str | None:
#     """
#     Moondream ko screenshot bhejo aur screen description lo.
    
#     Args:
#         img_bytes: PNG format mein screenshot bytes
        
#     Returns:
#         Description string ya None agar error aaye
#     """
#     for attempt in range(1, MAX_RETRIES + 1):
#         try:
#             print(f"   🤖 Moondream ko bhej raha hoon... (attempt {attempt})")
            
#             start = time.time()
            
#             response = ollama.chat(
#                 model=MODEL_NAME,
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": DESCRIBE_PROMPT,
#                         "images": [img_bytes],  # bytes directly pass karo
#                     }
#                 ],
#             )
            
#             elapsed = time.time() - start
#             description = response["message"]["content"].strip()
            
#             print(f"   ✅ Done! ({elapsed:.1f}s) — {description[:80]}...")
#             return description
 
#         except ollama.ResponseError as e:
#             print(f"   ❌ Ollama error (attempt {attempt}): {e}")
#             if attempt < MAX_RETRIES:
#                 time.sleep(RETRY_DELAY)
#         except Exception as e:
#             print(f"   ❌ Unexpected error (attempt {attempt}): {e}")
#             if attempt < MAX_RETRIES:
#                 time.sleep(RETRY_DELAY)
 
#     print("   ⚠️  Sab retries fail ho gayi, skipping this frame.")
#     return None
 
# # from capture import image_to_bytes

# # from PIL import Image
# # img = Image.open("test.png")

# # img_bytes = image_to_bytes(img)

# # print(describe_screen(img_bytes))


# def ask_for_help(img_bytes: bytes, context_entries: list[dict]) -> str:
#     """
#     Jab user Ctrl+Shift+H dabaaye — full context ke saath help maango.
    
#     Args:
#         img_bytes: Current screenshot
#         context_entries: Last N activity entries from SQLite
        
#     Returns:
#         AI ka helpful response
#     """
#     # Context format karo — newest first
#     if context_entries:
#         context_lines = []
#         for entry in context_entries:
#             ts = entry.get("timestamp", "")
#             desc = entry.get("description", "")
#             context_lines.append(f"[{ts}] {desc}")
#         context_str = "\n".join(context_lines)
#     else:
#         context_str = "No previous activity recorded yet."
 
#     # Current screen describe karo pehle
#     print("   📸 Current screen describe kar raha hoon...")
#     current_desc = describe_screen(img_bytes) or "Could not describe current screen."
 
#     # Ab full help prompt bhejo
#     help_prompt = HELP_PROMPT_TEMPLATE.format(
#         context=context_str,
#         current=current_desc,
#     )
 
#     print("   🧠 Help generate kar raha hoon...")
 
#     try:
#         start = time.time()
#         response = ollama.chat(
#             model=MODEL_NAME,
#             messages=[
#                 {
#                     "role": "user",
#                     "content": help_prompt,
#                     "images": [img_bytes],
#                 }
#             ],
#         )
#         elapsed = time.time() - start
#         answer = response["message"]["content"].strip()
#         print(f"   ✅ Help ready! ({elapsed:.1f}s)")
#         return answer
 
#     except Exception as e:
#         return f"Error getting help: {e}"
 
 
# def check_ollama_running()->bool:
#     """check the Ollama is  Running or not"""
    
#     try:
#         models = ollama.list()
#         # print(models)
#         models_name = [m.model for m in models.models] 
        
#         if not any(MODEL_NAME in name for name in models_name):
#             print(f"⚠️  '{MODEL_NAME}' model nahi mila!")
#             print(f"   Yeh command run karo: ollama pull {MODEL_NAME} Ya ollama check karo")
#             return False
        
#         print(f"✅ Ollama chal raha hai | Model '{MODEL_NAME}' ready!")
#         return True
 
#     except Exception as e:
#         print(f"❌ Ollama se connect nahi ho pa raha: {e}")
#         print("   Make sure Ollama running hai — ollama serve")
#         return False
    
    
# if __name__=="__main__":
    
#     print("=== AI Engine Test ===\n")
    
#     # Checking the Olllama
#     if not  check_ollama_running():
#         exit(1)
        
#     print("\n📸 Screenshot le raha hoon...")
#     from capture import take_screenshots, image_to_bytes    
    
#     screenshots = take_screenshots()
#     img_bytes = image_to_bytes(screenshots)
#     print(f"   Screenshot size: {len(img_bytes) / 1024:.1f} KB")
 
#     print("\n🤖 Moondream se description maang raha hoon...")
#     desc = describe_screen(img_bytes)
    
     
#     if desc:
#         print(f"\n📝 Screen Description:\n{desc}")
#     else:
#         print("❌ Description nahi mili.")

        
import ollama
import base64
import time
from datetime import datetime

# ── Settings ──────────────────────────────────────────────
VISION_MODEL = "moondream"       # Screen describe karne ke liye (vision model)
CHAT_MODEL   = "llama3.1:8b"    # Chat karne ke liye (text model) ✅ tera model sahi hai yahan
MAX_RETRIES  = 3
RETRY_DELAY  = 2
# ──────────────────────────────────────────────────────────


# ── Prompts ───────────────────────────────────────────────

DESCRIBE_PROMPT = """You are an AI assistant observing a user's screen.

Your task is to describe what is clearly visible on the screen in 5–6 concise sentences.

Follow these steps:
1. Identify the active application, website, or interface.
2. Describe what the user appears to be doing (e.g., coding, writing, browsing), based only on visible evidence.
3. Mention any visible errors, warnings, or notable text exactly as shown.
4. Prioritise the most relevant on-screen elements; ignore minor or unclear details.
5. If any part of the screen is unclear, ambiguous, or unreadable, explicitly state that uncertainty instead of guessing.

Constraints:
- Be factual and objective.
- Do not infer intent beyond what is visible.
- Keep sentences short and precise.
"""

HELP_SYSTEM_PROMPT = """You are a helpful AI assistant observing the user’s screen activity.

You have access to recent visible context of what the user has been doing.

When the user asks for help, follow these steps:
1. Infer the user’s goal based on recent visible actions and current screen state.
2. Identify any clear errors, warnings, or issues visible on the screen.
3. Provide specific, actionable steps to resolve the issue or achieve the goal.
4. Prioritise the most relevant and recent context; ignore unrelated past activity.
5. If the goal or issue is unclear, briefly state your assumption or ask for clarification instead of guessing.

Constraints:
- Be concise, clear, and practical.
- Do not invent errors or context that are not visible.
- Match the user’s language and tone.
"""
FIRST_HELP_TEMPLATE = """I have been watching your screen. Here is your recent activity (newest first):

{context}

Current screen:
{current}

Based on what I can see, please help the user understand:
1. What they are currently doing
2. Any errors or issues visible
3. What they should do next"""


# ── Screen Description ─────────────────────────────────────

def describe_screen(img_bytes: bytes) -> str | None:
    """
    Vision model ko screenshot bhejo aur description lo.
    Moondream image dekh sakta hai — llama3.1 nahi dekh sakta.

    Args:
        img_bytes: PNG format mein screenshot bytes

    Returns:
        Description string ya None agar error aaye
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"   👁️  Vision model ko bhej raha hoon... (attempt {attempt})")

            start = time.time()

            response = ollama.chat(
                model=VISION_MODEL,          # ✅ moondream — images dekh sakta hai
                messages=[
                    {
                        "role":    "user",
                        "content": DESCRIBE_PROMPT,
                        "images":  [img_bytes],
                    }
                ],
            )

            elapsed = time.time() - start
            description = response["message"]["content"].strip()

            print(f"   ✅ Done! ({elapsed:.1f}s) — {description[:80]}...")
            return description

        except ollama.ResponseError as e:
            print(f"   ❌ Ollama error (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"   ❌ Unexpected error (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    print("   ⚠️  Sab retries fail ho gayi, skipping this frame.")
    return None


# ── First Help Message ────────────────────────────────────

def ask_for_help(img_bytes: bytes, context_entries: list[dict]) -> str:
    """
    Ctrl+Shift+H dabane par — context padh ke pehla help message generate karo.
    Yeh chat ka pehla message hoga.

    Args:
        img_bytes       : Current screenshot
        context_entries : Recent activity entries from SQLite

    Returns:
        AI ka pehla help response (string)
    """
    # Context format karo
    if context_entries:
        context_lines = [
            f"[{e.get('timestamp', '')}] {e.get('description', '')}"
            for e in context_entries
        ]
        context_str = "\n".join(context_lines)
    else:
        context_str = "No previous activity recorded yet."

    # Pehle current screen describe karo (vision model se)
    print("   📸 Current screen describe kar raha hoon...")
    current_desc = describe_screen(img_bytes) or "Could not describe current screen."

    # Help prompt banao
    help_prompt = FIRST_HELP_TEMPLATE.format(
        context=context_str,
        current=current_desc,
    )

    print("   🧠 Pehla help message generate kar raha hoon...")

    try:
        start = time.time()

        response = ollama.chat(
            model=CHAT_MODEL,               # ✅ llama3.1 — text reasoning ke liye
            messages=[
                {"role": "system", "content": HELP_SYSTEM_PROMPT},
                {"role": "user",   "content": help_prompt},
            ],
        )

        elapsed = time.time() - start
        answer = response["message"]["content"].strip()
        print(f"   ✅ Help ready! ({elapsed:.1f}s)")
        return answer

    except Exception as e:
        return f"Error getting help: {e}"


# ── Chat Function ─────────────────────────────────────────

def chat_with_ai(user_message: str, chat_history: list[dict]) -> str:
    """
    User ke saath ongoing chat karo — puri history ke saath.
    Ctrl+Shift+H ke baad ka conversation yahan handle hota hai.

    Args:
        user_message : User ka naya message
        chat_history : Puri conversation history
                       [{"role": "user"/"assistant", "content": "..."}]

    Returns:
        AI ka response string
    """
    print(f"   💬 Chat response generate kar raha hoon...")

    # Messages list banao — system prompt + history + naya message
    messages = [{"role": "system", "content": HELP_SYSTEM_PROMPT}]

    # Pehle se jo conversation hui hai woh add karo
    for msg in chat_history:
        messages.append({
            "role":    msg["role"],
            "content": msg["content"],
        })

    # User ka naya message add karo
    messages.append({"role": "user", "content": user_message})

    try:
        start = time.time()

        response = ollama.chat(
            model=CHAT_MODEL,
            messages=messages,
        )

        elapsed = time.time() - start
        answer = response["message"]["content"].strip()
        print(f"   ✅ Chat response ready! ({elapsed:.1f}s)")
        return answer

    except Exception as e:
        return f"Error in chat: {e}"


# ── Ollama Check ──────────────────────────────────────────

def check_ollama_running() -> bool:
    """Check karo ki Ollama chal raha hai aur dono models available hain."""
    try:
        models = ollama.list()
        model_names = [m.model for m in models.models]   # ✅ tera fix sahi tha

        all_good = True

        # Vision model check
        if not any(VISION_MODEL in name for name in model_names):
            print(f"⚠️  Vision model '{VISION_MODEL}' nahi mila!")
            print(f"   Run karo: ollama pull {VISION_MODEL}")
            all_good = False
        else:
            print(f"✅ Vision model '{VISION_MODEL}' ready!")

        # Chat model check
        if not any(CHAT_MODEL in name for name in model_names):
            print(f"⚠️  Chat model '{CHAT_MODEL}' nahi mila!")
            print(f"   Run karo: ollama pull {CHAT_MODEL}")
            all_good = False
        else:
            print(f"✅ Chat model '{CHAT_MODEL}' ready!")

        return all_good

    except Exception as e:
        print(f"❌ Ollama se connect nahi ho pa raha: {e}")
        print("   Make sure Ollama running hai — ollama serve")
        return False


# ── Quick Test ────────────────────────────────────────────
if __name__ == "__main__":
    print("=== AI Engine Test ===\n")

    # Step 1: Ollama check
    if not check_ollama_running():
        exit(1)

    # Step 2: Screenshot lo aur describe karo
    print("\n📸 Screenshot le raha hoon...")
    from capture import take_screenshots, image_to_bytes

    screenshot = take_screenshots()
    img_bytes = image_to_bytes(screenshot)
    print(f"   Screenshot size: {len(img_bytes) / 1024:.1f} KB")

    # Step 3: Screen describe karo
    print("\n👁️  Screen describe kar raha hoon...")
    desc = describe_screen(img_bytes)

    if desc:
        print(f"\n📝 Screen Description:\n{desc}")
    else:
        print("❌ Description nahi mili.")
        exit(1)

    # Step 4: Chat test
    print("\n💬 Chat test kar raha hoon...")
    fake_history = [
        {"role": "assistant", "content": desc},
    ]
    reply = chat_with_ai("Isme koi error hai kya?", fake_history)
    print(f"\n🤖 Chat Reply:\n{reply}")