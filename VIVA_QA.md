# Viva preparation — Noyyal River Environmental Monitor

**Q1. What problem does your project address?**  
It supports inspection of selected reported water-quality observations for the Noyyal River around Tiruppur and links the available evidence to possible pollution-abatement actions.

**Q2. What are the inputs?**  
Two CSV datasets: `noyyal_tds_observations.csv` and `noyyal_2014_15_multiparameter.csv`.

**Q3. What does the system do?**  
It validates and cleans measurement records, presents descriptive summaries, enables filtering and CSV export, compares selected samples, and displays evidence-linked abatement recommendations.

**Q4. Why Streamlit?**  
Streamlit allows a Python data application to be built and shared quickly, with built-in navigation, metrics, tables, filters and deployment support.

**Q5. Why Pandas?**  
Pandas is used to read CSV files, convert measurement values to numeric form, remove incomplete records, remove duplicate IDs when available, filter records and calculate descriptive values.

**Q6. Why Plotly?**  
Plotly provides interactive charts that resize with the page and support hover inspection. Separate parameter charts also prevent TDS from visually overwhelming smaller-magnitude measurements.

**Q7. Is this a machine-learning prediction system?**  
No. The current implementation is descriptive analytics and transparent rule-based screening. It does not train a predictive model or claim prediction accuracy. This distinction is intentional because the available dataset is too small and heterogeneous to support a defensible predictive model.

**Q8. What is TDS?**  
Total dissolved solids: a measure of the combined concentration of dissolved substances in water, commonly expressed in mg/L. TDS does not identify the individual chemicals present.

**Q9. What do BOD and COD indicate?**  
BOD is biochemical oxygen demand, associated with oxygen consumed by microorganisms while decomposing biodegradable material. COD is chemical oxygen demand, an indicator of the oxygen equivalent required to chemically oxidize substances in a sample.

**Q10. Why are the 2014–15 and 2024 observations not treated as a trend?**  
They are reported observations from different dates and locations, and the available information does not establish a controlled, consistently sampled time series.

**Q11. Does a higher downstream value prove a particular industry caused pollution?**  
No. A two-location comparison alone cannot establish causation or identify a source. Source attribution requires systematic sampling, flow information, discharge data and appropriate laboratory investigation.

**Q12. What are the main limitations?**  
Small dataset; mixed dates, locations and reporting contexts; no controlled time series; TDS cannot identify chemical composition; screening is not a compliance verdict; current laboratory data are required for decisions.

**Q13. What would you do next with more data?**  
Collect repeated, georeferenced samples across seasons and upstream/downstream sites; include flow, rainfall, discharge and laboratory metadata; then evaluate statistical methods or ML only if the dataset is sufficiently large, representative and labelled.

**Q14. How is the application deployed?**  
The code and data are stored in GitHub, and Streamlit Community Cloud deploys the `app.py` entry point using the dependencies listed in `requirements.txt`.

**Q15. What is the key contribution?**  
A transparent and accessible interface that connects reported measurements, descriptive comparisons, data provenance and practical pollution-abatement recommendations.
