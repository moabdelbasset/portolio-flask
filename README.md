# Flask engineering portfolio

A responsive, server-rendered portfolio with editable content. No database or credentials needed for this milestone.

## Run locally

Requires Python 3.9 or later.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --port 5050
```

Open http://127.0.0.1:5050. For production serving later: `gunicorn --bind 0.0.0.0:8080 app:app`.

## Customize

- `content.json`: display name, biography, GitHub URL, skills, projects. The initial name is a placeholder inferred from the supplied GitHub handle; replace it with your preferred name. Skills describe the project stack, not verified proficiency.
- `templates/index.html`: page structure and hero headline.
- `static/style.css`: colors, typography, responsive layout.

Only the working lab is presented as existing. GitOps delivery is explicitly in progress. No invented delivery metrics, job history, or contact details are included.

`GET /healthz` returns a JSON health response. `GET /` renders the portfolio.

Next milestone: tests and container packaging, followed by GitHub Actions and an independently managed GitOps repository. Repository publishing and cluster deployment are not performed here. Revisit whether PostgreSQL serves a real portfolio feature before adding it.
