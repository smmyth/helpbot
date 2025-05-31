# HelpBot - Chatbot de Atendimento Automatizado

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/flask-%233584A1.svg?style=flat&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT-brightgreen)
![n8n](https://img.shields.io/badge/n8n-Automations-orange)

## 🚀 Visão Geral do Projeto

O **HelpBot** é um chatbot de atendimento automatizado para pequenas empresas, desenvolvido em Python com Flask, integração opcional com IA (OpenAI GPT), automação via n8n, e armazenamento em MongoDB. É um projeto modular, escalável e pronto para produção, demonstrando habilidades em API REST, integração de serviços, automação e boas práticas de software.

> **Motivação e Aprendizados**  
> Desenvolvi o HelpBot como parte da minha transição para a área de back-end, aplicando conceitos de APIs modernas, automação de fluxos reais via n8n, e integração com IA. O projeto serviu para consolidar habilidades técnicas e soft skills como documentação, testes e entrega de código limpo.

---

### ✨ Funcionalidades Principais

- API RESTful para envio e listagem de mensagens.
- Integração opcional com OpenAI (GPT-3.5-turbo ou configurável) para respostas geradas por IA.
- Integração opcional com n8n via webhooks para automação de processos (ex: CRM, notificações).
- Armazenamento de mensagens em MongoDB.
- Validação de dados de entrada usando Pydantic.
- Configuração baseada em variáveis de ambiente.
- Suporte a Docker e Docker Compose para fácil deploy.
- Testes unitários e de integração com Pytest.
- Documentação da API com Swagger/OpenAPI.

---

## 📚 Documentação Técnica

### Pré-requisitos

- Python 3.10+
- MongoDB 5.0+ (ou use a versão do Docker)
- Docker & Docker Compose (recomendado para fácil execução)
- Conta na OpenAI com chave de API (opcional, para funcionalidade de IA)
- Instância do n8n configurada com um webhook (opcional, para automações)

### Instalação e Configuração Local

Clone o repositório e acesse a pasta:

```bash
git clone https://github.com/seu-usuario/helpbot.git
cd helpbot
```

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure as variáveis de ambiente (copie o exemplo):

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais e configurações (veja `.env.example`).

Execute o MongoDB (localmente ou usando Docker):

```bash
docker-compose up -d mongo
```

Inicie a aplicação Flask:

```bash
flask run --host=0.0.0.0 --port=5000
```

Ou, para produção (Gunicorn):

```bash
gunicorn --bind 0.0.0.0:5000 "app:create_app()"
```

A aplicação estará disponível em http://localhost:5000.

---

### Execução com Docker (Recomendado)

Com Docker e Docker Compose instalados, basta rodar:

```bash
docker-compose up --build
```

A aplicação estará disponível em http://localhost:5000.  
O MongoDB estará acessível na porta 27017 do host.

---

### Testes

Para rodar os testes, garanta que `FLASK_ENV=testing` ou `TestConfig` use um banco de teste:

```bash
pytest tests/ -v
```

Para cobertura de testes (requer pytest-cov):

```bash
pytest --cov=app tests/
```

---

### Endpoints Principais da API

Base URL: `http://localhost:5000`

- **POST /api/v1/messages**  
  Envia uma nova mensagem para o chatbot.  
  Corpo da Requisição (JSON):

```json
{
  "content": "Qual o horário de funcionamento?",
  "user_id": "user_123_abc"
}
```

- **GET /api/v1/messages**  
  Lista as últimas mensagens (limite padrão de 100).

- **GET /api/v1/messages/{message_id}**  
  Busca uma mensagem específica pelo seu ID.

- **GET /health**  
  Verifica o status e a saúde do serviço.

---

### Documentação completa da API (Swagger)

Você pode visualizar a documentação completa da API usando um editor Swagger online e carregando o arquivo `app/static/swagger.yaml`, ou configurar o Flask para servir este arquivo como estático.

---

### Estrutura do Projeto

```
/
|-- app/                  # Módulo principal da aplicação Flask
|   |-- __init__.py       # Fábrica da aplicação (create_app)
|   |-- controller.py     # Lógica de negócio para mensagens
|   |-- models.py         # Modelos Pydantic para validação
|   |-- routes.py         # Definição das rotas da API
|   |-- services/         # Módulos de serviços externos (OpenAI, N8N)
|   |   |-- __init__.py
|   |   |-- n8n_integration.py
|   |   |-- openai_service.py
|   |-- static/           # Arquivos estáticos (ex: Swagger YAML)
|       |-- swagger.yaml
|-- tests/                # Testes automatizados
|   |-- conftest.py       # (Opcional) Fixtures globais para Pytest
|   |-- test_routes.py
|-- .env.example          # Arquivo de exemplo para variáveis de ambiente
|-- .gitignore            # Arquivos e pastas a serem ignorados pelo Git
|-- config.py             # Configurações da aplicação (classes de Config)
|-- docker-compose.yml    # Configuração do Docker Compose
|-- requirements.txt      # Dependências Python
|-- README.md             # Este arquivo
|-- webhook_automation.json # Exemplo de fluxo n8n (para importar no seu n8n)
```

---

### Integração com n8n (Exemplo de Webhook)

O arquivo `webhook_automation.json` contém um exemplo de fluxo pronto para importar no n8n, receber mensagens do HelpBot, processar dados e encaminhar para outros serviços.

- Importe o arquivo no seu n8n.
- Ative o webhook e copie a URL.
- Configure essa URL no `.env` (`N8N_WEBHOOK_URL`).

---

### 🖼️ Prints e Demonstração (Sugestões)

- GIF mostrando a interação via Postman/Insomnia.
- Print do fluxo importado e funcionando no n8n.
- Exemplo visual da documentação Swagger.

---

## 🛠 Habilidades Demonstradas

- Python intermediário/avançado (tipagem, Pydantic, estrutura modular)
- Flask & Flask-RESTful (APIs RESTful robustas)
- Integração de IA (OpenAI)
- Automação de fluxos (n8n)
- MongoDB (persistência NoSQL)
- Docker & Docker Compose (containerização)
- Testes automatizados (Pytest)
- Documentação técnica (Swagger/OpenAPI)
- Boas práticas de código (clean code, versionamento, SRP)
- Configuração e deploy (envs, Gunicorn)

---

## 🤝 Como Contribuir

1. Fork este repositório.
2. Crie uma branch: `git checkout -b feature/nome-da-sua-feature`
3. Faça commits claros.
4. Envie para o seu fork: `git push origin feature/nome-da-sua-feature`
5. Abra um Pull Request detalhado.

---

## 🔒 Segurança

- **Variáveis de Ambiente:** dados sensíveis (chaves de API, URIs de banco, SECRET_KEY) só no `.env`, nunca no Git.
- **Chaves de API:** use chaves reais apenas em ambientes seguros.
- **Validação:** toda entrada é validada pelo Pydantic.
- **Docker:** sempre use imagens confiáveis e atualizadas.

---

## 👨‍💻 Autor

Desenvolvido por Smmyth Albuquerque  
Recife/PE - Brasil  
Contato: smmythk@gmail.com  
LinkedIn: [linkedin.com/in/smmyth](https://linkedin.com/in/smmyth)  
GitHub: [github.com/seu-usuario](https://github.com/smmyth)

> Busco aplicar e expandir meus conhecimentos em Python, Flask, API REST e automações, contribuindo com times de tecnologia em ambientes colaborativos, ágeis e inovadores.  
> **Disponível para vagas de Desenvolvedor Back-End (Júnior, Estágio ou Trainee) — remoto, híbrido ou presencial (Recife/PE).**
