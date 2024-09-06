# importando todas as bibliotecas
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ytmusicapi import YTMusic

from testando.schemas import Musica, Musicas

# inicializando
app = FastAPI()

lista_musica = []

yt = YTMusic({
 "scope": "https://www.googleapis.com/auth/youtube",
 "token_type": "Bearer",
 "access_token": "ya29.a0AcM612xzwRSW1ZhBuU-3BVtrL--cF0fXLdObStFDlDrE7cEqSGeCVd9N5UgEB-V9BnOIgMpT1dRSlMIv0xde73-SsoEy-v5ptlkqCsslvI-GBLUOV1HsX-z0AvwZiyKUi8fZF3HW5o86PbLBANNHgyWfuDEEdVaCtoZIyku5sHTPI33b-v59aCgYKAXASARASFQHGX2Mis-ZJCPqaxO8tKr6fqLrA0w0187",
 "refresh_token": "1//0hh-ATI_R3kJxCgYIARAAGBESNwF-L9IrzCYfkWIOwjLI9K9PpxSboqoK9fJpFecNOc171sGRbG_6DtmzqATGoWkZQypY-JBuINo",
 "expires_at": 1725279178,
 "expires_in": 72508
})

# Configurar a pasta estática
app.mount("/templates", StaticFiles(directory="templates"), name="templates")


@app.get("/", response_class=HTMLResponse)
def serve_html():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())


@app.get("/search/", response_model=Musicas)
def buscar_musica(q: str = Query(None, description="Nome da musica ou artista a ser buscado")):
    result = yt.search(q)
    lista_musica.clear()
    if result:
        for i in range(len(result)):
            if result[i]['category'] == "Videos" or result[i]['resultType'] == "song":
                id_musica = str(result[i]['videoId'])
                title = str(result[i]['title'])
                # Verifica se há mais de um artista antes de tentar acessar o segundo
                if 'artists' in result[i] and len(result[i]['artists']) > 1:
                    artist = str(result[i]['artists'][1]['name'])
                else:
                    artist = str(result[i]['artists'][0]['name'])  # Pega o primeiro artista se não houver um segundo
                thumbnail_url = str(result[i]['thumbnails'][0]['url'])
                musica = Musica(id=id_musica, thumbnail=thumbnail_url, title=title, artist=artist)
                lista_musica.append(musica)

    return {'music': lista_musica}

# fastapi dev testando/app.py --host 0.0.0.0
