import json
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain.vectorstores import Chroma
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

# Caminhos dos arquivos
PDF_PATH = "quadro-curricular-1.pdf"
JSON_PATH = "Ementa BI CeT.json"

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

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(docs)

    vector_db = Chroma.from_documents(texts, embedding=Models().embeddings_ollama)
    return vector_db

# Função para buscar e responder com RAG
def perguntar_ao_rag(pergunta, vector_db):
    retriever = vector_db.as_retriever(search_kwargs={"k": 5})
    chain = RetrievalQA.from_chain_type(
        llm=Models().model_ollama,
        retriever=retriever,
        chain_type="stuff",
    )
    resposta = chain.run(pergunta)
    return resposta

# Função para carregar o JSON existente
def carregar_json(json_path):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"UFBA": []}

# Função para atualizar o JSON com novos componentes
def atualizar_json(json_data, novos_componentes):
    codigos_existentes = {item["CODIGO"] for item in json_data["UFBA"]}

    # Para cada novo componente, verifica se o código já existe
    for componente in novos_componentes:
        # Adiciona o componente apenas se o código não existir no conjunto de códigos existentes
        if componente["CODIGO"] not in codigos_existentes:
            json_data["UFBA"].append(componente)
            codigos_existentes.add(componente["CODIGO"])  # Atualiza o conjunto com o código novo
    
    return json_data

# Função para salvar o JSON atualizado
def salvar_json(json_data, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

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
        " Agora Organize por uma lista de matérias obrigatórias e outra não obrigatória."
    )

    # Processa o PDF e cria a base vetorial
    vector_db = processar_pdf(PDF_PATH)

    # Obtém a resposta do RAG
    resposta_rag = perguntar_ao_rag(pergunta, vector_db)

    # Converte a resposta em um formato utilizável
    novos_componentes = []
    for linha in resposta_rag.split("\n"):
        if " - " in linha:
            # Divide a linha em código e nome
            parte_codigo, nome = linha.split(" - ", 1)
            
            # Remover qualquer número ou ponto antes do código
            codigo = parte_codigo.strip().lstrip("0123456789.").strip()
            
            novos_componentes.append({
                "CODIGO": codigo,
                "NOME": nome.strip(),
                "CONTEUDO": "Descrição não disponível"
            })

    # Carrega e atualiza o JSON
    json_data = carregar_json(JSON_PATH)
    json_data = atualizar_json(json_data, novos_componentes)

    # Salva o JSON atualizado
    salvar_json(json_data, JSON_PATH)

    print(f"\n✅ JSON atualizado e salvo em {JSON_PATH}")
