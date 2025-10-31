# Calebet Backend

Projeto FastAPI utilizando SQLAlchemy, Pydantic e Uvicorn.

## Executando localmente

1. Crie um ambiente virtual e instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure as variáveis de ambiente copiando `.env.example` para `.env` e ajuste os valores conforme necessário.

3. Inicie o servidor de desenvolvimento:

   ```bash
   uvicorn app.main:app --reload
   ```

## Executando com Docker

```bash
docker build -t calebet-backend .
docker run -p 8000:8000 calebet-backend
```
