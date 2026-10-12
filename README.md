# Loop Social — Mini Social Media App

A mini social networking application built with Django, HTML, CSS, JavaScript, and SQLite.

## Features
- Register, log in, and log out
- User profiles with editable bio and optional avatar URL
- Create text posts with optional image URLs
- Chronological feed and search posts by text or username
- Like and unlike posts (one like per user per post)
- Add comments to posts
- Follow and unfollow members
- Discover and search people by username or bio
- Delete your own posts
- Django admin interface
- Responsive desktop and mobile layout

## Tech stack
- Frontend: HTML, CSS, JavaScript (Django templates)
- Backend: Python + Django
- Database: SQLite

## Setup on Windows / VS Code
Open the extracted folder (the folder containing `manage.py`) in VS Code and open Terminal.

1. Create and activate a virtual environment:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.

2. Install Django:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Create the database tables:
```powershell
python manage.py makemigrations social
python manage.py migrate
```

4. Optional: create an admin account:
```powershell
python manage.py createsuperuser
```

5. Start the server:
```powershell
python manage.py runserver
```
Open http://127.0.0.1:8000/ in your browser.

Routes: Feed `/`, Discover `/people/`, Admin `/admin/`.

## Test the features
1. Register a user and create a post.
2. Register another user in a separate browser/private window.
3. Follow the first user, like posts, and add comments.
4. Open your profile and edit your bio or avatar image URL.

## Notes
This is a learning/demo project. `DEBUG=True` and the development secret key are not suitable for production. Images use external URLs rather than file uploads. Django stores passwords as secure hashes. Likes and follow relationships have database uniqueness constraints.
