import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def map_inputs(df):
    song_songid = {}
    artist_artist_id = {}
    genre_genreid = {}
    for index, track in enumerate(df['track_name'].unique(), start=1):
        song_songid[track] = index

    for index, artist in enumerate(df['artist'].unique(), start=1):
        artist_artist_id[artist] = index

    for index, genre in enumerate(df['tags'].unique(), start=1):
        genre_genreid[genre] = index


    df['song_id'] = df['track_name'].map(song_songid)
    df['artist_id'] = df['artist'].map(artist_artist_id)
    df['genre_id'] = df['tags'].map(genre_genreid)
    return song_songid, artist_artist_id, genre_genreid


def get_song_artist_genre_dict(df):
    song_to_artist_genre_map = {}
    for index, row in df[['song_id', 'artist_id', 'genre_id']].drop_duplicates().iterrows():
        song_id = row['song_id']
        artist_id = row['artist_id']
        genre_id = row['genre_id']
        song_to_artist_genre_map[song_id] = (artist_id, genre_id)
    return song_to_artist_genre_map

def get_sequences(df):
    song_sequences = []
    next_songs = []
    artist_sequences = []
    genre_sequences = []
    for session_id, group in df.groupby('session_id'):
        songs = group[['track_name', 'artist', 'tags']]
        song_ids = group['song_id'].tolist()
        artist_ids = group['artist_id'].tolist()
        genre_ids = group['genre_id'].tolist()

        for i in range(1, len(songs)):
            sequence_ids = []
            artist_seq = []
            genre_seq = []
            seen_songs = set()

            for j in range(i):
                current_song_id = song_ids[j]
                current_artist_id = artist_ids[j]
                current_genre_id = genre_ids[j]

                if current_song_id not in seen_songs:
                    sequence_ids.append(current_song_id)
                    artist_seq.append(current_artist_id)
                    genre_seq.append(current_genre_id)
                    seen_songs.add(current_song_id)

            next_song_id = song_ids[i]
            song_sequences.append(sequence_ids)
            artist_sequences.append(artist_seq)
            genre_sequences.append(genre_seq)
            next_songs.append(next_song_id)

    song_lengths = [len(x) for x in song_sequences]
    


def main():
    df = pd.read_csv("alltracks.csv", index_col=0)
    index_to_delete = df[df['tags'] == '[]'].index # remove songs without tags
    df.drop(index_to_delete, inplace=True)
    df['date_listened'] = pd.to_datetime(df['date_listened'])
    df['session_id'] = (df['date_listened'].diff() > pd.Timedelta(minutes=20)).cumsum() # make sessions
    song_songid, artist_artist_id, genre_genreid = map_inputs(df)
    songid_song = {value: key for key, value in song_songid.items()}
    artistid_artist = {value: key for key, value in artist_artist_id.items()}
    genreid_genre = {value: key for key, value in genre_genreid.items()}
    song_artist_genre_dict = get_song_artist_genre_dict(df)
    