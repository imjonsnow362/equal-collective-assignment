# XRay Project

Lightweight demo project that shows an XRay SDK integration and a small Django app.

**Quick Start**

- **Requirements:** Python 3.8+ (use `python3`), `virtualenv` (recommended).
- **Activate existing venv:**

```bash
source venv/bin/activate
```

- **Run the demo script:**

```bash
python3 demo_app.py
```

- **Run the Django development server:**

1. Activate your virtualenv (see above).
2. Install dependencies if you maintain a `requirements.txt` (not included):

```bash
pip install -r requirements.txt  # optional
```

3. Run migrations and start server:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser  # optional, for admin access
python3 manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` for the Django admin or the API endpoints under `/api/` as defined in `config/urls.py`.

**Project layout (important files)**

- `manage.py` — Django management entrypoint.
- `demo_app.py` — standalone demo showing the `XRay` SDK usage (logging pipeline steps).
- `xray_sdk.py` — local SDK module used by `demo_app.py` and possibly Django views.
- `config/` — Django project settings and URL configuration:
  - `config/settings.py` — main settings (INSTALLED_APPS, DB, etc.)
  - `config/urls.py` — root URL routes (includes `core.urls`).
- `core/` — Django app containing models, views, serializers, and URLs.
- `db.sqlite3` — local SQLite DB (generated at runtime). This file is ignored by the repository `.gitignore`.

**What I added/changed**

- A project `.gitignore` exists at the repo root to exclude `venv/`, `__pycache__/`, `db.sqlite3`, editor files, and other generated artifacts.

**Notes & recommendations**

- Keep Django migrations in source control (the default) unless you have a specific reason not to. If you'd rather ignore migrations, add the app migrations directory to `.gitignore`.
- If `db.sqlite3` or files inside `venv/` are already committed, remove them from git with:

```bash
git rm --cached db.sqlite3
git rm -r --cached venv/
git commit -m "Remove local database and virtualenv from repo"
```

- Consider adding a `requirements.txt` (or `pyproject.toml`) so contributors can install exact dependencies:

```bash
pip freeze > requirements.txt
```

- The demo script uses `python3 demo_app.py` — on some systems running `python demo_app.py` may target Python 2, so prefer `python3`.

**If you want me to**

- Commit the README for you (done). 
- Remove already-tracked files that should be ignored (`db.sqlite3`, `venv/`, `__pycache__/`) — I can prepare and run the safe `git rm --cached` commands if you allow.
- Generate a `requirements.txt` from the virtualenv and add it to the repo.

If you'd like any of those follow-ups, tell me which and I'll proceed.
