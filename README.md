# Alerta Digital
**Pense antes de clicar. Proteja-se com informação.**

Aplicação educativa de extensão universitária sobre prevenção de golpes digitais. Inclui frontend React/TypeScript, API FastAPI, analisador local baseado em regras, integração opcional com API compatível com OpenAI, simulador, biblioteca, guia e conteúdo educativo.

## Requisitos
- Windows 10/11
- Python 3.10+
- Node.js 20+ e npm
- Visual Studio Code

## Estrutura
```text
alerta-digital/
├── backend/
│   ├── app/
│   │   ├── core/config.py
│   │   ├── routes/analysis.py
│   │   ├── schemas/analysis.py
│   │   ├── services/analyzer.py
│   │   └── main.py
│   ├── tests/test_analyzer.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/components/
│   ├── src/data/
│   ├── src/pages/
│   ├── src/services/
│   ├── src/types/
│   └── arquivos Vite/Tailwind
├── .gitignore
└── README.md
```

## 1. Executar no Windows (PowerShell)
Abra a pasta `alerta-digital` no VS Code. Abra dois terminais.

### Backend
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
# Se o PowerShell bloquear a ativação nesta sessão:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```
API: `http://127.0.0.1:8000`  
Documentação interativa: `http://127.0.0.1:8000/docs`

### Frontend (segundo terminal)
```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```
Abra o endereço mostrado pelo Vite (normalmente `http://localhost:5173`).

## 2. IA opcional
Por padrão, o sistema usa o analisador local e identifica isso explicitamente na resposta. Para habilitar IA externa, edite `backend/.env`:
```env
AI_PROVIDER=openai_compatible
AI_API_KEY=sua-chave
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```
O backend envia o texto da mensagem ao endpoint configurado. **Não cole dados pessoais, senhas, códigos ou informações bancárias.** Ao ativar IA externa, o conteúdo será processado pelo provedor configurado e ficará sujeito às políticas dele. A chave permanece apenas no backend. Sem chave, com `AI_PROVIDER=local` ou com falha no provedor, o sistema utiliza o analisador local e informa a origem. Configure apenas um serviço cujo tratamento de dados você tenha avaliado.

## 3. Disponibilizar para celulares na mesma rede
O frontend local pode ser iniciado com `npm run dev -- --host 0.0.0.0`. Configure `VITE_API_URL` com o endereço IP local do computador e inicie o backend com `uvicorn app.main:app --host 0.0.0.0 --port 8000`. Libere as portas necessárias no firewall somente em rede confiável. Dispositivos precisam estar na mesma rede Wi-Fi.

## 4. Publicar na internet
Uma opção é publicar o frontend em Vercel ou Netlify e o backend em Render ou serviço equivalente. Planos gratuitos, limites, suspensão por inatividade e disponibilidade mudam; confira os preços e condições atuais antes de escolher.
1. Envie o projeto para um repositório Git.
2. Publique `frontend` como projeto Vite. Defina `VITE_API_URL` com a URL pública do backend (sem barra final).
3. Publique `backend` como serviço Python. Build: `pip install -r requirements.txt`; start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Defina `CORS_ORIGINS` no backend com a URL exata do frontend publicado, separando múltiplas origens por vírgula.
5. Faça um teste real no celular: abra a página, analise um texto fictício, percorra o quiz e confira a biblioteca.
6. Gere um QR Code a partir da URL pública do frontend usando um gerador confiável ou a função de QR Code do serviço de publicação. Teste o QR Code em outro aparelho antes de imprimir.

Não use `localhost` como endereço público. Não coloque a chave da IA em variáveis `VITE_*`, pois elas são expostas no navegador.

## 5. Testes
Com o ambiente virtual ativo dentro de `backend`:
```powershell
pip install -r requirements.txt
pytest -q
```
O teste automatizado cobre regras principais, texto vazio e limite de tamanho. Testes de interface em navegadores reais devem ser feitos após instalar as dependências do frontend.

## Privacidade e limites
- Não há cadastro, login ou banco de dados.
- O backend não persiste o conteúdo recebido e não inclui o texto da mensagem nos logs da aplicação.
- A mensagem é processada em memória durante a solicitação.
- A integração externa é opcional e envia o texto ao provedor configurado.
- A classificação é educativa, não é confirmação de fraude nem probabilidade estatística.
- Poucos sinais identificados não significam que a mensagem seja segura.

## Rotas da API
- `GET /api/health`
- `POST /api/analyze` com JSON `{ "message": "texto para análise" }`
