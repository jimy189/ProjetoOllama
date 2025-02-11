Este projeto utiliza um **modelo de linguagem natural (LLM)** para classificar disciplinas com base no perfil do usuário. O script lê um arquivo JSON contendo as matérias, faz perguntas ao LLM e calcula a precisão da classificação.

## 🚀 Tecnologias Utilizadas
- **Python**
- **Requests** (para chamadas HTTP)
- **JSON** (para manipulação dos dados)
- **LLM Local** (exemplo: Ollama)

## 📂 Estrutura do Projeto
📂 projeto
│-- 📄 script.py          # Script principal
│-- 📄 requirements.txt   # Dependências
│-- 📄 README.md         # Documentação
│-- 📂 data
│   └── 📄 Ementa BI CeT.json  # Base de disciplinas


## 📌 Pré-requisitos
1. **Python 3.x** instalado.
2. Um **LLM local** rodando em http://localhost:11434/api/chat.
3. **Instalação das dependências:**

bash
pip install -r requirements.txt


## 🔧 Como Rodar o Projeto
### 1️⃣ Criar e Ativar um Ambiente Virtual (Opcional, mas Recomendado)
bash
python -m venv venv  # Cria o ambiente virtual

- **Windows:**

bash
venv\Scripts\activate

- **Linux/Mac:**

bash
source venv/bin/activate


### 2️⃣ Instalar Dependências
bash
pip install requests
pip install langchain 
pip install langchain-community
pip install langchain-ollama
pip install langchain
pip install chromadb
pip install PyPDF2


### 3️⃣ Certificar-se de que o Servidor LLM está Rodando
Se estiver utilizando o **Ollama**, execute:
bash
ollama run llama3.2:3b


### 4️⃣ Rodar o Script
bash
python Projeto.py
python rag.py
python rag2.py


## 📊 Funcionalidades Projeto.py
✔️ Lê um arquivo JSON com disciplinas.
✔️ Faz perguntas ao LLM para definir o perfil do usuário.
✔️ Classifica as matérias com base nas respostas.
✔️ Calcula a precisão da classificação.


## 📊 Funcionalidades rag.py
✔️ Lê um arquivo em PDF com ementa do curso.
✔️ Mostra o que extraiu do pdf.


## 📊 Funcionalidades rag2.py
✔️ Lê um arquivo em PDF com ementa do curso.
✔️ Mostra o que extraiu do pdf.
✔️ Verifica no json o se existe a matéria, se não existir ele atualizar o 
o json com matéria nova.
✔️ Rode de novo Projeto.py para ter um novo resultado.

## 📊 Fine Tuning
Passe o arquivo no colab question-fine-tuning.json que esta 
no repositório.
https://drive.google.com/file/d/11jJgwZkAAJmgSxdcb6crSnFu7atM92H-/view?usp=sharing

