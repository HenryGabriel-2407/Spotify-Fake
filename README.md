# Spotify Fake
 Trabalho de Engenharia de Software

## Antes de tudo...
 Primeiro passo vai criar e inicializar um ambiente virtual para este projeto
 - ```pip install poetry```
 - ```poetry new nome_projeto```
 - ```cd nome_projeto```
 - ```poetry shell```
   
Em seguida vamos instalar as bibliotecas necessárias como fastapi[standard] (que é a principal ferramenta para abrir o servidor e realizar as operações), pydantic (para validação de entrada e saída de dados), ruff (para "legibilidade"), taskipy (para abstrair comandos longos) e pytest (para realizar testes - como o próprio nome fala...)

 - ```poetry add nome_biblioteca```
 - ```poetry update``` (é importante que sempre faça isso para atualizar alguma ferramenta e evitar erros)

Agora vamos ter acesso a api do Spotify, vai a este link: https://developer.spotify.com/documentation/web-api
Realiza o login na sua conta e recarrega a página do link e na sua conta existe a aba "dashboard" e clica em "crate app" e realiza as suas configurações e coloca esta URL neste campo para Spotify saber aonde vai destinar o uso da api;
![image](https://github.com/user-attachments/assets/0f3bf616-9bae-49fe-96df-de40509597e3)
Com isso pronto, vai em "dashboard", no app criado e em "settings" e copia seu Client ID e Client secret (esses tokens são temporários por aporximadamente uma hora até receberem novos tokens) e escreva este seguinte códio em app.py:
```
# Informações de autenticação do Spotify
client_id = "CLIENT_ID que copiou em settings"
client_secret = "CLIENT_SECRET que copiou em settings"

# URL para obter o token de acesso
token_url = "https://accounts.spotify.com/api/token"

# Codificar credenciais em Base64
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# Definir os parâmetros e cabeçalhos para obter o token
data = {
    'grant_type': 'client_credentials'
}
headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/x-www-form-urlencoded'
}
````
Recomendo que antes do poetry update escrever o seu arquivo .toml semelhante a meu. E por fim, já podemos iniciar o "servidor" e por a mão na massa! como ```task run``` (personalizei este comando para iniciar o fastapi e o servidor, mas pode escrever fastapi dev nome_da_pasta/app.py [como pode ver nos códigos])
