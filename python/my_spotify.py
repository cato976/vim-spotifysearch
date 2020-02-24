import vim
import spotipy
import os
import json
import spotipy.util as util

from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
token = ''


def windows_uri_opener(uri):
    # vim.current.buffer.append(str(os.getenv('SPOTIFY_USER_ID')), 0)
    global token
    if(token == ''):
        token = util.prompt_for_user_token(
                username=os.getenv('SPOTIPY_USER_ID'),
                scope='user-modify-playback-state',
                redirect_uri='http://google.com')

    # print(token)
    s = spotipy.Spotify(auth=token)
    print(vim.eval('a:uri'))
    print(vim.eval('s:the_uri'))
    internal_uri = vim.eval('s:the_uri')

    track_details = s.track(internal_uri)
    print(track_details)
    # y = json.loads(str(track_details))
    y = json.dumps(track_details)
    track_json = json.loads(y)
    # vim.current.buffer.append(str(track_details), 0)
    # vim.current.buffer.append(str(track_json), 2)
    # vim.current.buffer.append(y, 4)
    print(track_json['album'])

    s.start_playback(device_id=os.getenv(
        'SPOTIFY_DEVICE_ID'),
        context_uri=track_json['album']['uri'],
        offset=track_json['track_number']-1)


def track_search(track):
    client_credentials_manager = SpotifyClientCredentials()
    s = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    results = s.search(vim.eval("a:track"), type="track")
    results['tracks']['next'] = 'None'
    results['tracks']['previous'] = 'None'

    vim.vars['tracks'] = dict(results)  # vim.Dictionary(results)


def artist_lookup(artist_uri):
    client_credentials_manager = SpotifyClientCredentials()

    s = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = s.artist_albums(vim.eval("a:artist_uri"), album_type='album')
    results['previous'] = 'None'
    results['next'] = 'None'
    vim.vars['tracks'] = dict(results)  # vim.Dictionary(results)


def album_lookup(album_uri):
    client_credentials_manager = SpotifyClientCredentials()
    s = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    results = s.album(vim.eval("a:album_uri"))
    results['tracks']['next'] = 'None'
    results['tracks']['previous'] = 'None'
    vim.vars['tracks'] = dict(results)  # vim.Dictionary(results)
