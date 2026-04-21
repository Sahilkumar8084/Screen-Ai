# import keyboard
# import threading
# import time
# from datetime import datetime
# from capture import take_screenshots, image_to_bytes
# from ai_engine import ask_for_help
# from context import ContextBuffer

# #___Settings__________
# HELP_HOTKEY = "ctrl+shift+h"       # Yeh dabao help maangne ke liye
# CLEAR_HOTKEY = "ctrl+shift+c"      # Context clear karne ke liye
# STATS_HOTKEY = "ctrl+shift+s"      # Stats dekhne ke liye
# # ──────────────────────────────────────────────────────────

# def print_banner():
#     """Startup pe sundar banner print karo."""
#     print("""
# ╔══════════════════════════════════════════════════════╗
# ║           🤖 Screen AI — Query System Ready          ║
# ╠══════════════════════════════════════════════════════╣
# ║  Ctrl+Shift+H  →  Help maango (AI se poochho)       ║
# ║  Ctrl+Shift+S  →  Stats dekho                       ║
# ║  Ctrl+Shift+C  →  Context clear karo                ║
# ║  Ctrl+C        →  Band karo                         ║
# ╚══════════════════════════════════════════════════════╝
# """)
    
# def print_help_response(response: str, timestamp: str):
#     """AI ka help response sundar format mein print karo."""
#     print("\n" + "═" * 60)
#     print(f"🤖 AI HELP  [{timestamp}]")
#     print("═" * 60)
#     print(response)
#     print("═" * 60 + "\n")\
        
# def print_stats(buf: ContextBuffer):
#     """Context buffer ki stats print karo."""
#     s = buf.stats()
#     print(f"""
# 📊 Context Buffer Stats:
#    Total entries : {s['total_entries']}
#    Oldest entry  : {s['oldest'] or 'N/A'}
#    Newest entry  : {s['newest'] or 'N/A'}
#    DB size       : {s['db_size_kb']} KB
# """)

    
# class QuerySystem:
#     def __init__(self,context_buffer: ContextBuffer):
#         self.buf = context_buffer
#         self.is_processing=False
#         self._stop_event = threading.Event()
        
#     #_____HOTKEYS__________
    
#     def _handle_help(self):
#         """Ctrl+Shift+H dabane par yeh chalta hai."""

#         if self.is_processing:
#             print("\n⏳ Pehle wali request abhi chal rahi hai, thoda ruko...")
#             return
#         thread = threading.Thread(target=self._process_help,daemon=True)
#         thread.start()
        
        
#     def _process_help(self):
#         self.is_processing=True
#         timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

#         try:
#             print(f"\n🆘 Help request [{timestamp}] — processing...")

#             # 1. Current screenshot lo
#             print("   📸 Screen capture kar raha hoon...")
#             screenshot = take_screenshots()
#             img_bytes = image_to_bytes(screenshot)

#             # 2. Recent context lo
#             print("   📋 Context load kar raha hoon...")
#             recent_entries = self.buf.get_recent()
#             print(f"   → {len(recent_entries)} recent entries mili")

#             # 3. AI se help maango
#             response = ask_for_help(img_bytes, recent_entries)

#             # 4. Response print karo
#             print_help_response(response, timestamp)

#         except Exception as e:
#             print(f"\n❌ Help request mein error: {e}")

#         finally:
#             self.is_processing = False
            
#     def _handle_stats(self):
#         """Ctrl+Shift+S dabane par stats print karo."""
#         print_stats(self.buf)
#         self.buf.print_recent(n=3)

#     def _handle_clear(self):
#         """Ctrl+Shift+C dabane par context clear karo."""
#         confirm = input("\n⚠️  Saara context delete karna chahte ho? (y/n): ").strip().lower()
#         if confirm == "y":
#             self.buf.clear()
#             print("✅ Context clear ho gaya!")
#         else:
#             print("❌ Cancel kar diya.")
            
# #_______This is the Main Loop_________

            
#     def start(self):
#         ''' HotKeys register karo aur login karna suru karo and press Ctrl+C to Stop this Loop'''
        
#         print_banner()
#                 # Hotkeys register karo
#         keyboard.add_hotkey(HELP_HOTKEY,  self._handle_help,  suppress=True)
#         keyboard.add_hotkey(STATS_HOTKEY, self._handle_stats, suppress=True)
#         keyboard.add_hotkey(CLEAR_HOTKEY, self._handle_clear, suppress=True)

#         print(f"⌨️  Hotkeys active! '{HELP_HOTKEY}' dabao help ke liye.\n")

#         try:
#             # Sirf wait karo — hotkeys background mein kaam karte hain
#             while not self._stop_event.is_set():
#                 time.sleep(0.1)

#         except KeyboardInterrupt:
#             print("\n🛑 Query system band ho raha hai...")

#         finally:
#             keyboard.unhook_all()
#             print("✅ Hotkeys unregistered.") 
            
