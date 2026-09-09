# Flask engineering portfolio

A responsive, server-rendered portfolio with editable content. No database or credentials needed for this milestone.

## Run locally

Requires Python 3.9 or later.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.lock.txt
flask --app app run --port 5050
```

Open http://127.0.0.1:5050. For production serving later: `gunicorn --bind 0.0.0.0:8080 app:app`.

## Customize

- `content.json`: display name, biography, GitHub URL, skills, projects. The initial name is a placeholder inferred from the supplied GitHub handle; replace it with your preferred name. Skills describe the project stack, not verified proficiency.
- `templates/index.html`: page structure and hero headline.
- `static/style.css`: colors, typography, responsive layout.

Only the working lab is presented as existing. GitOps delivery is explicitly in progress. No invented delivery metrics, job history, or contact details are included.

`GET /healthz` returns a JSON health response. `GET /` renders the portfolio.

Next milestone: GitHub Actions and an independently managed GitOps repository. Repository publishing and cluster deployment are not performed here. Revisit whether PostgreSQL serves a real portfolio feature before adding it.


## Run tests

From the repository root, with the virtual environment activated:

```sh
python -m unittest discover -s tests -v
```

The tests use Python's standard library and Flask's test client; no extra test dependencies are needed. They cover page rendering, project links, HTML escaping, CSS delivery, health checks, missing routes, and rejected writes. `/healthz` is a process liveness check; it does not validate the content file. Use `/` for an eventual readiness probe if rendering availability is required.

## Build and run the container

Start Docker (or substitute `podman` for `docker`), then run from the repository root:

```sh
docker build -t portfolio:local .
docker run --rm --name portfolio -p 127.0.0.1:8080:8080 portfolio:local
```

Visit http://127.0.0.1:8080. In another terminal:

```sh
curl --fail http://127.0.0.1:8080/healthz
curl --fail --output /dev/null http://127.0.0.1:8080/
```

Stop the container with Ctrl+C. To check operation with an arbitrary UID and read-only root filesystem:

```sh
docker run --rm --name portfolio -p 127.0.0.1:8080:8080 \
  --user 1001230000:0 --read-only \
  --tmpfs /tmp:rw,nosuid,nodev,size=64m \
  --cap-drop ALL --security-opt no-new-privileges portfolio:local
```

Repeat both curl checks. The image defaults to non-root UID 1001 and permits OpenShift to assign a different UID. Application files are readable without granting runtime write access; Gunicorn uses `/tmp` for worker temporary files and sends logs to stdout/stderr. Port 8080 requires no privileged binding. See [Red Hat's image guidelines](https://docs.redhat.com/en/documentation/openshift_container_platform/4.19/html/images/creating-images).

The image uses Python 3.12 and the existing fully pinned dependency list. The base tag can change; pin its verified digest when introducing release automation. Tests currently run outside the final image, keeping test files out of production packaging. Building on an ARM Mac produces an ARM image by default; select the cluster's verified architecture when building release images.
