# FilthyCashout

Mobile-first landing page and an early survey-helper API.

## What's included

- Responsive static website in `index.html` (works on GitHub Pages).
- Client-side survey hostname detection for Qualtrics, Your-Surveys, Survey Junkie, and Pollfish.
- Optional FastAPI backend with `GET /api/health` and `POST /api/detect`.
- URL validation, hostname-boundary checks, and configurable CORS.
- Basic API tests.

## Important architecture note

**GitHub Pages only serves static files.** It does not run the Python API. Deploy the API separately (for example, to a Python-capable host), then paste its HTTPS base URL into the Survey Helper's optional API field. Configure `CORS_ORIGINS` on the API host to include your actual GitHub Pages origin, such as `https://filthycashout.github.io`, and any custom domain you control.

The API only classifies hostnames. A hostname match does not prove a link is safe or that a survey is genuine. The app does not open survey links, bypass eligibility, fabricate demographics, or submit survey answers. The answer-suggestion endpoint is intentionally disabled until a truthful, user-reviewed implementation is added.

## Run the API locally

Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn api.autofill:app --reload --port 8000
```

Health check: `http://127.0.0.1:8000/api/health`

Interactive API docs: `http://127.0.0.1:8000/docs`

Example detection request:

```bash
curl -X POST http://127.0.0.1:8000/api/detect \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://example.qualtrics.com/jfe/form/abc"}'
```

## Run tests

```bash
pip install -r requirements.txt
pytest -q
```

## Deploy the website

1. Open repository **Settings → Pages**.
2. Select **Deploy from a branch**, branch `main`, folder `/ (root)`, if that is your current publishing setup.
3. Or configure Pages to deploy with GitHub Actions.
4. Merge the reviewed website changes into the publishing branch, then check the Actions tab and the live site.

This working branch does not change `main` or publish the site by itself.

## Roadmap

- [x] Mobile-first landing page and navigation.
- [x] Safe survey provider detection.
- [x] Minimal FastAPI API and test coverage.
- [ ] Deploy API to a Python-capable host and configure production CORS.
- [ ] Add answer suggestions grounded only in facts the user provides, with edit/review before use.
- [ ] Add browser/Android autofill only with explicit user action and provider terms compliance.
- [ ] Verify production GitHub Pages deployment and replace placeholder destinations with confirmed official links.
