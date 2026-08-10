# Library Management System

A Django (MVT) web application for managing a library: users register, deposit funds into a virtual balance, borrow and return books, and leave reviews.

## Overview

Users create an account, deposit money into their library balance, and use that balance to borrow books. Every book belongs to one or more categories. Borrowed books appear on the user's profile with a one-click return that refunds the balance. Registered users can review books, edit their profile, change their password, and upload a profile image. Staff can manage books, categories, users, and transactions from the Django admin panel.

## Features

- User registration, login, logout, profile, edit profile, change password, and profile image upload
- Book catalogue with category filtering
- Book detail pages with reviews
- Deposit money into a user balance (each deposit is recorded as a `Transaction`)
- Borrow books (deducts balance, prevents borrowing the same book twice)
- Return books (refunds balance; users can only return their own books)
- Email notifications for registration, login, borrowing, returning, and depositing
- Django admin panel for staff

## Tech Stack

- Python 3.14, Django 6.1 (MVT pattern)
- SQLite for local development, PostgreSQL for production
- Tailwind CSS v1.9.6 via CDN plus custom component CSS
- Vanilla JavaScript (mobile navigation, image preview, dismissible alerts)
- Gunicorn + WhiteNoise for production serving
- Pillow for image fields, django-environ for environment configuration

## Project Structure

```
Library_management/
├── libraryManagementSystem/    # Project configuration (settings, urls, wsgi)
│   └── settings.py             # All settings read from environment variables
├── core/                       # Home page, base templates, static images
├── accounts/                   # User registration, login, profile, return
│   ├── models.py               # UserAccount (one-to-one with User)
│   ├── signals.py              # Auto-creates a UserAccount for every User
│   ├── forms.py                # Registration, edit profile, image forms
│   └── urls.py
├── book/                       # Books, details, reviews, borrowing
│   └── models.py               # Book, BookReview, BorrowBooK
├── category/                   # Book categories
├── transaction/                # Deposits and Transaction records
├── media/                      # User-uploaded images (gitignored)
├── requirements.txt
├── .env.example                # Template for environment variables
├── build.sh                    # Render build command
└── render.yaml                 # Render service + database + disk
```

## Installation

1. Clone the repository and enter the directory.
2. Create a virtual environment and activate it:

Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:
```bat
py -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create your environment file:
```bash
cp .env.example .env
```
Then fill in `SECRET_KEY`, `EMAIL`, and `EMAIL_PASSWORD`.

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key. Use a long random value in production. |
| `DJANGO_DEBUG` | `True` in development, `False` in production. Defaults to `True`. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames. Defaults to `localhost,127.0.0.1`. |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated HTTPS origins, e.g. `https://your-app.onrender.com`. |
| `EMAIL` / `EMAIL_PASSWORD` | Gmail address and App Password used for notifications. |
| `DATABASE_URL` | Database connection string. Leave empty for local SQLite, or use `postgres://USER:PASSWORD@HOST:5432/DBNAME`. |
| `DJANGO_MEDIA_ROOT` | Optional override for the uploads directory. |

Never commit your real `.env` file.

## Database Setup

```bash
python manage.py migrate
```

## Running Locally

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Admin User

```bash
python manage.py createsuperuser
```

A `UserAccount` is created automatically for every user (including staff). Log in at `/admin/` to add books, categories, and manage the site.

## Testing

```bash
python manage.py test
```

The suite covers registration, login-protection, profile, return ownership, borrowing (including exact-balance and double-borrow cases), reviews, deposits, and category filtering.

## Static Files

- `collectstatic` gathers static files into `staticfiles/` and WhiteNoise serves them in production.
- User-uploaded images are stored under `media/` (`MEDIA_ROOT`) and served at `/media/`.
- In development, Django serves media directly; in production, media is served from a persistent disk (see Deployment).

## Deployment (Render)

1. Create a GitHub repository and push the project. Run `git rm -r --cached db.sqlite3 accounts/media book/media` first so the local database and uploads are not committed.
2. On Render, create a new Web Service connected to the repository (or use the included `render.yaml` with a Blueprint).
3. Set the build command to `./build.sh` and the start command to:
   ```
   gunicorn libraryManagementSystem.wsgi:application
   ```
4. Configure the environment variables described above. Important production values:
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=your-app.onrender.com`
   - `CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com`
   - `DATABASE_URL` — from the Render PostgreSQL instance
   - `SECRET_KEY` — a long random value (e.g. `python -c "import secrets; print(secrets.token_urlsafe(50))"`)
   - `EMAIL`, `EMAIL_PASSWORD`
5. Provision a Render PostgreSQL database and attach `DATABASE_URL`.
6. For persistent uploads, mount a disk at `/var/data` and set `DJANGO_MEDIA_ROOT=/var/data/media` (already configured in `render.yaml`).
7. `build.sh` runs `pip install`, `collectstatic`, and `migrate` automatically on each deploy.
8. After the first deploy, create an admin user with `python manage.py createsuperuser` (via the Render shell) and add books and categories.

The existing live deployment is at https://library-management-qonj.onrender.com.

## Security Notes

- Keep `SECRET_KEY`, `EMAIL_PASSWORD`, and the database password only in environment variables, never in the repository.
- `DEBUG` must be `False` and `ALLOWED_HOSTS` must list only your real hostnames in production.
- `CSRF_TRUSTED_ORIGINS` must contain your exact HTTPS origin.
- Use a Gmail App Password, not your normal Gmail password, for `EMAIL_PASSWORD`.
- Never commit `db.sqlite3`, `media/`, `staticfiles/`, or `.env`.

## Known Limitations

- Borrow and return actions are triggered by GET links (a pre-existing design choice); they are not protected by CSRF tokens.
- The balance is a simple virtual wallet simulation, not a real payment system.
- Seed books, categories, and images are not committed; a fresh deployment starts with an empty catalogue until data is added through the admin panel.
- The development `SECRET_KEY` currently in use is shorter than recommended; generate a long random key for production.

## Future Improvements

- Convert borrow/return to POST forms with CSRF protection.
- A transaction history page for users.
- Star ratings on books (the model field was removed as unused and can be added back with a rating feature).
- Book search and pagination.
- Borrow due dates and overdue notices.
