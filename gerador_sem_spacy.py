import random
def is_pontuacao(token): #parte para identificar se é pontuação
    return token in '.,!?;:()“”"—'
def clean_and_read_text(input_file):
    #Lê o texto a partir de 'CAPITULO PRIMEIRO', exclui linhas 'CAPÍTULO', separa pontuação como palavras.
    with open(input_file, encoding='utf-8') as reader:
        text = ''
        start = False #SÓ VIRA True quando encontrar o primeiro Capitulo
        for line in reader:
            line = line.strip() #limpa a string
            if line.startswith('CAPÍTULO'):
                start = True
                continue
            if line=='Fim':
                start = False #vira false se encontrar fim
                continue
            if start:
                text += ' ' + line.lower() #coloca espaço entre as frases e deixa minusculo               
    texto_tratado = ''
    for caractere in text:
        if is_pontuacao(caractere):
            texto_tratado += ' ' + caractere + ' ' #coloca espaço entre as pontuações e o texto
        else:
            texto_tratado += caractere

    palavras = texto_tratado.split() #cria ums lista separando cada palavra
    return palavras

def build_pentagram_model(palavras): #é oq cria o modelo do nosso pentagrama, meio parecido com o window
    modelo = {}

    for i in range(len(palavras) - 5):
        chave = tuple(palavras[i:i+5]) #cria uma tupla com 5 palavras
        proxima = palavras[i+5]

        if chave not in modelo: 
            modelo[chave] = {}
        modelo[chave][proxima] = modelo[chave].get(proxima, 0) + 1 #cria um dicionario dentro do dicionario no qual o dicionario interno tem como as chaves as proximas possivei palavras e quantas vezes cada uma aparece

    return modelo

def generate_text(modelo, start_words=None, length=40):
    #Gera texto com base em modelo de pentagramas, evitando começar com pontuação.
    if not modelo:
        return "Erro: modelo vazio."
    if not start_words:
        chaves_validas = []
        for key in modelo.keys():
            if not is_pontuacao(key[0]): #se for pontuação n vale
                chaves_validas.append(key)     
        if not chaves_validas:
            return "Erro: sem chave inicial válida."
        start_words = random.choice(chaves_validas) #escolhe um das chaves validas
    else:
        start_words = tuple(start_words)
        chaves_possiveis = [] 
        if len(start_words) != 5 or start_words not in modelo: #se n for um pentagrama ou se o gradrigrama n estiver no modelo
            for key in modelo:
                if key[:len(start_words)] == start_words: #comparando uma chave q existe
                    chaves_possiveis.append(key)
            if not chaves_possiveis:
                return f"Erro: sequência inicial {start_words} não encontrada no modelo."
        
            start_words = random.choice(chaves_possiveis)


    resultado = list(start_words) #tranforma em lista a chave escolhida para começar
    chave_atual = start_words

    for _ in range(length - 5):
        proximas = modelo.get(chave_atual)
        if not proximas:
            break

        palavras = list(proximas.keys())
        pesos = list(proximas.values())
        escolhida = random.choices(palavras, weights=pesos)[0] #o [0] é pra pegar só a palavra sorteada n a lista da palavra sorteada
        resultado.append(escolhida)
        chave_atual = (*chave_atual[1:], escolhida) #chave atual vira o pentagrama com a nova palavra e sem a primeira

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
        if palavra in '.!?;:—':
            texto = texto + palavra 
            nova_frase = True
        elif palavra == ',':
            texto = texto + palavra
            nova_frase = False
        else:
            if nova_frase:
                palavra = palavra.capitalize() #deixa maiusculo a primeira letra
                nova_frase = False
            texto += ' ' + palavra

    return texto.strip()

# === EXECUÇÃO ===

arquivo = "obras.txt"
texto = clean_and_read_text(arquivo)
modelo = build_pentagram_model(texto)

tokens_gerados = generate_text(modelo,length=200)
print(len(texto))
print("\nTexto gerado:\n")
print(formatar_texto(tokens_gerados))