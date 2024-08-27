# RNN playlist generator

## Description
RNN model that generates songs based on your listening patterns collected from lastfm's API.

## Usage
You'll first need to have a lastfm account.
Open lastfmapi.ipynb and run the script with your username. - This will generate a csv file of all the songs you've listened to from a starting date.
After running the script, you'll have "alltracks.csv" in your directory.
You can now run genre_predictor.ipynb to generate your playlist!

## Model architecture
The model is an RNN model with 3 inputs, song_id, artist_id, and genre_id.
The inputs are encoded and processed into an embedding layer, a hidden layer and finally, the output layer.
