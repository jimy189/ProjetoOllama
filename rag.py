import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Caminho do arquivo PDF
PDF_PATH = "quadro-curricular-1.pdf"

# Configuração dos modelos
class Models:
    def __init__(self):
        self.embeddings_ollama = OllamaEmbeddings(model="mxbai-embed-large")
        self.model_ollama = ChatOllama(model="llama3.2", temperature=0)

# Função para carregar e indexar o PDF
def processar_pdf(pdf_path):
    print("Carregando e indexando o PDF...")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    # Divide o texto em partes menores para indexação eficiente
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    # Cria um banco de vetores com ChromaDB
    vector_db = Chroma.from_documents(texts, embedding=Models().embeddings_ollama)
    return vector_db

# Função para buscar e responder com RAG
def perguntar_ao_rag(pergunta, vector_db):
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})  # Busca os 5 trechos mais relevantes
    chain = RetrievalQA.from_chain_type(
        llm=Models().model_ollama,
        retriever=retriever,
        chain_type="stuff",
    )
    resposta = chain.run(pergunta)
    return resposta

# Execução principal
if __name__ == "__main__":
    pergunta = (
    "Liste todos os Componentes Curriculares Obrigatórios presentes no documento, incluindo seus códigos e nomes completos."
    " Certifique-se de recuperar as seguintes disciplinas:"
    " HACA01 - Estudos Sobre a Contemporaneidade I,"
    " HACA02 - Elementos Acadêmicos e Profissionais em Ciência e Tecnologia,"
    " HACA09 - Ciência e Tecnologia I,"
    " HACA34 - Estudos Sobre a Contemporaneidade II,"
    " HACA38 - Ciência e Tecnologia II,"
    " LETE43 - Língua Portuguesa, Poder e Diversidade Cultural,"
    " LETE45 - Leitura e Produção de Textos em Língua Portuguesa."
    " Me liste Componentes curriculares oferecidos pelo IHAC:"
    " Certifique-se de recuperar as seguintes disciplinas:"
    " HACA39 - Ciência e Tecnologia III,"
    " HACA46 - Tópicos Especiais em Ciências I,"
    " HACA47 - Tópicos Especiais em Tecnologias I,"
    " HACA53 - Ciência e Tecnologia IV,"
    " HACA88 - Desenvolvimento de Produto e Produção Industrial,"
    " HACA89 - Concepção de Produtos Tecnológicos,"
    " HACA90 - Sistemas de Inovação em Ciência e Tecnologia,"
    " HACA91 - Fundamentos de Nanociência e Nanotecnologia,"
    " HACA92 - Gestão de Projetos de Pesquisa e Desenvolvimento,"
    " HACA93 - Dispositivos Tecnológicos Práticos I,"
    " HACA94 - Dispositivos Tecnológicos Práticos II,"
    " HACA95 - Fundamentos de Ciências dos Novos Materiais,"
    " HACA96 - Laboratório de Ciência e Tecnologia,"
    " HACA97 - Fundamentos de Espectroscopia,"
    " HACA98 - Fundamentos de Engenharia Biomédica e Clínica,"
    " HACA99 - Fundamentos de Biomateriais e Biotecnologia,"
    " HACB01 - Fundamentos de Microscopia,"
    " HACB02 - Gestão de Pequenas Empresas de Base Tecnológica,"
    " HACB03 - Fundamentos de Cristalografia e Difração de Raios X,"
    " HACB04 - Empreendedorismo e Inovação,"
    " HACB05 - Tópicos Especiais em Ciências II,"
    " HACB06 - Tópicos Especiais em Tecnologias II"
    " Agora Organize por uma lista de materias obrigatorias e outra não obrigatoria"
    
)

    # Processa o PDF e cria a base vetorial
    vector_db = processar_pdf(PDF_PATH)


    resposta = perguntar_ao_rag(pergunta, vector_db)
    print(f"\n🔹 Resposta do RAG: {resposta}")

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
