# Reel Critic

## Description

Reel Critic is a web application that allows users to view and ranked movies and TV shows. It provides a platform to browse through top-ranked content, view detailed information, trailers, sign up/log in and to manage content. and add or update movies and TV shows. The application uses Flask for the backend, SQLite for the database.

### Features

- View top-ranked movies and TV shows
- Detailed information for each movie and TV show
- Trailers and ratings for each movie and TV show
- Subscribe to Weekly newsletter
- Sign up for an account or Log in (authenticated users only)
- Add, update, and delete movies and TV shows (authenticated users only)
- Responsive design compatible with various screen sizes
- Pre-populated with example movies, TV shows, and a test user for demonstration purposes

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/your-repository.git

   ```

2. **Navigate to the Project Directory**

   ````bash
   cd your-repository

   ```

   ````

3. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

   ```

4. **Install the Project Dependencies**

   ```bash
   pip install -r requirements.txt

   ```

5. **Set Up the Database**

   ```bash
   flask db upgrade

   ```

6. **Run the Application**

   ```bash
   flask run

   ```

## Usage

After running the application, open your web browser and go to http://127.0.0.1:5000 to access the web app.

### Acknowledgements

- Flask: Web framework used for the backend.
- SQLite: Database used for storing data.
- Bootstrap: Frontend framework used for styling.
- JavaScript: Library used for dynamic content.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- Alembic: Database migration tool for SQLAlchemy.
