import random
import re

def clean_and_read_text(input_file):
    """Lê o arquivo a partir de 'Capítulo ' e limpa o texto."""
    reader = open(input_file, encoding='utf-8')
    text = ''
    start = False

    for line in reader:
        if not start and 'Capítulo ' in line:
            start = True
        if start:
            text += line.lower()

    reader.close()

    # Remove pontuação, números etc.
    text = re.sub(r'[^a-zà-úçãõ\s]', '', text)
    return text

def build_bigram_model(text):
    """Cria um dicionário de bigramas com contagem de frequência."""
    palavras = text.split()
    bigramas = {}

    for i in range(len(palavras) - 1):
        p1 = palavras[i]
        p2 = palavras[i + 1]

        if p1 not in bigramas:
            bigramas[p1] = {}
        if p2 not in bigramas[p1]:
            bigramas[p1][p2] = 0

        bigramas[p1][p2] += 1

    return bigramas

def generate_text(bigramas, start_word=None, length=20):
    """Gera texto a partir do modelo de bigramas."""
    if not start_word:
        start_word = random.choice(list(bigramas.keys()))

    palavra_atual = start_word
    resultado = [palavra_atual]

    for _ in range(length - 1):
        proximas = bigramas.get(palavra_atual)
        if not proximas:
            break

        palavras = list(proximas.keys())
        pesos = list(proximas.values())
        palavra_atual = random.choices(palavras, weights=pesos)[0]
        resultado.append(palavra_atual)

    return ' '.join(resultado)
 # como usar:
arquivo = 'livro.txt' #mudar para um que definirmos

texto = clean_and_read_text(arquivo)
modelo = build_bigram_model(texto)

# Com palavra inicial definida
print(generate_text(modelo, start_word='ela', length=30))

# Ou aleatória (deixa sem o parâmetro start_word)
print(generate_text(modelo, length=30))
