# API user Fastapi
Projeto de API usando FastAPI com estrutura MVC, autenticação JWT e <strike>testes unitários</strike> 

- [x] Fastapi
- [x] SQLAlchemy
- [x] SqLite
- [x] User CRUD
- [x] Paginação
- [x] JWT
- [ ] <strike>Filtros</strike>
- [ ] <strike>Testes unitários</strike>


## Rodar projeto localmente

Clone o projeto e vá para o diretório do mesmo
```bash
$ git clone https://github.com/hinnaxi/user-api-fastapi.git
$ cd user-api-fastapi
```

Crie e ative o ambiente virtual do python
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Instale os pacotes com pip
```bash
$ pip install -r requirements.txt
```

Copie o arquivo .env.example e renome para .env
```bash
$ cp .env.example .env
```

Não esqueça de gerar e inserir o JWT_SECRET_KEY no .env
```bash
$ openssl rand -hex 32
```

Execute a aplicação
```bash
$ uvicorn src.main:app --reload
```

## Documentação interativa do Fastapi
```http
  GET 127.0.0.1:8000/docs
```
