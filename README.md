# julie-dashboard

Julie's "Still Rising · Live Progress" page: https://julie-dashboard.vercel.app/

- `data.json` is the only file to edit for updates. `index.html` reads it at load.
- Run `python3 scripts/check.py` before every push (Julie-facing rules: no em dashes, no money, no private goals).
- Push to `main` = live in about a minute (Vercel). Any other branch = Vercel preview.
- The Dropbox `sites/julie-dashboard` folder is retired; this repo is the source of truth.
