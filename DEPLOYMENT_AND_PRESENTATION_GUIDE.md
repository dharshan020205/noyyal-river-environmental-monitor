# Task 3 – Deployment and presentation guide

## Run locally (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Deploy with Streamlit Community Cloud
1. Create/sign in to GitHub and create a repository such as `noyyal-river-pollution-monitor`.
2. Upload the **contents** of this project folder to the repository root (do not upload only the ZIP).
3. Confirm that `app.py`, `requirements.txt`, `noyyal_tds_observations.csv`, and `noyyal_2014_15_multiparameter.csv` are at the repository root.
4. Visit https://share.streamlit.io/ and sign in with GitHub.
5. Select **Create app**, choose the repository and branch (`main`), set the app file path to `app.py`, and click **Deploy**.
6. Open the generated `https://....streamlit.app` URL on both a phone and laptop.
7. After code changes, commit and push to GitHub; Community Cloud redeploys from the repository.

Official instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

Do not commit passwords, API keys or private credentials. This project currently requires no secrets. The CSV files must be in GitHub because the cloud app cannot access files stored only on your PC.

## Presentation plan (5–7 minutes)

### Opening (30 sec)
“Our project is a Python-based environmental monitoring and pollution-abatement decision-support prototype focused on reported water-quality observations from the Noyyal River in Tiruppur.”

### Problem (45 sec)
“Textile wet-processing and urban wastewater can affect river water quality. TDS, TSS, BOD and COD describe different aspects of water quality. Our goal is to organize published observations, compare locations and connect findings to practical abatement actions.”

### Dataset (60 sec)
“We use a small dataset from published sources. The 2014–15 report contains upstream and downstream sample values for multiple parameters. A 2024 report citing TNPCB field measurements gives TDS values at Somanur and Athupalayam. Each observation retains its date and source.”

### Live demonstration (2 min)
1. Overview: explain the three KPI cards and compact TDS chart.
2. Data explorer: demonstrate location/date filters and CSV download.
3. Comparative analysis: explain the two 2014–15 samples and relative increases in TSS, BOD and COD.
4. Abatement plan: connect recommendations to the parameters.
5. Methodology & sources: explain preprocessing, source traceability and limitations.

### Technical explanation (60 sec)
“Python and Pandas load and clean the CSV data. Matplotlib generates the charts. Streamlit provides the interactive web interface. Transparent screening rules compare reported values and flag relative increases. This is a data-analysis and rule-based decision-support prototype, not a trained predictive ML model.”

### Conclusion (30 sec)
“The prototype demonstrates how environmental data can be converted into accessible visual evidence and practical recommendations. A larger, consistently sampled dataset would be needed to train and validate a predictive model.”

## Likely viva questions

**Why TDS?** TDS indicates the total concentration of dissolved substances and is relevant to saline wastewater and textile dyeing. It must be interpreted with other indicators.

**TDS vs TSS?** TDS represents dissolved substances; TSS represents suspended particles.

**What do BOD and COD indicate?** BOD estimates oxygen demand associated with biodegradable organic matter. COD estimates oxygen equivalent for chemically oxidizable substances.

**Why no ML model?** The available dataset has very few observations from different dates and locations. Training a model would risk overfitting and misleading performance claims. The assignment permits data analysis OR machine learning.

**What is ZLD?** Zero Liquid Discharge aims to recover/reuse wastewater and manage remaining concentrate and solids so routine liquid effluent is not discharged.

**Can this certify drinking-water safety?** No. It is an academic screening tool. Safety requires current, comprehensive laboratory testing against applicable standards.

**How could it become real-time?** Connect calibrated sensors or an approved data feed, store timestamped readings, validate them and define scientifically justified alert thresholds.

## Final demonstration checklist
- [ ] Run the app locally before presenting.
- [ ] Test all five sidebar pages.
- [ ] Test both filters and CSV download.
- [ ] Test the deployed URL on a phone and laptop.
- [ ] Keep screenshots and a local copy in case Wi-Fi fails.
- [ ] Explain clearly why this version does not claim ML prediction.
