import random

def clean_and_read_text(input_file):
    #Lê o texto a partir de 'CAPITULO PRIMEIRO', exclui linhas 'CAPÍTULO', separa pontuação como palavras.
    with open(input_file, encoding='utf-8') as reader:
        text = ''
        start = False #SÓ VIRA True quando encontrar o primeiro Capitulo
        for line in reader:
            line = line.strip()
            if not start and 'CAPÍTULO PRIMEIRO' in line:
                start = True
                continue
            if start:
                if line.startswith('CAPÍTULO') or line.startswith('Fim'):   #tira as linhas que começam com capitulo
                    continue
                text += ' ' + line.lower()

    pontuacoes = ['.', ',', '!', '?', ';', ':', '(', ')', '“', '”', '"',]
    texto_tratado = ''
    for caractere in text:
        if caractere in pontuacoes:
            texto_tratado += ' ' + caractere + ' ' #coloca espaço entre as pontuações
        else:
            texto_tratado += caractere

    palavras = texto_tratado.split()
    return ' '.join(palavras)

def build_hexagram_model(text): #é oq cria o modelo do nosso hexagrama, meio parecido com o window
    palavras = text.split()
    modelo = {}

    for i in range(len(palavras) - 6):
        chave = tuple(palavras[i:i+6]) #cria uma tupla com 6 palavras
        proxima = palavras[i+6]

        if chave not in modelo: 
            modelo[chave] = {}
        modelo[chave][proxima] = modelo[chave].get(proxima, 0) + 1 #cria um dicionario dentro do dicionario no qual o dicionario interno tem como as chaves as proximas possivei palavras e quantas vezes cada uma aparece

    return modelo

def is_pontuacao(token): #parte para identificar se é pontuação
    return token in '.,!?;:()“”"'

def generate_text(modelo, start_words=None, length=40):
    #Gera texto com base em modelo de hexagramas, evitando começar com pontuação.
    if not modelo:
        return "Erro: modelo vazio."

    if not start_words:
        chaves_validas = [k for k in modelo.keys() if not is_pontuacao(k[0])] #se for pontuação n vale
        if not chaves_validas:
            return "Erro: sem chave inicial válida."
        start_words = random.choice(chaves_validas) #escolhe um das chaves validas
    else:
        start_words = tuple(start_words) #pra caso tenha uma palavra inicial definida

    resultado = list(start_words) #tranforma em lista a chave escolhida para começar
    chave_atual = start_words

    for _ in range(length - 6):
        proximas = modelo.get(chave_atual)
        if not proximas:
            break

        palavras = list(proximas.keys())
        pesos = list(proximas.values())
        escolhida = random.choices(palavras, weights=pesos)[0]
        resultado.append(escolhida)
        chave_atual = (*chave_atual[1:], escolhida) #chave atual vira o hexagrma com a nova palavra e sem a primeira

    return resultado  # retorna lista de palavras

def formatar_texto(palavras):
    #Ajusta pontuação, letra maiuscula após ponto e corta no último ponto final.
    ultimo_ponto = None
    for i in reversed(range(len(palavras))):
        if palavras[i] == '.':
            ultimo_ponto = i
            break
    if ultimo_ponto is not None:
        palavras = palavras[:ultimo_ponto + 1]#se já tiver achado algum . ele para nesse ultimo . a frase

    texto = ''
    nova_frase = True

    for palavra in palavras: #junta a pontuação a palavra e deixa maiuscula depois do ponto final
        if palavra == '.':
            texto = texto.rstrip() + palavra #tira o espaço do lado direito da frase pra juntar a pontuação
            nova_frase = True
        elif palavra in ',!?;:':
            texto = texto.rstrip() + palavra
            nova_frase = False
        else:
            if nova_frase:
                palavra = palavra.capitalize() #deixa maiusculo a primeira letra
                nova_frase = False
            texto += ' ' + palavra

    return texto.strip()

# === EXECUÇÃO ===

arquivo = "memoriasBras-_1_.txt"
texto = clean_and_read_text(arquivo)
modelo = build_hexagram_model(texto)

tokens_gerados = generate_text(modelo, length=100)
print(len(texto))
print("\nTexto gerado:\n")
print(formatar_texto(tokens_gerados))