#     def stop(self):
#         """ Query System Bannd karne ke liye...""" 
#         self._stop_event().set() 
        
        
# #_________QUICK TEST ____________
# if __name__ == "__main__":
#     print("=== Query System Test ===")
#     print("Note: Is test mein actual AI call nahi hoga.")
#     print("      Sirf hotkey detection test hoga.\n")

#     # Fake context buffer ke saath test karo
#     buf = ContextBuffer(db_path="test_query.db")

#     # Kuch fake entries daalo
#     buf.save("User has VS Code open with main.py file.")
#     buf.save("User is writing a Python function for data processing.")
#     buf.save("Terminal shows SyntaxError on line 42.")

#     print("✅ Context buffer ready with 3 fake entries.")
#     print(f"\nAb '{HELP_HOTKEY}' dabao — test response dikhega.")
#     print("Ctrl+C dabao band karne ke liye.\n")

#     # Override _process_help for testing (no actual AI call)
#     def fake_help(self):
#         self.is_processing = True
#         timestamp = datetime.now().strftime("%H:%M:%S")
#         fake_response = """1. Kya kar raha hai user:
#    User Python code likh raha hai VS Code mein.

# 2. Issue kya lag raha hai:
#    Line 42 par SyntaxError hai terminal mein.

# 3. Kya karna chahiye:
#    → Line 42 check karo — missing colon, bracket ya indentation hogi.
#    → `python -m py_compile main.py` run karo errors dekhne ke liye."""

#         print_help_response(fake_response, timestamp)
#         self.is_processing = False

#     import types
#     qs = QuerySystem(buf)
#     qs._process_help = types.MethodType(fake_help, qs)
#     qs.start()

#     # Cleanup
#     import os
#     if os.path.exists("test_query.db"):
#         os.remove("test_query.db")



import sqlite3
import json
from datetime import datetime
from pathlib import Path

# ── Settings ──────────────────────────────────────────────
DB_PATH = "screen_ai_context.db"
MAX_ENTRIES = 200
RECENT_FOR_HELP = 20
# ──────────────────────────────────────────────────────────


