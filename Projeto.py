import json
import requests

# Nome do arquivo JSON
arquivo_json = "Ementa BI CeT.json"

# URL da API LLM
url_llm = "http://localhost:11434/api/chat"

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
    
    # Classificação esperada (fornecida)
classificacao_esperada = {
    "Infraestrutura": [
        "HACA09 - CIÊNCIA E TECNOLOGIA I",
        "HACA38 - CIÊNCIA E TECNOLOGIA II",
        "LETE45 - LEITURA E PRODUÇÃO DE TEXTOS EM LÍNGUA PORTUGUESA",
        "HACA02 - ELEMENTOS ACADÊMICOS E PROFISSIONAIS EM CIÊNCIA E TECNOLOGIA",
        "HACB07 - ARQUEOLOGIA DAS ARTES E TECNOLOGIAS",
        "HACA89 - CONCEPÇÃO DE PRODUTOS TECNOLÓGICOS",
        "HACA93 - DISPOSITIVOS TECNOLÓGICOS PRÁTICOS I",
        "HACA94 - DISPOSITIVOS TECNOLÓGICOS PRÁTICOS II",
        "HACB04 - EMPREENDEDORISMO E INOVAÇÃO"
    ],
    "Desenvolvimento": [
        "HACA09 - CIÊNCIA E TECNOLOGIA I",
        "HACA38 - CIÊNCIA E TECNOLOGIA II",
        "LETE45 - LEITURA E PRODUÇÃO DE TEXTOS EM LÍNGUA PORTUGUESA",
        "HACA02 - ELEMENTOS ACADÊMICOS E PROFISSIONAIS EM CIÊNCIA E TECNOLOGIA",
        "HACB07 - ARQUEOLOGIA DAS ARTES E TECNOLOGIAS",
        "HACA96 - LABORATÓRIO DE CIÊNCIA E TECNOLOGIA",
        "HACA10 - LINGUAGENS E AMBIENTES DE PROGRAMAÇÃO EM ARTES",
        "HACB14 - SISTEMAS DIGITAIS EM ARTES",
        "HACB08 - TECNOLOGIA DA INFORMAÇÃO E AS ARTES"
    ],
    "Ciência de Dados": [
        "HACA09 - CIÊNCIA E TECNOLOGIA I",
        "HACA38 - CIÊNCIA E TECNOLOGIA II",
        "LETE45 - LEITURA E PRODUÇÃO DE TEXTOS EM LÍNGUA PORTUGUESA",
        "HACA02 - ELEMENTOS ACADÊMICOS E PROFISSIONAIS EM CIÊNCIA E TECNOLOGIA",
        "HACB07 - ARQUEOLOGIA DAS ARTES E TECNOLOGIAS",
        "HACA53 - CIÊNCIA E TECNOLOGIA IV",
        "HACA39 - CIÊNCIA E TECNOLOGIA III",
        "HACA82 - ARTE E MATEMATICA",
        "HACA41 - TECNOLOGIAS APLICADAS ÀS ARTES"
    ]
}

