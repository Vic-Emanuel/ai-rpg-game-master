from pydantic import BaseModel
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.genai.errors import ServerError
import time

load_dotenv()

class TurnoMestre(BaseModel):
    narracao: str
    delta_hp: int
    local_atual: str
    opcoes_acao: list[str]

class MestreRPG:

    #Inicializar o client
    def __init__(self):
        self.client = genai.Client()
    #Crio o chat
        self.chat = self.client.chats.create(
            model="gemini-3.8-flash",
            config=types.GenerateContentConfig(
                system_instruction="Você é um mestre de RPG, controle o HP, guie a história, mostre o local atual e as opções de ação",
                response_mime_type="application/json",
                response_schema=TurnoMestre
            )
        )
         
    def playerTurno(self, acao_jogador: str) -> TurnoMestre:
        #Aqui é pra enviar a ação do jogador pra IA, e eu coloquei o for tentativa em range pra o sistema ficar insistindo no modelo de IA se ele não estiver disponível
        for tentativa in range(3):
            try:
                resposta = self.chat.send_message(acao_jogador)
                break
            except ServerError:  
                #se a tentativa chegar no 2 e não funcionar, ele dá um 'raise' que aumenta o limite
                if tentativa == 2:
                    raise 
                else:
                    #pro tempo ir aumentando cada tentativa pra não travar o pc
                    tempo = 5 + (tentativa + 1)
                    time.sleep(tempo)

        estado_atual: TurnoMestre = resposta.parsed
        return estado_atual

mestre = MestreRPG()

#pra começar!
hp_atual = 100
estado = mestre.playerTurno("começar aventura")

while hp_atual > 0:
    hp_atual += estado.delta_hp
    print(f"\n Local: {estado.local_atual} |  HP: {hp_atual}")
    print(f" {estado.narracao}\n")

    print("Sugestões:")
    for i, opcao in enumerate(estado.opcoes_acao, 1):
        print(f"  {i}. {opcao}")

     #Ação jogador
    texto_jogador = input("\nO que você faz? > ")
    
    estado = mestre.playerTurno(texto_jogador)

print ("Você morreu.")