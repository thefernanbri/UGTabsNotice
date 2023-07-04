import requests
from bs4 import BeautifulSoup
import json
import datetime
from jinja2 import Environment, FileSystemLoader
import webbrowser
import os

# Define o nome do arquivo de controle
arquivo_controle = "arquivo_controle.txt"

# Obtém a data atual
data_atual = datetime.date.today()

# Verifica se o arquivo de controle existe e contém a data atual
if os.path.exists(arquivo_controle):
    with open(arquivo_controle, "r") as arquivo:
        data_ultima_execucao = arquivo.read().strip()
        if data_ultima_execucao == str(data_atual):
            print("O script já foi iniciado hoje. A execução será interrompida.")
            exit()

# Atualiza o arquivo de controle com a data atual
with open(arquivo_controle, "w") as arquivo:
    arquivo.write(str(data_atual))

# URL da página a ser extraída
url = 'https://www.ultimate-guitar.com/explore?order=date_desc&type[]=Official'

# Nome do arquivo para armazenar a última verificação
ultimo_arquivo = 'ultima_verificacao.txt'
# Nome do arquivo para armazenar o template HTML
template_arquivo = 'tabs_template.html'
# Nome do arquivo gerado
html_output = 'tabs.html'

try:
    # Fazer a requisição HTTP
    response = requests.get(url)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Extrair o conteúdo HTML da resposta
        html_content = response.text

        # Analisar o HTML usando o BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrar o elemento <div> com a classe 'js-store' e obter o atributo 'data-content'
        div_element = soup.find('div', class_='js-store')
        data_content = div_element.get('data-content')

        # Converter o conteúdo em formato JSON em um objeto Python
        data = json.loads(data_content)

        # Acessar as chaves necessárias para chegar à lista de tabs
        tabs = data['store']['page']['data']['data']['tabs']

        # Ler a data e hora da última verificação
        ultima_verificacao = None
        try:
            with open(ultimo_arquivo, 'r') as file:
                ultima_verificacao = file.read().strip()
        except FileNotFoundError:
            pass

        # Armazenar a data e hora atual
        current_datetime = datetime.datetime.now()

        # Verificar se houve adição de novas tabs desde a última verificação
        if ultima_verificacao != str(current_datetime):
            # Atualizar a data e hora da última verificação
            with open(ultimo_arquivo, 'w') as file:
                file.write(str(current_datetime))

            # Percorrer os tabs e extrair os dados desejados
            today_tabs = []
            for tab in tabs:
                timestamp = int(tab['date'])
                tab_datetime = datetime.datetime.fromtimestamp(timestamp)

                # Verificar se a tab foi adicionada hoje ou depois da última verificação
                if tab_datetime.date() == current_datetime.date() and tab_datetime >= datetime.datetime.strptime(ultima_verificacao, '%Y-%m-%d %H:%M:%S.%f'):
                    formatted_date = tab_datetime.strftime('%d/%m/%Y %H:%M:%S')
                    tab['formatted_date'] = formatted_date
                    today_tabs.append(tab)

            # Verificar se há novas tabs para criar o template
            if today_tabs:
                # Carregar o template HTML
                env = Environment(loader=FileSystemLoader('.'))
                template = env.get_template(template_arquivo)

                # Renderizar o template com os dados das tabs
                output = template.render(tabs=today_tabs)

                # Salvar o HTML resultante em um arquivo
                with open(html_output, 'w') as file:
                    file.write(output)
                print("Template HTML criado com sucesso.")

                # Abrir o arquivo no navegador
                webbrowser.open(html_output)
            else:
                print("Nenhuma nova tab foi adicionada desde a última verificação.")

        else:
            print("Nenhuma nova tab foi adicionada desde a última verificação.")

    else:
        print("A requisição falhou.")

except Exception as e:
    print("Ocorreu um erro:", str(e))
    os.system("pause")
