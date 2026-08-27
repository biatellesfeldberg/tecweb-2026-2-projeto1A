import sqlite3

class Database:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name + ".db")

        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL
            )
            """
        )
    
    def add(self, note):
        self.conn.execute(
            f"""
            INSERT INTO note (title, content)
            VALUES ('{note.title}', '{note.content}')
            """
        )

        self.conn.commit()
    
    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")

        notes = []

        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]

            note = Note(id, title, content)
            notes.append(note)

        return notes
    
    def get_by_id(self, note_id):
        cursor = self.conn.execute(
            f"SELECT id, title, content FROM note WHERE id = {note_id}"
        )

        linha = cursor.fetchone()

        return Note(linha[0], linha[1], linha[2])

    def update(self, entry):
        self.conn.execute(
            f"""
            UPDATE note
            SET title = '{entry.title}', content = '{entry.content}'
            WHERE id = {entry.id}
            """
        )

        self.conn.commit()
    
    def delete(self, note_id):
        self.conn.execute(
            f"""
            DELETE FROM note
            WHERE id = {note_id}
            """
        )

        self.conn.commit()

class Note:
    def __init__(self, id=None, title=None, content=''):
        self.id = id
        self.title = title
        self.content = content
