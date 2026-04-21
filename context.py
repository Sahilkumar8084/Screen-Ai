import sqlite3
import json
from datetime import datetime
from pathlib import Path


#______Settings___________
DB_PATH="screen_ai_context.db"
MAX_ENTRIES=200
RECENT_FOR_HELP =20

class ContextBuffer:
    
    def __init__(self,db_path:str = DB_PATH):
        self.db_path = db_path
        self._init_db()
        print(f"✅ Context buffer ready! Database: '{self.db_path}'")
    
    #DataBase Setup_______________
    
    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
                    CREATE TABLE IF NOT EXISTS activity_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp   TEXT NOT NULL,
                    description TEXT NOT NULL,
                    extra       TEXT DEFAULT '{}'
                )
               """)
            # Fast Lookup ke liye
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON activity_log (timestamp DESC)
            """)
            # Chat history table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role       TEXT NOT NULL,
                    content    TEXT NOT NULL,
                    timestamp  TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session
                ON chat_history (session_id, id ASC)
            """)
            conn.commit()
        
    def _connect(self)->sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row #this will return the Dict like rows
    
        return conn
    def save(self,description:str , extra: dict =None) ->int:
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
        
        #Poorani Entries Clean Up karo bhai
        
        self._cleanup()
        return new_id
    
    def _cleanup(self):
        ''' MAX_ENTRIES se zyaa entries hone pe sabko delte kardoo taki space rahe'''
        
        with self._connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM activity_log").fetchone()[0]
            
            if count >MAX_ENTRIES:
                to_delete = count -MAX_ENTRIES        
                
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

                
    #__READ____________
    
    def get_recent(self, n: int= RECENT_FOR_HELP) ->list[dict]:
        
        
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT id, timestamp, description, extra
                FROM activity_log
                ORDER BY id DESC
                LIMIT ?
            """, (n,)).fetchall()
            
        result = []
        
        for row in rows:
            result.append({
                "id":          row["id"],
                "timestamp":   row["timestamp"],
                "description": row["description"],
                "extra":       json.loads(row["extra"]),
            })
            
        return result
    
    def get_all(self) -> list[dict]:
        
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT id, timestamp, description, extra
                FROM activity_log
                ORDER BY id ASC
            """).fetchall()
            
        return[
            {
                "id":          row["id"],
                "timestamp":   row["timestamp"],
                "description": row["description"],
                "extra":       json.loads(row["extra"]),
            }
            for row in rows
        ]
    def search(self,keyword: str)->list[dict]:
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
        
    ##___STATS___________
    
    def stats(self)->dict:
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM activity_log").fetchone()[0]
            oldest = conn.execute(
                "SELECT timestamp FROM activity_log ORDER BY id ASC LIMIT 1"
            ).fetchone()
            newest = conn.execute(
                "SELECT timestamp FROM activity_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
            
            return{
                            "total_entries": total,
            "oldest":        oldest[0] if oldest else None,
            "newest":        newest[0] if newest else None,
            "db_size_kb":    round(Path(self.db_path).stat().st_size / 1024, 1) if Path(self.db_path).exists() else 0,
                
            }
            
    def clear(self):
        with self._connect() as conn:
            conn.execute("DELETE FROM activity_log")
            conn.commit()
        print("🗑️  Context buffer cleared!")
        
        
    #Print the recent 
        
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
            
    # ── Chat History Functions ────────────────────────────────

    def save_chat(self, session_id: str, role: str, content: str) -> int:
        """Ek chat message save karo."""
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
        """Ek session ki poori chat history lo."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT role, content, timestamp
                FROM chat_history
                WHERE session_id = ?
                ORDER BY id ASC
            """, (session_id,)).fetchall()
        return [
            {"role": r["role"], "content": r["content"], "timestamp": r["timestamp"]}
            for r in rows
        ]

    def get_all_sessions(self) -> list[str]:
        """Saare session IDs lo (newest first)."""
        with self._connect() as conn:
            rows = conn.execute("""
                SELECT DISTINCT session_id
                FROM chat_history
                ORDER BY id DESC
            """).fetchall()
        return [r["session_id"] for r in rows]

    def clear_chat(self, session_id: str = None):
        """Ek session ya saari chat history clear karo."""
        with self._connect() as conn:
            if session_id:
                conn.execute("DELETE FROM chat_history WHERE session_id = ?", (session_id,))
            else:
                conn.execute("DELETE FROM chat_history")
            conn.commit()
        print(f"🗑️  Chat history cleared! (session: {session_id or 'ALL'})")


#__________Quick TEst____________

if __name__ == "__main__":
    print("=== Context Buffer Test ===\n")

    # Test database banao
    buf = ContextBuffer(db_path="test_context.db")

    # Kuch fake entries save karo
    print("\n📝 Fake entries save kar raha hoon...")
    buf.save("User has VS Code open with a Python file. Line 23 has a red underline.")
    buf.save("User switched to Chrome and searched 'python modulenotfounderror fix'.")
    buf.save("User is reading a Stack Overflow answer about virtual environments.")
    buf.save("User went back to VS Code and is typing in the terminal.")
    buf.save("Terminal shows: ModuleNotFoundError: No module named 'requests'")

    # Recent entries print karo
    buf.print_recent(n=5)

    # Search test
    print("🔍 'terminal' keyword search:")
    results = buf.search("terminal")
    for r in results:
        print(f"  [{r['timestamp']}] {r['description'][:60]}...")

    # Stats
    print(f"\n📊 Stats: {buf.stats()}")

    # Cleanup test database
    import os
    os.remove("test_context.db")
    print("\n✅ Test complete! test_context.db delete kar di.")