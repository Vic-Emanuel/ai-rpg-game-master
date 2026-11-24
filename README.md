#O que é: RPG interativo no terminal com Mestre narrativo usando google-genai e saída estruturada com Pydantic (TurnoMestre).

#Decisões técnicas aplicadas: validação de schema JSON/tipado, retry com backoff em ServerError (503), controle de hp_atual no código separado do delta_hp do turno e credenciais via .env.

#Como rodar: criar ambiente virtual, instalar dependências (google-genai, pydantic, python-dotenv), criar .env com GEMINI_API_KEY=... e executar o script.