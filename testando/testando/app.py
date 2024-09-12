from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from testando.schemas import Musica, Musicas

import base64
import requests
import random


# Inicializando o fastapi
app = FastAPI()

# Informações de autenticação do Spotify
client_id = "03d8c173d4dc4b2fadfc95c767e82645"
client_secret = "1fc63f29ccfd4a0e8d5769073a137964"

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

# Configurar a pasta estática
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

@app.get("/", response_class=HTMLResponse)
def serve_html():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

def get_access_token():
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['access_token']
    else:
        return None

@app.get("/search/", response_model=Musicas)
def buscar_musica(q: str = Query(None, description="Nome da música ou artista a ser buscado")):
    access_token = get_access_token() #vai verificar se o usuário possui acesso
    if not access_token:
        return Musicas(musicas=[])

    search_headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    results = []

    # Buscar por músicas
    search_params = {
        'q': f'track:"{q}"',
        'type': 'track',
        'limit': 20
    }
    search_url = "https://api.spotify.com/v1/search"
    response = requests.get(search_url, headers=search_headers, params=search_params)
    
    if response.status_code == 200:
        search_results = response.json()
        tracks = search_results.get('tracks', {}).get('items', [])
        
        if tracks:
            results.extend([Musica(link=f"https://open.spotify.com/embed/track/{track['id']}") for track in tracks])

    # Buscar por artistas
    search_params = {
        'q': q,
        'type': 'artist',
        'limit': 5 
    }
    response = requests.get(search_url, headers=search_headers, params=search_params)
    
    if response.status_code == 200:
        search_results = response.json()
        artists = search_results.get('artists', {}).get('items', [])
        
        if artists:
            artist_id = artists[0]['id']
            # Buscar as músicas do artista
            tracks_params = {
                'limit': 20
            }
            tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
            response = requests.get(tracks_url, headers=search_headers, params=tracks_params)
            
            if response.status_code == 200:
                tracks_results = response.json()
                tracks = tracks_results.get('tracks', [])
                
                results.extend([Musica(link=f"https://open.spotify.com/embed/track/{track['id']}") for track in tracks])

    # Embaralhar a lista de resultados antes de retornar
    random.shuffle(results)
    return Musicas(musicas=results)
