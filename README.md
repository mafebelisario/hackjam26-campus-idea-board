# Campus Idea Board — Student Starter

This is a **working starter**, not a blank skeleton. Follow `WORKSHOP_TASKS.md` to build understanding and make changes during the live workshop. The instructor's complete reference is in the sibling `solution/` folder of the distributed ZIP.

## Quick start
1. Install Python 3.10+ and open a terminal in this folder.
2. Create a virtual environment: `python -m venv .venv` (Windows: `py -m venv .venv` also works).
3. Activate: Windows PowerShell `.\.venv\Scripts\Activate.ps1`; macOS/Linux `source .venv/bin/activate`.
4. Install: `python -m pip install -r requirements.txt`.
5. Run: `python app.py`.
6. Open `http://127.0.0.1:5000` in your browser.

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe app.py` without activating.

The database `ideas.db` is created automatically. No account, API key, or cloud database is required.

## API
- `GET /api/ideas` — returns all ideas as JSON
- `POST /api/ideas` — accepts `{ "title": "...", "description": "...", "category": "Home Turf" }`
- `POST /api/ideas/<id>/upvote` — optional stretch feature

For local demonstration only: no user accounts, authentication, or voting limits. Do not deploy publicly without hardening.
