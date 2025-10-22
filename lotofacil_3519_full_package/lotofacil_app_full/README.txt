Gerador Lotofácil - Pacote deployável (concurso 3519)
================================================
Conteúdo:
- app.py            -> Flask backend simples
- requisitos.txt    -> Dependências
- static/index.html -> Frontend leve
- jogos_3519.csv    -> CSV com 5 jogos preparados
- historico.json    -> (vazio) para histórico de resultados
- config.json       -> (opcional) configurações iniciais

Como usar localmente
--------------------
1) Criar virtualenv:
   python -m venv env
   source env/bin/activate   # linux/mac
   env\Scripts\activate    # windows

2) Instalar dependências:
   pip install -r requirements.txt

3) Rodar:
   python app.py
   Abrir http://localhost:5000

Deploy (opções recomendadas)
---------------------------
Recomendamos Render (render.com) ou Railway (railway.app) para deploy rápido de apps Flask.
- Render: tutorial oficial "Deploy a Flask App on Render". Render aceita deploy direto de um repositório GitHub e gera uma URL pública rapidamente. (Documentação: render.com/docs/deploy-flask). 
- Railway: também permite deploy a partir de GitHub com detecção automática do app Python (docs: railway.com/guides/flask).

Observações importantes:
- Heroku encerrou o suporte ao plano gratuito (desde 2022), por isso preferimos Render ou Railway. 
- Para produção, implemente um método seguro de atualização automática de resultados (scraper/API) e rate-limit para evitar bloqueios no site de origem.

Referências úteis:
- Render quickstart: https://render.com/docs/deploy-flask
- Railway Flask guide: https://docs.railway.com/guides/flask
- Nota sobre fim do free tier Heroku: https://www.heroku.com/blog/next-chapter

Se quiser, eu monto e envio também um arquivo Dockerfile e um workflow simples para GitHub Actions para deploy automático.
