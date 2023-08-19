# Filter spotify playlists

The purpose of this repository is to create a filtered playlist based on an existing one and the artists you send to the API.

## Table of Contents

1. [Create Spotify app](#create-spotify-app)
2. [Configure .env file](#configure-env-file)
3. [Running the App](#running-the-app)

## Create Spotify app

To create a Spotify app, follow these steps:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in with your Spotify account.
2. Click on "Create an App" and fill in the required information such as the app name and app description.
3. After creating the app, you will be redirected to the app dashboard. Here, you can find your Client ID and Client Secret, which are required for authentication.
4. Make sure to configure the app settings, such as adding redirect URIs and setting the app permissions.
5. Once you have completed the necessary configurations, you can start using the Spotify API in your app.

For more detailed instructions, you can refer to the [Spotify for Developers documentation](https://developer.spotify.com/documentation/general/guides/app-settings/).

## Configure .env file

To configure the `filter_spotify_playlists/.env` file, you need to provide the following information:

SPOTIPY_CLIENT_ID=<your_client_id>
SPOTIPY_CLIENT_SECRET=<your_client_secret>
SPOTIPY_REDIRECT_URI=<your_redirect_uri>

Make sure to replace `<your_client_id>`, `<your_client_secret>`, and `<your_redirect_uri>` with the actual values from your Spotify app.

## Running the App

To run the app and install dependencies with Poetry, follow these steps:

1. Make sure you have Poetry installed. If not, you can install it by following the instructions in the [Poetry documentation](https://python-poetry.org/docs/#installation).
2. Open a terminal and navigate to the root directory of the project.
3. Activate the virtual environment by running the command:

   ```bash
   poetry shell
   ```

4. Install the project dependencies by running the command:

   ```bash
   poetry install
   ```

5. Navigate to the `filter_spotify_playlists` directory by running the command:

   ```bash
   cd filter_spotify_playlists
   ```

6. Run the app with Uvicorn and specify the environment file by running the command:

   ```bash
   uvicorn main:app --env-file .env
   ```

This will start the app and make it accessible at the specified address.
