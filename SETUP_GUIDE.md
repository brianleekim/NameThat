# NameThat - Local Setup Guide

This guide will help you set up the NameThat music guessing game locally on your machine.

## Prerequisites

- Python 3.8 or higher
- A Spotify account
- A Spotify Developer account

## Step 1: Clone the Project

```bash
git clone <repository-url>
cd NameThat
```

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Set Up Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app or use an existing one
3. In your app settings, add this redirect URI:
   ```
   http://127.0.0.1:8000/api/callback/
   ```
   Or if you want to use a different port (like 8080):
   ```
   http://127.0.0.1:8080/api/callback/
   ```
4. Copy your `Client ID` and `Client Secret`

## Step 4: Create Environment File

Create a `.env` file in the project root with your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8080/api/callback/
```

## Step 5: Run Setup Checker

```bash
python check_setup.py
```

This will verify your configuration is correct.

## Step 6: Set Up Database

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Start the Server

```bash
python manage.py runserver 8080
```

## Step 8: Test the Application

1. Open your browser and go to: `http://127.0.0.1:8080/api/login/`
2. You should be redirected to Spotify for authorization
3. After authorizing, you should see your playlists

## Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error**
   - Make sure the redirect URI in your Spotify app exactly matches: `http://127.0.0.1:8000/api/callback/`
   - Check for typos or extra spaces

2. **"Client ID not found" error**
   - Verify your `SPOTIFY_CLIENT_ID` in the `.env` file
   - Make sure there are no extra spaces or quotes

3. **Import errors**
   - Run `pip install -r requirements.txt` to install all dependencies

4. **Database errors**
   - Run `python manage.py makemigrations` and `python manage.py migrate`

5. **Port already in use**
   - Kill any existing Django server: `pkill -f runserver`
   - Or use a different port: `python manage.py runserver 8001`

### Still Having Issues?

Run the setup checker to identify specific problems:
```bash
python check_setup.py
```

## API Endpoints

- `GET /api/login/` - Start Spotify OAuth flow
- `GET /api/callback/` - Handle OAuth callback
- `GET /api/playlists/` - Get user's playlists
- `POST /api/round/` - Start a new game round

## Next Steps

Once the basic setup is working, you can:
1. Create a frontend interface
2. Implement the game logic
3. Add user authentication
4. Deploy to production 