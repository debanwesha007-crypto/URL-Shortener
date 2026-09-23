# 🔗 URL Shortener

A simple and lightweight **URL Shortener** built with **Python, Flask,
and SQLite**.

The application converts long URLs into short, easy-to-share links and
provides a web interface as well as REST API endpoints for creating,
viewing, and deleting shortened URLs.

------------------------------------------------------------------------

## 🚀 Features

-   🔗 Shorten long URLs into unique 6-character codes
-   ✨ Create custom short codes
-   🔄 Redirect short URLs to their original URLs
-   📊 Track the number of clicks on each shortened URL
-   📋 View all shortened URLs
-   🗑️ Delete shortened URLs
-   ✅ Basic URL validation
-   🌐 Web-based interface
-   🔌 REST API support
-   💾 SQLite database for storing URL mappings
-   📱 Simple and responsive frontend

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Technology   Purpose
  ------------ --------------------------
  Python       Backend programming
  Flask        Web framework / REST API
  SQLite       Database
  HTML         Frontend structure
  CSS          Frontend styling
  JavaScript   Frontend interactions
  Gunicorn     Production WSGI server

------------------------------------------------------------------------

## 📁 Project Structure

``` text
URL-Shortener/
└── url-shortener/
    ├── app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    ├── shortener.db
    ├── static/
    │   ├── app.js
    │   └── style.css
    └── templates/
        └── index.html
```

> `shortener.db` is created automatically when the application
> initializes the database.

------------------------------------------------------------------------

## ⚙️ How It Works

1.  The user enters a long URL.
2.  The Flask backend validates and normalizes the URL.
3.  A unique short code is generated.
4.  The URL mapping is stored in SQLite.
5.  The application returns a shortened URL.
6.  When the shortened URL is opened, the backend looks up the original
    URL and redirects the user.
7.  Each successful redirect increments the click counter.

------------------------------------------------------------------------

## 🔌 API Endpoints

### 1. Shorten a URL

**POST**

``` text
/api/shorten
```

### Request

``` json
{
  "url": "https://example.com/a/very/long/url"
}
```

### Custom short code

``` json
{
  "url": "https://example.com",
  "custom_code": "my-link"
}
```

### Response

``` json
{
  "short_code": "abc123",
  "short_url": "https://your-domain.com/abc123",
  "original_url": "https://example.com"
}
```

------------------------------------------------------------------------

### 2. Get all shortened URLs

**GET**

``` text
/api/urls
```

Returns the shortened URLs with their original URLs, creation time, and
click count.

------------------------------------------------------------------------

### 3. Delete a shortened URL

**DELETE**

``` text
/api/urls/<short_code>
```

Example:

``` text
/api/urls/abc123
```

------------------------------------------------------------------------

### 4. Redirect

**GET**

``` text
/<short_code>
```

Example:

``` text
/abc123
```

The user is redirected to the original URL and the click count is
increased.

------------------------------------------------------------------------

## 💻 Run Locally

### 1. Clone the repository

``` bash
git clone https://github.com/debanwesha007-crypto/URL-Shortener.git
```

### 2. Navigate to the project

``` bash
cd URL-Shortener/url-shortener
```

### 3. Create a virtual environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

``` bash
pip install -r requirements.txt
```

### 5. Run the application

``` bash
python app.py
```

The application will be available at:

``` text
http://127.0.0.1:5000
```

------------------------------------------------------------------------

## 📦 Dependencies

The project uses:

``` text
Flask==3.0.3
gunicorn
```

------------------------------------------------------------------------

## 🌍 Deployment

The application can be deployed as a Python Web Service on platforms
such as **Render**.

For Render, use:

``` text
Root Directory:
url-shortener

Build Command:
pip install -r requirements.txt

Start Command:
gunicorn app:app
```

The Flask application object is defined as:

``` python
app = Flask(__name__)
```

so `gunicorn app:app` starts the application correctly.

### ⚠️ Database Note

This project currently uses SQLite. SQLite is suitable for local
development, demonstrations, and portfolio projects, but a production
URL-shortening service should use a persistent database such as
PostgreSQL.

------------------------------------------------------------------------

## 📸 Application

The application provides a simple interface where users can:

-   Enter a URL
-   Generate a short link
-   Create a custom code
-   View shortened URLs
-   Track clicks
-   Delete URL mappings

------------------------------------------------------------------------

## 🎯 Future Improvements

-   🔐 User authentication
-   📊 Advanced analytics and click statistics
-   🌍 PostgreSQL integration
-   🔒 Rate limiting and abuse protection
-   📱 Improved mobile UI
-   🔗 QR code generation
-   ⏳ Link expiration
-   👤 User-specific URL management
-   🛡️ Enhanced URL security and validation

------------------------------------------------------------------------

## 👩‍💻 Author

**Anwesha Deb**

GitHub:\
https://github.com/debanwesha007-crypto

------------------------------------------------------------------------

## 📄 License

This project is available for educational and portfolio purposes.
