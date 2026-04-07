# Projeto Alexandria

## Primeiros passos

1. Baixe o MySQL e configure um usuário

2. Crie um schema chamado `pi003`

3. Para começar o projeto, crie um arquivo `.env`, com propriedades ajustadas conforme o sistema pede, na raiz do projeto, há um `.env.example` que supre essas necessidades.

```ini
# Chave do servidor
## Pode usar https://randomkeygen.com/encryption-key em ambiente de desenvolvimento
## Para produção gere de um secrets.token_urlsafe(64)
SERVER_KEY=abc

# Propriedades Banco de dados
## Usuário base de dados
DB_USER=foo
## Senha
DB_PSWD=mypassword123
## Endereço
DB_HOST=127.0.0.1 # Esse é o endereço padrão
## Porta 
DB_PORT=3306 # Essa é a porta padrão do MySQL
```

4. Pode baixar o gerenciador de projetos uv (https://docs.astral.sh/uv/), ou utilize um ambiente virtual python, 

```
uv pip install -r requirements.txt

python -m virtualenv .venv
pip install -r requirements.txt
```

5. Entre no ambiente virtual:
    - Windows: `.venv/Scripts/activate`
    - Linux: `source .venv/bin/activate`

6. Rode os comandos:+, na pasta raiz do projeto:

```sh
python main.py makemigrations
python main.py migrate
python main.py runserver
```