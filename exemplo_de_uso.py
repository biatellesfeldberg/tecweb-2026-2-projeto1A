from database import Database
from database import Note

db = Database('banco')

db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
print("ANTES DO UPDATE:")

for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')

note = notes[0]

note.title = 'Pão doce atualizado'
note.content = 'Novo conteúdo da anotação'
db.update(note)

notes = db.get_all()
print("DEPOIS DO UPDATE:")

for note in notes:
    print(f'Anotação {note.id}:\n Título: {note.title}\n Conteúdo: {note.content}\n')