import json
from pathlib import Path

def extract_route(request):
    # Seapara a requisição pelos espaços e pega o segundo elemento,
    # que corresponde à rota socilitada pelo cliente
    route = request.split()[1]

    # Remove a "/" inicial da rota
    return route[1:]

def read_file(path):
    # Abre o arquivo indicado por "path" 
    with open(path, "rb") as file: # rb - read binary (leitura binária), retornar como dados binários
        
        # Lê todo o conteúdo do arquivo e o retorna como bytes
        return file.read()

def load_data(filename):
    # Monta o caminho do arquivo dentro da pasta "data"
    filepath = Path("data") / filename

    # Abre o arquivo JSON no modo de leitura
    with open(filepath, "r") as file:

        # Converte o conteúdo JSON em um objeto Python e o retorna
        return json.load(file)

def load_template(filename):
    # Monta o caminho do arquivo dentro da pasta "templates"
    filepath = Path("templates") / filename

    # Abre o arquivo no modo de leitura de texto
    with open(filepath, "r") as file:
        # Lê e retorna todo o conteúdo do template como uma string
        return file.read()

def add_note(note):
    # Carrega a lista de anotações que já existem no arquivo notes.json
    notes = load_data('notes.json')

    # Adiciona a nova anotação à lista
    notes.append(note)

    # Monta o caminho até o arquivo notes.json
    filepath = Path('data') / 'notes.json'

    # Abre o arquivo no modo de escrita
    with open(filepath, 'w') as file:
        # Salva a lista atualizada no arquivo JSON
        json.dump(notes, file)

def build_response(body='', code=200, reason='OK', headers=''):
    # Cria a primeira linha da resposta HTTP com o código e a razão
    response = f'HTTP/1.1 {code} {reason}\n'

    # Adiciona os headers à resposta
    if headers:
        response += headers + '\n'

    # Adiciona uma linha vazia para separar o cabeçalho do corpo
    response += '\n'

    # Converte a resposta para bytes
    response = response.encode()

    # Se o body for uma string, converte também para bytes
    if isinstance(body, str):
        body = body.encode()

    # Retorna o cabeçalho HTTP junto com o corpo da resposta
    return response + body