from urllib.parse import unquote_plus
from utils import load_template, build_response
from database import Database, Note

db = Database('notes')


def index(request):
    # Verifica se a requisição recebida é do tipo POST
    if request.startswith('POST'):

        # Remove os caracteres "\r" da requisição
        request = request.replace('\r', '')

        # Separa o cabeçalho do corpo da requisição
        partes = request.split('\n\n')
        corpo = partes[1]

        # Dicionário que armazenará os dados enviados pelo formulário
        params = {}

        # Separa cada par chave=valor enviado pelo formulário
        for chave_valor in corpo.split('&'):

            # Separa o nome do campo do seu valor
            chave, valor = chave_valor.split('=', 1)

            # Decodifica o valor recebido e adiciona ao dicionário
            params[chave] = unquote_plus(valor)

        # Salva a nova anotação no banco SQLite
        db.add(Note(title=params['titulo'], content=params['detalhes']))

        # Redireciona o navegador para a página inicial
        return build_response(
            code=303,
            reason='See Other',
            headers='Location: /'
        )

    # Carrega o template HTML utilizado para cada anotação
    note_template = load_template('components/note.html')

    # Cria o HTML de todas as anotações
    notes_li = [
        note_template.format(
            id=note.id,
            title=note.title,
            details=note.content
        )
        for note in db.get_all()
    ]

    # Junta todas as anotações
    notes = '\n'.join(notes_li)

    # Monta o corpo HTML da página
    body = load_template('index.html').format(notes=notes).encode()

    # Constrói a resposta HTTP com status 200 OK
    return build_response(body=body)


def delete(request):
    # Pega o id da rota GET /delete/<NOTA_ID>
    note_id = request.split()[1].split('/')[-1]

    # Apaga a anotação no banco SQLite
    db.delete(note_id)

    # Redireciona o navegador para a página inicial
    return build_response(
        code=303,
        reason='See Other',
        headers='Location: /'
    )


def edit(request):
    # Pega o id da rota /edit/<NOTA_ID>
    note_id = request.split()[1].split('/')[-1]

    if request.startswith('POST'):

        # Remove os caracteres "\r" da requisição
        request = request.replace('\r', '')

        # Separa o cabeçalho do corpo da requisição
        partes = request.split('\n\n')
        corpo = partes[1]

        # Dicionário que armazenará os dados enviados pelo formulário
        params = {}

        # Separa cada par chave=valor enviado pelo formulário
        for chave_valor in corpo.split('&'):

            # Separa o nome do campo do seu valor
            chave, valor = chave_valor.split('=', 1)

            # Decodifica o valor recebido e adiciona ao dicionário
            params[chave] = unquote_plus(valor)

        # Atualiza a anotação no banco SQLite
        db.update(Note(id=note_id, title=params['titulo'], content=params['detalhes']))

        # Redireciona o navegador para a página inicial
        return build_response(
            code=303,
            reason='See Other',
            headers='Location: /'
        )

    # Busca a anotação pelo id e preenche a página de edição
    note = db.get_by_id(note_id)

    body = load_template('edit.html').format(
        title=note.title or '',
        details=note.content or ''
    ).encode()

    return build_response(body=body)