from openai import OpenAI
import pandas as pd
from dotenv import load_dotenv
import os

def load_open_ai_key():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    
    # Obtém a chave OPEN_AI_KEY do ambiente
    open_ai_key = os.getenv("OPEN_AI_KEY")
    
    # Retorna a chave ou lança um erro se não for encontrada
    if open_ai_key:
        return open_ai_key
    else:
        raise ValueError("OPEN_AI_KEY não encontrada no arquivo .env")


def gerar_resposta_openai(mensagens_df, nome_contato):
    """
    Função que cria o histórico de mensagens para um contato específico e faz uma chamada à API da OpenAI 
    para gerar uma resposta considerando o contexto da conversa.

    Parâmetros:
    - mensagens_df: DataFrame contendo o histórico de mensagens.
    - nome_contato: Nome do contato para quem será gerada a resposta.
    - api_key: Chave da API da OpenAI.

    Retorna:
    - Resposta gerada pela API da OpenAI.
    """
    
    # Filtra o DataFrame para obter apenas as mensagens do contato específico
    mensagens_contato = mensagens_df[mensagens_df['nome_contato'] == nome_contato]

    # Ordena as mensagens pelo tempo para garantir que estão na ordem correta
    mensagens_contato = mensagens_contato.sort_values(by='time')

    # Cria uma lista de dicionários com o formato {'role': 'user' ou 'assistant', 'content': 'mensagem'}
    historico_conversa = []
    historico_conversa.append({
            'role': 'system',
            'content': 'Você é um assistente de vendas de uma empresa chamada Sales IA. Diga que está pronto para ajudar no que for preciso. Apresente-se como Sarah.'
        })
    for _, row in mensagens_contato.iterrows():
        historico_conversa.append({
            'role': row['role'],
            'content': row['mensagem']
        })

    # Prepara o contexto para a chamada da API
    #openai.api_key = api_key

    try:
        api_key = load_dotenv()
        client = OpenAI(api_key=api_key)

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=historico_conversa
        )

        return completion.choices[0].message.content
        
    except Exception as e:
        print(f"Erro ao gerar resposta com a OpenAI: {str(e)}")
        return None
