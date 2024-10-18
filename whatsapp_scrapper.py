from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd
from datetime import datetime
from PIL import Image
from io import BytesIO
import base64
import openai_api

def initial_config():
    dir_path = os.getcwd()
    chrome_options2 = Options()
    #chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/profile/whatsapp")
    chrome_options2.add_argument("--start-fullscreen")
    driver = webdriver.Chrome(options=chrome_options2)         
    url = "https://web.whatsapp.com"
    driver.get(url)
    return driver


#******************* GLOBALS ************************
mensagens_df = pd.DataFrame(columns=['nome_contato', 'mensagem', 'role', 'time'])
driver = initial_config()
STOP = False
RUNNING = False

def verifica_conectado():
    global driver
    try:
        conversas_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "x1qlqyl8.x1pd3egz.xcgk4ki"))
            )
        
        return 200
    except:
        return 500
        
        
            
def getqrcode():
    try:
        global driver
        
        url = "https://web.whatsapp.com"
        driver.get(url)
        
        print("procurando elemento")
        # Aguarda o QR code aparecer
        qr_code_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan this QR code to link a device!']"))
        )

        # Captura a imagem do QR code
        qr_code_base64 = qr_code_element.screenshot_as_base64
        return qr_code_base64
    except:
        return 500

#***********************************  NOVA CONVERSA ******************************************
def nova_conversa(driver, mensagens_df, contact_name):  
    """
    Função que coleta todas as mensagens de uma nova conversa em um chat do WhatsApp Web,
    organizando as mensagens de entrada (recebidas) e saída (enviadas) em um DataFrame.
    """
    # Lista para armazenar mensagens recebidas na conversa (entradas)
    mensagens_entrada = []

    # Coleta todas as mensagens de entrada (recebidas) da conversa
    menssages_in = driver.find_elements(By.CLASS_NAME, "message-in.focusable-list-item._amjy._amjz._amjw")
    for i in menssages_in:
        try:
            copyable_texts = i.find_element(By.CLASS_NAME, "copyable-text")
            mensagens_entrada.append(copyable_texts.find_element(By.TAG_NAME, "span").text)
        except:
            None

    # Cria um DataFrame auxiliar para armazenar as mensagens recebidas
    aux_df = pd.DataFrame(columns=['nome_contato', 'mensagem', 'role', 'time'])
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Preenche o DataFrame com as mensagens de entrada
    aux_df['mensagem'] = mensagens_entrada
    aux_df['nome_contato'] = contact_name
    aux_df['role'] = 'user'
    aux_df['time'] = hora_atual

    # Concatenar o DataFrame auxiliar com o DataFrame original de mensagens
    mensagens_df = pd.concat([aux_df, mensagens_df])
    
    # Lista para armazenar mensagens enviadas na conversa (saídas)
    mensages_saida = []
    menssages_out = driver.find_elements(By.CLASS_NAME, "message-out.focusable-list-item._amjy._amjz._amjw")
    for i in menssages_out:
        try:
            copyable_texts = i.find_element(By.CLASS_NAME, "copyable-text")
            mensages_saida.append(copyable_texts.find_element(By.TAG_NAME, "span").text)
        except:
            None

    aux_df = pd.DataFrame(columns=['nome_contato', 'mensagem', 'role', 'time'])
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Preenche o DataFrame com as mensagens de saída
    aux_df['mensagem'] = mensages_saida
    aux_df['nome_contato'] = contact_name
    aux_df['role'] = 'assistant'
    aux_df['time'] = hora_atual

    # Concatenar o DataFrame auxiliar com o DataFrame original de mensagens
    mensagens_df = pd.concat([aux_df, mensagens_df])
    
    # Retorna o DataFrame atualizado com todas as mensagens da nova conversa
    return mensagens_df

def read_last_message(driver):
    """
    Função que lê a última mensagem recebida de um chat no WhatsApp Web.
    """
    last_message = ''
    menssages_in = driver.find_elements(By.CLASS_NAME, "message-in.focusable-list-item._amjy._amjz._amjw")
    
    for i in menssages_in:
        try:
            copyable_texts = i.find_element(By.CLASS_NAME, "copyable-text")
            last_message = copyable_texts.find_element(By.TAG_NAME, "span").text
        except:
            print("Erro ao carregar a ultima mensagem!")
    
    return last_message

