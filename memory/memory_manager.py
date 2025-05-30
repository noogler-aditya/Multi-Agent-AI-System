import sqlite3
import json
from datetime import datetime

class MemoryManager:
    def __init__(self, database_path="shared_memory.db"):
        """Initialize database connection with specified path"""
        self.connection = sqlite3.connect(database_path, check_same_thread=False)
        self.initialize_database()

    def initialize_database(self):
        """Set up the memory table if it doesn't exist"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            format TEXT,
            timestamp TEXT,
            conversation_id TEXT,
            extracted_data TEXT
        )
        """
        self.connection.execute(create_table_query)
        self.connection.commit()

    def store_memory(self, source, format_type, conversation_id, data: dict):
        """Store a new memory entry in the database"""
        current_time = datetime.utcnow().isoformat()
        serialized_data = json.dumps(data)
        
        insert_query = """
        INSERT INTO memory (source, format, timestamp, conversation_id, extracted_data)
        VALUES (?, ?, ?, ?, ?)
        """
        self.connection.execute(insert_query, (source, format_type, current_time, 
                                             conversation_id, serialized_data))
        self.connection.commit()

    def retrieve_conversation(self, conversation_id):
        """Fetch all entries for a specific conversation"""
        select_query = "SELECT * FROM memory WHERE conversation_id = ? ORDER BY timestamp"
        cursor = self.connection.execute(select_query, (conversation_id,))
        
        memory_entries = []
        for row in cursor.fetchall():
            entry = {
                "id": row[0],
                "source": row[1],
                "format": row[2],
                "timestamp": row[3],
                "conversation_id": row[4],
                "extracted_data": json.loads(row[5])
            }
            memory_entries.append(entry)
        return memory_entries

    def cleanup(self):
        """Close the database connection"""
        self.connection.close()
