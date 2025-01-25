Documentação para Executar o Projeto
Este documento detalha como configurar, executar e interpretar os resultados do código fornecido, que utiliza uma API LLM para classificar matérias em trilhas de estudo com base em um arquivo JSON de entrada.

Requisitos
Certifique-se de ter os seguintes requisitos antes de executar o projeto:

Python:

Versão 3.8 ou superior.
Bibliotecas Python:

json
requests (instale com pip install requests)
Servidor LLM API:

Deve estar rodando localmente no endereço http://localhost:11434/api/chat.

Configuração
Clonar ou baixar o projeto: Certifique-se de que o código-fonte e o arquivo JSON estejam na mesma pasta.

Instalar bibliotecas necessárias: Execute o comando abaixo no terminal para instalar a biblioteca requests:
pip install requests
Configurar o servidor da API LLM:

Certifique-se de que o servidor da API LLM está em execução e acessível no endereço configurado: http://localhost:11434/api/chat.
Se o endereço ou porta forem diferentes, edite o valor de url_llm no código.

Abra o terminal na pasta onde o arquivo Python está localizado.

Execute o script com o comando:
python nome_do_arquivo.py

Como Interpretar os Resultados
Recomendações de matérias: Use a lista gerada para identificar em quais trilhas cada matéria foi classificada.

Relatório de Avaliação:

Acertos: Quantidade de matérias corretamente classificadas em cada trilha.
Erros: Matérias classificadas incorretamente.
Score total: Precisão geral do modelo, útil para avaliar a qualidade da classificação.