def insert_message_dataframe(nome_contato, message):
    """
    Função que insere uma nova mensagem enviada pelo assistente em um DataFrame.
    """
    global mensagens_df
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Cria um dicionário com as informações da nova mensagem
    nova_mensagem = {
        'mensagem': message,
        'nome_contato': nome_contato,
        'role': 'assistant',  # Define o role como 'assistant'
        'time': hora_atual
    }

    # Converte o dicionário para DataFrame
    aux_df = pd.DataFrame([nova_mensagem])
    
    # Concatena a nova mensagem ao DataFrame original
    mensagens_df = pd.concat([mensagens_df, aux_df], ignore_index=True)
    
    #mensagens_df.to_excel("mensagens_df.xlsx")
    
    print("Mensagem do assistente registrada no DataFrame!")
    return mensagens_df


def send_message(driver, nome_contato, mensagens_df, text):
    """
    Função que envia uma mensagem para um contato no WhatsApp Web e registra a mensagem no DataFrame.
    """
    try:
        print("### Escrevendo resposta")
        
        mensagem = text
                
        # Combinando `contenteditable`, `aria-placeholder`, e `role`
        message_box = driver.find_element(By.XPATH, "//div[@contenteditable='true' and @aria-placeholder='Digite uma mensagem' and @role='textbox']")
        # Certifique-se que o elemento está visível
        driver.execute_script("arguments[0].scrollIntoView(true);", message_box)
        time.sleep(0.5)
        # Clique e insira o texto
        message_box.click()
        message_box.send_keys(mensagem)
        
        send_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Enviar']")
        send_button.click()
        
        
        #insert_message_dataframe(nome_contato, mensagem)
        print("### Resposta enviada")
        
        return mensagens_df
    except Exception as e:
        print(f"Erro ao enviar a resposta da mensagem: {str(e)}")
        return mensagens_df 

def process_new_conversation(driver, mensagens_df, contact_name):
    """
    Função para processar uma nova conversa e enviar a resposta automática.
    """
    print(f"### Nova CONVERSA com: {contact_name}")
    mensagens_df = nova_conversa(driver, mensagens_df, contact_name)
    #mensagens_df = send_message(driver, contact_name, mensagens_df, "resposta automatica")
    return mensagens_df

def process_existing_conversation(driver, mensagens_df, contact_name):
    """
    Função para processar uma conversa existente e enviar a resposta automática.
    """
    print(f"### Nova mensagem de: {contact_name}")
    mensagem = read_last_message(driver)
    hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nova_mensagem = {'mensagem': [mensagem], 'nome_contato': [contact_name], 'role': ['user'], 'time': hora_atual}
    
    aux_df = pd.DataFrame(data=nova_mensagem)
    mensagens_df = pd.concat([mensagens_df, aux_df])
    
    # Responde automaticamente à última mensagem recebida
    #mensagens_df = send_message(driver, contact_name, mensagens_df, "resposta automatica")
    return mensagens_df

def verify_open_chat(driver):
    """
    Função para verificar se há novas mensagens no chat que está aberto.
    """
    global mensagens_df
    try:
        nome_contato = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div/div/div/span").text
        print(f"Conversando com {nome_contato}")

        ultima_mensagem_chat = read_last_message(driver)
        print(f"## Última mensagem no chat: {ultima_mensagem_chat}")

        filtro = (mensagens_df['role'] == 'user') & (mensagens_df['nome_contato'] == nome_contato)
        ultima_mensagem_dataframe = mensagens_df[filtro].tail(1)
        print(f"## Última mensagem no Dataframe: {ultima_mensagem_dataframe['mensagem'].values[0]}")
        
        if ultima_mensagem_chat != ultima_mensagem_dataframe['mensagem'].values[0]:
            hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nova_mensagem = {'mensagem': [ultima_mensagem_chat], 'nome_contato': [nome_contato], 'role': ['user'], 'time': hora_atual}
            aux_df = pd.DataFrame(data=nova_mensagem)
            mensagens_df = pd.concat([mensagens_df, aux_df])

            #mensagens_df = send_message(driver, nome_contato, mensagens_df, "resposta automatica")
            print(mensagens_df)
        
        return mensagens_df
    except Exception as e:
        print("Nenhuma mensagem nova na conversa")
        return mensagens_df



