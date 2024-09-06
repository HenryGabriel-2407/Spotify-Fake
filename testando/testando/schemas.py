from typing import List

from pydantic import BaseModel


class Musica(BaseModel):
    id: str
    title: str
    artist: str
    thumbnail: str


class Musicas(BaseModel):
    music: List[Musica]
