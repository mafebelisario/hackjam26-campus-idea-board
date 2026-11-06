# Student challenges — work in this order

The app already runs so nobody gets blocked by setup. **You will build and improve it during the session.**

1. **Frontend (20–38 min):** Open `templates/index.html`. Change the heading and the example placeholder. In `static/style.css`, adjust the gold accent or panel background. Refresh to see the change.
2. **Flask API (38–55 min):** Open `app.py`. Identify `GET /api/ideas` and `POST /api/ideas`. Change the success message in `static/app.js`. Test a POST using the browser form.
3. **SQLite (55–68 min):** Locate the `CREATE TABLE` and `INSERT INTO` statements. Submit an idea, refresh, and confirm it remains. Explain why the `?` placeholders protect SQL queries.
4. **Connect (68–80 min):** Open browser DevTools → Network, submit an idea, and inspect the POST request and JSON response.
5. **Stretch (80–90 min):** Change a category label consistently in both HTML and Python; or customize the CSS. Advanced: add an optional author field to the database and form.

**For instructors who want live implementation rather than guided edits:** start from the `solution` directory, remove the `add_idea` route body and re-create its validation/INSERT together, using the full solution as a reliable fallback. Do not remove the route in the shared student starter before the event.
