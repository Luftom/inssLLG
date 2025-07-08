import random
import spacy

nlp = spacy.load("pt_core_news_sm")
nlp.max_length = 2000000

def processar_texto_com_spacy(texto):
    doc = nlp(texto)
    resultado = []

    for token in doc:
        if token.is_space:
            continue
        resultado.append((token.lemma_, token.pos_, token.text.lower()))
        # inclui até pontuação como "." ou ","

    return resultado

def clean_and_read_text(input_file:str) -> list:
    #Lê o texto a partir de 'CAPITULO PRIMEIRO', exclui linhas 'CAPÍTULO', separa pontuação como palavras.
    with open(input_file, encoding='utf-8') as reader:
        text = ''
        start = False #SÓ VIRA True quando encontrar o primeiro Capitulo
        for line in reader:
            line = line.strip()
            if line.startswith('CAPÍTULO'):
                start = True
                continue
            if line=='Fim':
                start = False #vira false se encontrar fim
                continue
            if start:
                text += ' '+line.lower()

    pontuacoes = ['.', ',', '!', '?', ';', ':', '(', ')', '“', '”', '"', '—']
    texto_tratado = ''
    for caractere in text:
        if caractere in pontuacoes:
            texto_tratado += ' ' + caractere + ' ' #coloca espaço entre as pontuações
        else:
            texto_tratado += caractere

    palavras = texto_tratado.split()
    return ' '.join(palavras)

def build_quadrigram_model_com_original(tokens):
    modelo = {}

    for i in range(len(tokens) - 4):
        # chave = (lema, POS) das 4 palavras
        chave = tuple((tokens[j][0], tokens[j][1]) for j in range(i, i + 4))
        # valor = (lema, POS, palavra original) da próxima palavra
        proxima = tokens[i + 4]

        if chave not in modelo:
            modelo[chave] = {}

        if proxima not in modelo[chave]:
            modelo[chave][proxima] = 0

        modelo[chave][proxima] += 1

    return modelo
    return modelo

def generate_text_com_original(modelo, length=40):
    chaves_validas = [k for k in modelo if k[0][1] != 'PUNCT']
    if not chaves_validas:
        return []

    chave_atual = random.choice(chaves_validas)
    resultado = []

    # Inicializa resultado com formas originais associadas à chave
    for lema, pos in chave_atual:
        for entradas in modelo.values():
            for palavra in entradas:
                if palavra[0] == lema and palavra[1] == pos:
                    resultado.append(palavra[2])
                    break
            else:
                continue
            break

    for _ in range(length - 4):
        proximas = modelo.get(chave_atual)
        if not proximas:
            break

        escolhas = list(proximas.keys())
        pesos = list(proximas.values())
        escolhida = random.choices(escolhas, weights=pesos)[0]
        resultado.append(escolhida[2])  # forma original
        chave_atual = (*chave_atual[1:], (escolhida[0], escolhida[1]))

    return resultado

def formatar_texto_lemas(lemas_pos):
    palavras = [lema for lema, pos in lemas_pos]
    return formatar_texto(palavras)

def is_pontuacao(token): #parte para identificar se é pontuação
    return token in '.,!?;:()—“”"'

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

tokens = processar_texto_com_spacy(texto)
modelo = build_quadrigram_model_com_original(tokens)
tokens_gerados = generate_text_com_original(modelo, length=1000)

# tokens_gerados agora tem ["ela", "foi", ",", "mas", "voltou", "."]
print("\nTexto gerado:\n")
print(formatar_texto(tokens_gerados))