class ContextBuffer:

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()          # ✅ Fix: pehle double underscore galat tha
        print(f"✅ Context buffer ready! Database: '{self.db_path}'")

    # ── Database Setup ─────────────────────────────────────

    def _init_db(self):
        """Database aur tables banao agar exist nahi karte."""
        with self._connect() as conn:                   # ✅ Fix: sab andar hai ab
            conn.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp   TEXT NOT NULL,
                    description TEXT NOT NULL,
                    extra       TEXT DEFAULT '{}'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON activity_log (timestamp DESC)
            """)

            # ── NAYA: Chat history table ──────────────────
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  TEXT NOT NULL,
                    role        TEXT NOT NULL,
                    content     TEXT NOT NULL,
                    timestamp   TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session
                ON chat_history (session_id, id ASC)
            """)
            conn.commit()                               # ✅ Fix: commit andar tha

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn                                     # ✅ Fix: return sahi indent mein

    # ── Activity Log: Write ────────────────────────────────

    def save(self, description: str, extra: dict = None) -> int:
        """Screen description SQLite mein save karo."""
        timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        extra_json = json.dumps(extra or {})

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO activity_log (timestamp, description, extra) VALUES (?, ?, ?)",
                (timestamp, description, extra_json),
            )
            new_id = cursor.lastrowid
            conn.commit()

        print(f"   💾 Saved entry #{new_id} at {timestamp}")
        self._cleanup()
        return new_id

    def _cleanup(self):
        """MAX_ENTRIES se zyada hone par purani entries delete karo."""
        with self._connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM activity_log").fetchone()[0]

            if count > MAX_ENTRIES:
                to_delete = count - MAX_ENTRIES
                conn.execute("""
                    DELETE FROM activity_log
                    WHERE id IN (
                        SELECT id FROM activity_log
                        ORDER BY id ASC
                        LIMIT ?
                    )
                """, (to_delete,))
                conn.commit()
                print(f"   🧹 {to_delete} purani entries delete ki (limit: {MAX_ENTRIES})")

    # ── Activity Log: Read ─────────────────────────────────

    def get_recent(self, n: int = RECENT_FOR_HELP) -> list[dict]:
        """Recent N activity entries lo — newest first."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT id, timestamp, description, extra
                FROM activity_log
                ORDER BY id DESC
                LIMIT ?
            """, (n,)).fetchall()

        return [
            {
                "id":          row["id"],
                "timestamp":   row["timestamp"],
                "description": row["description"],
                "extra":       json.loads(row["extra"]),
            }
            for row in rows
        ]

    def get_all(self) -> list[dict]:
        """Saari activity entries lo — oldest first."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT id, timestamp, description, extra
                FROM activity_log
                ORDER BY id ASC
            """).fetchall()

        return [
            {
                "id":          row["id"],
                "timestamp":   row["timestamp"],
                "description": row["description"],
                "extra":       json.loads(row["extra"]),
            }
            for row in rows
        ]

    def search(self, keyword: str) -> list[dict]:
        """Description mein keyword search karo."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT id, timestamp, description, extra
                FROM activity_log
                WHERE LOWER(description) LIKE LOWER(?)
                ORDER BY id DESC
            """, (f"%{keyword}%",)).fetchall()

        return [
            {
                "id":          row["id"],
                "timestamp":   row["timestamp"],
                "description": row["description"],
                "extra":       json.loads(row["extra"]),
            }
            for row in rows
        ]

    # ── Chat History: Write ────────────────────────────────

    def save_chat(self, session_id: str, role: str, content: str) -> int:
        """
        Ek chat message save karo.

        Args:
            session_id : Unique session ID (har Ctrl+Shift+H press ka alag session)
            role       : 'user' ya 'assistant'
            content    : Message content

        Returns:
            Naye message ka ID
        """
        timestamp = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO chat_history (session_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
                (session_id, role, content, timestamp),
            )
            new_id = cursor.lastrowid
            conn.commit()

        return new_id

    def get_chat_history(self, session_id: str) -> list[dict]:
        """
        Ek session ki poori chat history lo — oldest first.

        Args:
            session_id: Jis session ki history chahiye

        Returns:
            List of {role, content, timestamp}
        """
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT role, content, timestamp
                FROM chat_history
                WHERE session_id = ?
                ORDER BY id ASC
            """, (session_id,)).fetchall()

        return [
            {
                "role":      row["role"],
                "content":   row["content"],
                "timestamp": row["timestamp"],
            }
            for row in rows
        ]

    def get_all_sessions(self) -> list[str]:
        """Saare unique session IDs lo — newest first."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT DISTINCT session_id, MIN(timestamp) as started
                FROM chat_history
                GROUP BY session_id
                ORDER BY started DESC
            """).fetchall()

        return [row["session_id"] for row in rows]

    def clear_chat(self, session_id: str = None):
        """
        Chat history clear karo.
        session_id diya → sirf us session ki
        session_id nahi diya → saari chat history
        """
        with self._connect() as conn:
            if session_id:
                conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
                print(f"🗑️  Session '{session_id}' ki chat clear!")
            else:
                conn.execute("DELETE FROM chat_history")
                print("🗑️  Saari chat history clear!")
            conn.commit()

    # ── Stats ──────────────────────────────────────────────

    def stats(self) -> dict:
        """Database ke baare mein basic stats lo."""
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM activity_log").fetchone()[0]
            oldest = conn.execute(
                "SELECT timestamp FROM activity_log ORDER BY id ASC LIMIT 1"
            ).fetchone()
            newest = conn.execute(
                "SELECT timestamp FROM activity_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
            total_chats = conn.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
            total_sessions = conn.execute(
                "SELECT COUNT(DISTINCT session_id) FROM chat_history"
            ).fetchone()[0]

        return {
            "total_entries":   total,
            "oldest":          oldest[0] if oldest else None,
            "newest":          newest[0] if newest else None,
            "db_size_kb":      round(Path(self.db_path).stat().st_size / 1024, 1)
                               if Path(self.db_path).exists() else 0,
            "total_chats":     total_chats,
            "total_sessions":  total_sessions,
        }

    def clear(self):
        """Saara activity context wipe karo."""
        with self._connect() as conn:
            conn.execute("DELETE FROM activity_log")
            conn.commit()
        print("🗑️  Context buffer cleared!")

    # ── Pretty Print ───────────────────────────────────────

    def print_recent(self, n: int = 5):
        """Recent entries terminal mein print karo — debug ke liye."""
        entries = self.get_recent(n)
        if not entries:
            print("📭 Abhi koi entries nahi hain.")
            return

        print(f"\n📋 Last {len(entries)} entries (newest first):")
        print("─" * 60)
        for e in entries:
            print(f"[{e['timestamp']}] #{e['id']}")
            print(f"  {e['description']}")
            print()


# ── Quick Test ────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Context Buffer Test ===\n")

    buf = ContextBuffer(db_path="test_context.db")

    # Activity log test
    print("\n📝 Activity entries save kar raha hoon...")
    buf.save("User has VS Code open with a Python file. Line 23 has a red underline.")
    buf.save("User switched to Chrome and searched 'python modulenotfounderror fix'.")
    buf.save("User is reading a Stack Overflow answer about virtual environments.")
    buf.save("Terminal shows: ModuleNotFoundError: No module named 'requests'")

    buf.print_recent(n=4)

    # Chat history test
    print("\n💬 Chat history test...")
    session = "session_001"
    buf.save_chat(session, "assistant", "Maine dekha ki tumhare terminal mein ModuleNotFoundError hai.")
    buf.save_chat(session, "user", "Isko kaise fix karun?")
    buf.save_chat(session, "assistant", "pip install requests run karo terminal mein.")

    history = buf.get_chat_history(session)
    print(f"Session '{session}' mein {len(history)} messages:")
    for msg in history:
        icon = "🤖" if msg["role"] == "assistant" else "👤"
        print(f"  {icon} [{msg['role']}]: {msg['content'][:60]}")

    # Stats
    print(f"\n📊 Stats: {buf.stats()}")

    # Cleanup
    import os
    os.remove("test_context.db")
    print("\n✅ Test complete! test_context.db delete kar di.")