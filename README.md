# MoviWeb App

MoviWeb is a Flask web application for managing users and their favorite movies.

Each user can have their own movie collection. Movies can be added by entering only the movie title. The application automatically gets additional movie information from the OMDb API.

## Features

- Create users
- Display all users
- Show movies for a specific user
- Add movies by title
- Get movie information automatically from the OMDb API
- Update movie information
- Delete movies
- Store data in a SQLite database
- Custom 404 error page

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- HTML
- CSS
- OMDb API
- Requests
- python-dotenv

## Project Structure

```text
MovieWebApp/
│
├── app.py
├── data_manager.py
├── models.py
├── requirements.txt
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── movies.html
    └── 404.html
```

## Installation

Clone the repository and open the project directory.

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## OMDb API

The application uses the OMDb API to get movie information.

Create a `.env` file in the main project directory:

```text
OMDB_API_KEY=your_api_key
```

Replace `your_api_key` with your own OMDb API key.

The `.env` file is ignored by Git and should not be uploaded to GitHub.

## Run the Application

Start the application with:

```bash
python app.py
```

Then open the following address in your browser:

```text
http://127.0.0.1:5000
```

## Usage

1. Create a user.
2. Select the user.
3. Enter a movie title.
4. Click **Create**.
5. MoviWeb gets the director, year and poster automatically from the OMDb API.
6. Movies can also be updated or deleted.

## Author

Hans-Günter Klemp