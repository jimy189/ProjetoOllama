import json
import requests

# Nome do arquivo JSON
arquivo_json = "Ementa BI CeT.json"

# URL da API LLM
url_llm = "http://localhost:11434/api/chat"

# Classificação esperada (fornecida)
classificacao_esperada = {
    "Infraestrutura": [
        "HACA93 - Dispositivos Tecnológicos Práticos I",
        "HACA94 - Dispositivos Tecnológicos Práticos II",
        "HACB14 - Sistemas Digitais em Artes",
        "HACB08 - Tecnologia da Informação e as Artes",
        "HACA53 - Ciência e Tecnologia IV",
        "HACA39 - Ciência e Tecnologia III",
        "HACA96 - Laboratório de Ciência e Tecnologia",
        "HACA41 - Tecnologias Aplicadas às Artes",
        "HACA89 - Concepção de Produtos Tecnológicos"
    ],
    "Desenvolvimento": [
        "HACB10 - Linguagens e Ambientes de Programação em Artes",
        "HACB28 - Computação Aplicada",
        "HACA89 - Concepção de Produtos Tecnológicos",
        "HACA41 - Tecnologias Aplicadas às Artes",
        "HACA53 - Ciência e Tecnologia IV",
        "HACA39 - Ciência e Tecnologia III",
        "HACA38 - Ciência e Tecnologia II",
        "HACA09 - Ciência e Tecnologia I",
        "HACA93 - Dispositivos Tecnológicos Práticos I",
        "HACA94 - Dispositivos Tecnológicos Práticos II",
        "HACB04 - Empreendedorismo e Inovação"
    ],
    "Ciência de Dados": [
        "HACA83 - Matemática, Natureza e Sociedade",
        "HACA96 - Laboratório de Ciência e Tecnologia",
        "HACA90 - Sistemas de Inovação em Ciência e Tecnologia",
        "HACB28 - Computação Aplicada",
        "HACA38 - Ciência e Tecnologia II",
        "HACA09 - Ciência e Tecnologia I",
        "HACA53 - Ciência e Tecnologia IV",
        "HACA39 - Ciência e Tecnologia III",
        "HACB04 - Empreendedorismo e Inovação"
    ]
}

# Função para carregar os dados do JSON
def carregar_ementa_json(arquivo):
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return {}

# Função para consultar o LLM
def consultar_llm(conteudo):
    try:
        data = {
            "model": "llama3.2:3b",
            "messages": [{"role": "user", "content": conteudo}],
            "stream": False
        }
        response = requests.post(url_llm, json=data)
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "Sem resposta").lower()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar o LLM: {e}")
        return "erro ao processar"

# Função para classificar matérias usando o LLM
def classificar_materias_com_llm(dados_ementa):
    trilhas = {
        "Infraestrutura": [],
        "Desenvolvimento": [],
        "Ciência de Dados": []
    }

    if "UFBA" not in dados_ementa:
        print("Dados do JSON não possuem a estrutura esperada.")
        return trilhas

    for materia in dados_ementa["UFBA"]:
        conteudo = materia.get("CONTEUDO", "")
        codigo = materia.get("CODIGO", "Sem código")
        nome = materia.get("NOME", "Sem nome")
        pergunta = (
            f"Com base no seguinte conteúdo: '{conteudo}', "
            "em quais trilhas esta matéria se encaixa melhor? "
            "(Infraestrutura, Desenvolvimento, Ciência de Dados ou múltiplas)"
        )
        
        resposta = consultar_llm(pergunta)

        # Normalizar e verificar a resposta
        for trilha in trilhas.keys():
            if trilha.lower() in resposta:
                trilhas[trilha].append(f"{codigo} - {nome}")

    return trilhas

# Função para calcular a precisão
def calcular_precisao(classificacao_esperada, classificacao_predita):
    resultados = {}
    total_acertos = 0
    total_materias = 0

    for trilha, materias_esperadas in classificacao_esperada.items():
        materias_preditas = classificacao_predita.get(trilha, [])
        acertos = set(materias_esperadas) & set(materias_preditas)
        erros = set(materias_preditas) - set(materias_esperadas)
        resultados[trilha] = {
            "acertos": len(acertos),
            "erros": len(erros),
            "total": len(materias_esperadas),
            "detalhe_acertos": list(acertos),
            "detalhe_erros": list(erros)
        }
        total_acertos += len(acertos)
        total_materias += len(materias_esperadas)

    precisao = (total_acertos / total_materias) * 100 if total_materias > 0 else 0
    return resultados, precisao

# Carregar os dados do JSON
ementa = carregar_ementa_json(arquivo_json)

# Classificar as matérias em trilhas usando o LLM
trilhas_materias = classificar_materias_com_llm(ementa)

# Exibir as recomendações de matérias
print("\nRecomendações de matérias por trilha:")

for trilha, materias in trilhas_materias.items():
    print(f"\nTrilha: {trilha}")
    for materia in materias:
        print(materia)

# Avaliar a precisão
resultados_avaliacao, score_total = calcular_precisao(classificacao_esperada, trilhas_materias)

# Exibir o relatório de avaliação
print("\nRelatório de Avaliação:")
for trilha, resultado in resultados_avaliacao.items():
    print(f"\nTrilha: {trilha}")
    print(f" - Acertos: {resultado['acertos']} de {resultado['total']} ({(resultado['acertos'] / resultado['total']) * 100:.2f}% precisão)")
    print(f" - Erros: {resultado['erros']}")
    print(f" - Detalhe dos acertos: {resultado['detalhe_acertos']}")
    print(f" - Detalhe dos erros: {resultado['detalhe_erros']}")

print(f"\nScore total de classificação: {score_total:.2f}%")