# Lista de perguntas a serem feitas ao LLM
perguntas = [
        "1. Como os aspectos multidisciplinares e históricos da ciência e tecnologia podem ser aplicados para resolver problemas vinculados à sociedade?",
        "2. De que forma a linguagem matemática e a abordagem multidisciplinar contribuem para a solução de problemas relacionados à ciência da computação?",
        "3. Quais são as competências necessárias para a produção de textos acadêmicos, como resumos, resenhas críticas e artigos?",
        "4. Como a integração entre metodologia científica, expressão gráfica e ferramentas CAD pode auxiliar no desenvolvimento de projetos tecnológicos?",
        "5. Como as novas configurações artísticas são influenciadas pela cultura digital e pela mediação tecnológica?",
        "6. Qual é a relação entre conceitos matemáticos, como simetria e proporção, e a estética artística?",
        "7. Como as tecnologias comunicacionais podem ser utilizadas como elementos expressivos em projetos artísticos interativos?",
        "8. Como conhecimentos multidisciplinares derivados da física podem ser aplicados para resolver problemas vinculados à sociedade?",
        "9. De que forma os conteúdos multidisciplinares derivados da química e biologia são utilizados para abordar demandas sociais?",
        "10. Como a organização de sistemas computacionais impacta áreas multidisciplinares?",
        "11. Como o design estético, a funcionalidade e o posicionamento estratégico no mercado são integrados no desenvolvimento de produtos tecnológicos?",
        "12. Como os conhecimentos de eletricidade e eletrônica podem ser aplicados para resolver problemas práticos?",
        "13. De que forma microprocessadores e microcontroladores são utilizados em soluções tecnológicas?",
        "14. Como o desenvolvimento de produtos e serviços inovadores pode ser planejado, desde a pesquisa de mercado até o plano de negócios?",
        "15. Como experimentos históricos e modernos podem ser utilizados para ensinar o método científico?",
        "16. Como linguagens de programação, como C, Java e MATLAB, podem ser aplicadas em projetos artísticos?",
        "17. Como os conceitos matemáticos podem ser conectados a descobertas históricas e aplicações contemporâneas?",
        "18. Qual é a relação entre governo, universidade e indústria no fomento à inovação tecnológica?",
        "19. Como o processamento digital de sinais pode ser aplicado em projetos artísticos interativos?",
        "20. Como redes e sistemas computacionais podem ser utilizados em projetos artísticos?",
        "21. Como a interatividade e a imersão são aplicadas em configurações artísticas digitais?",
        "22. Quais são os temas atuais em tecnologias contemporâneas que impactam a arte e a ciência?",
        "23. Quais são os tópicos multidisciplinares e históricos relevantes para o desenvolvimento de inovações tecnológicas?",
        "24. Como técnicas e desenvolvimentos inovadores são explorados em campos tecnológicos específicos?"
    ]

# Coletar respostas do LLM
respostas_usuario = {}
for pergunta in perguntas:
    respostas_usuario[pergunta] = consultar_llm(pergunta)

# Função para recomendar matérias com base nas respostas do LLM e na ementa
def recomendar_materias(dados_ementa, respostas):
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
            f"e nas respostas do usuário: {respostas}, "
            "quais trilhas são mais adequadas para essa matéria? (Infraestrutura, Desenvolvimento, Ciência de Dados)"
        )
        resposta = consultar_llm(pergunta)

        for trilha in trilhas.keys():
            if trilha.lower() in resposta:
                trilhas[trilha].append(f"{codigo} - {nome}")
    
    return trilhas

# Carregar os dados do JSON
dados_ementa = carregar_ementa_json(arquivo_json)

# Obter recomendações com base nas respostas e na ementa
recomendacoes = recomendar_materias(dados_ementa, respostas_usuario)

# Exibir apenas as recomendações
print("\nRecomendações de matérias por trilha:")
for trilha, materias in recomendacoes.items():
    print(f"\nTrilha: {trilha}")
    for materia in materias:
        print(materia)


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


 # Avaliar a precisão
resultados_avaliacao, score_total = calcular_precisao(classificacao_esperada, recomendacoes)

# Exibir o relatório de avaliação
print("\nRelatório de Avaliação:")
for trilha, resultado in resultados_avaliacao.items():
    print(f"\nTrilha: {trilha}")
    print(f" - Acertos: {resultado['acertos']} de {resultado['total']} ({(resultado['acertos'] / resultado['total']) * 100:.2f}% precisão)")
    print(f" - Erros: {resultado['erros']}")
    print(f" - Detalhe dos acertos: {resultado['detalhe_acertos']}")
    print(f" - Detalhe dos erros: {resultado['detalhe_erros']}")

print(f"\nScore total de classificação: {score_total:.2f}%")
