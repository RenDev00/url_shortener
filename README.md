# URL Shortener
A Flask-based web app to shorten long URLs with persistant storage powered by [Supabase](https://supabase.com/) Postgres. An already deployed version, which is powered by [Render](https://render.com/), can be found [here](https://url-shortener-q5tt.onrender.com/).

## Features
- Shorten long URLs to 6-character codes.
- Redirect short URLs to their original URLs.
- Keep track of URL click counts.
- Copy-to-clipboard functionality (JavaScript).
- Unit tests with pytest.

## Screenshots
### Home Page
![Home Page](https://i.imgur.com/WRjb1RR.png)
*Enter a URL to get a shortened link.*

### Shortened URL
![Short URL](https://i.imgur.com/hT3HY10.png)
*Generated short URL with clickable copy-to-clipboard link.*

## Setup
1. Clone the repo:
```bash
git clone https://github.com/RenDev00/url_shortener.git
cd url_shortener
```
2. Install requirements:
```bash
pip install -r requirements.txt
```
3. Create a `./src/.env` file and fill it with your information according to the following template:
```
SUPABASE_KEY = <your supabase api key>
SUPABASE_URL = <your supabase api url>
HOST_URL = <link to your render webservice | http://127.0.0.1:5000 for local testing>
```
4. Run the app locally:
```bash
flask --app .\src\main.py run
```
Or use gunicorn to run it in a production environment:
```bash
cd src && gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## Testing
Run the tests using pytest:
```bash
pytest tests/
```

## License
MIT
