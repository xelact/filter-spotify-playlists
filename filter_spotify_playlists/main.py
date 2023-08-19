import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import FastAPI, responses
from spotipy.client import SpotifyException
from pydantic import BaseModel

app = FastAPI()
scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


@app.get("/")
def read_root():
    return {"message": "API is running"}


def get_playlist_tracks(playlist_id: str):
    playlist = sp.playlist(playlist_id)
    tracks = []
    new_tracks = playlist["tracks"]
    tracks.extend(new_tracks["items"])
    while new_tracks["next"]:
        new_tracks = sp.next(new_tracks)
        tracks.extend(new_tracks["items"])
    return tracks


@app.get("/playlist_artists/{playlist_id}")
def get_playlist_artists(playlist_id: str):
    try:
        tracks = get_playlist_tracks(playlist_id)
        artists = {}
        for track in tracks:
            artists_of_track = track["track"]["artists"]
            for artist in artists_of_track:
                if artist["name"] not in artists:
                    artists[artist["name"]] = artist["id"]
        return {"artists": artists}
    except SpotifyException as e:
        if e.http_status == 404:
            return responses.JSONResponse(
                status_code=404, content={"message": "Playlist not found"}
            )
        else:
            return responses.JSONResponse(
                status_code=500, content={"message": "Something went wrong"}
            )


class Artists(BaseModel):
    # the POST will contain a JSON of variable length, e.g. { "Casino Montreal": "0VXzhlJIwcZxSkxRUqIAG5", "The Beatles": "3WrFJ7ztbogyGnTHbHJFl2" }
    # the key is the artist name, the value is the artist id
    artists: dict[str, str]


@app.post("/create_copy_playlist/{playlist_id}")
def create_copy_playlist(playlist_id: str, artists: Artists):
    # get the tracks of the original playlist that match the artists provided
    all_tracks = get_playlist_tracks(playlist_id)
    tracks = set()
    for track in all_tracks:
        artists_of_track = track["track"]["artists"]
        for artist in artists_of_track:
            if artist["name"] in artists.artists:
                tracks.add(track["track"]["id"])

    # create a new playlist with the same name as the original playlist
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist["name"]
    new_playlist = sp.user_playlist_create(
        sp.me()["id"], playlist_name + " (filtered)", public=False
    )

    # add the tracks to the new playlist
    tracks = list(tracks)
    while tracks:
        if len(tracks) < 100:
            sp.playlist_add_items(new_playlist["id"], tracks)
            tracks = []
        else:
            sp.playlist_add_items(new_playlist["id"], tracks[:100])
            tracks = tracks[100:]

    return {"id": new_playlist["id"]}
