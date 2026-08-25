from urllib.parse import unquote_plus
from utils import load_data, load_template, add_note, build_response


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

        # Salva a nova anotação no notes.json
        add_note(params)

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
            title=dados['titulo'],
            details=dados['detalhes']
        )
        for dados in load_data('notes.json')
    ]

    # Junta todas as anotações
    notes = '\n'.join(notes_li)

    # Monta o corpo HTML da página
    body = load_template('index.html').format(notes=notes).encode()

    # Constrói a resposta HTTP com status 200 OK
    return build_response(body=body)