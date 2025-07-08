import random
import spacy

# Carrega o modelo do spaCy para português
nlp = spacy.load("pt_core_news_sm")
nlp.max_length = 2000000

# Processa o texto com spaCy e retorna tuplas com lema, POS e forma original
def processar_texto_com_spacy(texto):
    doc = nlp(texto)
    resultado = []

    for token in doc:
        if token.is_space:
            continue
        resultado.append((token.lemma_, token.pos_, token.text.lower()))

    return resultado

# Lê e limpa o texto
def clean_and_read_text(input_file):
    with open(input_file, encoding='utf-8') as reader:
        text = ''
        start = False
        for line in reader:
            line = line.strip()
            if line.startswith('CAPÍTULO'):
                start = True
                continue
            if line == 'Fim':
                start = False
                continue
            if start:
                text += ' ' + line.lower()

    pontuacoes = ['.', ',', '!', '?', ';', ':', '(', ')', '“', '”', '"', '—']
    texto_tratado = ''
    for caractere in text:
        if caractere in pontuacoes:
            texto_tratado += ' ' + caractere + ' '
        else:
            texto_tratado += caractere

    palavras = texto_tratado.split()
    return ' '.join(palavras)

# Constrói o modelo de n-gramas com lema, POS e forma original
def build_ngram_model(tokens, n):
    modelo = {}
    for i in range(len(tokens) - n):
        chave = tuple((tokens[j][0], tokens[j][1]) for j in range(i, i + n))
        proxima = tokens[i + n]

        if chave not in modelo:
            modelo[chave] = {}

        if proxima not in modelo[chave]:
            modelo[chave][proxima] = 0

        modelo[chave][proxima] += 1

    return modelo

# Gera texto usando o modelo de n-gramas
def generate_text_com_original(modelo, n=4, length=40):
    chaves_validas = [k for k in modelo if k[0][1] != 'PUNCT']
    if not chaves_validas:
        return []

    chave_atual = random.choice(chaves_validas)
    resultado = []

    # Recupera formas originais iniciais
    for lema, pos in chave_atual:
        for entradas in modelo.values():
            for palavra in entradas:
                if palavra[0] == lema and palavra[1] == pos:
                    resultado.append(palavra[2])
                    break
            else:
                continue
            break

    for _ in range(length - n):
        proximas = modelo.get(chave_atual)
        if not proximas:
            break

        escolhas = list(proximas.keys())
        pesos = list(proximas.values())
        escolhida = random.choices(escolhas, weights=pesos)[0]
        resultado.append(escolhida[2])
        chave_atual = (*chave_atual[1:], (escolhida[0], escolhida[1]))

    return resultado

# Formata o texto final com pontuação e maiúsculas
def formatar_texto(palavras):
    ultimo_ponto = None
    for i in reversed(range(len(palavras))):
        if palavras[i] == '.':
            ultimo_ponto = i
            break
    if ultimo_ponto is not None:
        palavras = palavras[:ultimo_ponto + 1]

    texto = ''
    nova_frase = True

    for palavra in palavras:
        if palavra in '.!?;:—':
            texto = texto.rstrip() + palavra
            nova_frase = True
        elif palavra in ',()“”"':
            texto = texto.rstrip() + palavra
            nova_frase = False
        else:
            if nova_frase:
                palavra = palavra.capitalize()
                nova_frase = False
            texto += ' ' + palavra

    return texto.strip()

# === EXECUÇÃO ===
arquivo = "memoriasBras-_1_.txt"
texto = clean_and_read_text(arquivo)

tokens = processar_texto_com_spacy(texto)
n = 1  # Mude aqui para 3, 5, 6, etc. se quiser outro n-grama
modelo = build_ngram_model(tokens, n)
tokens_gerados = generate_text_com_original(modelo, n=n, length=100)

print("\nTexto gerado:\n")
print(formatar_texto(tokens_gerados))
