# Deployment checklist

## A. Local final test
From the project folder:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8503
```
Open `http://localhost:8503`. Confirm all five navigation pages work and there are no red error messages.

## B. GitHub
1. Create a GitHub repository, for example `noyyal-river-environmental-monitor`.
2. Put `app.py`, both CSV datasets, `requirements.txt`, `README.md`, and your report in the repository.
3. Do not upload `.venv/`, `__pycache__/`, or private credentials.
4. In the VS Code terminal:
```powershell
git init
git add app.py requirements.txt README.md noyyal_tds_observations.csv noyyal_2014_15_multiparameter.csv
git commit -m "Prepare Noyyal River monitoring prototype"
git branch -M main
git remote add origin https://github.com/dharshan020205/https://github.com/dharshan020205/noyyal-river-environmental-monitor.git
git push -u origin main
```
If the repository already exists locally, do not run `git init` or add a second `origin`; inspect with `git remote -v` and `git status` first.

## C. Streamlit Community Cloud
1. Sign in at https://share.streamlit.io/ using the GitHub account that owns the repository.
2. Select **Create app**.
3. Choose the repository, branch `main`, and main file path `app.py`.
4. Deploy.
5. Wait for build completion. If deployment fails, inspect the app logs; most common causes are missing CSV files, incorrect file names, or dependency errors.
6. Open the public URL on a phone and another device.

## D. Final deployment sanity check
- Verify the app loads without your laptop running.
- Verify both datasets are committed and available to the deployed app.
- Verify CSV download buttons work.
- Verify source links work.
- Keep a local copy and a screenshot/video of the working deployed app.

## Privacy and repository hygiene
The two project datasets appear to be research/project data. Confirm they are intended for public release before pushing them. Never commit passwords, API keys, tokens, or personal data.
