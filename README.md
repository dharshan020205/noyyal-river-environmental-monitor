# Noyyal River Environmental Monitor — final presentation pack

## What is included
- `app.py`: replacement Streamlit application with responsive layout, interactive Plotly charts, data filters, CSV downloads, methodology, source links and abatement recommendations.
- `requirements.txt`: runtime dependencies.
- `DEPLOYMENT.md`: local run and Streamlit Community Cloud deployment steps.
- `PRESENTATION_SCRIPT.md`: concise demonstration script.
- `VIVA_QA.md`: likely viva questions and defensible answers.
- `PROJECT_SCOPE.md`: what the prototype does and does not claim.

## Important: preserve your existing data
Keep these two CSV files in the same folder as `app.py`:
- `noyyal_tds_observations.csv`
- `noyyal_2014_15_multiparameter.csv`

Do not rename their columns. The application expects the schema shown in the original project. Keep your existing `Task3_Technical_Report.docx` too.

## Replace the app
1. Extract this ZIP.
2. Copy the new `app.py` and `requirements.txt` into your existing `Task3_Noyyal_Wastewater_Project` folder.
3. Allow Windows to replace the old files.
4. Keep both CSVs in that same folder.
5. In VS Code, open the integrated terminal at the project folder.

## Run locally
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8503
```
Open `http://localhost:8503`.

If port 8503 is already in use, stop the old server with `Ctrl+C`, or use `--server.port 8504`.

## Before submission
- Run through all five pages.
- Confirm the two CSVs load.
- Test all three filters and both CSV downloads.
- Check the charts on a narrow browser window and a phone.
- Confirm all source links open.
- Commit the final files and datasets to a GitHub repository before cloud deployment.
- Do not describe this as a trained AI prediction model. It is a descriptive, rule-based decision-support prototype.