def stopprocess():
    global STOP
    STOP = True

def getmessagesdf():
    global mensagens_df

    # Redefine o índice para garantir que seja único
    mensagens_df = mensagens_df.reset_index(drop=True)

    # Agora você pode converter para JSON sem problemas
    try:
        
        #json_data = mensagens_df.to_json()
        json_data = mensagens_df.to_json(orient="records")
        return json_data
    except ValueError as e:
        print(f"Erro ao converter para JSON: {e}")
        
        return None
    

def search_contact_by_name(driver,name): 
    print("Procurando Contato")   
    #Insere no name na caixa de busca do whatsapp
    caixa_pesquisa = driver.find_element(By.CLASS_NAME, "x1hx0egp.x6ikm8r.x1odjw0f.x6prxxf.x1k6rcq7.x1whj5v")
    #caixa_pesquisa.clear()
     # Método alternativo 1: Seleciona e apaga o texto existente
    caixa_pesquisa.send_keys(Keys.CONTROL + 'a')  # Ctrl + A para selecionar tudo (ou Command + A no macOS)
    caixa_pesquisa.send_keys(Keys.BACKSPACE)      # Apaga o texto selecionado
    caixa_pesquisa.send_keys(name)

    time.sleep(0.5)

    #procura o resultado que possui o name e clica no elemento
    resultados_da_pesquisa = driver.find_element(By.CLASS_NAME, 'x1y332i5.x1n2onr6.x6ikm8r.x10wlt62')
    
    xpath = f"//span[@title='{name}']"
    #xpath = f"//span[@title=normalize-space('{name}')]"
    busca = resultados_da_pesquisa.find_element(By.XPATH, xpath)
    print("Contato Encontrado")    
    print(busca.text)
    
    # Scrolling the element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", busca)
    time.sleep(0.5)  # Small pause to allow for scroll completion

    busca.click()
    
    return busca

def send_message_from_frontend(nome_contato, mensagem):
    global mensagens_df
    global driver
    
    try:
        #procura o contato na caixa de pesquisa
        search_contact_by_name(driver,nome_contato)
        time.sleep(0.5)
        #Manda mensagem para o contato
        mensagens_df = send_message(driver, nome_contato, mensagens_df, mensagem)
        
        return 200
    except Exception as e:
        print(e)
        return 500
    
    
def startprocess():
    global STOP
    global mensagens_df
    global RUNNING
    
    if RUNNING == True:
        print("Já está rodadando!")
        return None
    
    STOP = False                
    RUNNING = True

    print("### Iniciando o processo!")
    while not STOP:
        try:
            notificacao = driver.find_elements(By.CLASS_NAME, "x7h3shv")
            notificacao[1].click()
            time.sleep(0.5)
            print(f"### Notificação encontrada!")

            contact_name = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/header/div[2]/div/div/div/span").text

            if mensagens_df[mensagens_df['nome_contato'] == contact_name].empty:
                print(f"### Novo Contato!")
                #mensagens_df = process_new_conversation(driver, mensagens_df, contact_name)
                mensagens_df = process_existing_conversation(driver, mensagens_df, contact_name)
            else:
                print(f"### Contato existente {contact_name}")
                mensagens_df = process_existing_conversation(driver, mensagens_df, contact_name)

        except Exception as e:            
            time.sleep(0.5)

        mensagens_df = verify_open_chat(driver)
        
    
def resetmessages():
    global mensagens_df
    
    try:
        mensagens_df = pd.DataFrame(columns=['nome_contato', 'mensagem', 'role', 'time'])
    except:
        return 500
    
    return 200
