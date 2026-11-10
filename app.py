from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
OBS_FILE = ROOT / "noyyal_tds_observations.csv"
MULTI_FILE = ROOT / "noyyal_2014_15_multiparameter.csv"

st.set_page_config(
    page_title="Noyyal River | Water Quality Monitor",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Responsive styling: charts use Plotly's responsive renderer; tables remain horizontally scrollable.
st.markdown("""
<style>
:root { --accent:#28b8a6; }
.block-container { max-width: 1440px; padding-top: 1.25rem; padding-bottom: 2.5rem; }
[data-testid="stMetric"] { background: rgba(40,184,166,.07); border: 1px solid rgba(40,184,166,.22); padding:  .8rem 1rem; border-radius: 14px; }
[data-testid="stMetricValue"] { font-size: clamp(1.25rem, 2.4vw, 2rem); }
section[data-testid="stSidebar"] { min-width: 245px; }
h1 { letter-spacing: -.025em; }
.small-muted { color: #9aa4b2; font-size: .88rem; }
div[data-testid="stPlotlyChart"] { width: 100%; }
@media (max-width: 760px) {
  .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: .8rem; }
  h1 { font-size: 1.65rem !important; }
  h2 { font-size: 1.3rem !important; }
  section[data-testid="stSidebar"] { min-width: 0; }
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 💧 Noyyal Monitor")
st.sidebar.caption("Water-quality evidence • Tiruppur, Tamil Nadu")
page = st.sidebar.radio(
    "Navigate",
    ["Overview", "Data explorer", "Comparative analysis", "Abatement plan", "Methodology & sources"],
)
st.sidebar.divider()
st.sidebar.caption("Academic prototype · Descriptive and rule-based analysis")

@st.cache_data
def load_data():
    if not OBS_FILE.exists():
        raise FileNotFoundError(f"Missing dataset: {OBS_FILE.name}")
    if not MULTI_FILE.exists():
        raise FileNotFoundError(f"Missing dataset: {MULTI_FILE.name}")

    obs = pd.read_csv(OBS_FILE)
    multi = pd.read_csv(MULTI_FILE)

    required = {"date_or_period", "location", "value", "unit"}
    missing = required - set(obs.columns)
    if missing:
        raise ValueError(f"{OBS_FILE.name} is missing columns: {', '.join(sorted(missing))}")

    obs["value"] = pd.to_numeric(obs["value"], errors="coerce")
    obs = obs.dropna(subset=["value", "location", "date_or_period"]).copy()
    obs = obs[obs["value"] >= 0].copy()
    if "record_id" in obs.columns:
        obs = obs.drop_duplicates(subset=["record_id"])
    for col in ["parameter", "source", "source_url", "note"]:
        if col not in obs.columns:
            obs[col] = "Not specified"
    obs["parameter"] = obs["parameter"].fillna("Not specified").astype(str)
    obs["location"] = obs["location"].fillna("Not specified").astype(str)
    obs["date_or_period"] = obs["date_or_period"].astype(str)
    return obs, multi

try:
    df, multi = load_data()
except Exception as exc:
    st.error(f"Could not load the project datasets: {exc}")
    st.info("Keep both CSV files in the same folder as app.py, then restart Streamlit.")
    st.stop()

def section_intro(title, subtitle):
    st.title(title)
    st.caption(subtitle)

def chart_config(fig, height=390):
    fig.update_layout(
        height=height,
        autosize=True,
        margin=dict(l=12, r=12, t=55, b=35),
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True, gridcolor="rgba(150,150,150,.18)")
    return fig

def safe_num(row, col):
    return pd.to_numeric(row.get(col), errors="coerce")

st.sidebar.caption(f"{len(df)} valid observation rows loaded")

if page == "Overview":
    section_intro("Noyyal River Environmental Monitor",
                  "Evidence-based water-quality exploration and pollution-abatement decision support · Tiruppur, Tamil Nadu")
    st.info(
        "This academic prototype cleans and compares a small set of published/reported observations. "
        "It provides descriptive analytics and transparent screening rules; it does not forecast water quality "
        "or establish regulatory compliance.",
        icon="ℹ️",
    )

    tds = df[df["parameter"].str.contains("TDS", case=False, na=False)].copy()
    values = tds["value"] if not tds.empty else df["value"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Valid TDS observations", f"{len(tds):,}" if not tds.empty else "0")
    c2.metric("Highest reported TDS", f"{values.max():,.0f} mg/L" if len(values) else "—")
    c3.metric("Lowest reported TDS", f"{values.min():,.0f} mg/L" if len(values) else "—")
    c4.metric("Locations represented", f"{df['location'].nunique():,}")

    st.subheader("Reported TDS observations")
    if not tds.empty:
        tds["display_label"] = tds["location"] + " · " + tds["date_or_period"]
        fig = px.bar(
            tds, x="display_label", y="value", color="location",
            text=tds["value"].map(lambda x: f"{x:,.0f}"),
            labels={"display_label": "Reported location and period", "value": "TDS (mg/L)", "location": "Location"},
            title="Reported TDS at selected Noyyal River locations",
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(showlegend=False)
        st.plotly_chart(chart_config(fig, 430), use_container_width=True)
    else:
        st.warning("No TDS rows were found in the observation dataset.")

    st.subheader("Key observations")
    st.markdown(
        "- The 2014–15 upstream and downstream values are separate reported samples, not a continuous time series.\n"
        "- The 26 February 2024 report lists TDS values of 1,610 mg/L at Somanur and 2,160 mg/L at Athupalayam.\n"
        "- The difference between those two reported 2024 values is 550 mg/L. The cited news report attributes the increase primarily to sewage discharge, quoting TNPCB officials."
    )
    st.caption("Interpretation must account for differences in sampling date, location, method and reporting context.")

elif page == "Data explorer":
    section_intro("Data explorer", "Filter, inspect and export the observations used by this prototype.")
    col1, col2, col3 = st.columns([1, 1, 1])
    locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
    periods = ["All"] + sorted(df["date_or_period"].dropna().unique().tolist())
    parameters = ["All"] + sorted(df["parameter"].dropna().unique().tolist())
    with col1:
        chosen_location = st.selectbox("Sampling location", locations)
    with col2:
        chosen_period = st.selectbox("Date / reporting period", periods)
    with col3:
        chosen_parameter = st.selectbox("Parameter", parameters)

    view = df.copy()
    if chosen_location != "All":
        view = view[view["location"] == chosen_location]
    if chosen_period != "All":
        view = view[view["date_or_period"] == chosen_period]
    if chosen_parameter != "All":
        view = view[view["parameter"] == chosen_parameter]

    st.write(f"**{len(view)}** matching record(s)")
    display_cols = [c for c in ["date_or_period", "location", "parameter", "value", "unit", "source", "note"] if c in view.columns]
    st.dataframe(view[display_cols], use_container_width=True, hide_index=True)
    st.download_button(
        "⬇ Download filtered observations (CSV)",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="noyyal_filtered_observations.csv",
        mime="text/csv",
        use_container_width=False,
    )
    with st.expander("Inspect the complete 2014–15 multi-parameter dataset"):
        st.dataframe(multi, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Download multi-parameter dataset (CSV)",
            data=multi.to_csv(index=False).encode("utf-8"),
            file_name="noyyal_2014_15_multiparameter.csv",
            mime="text/csv",
        )

elif page == "Comparative analysis":
    section_intro("Comparative analysis", "Compare the two reported 2014–15 samples without implying a long-term trend.")
    st.caption("CPCB-referenced 2014–15 observations reproduced in the cited municipal project report.")
    st.dataframe(multi, use_container_width=True, hide_index=True)

    required_cols = ["TSS_mg_L", "TDS_mg_L", "BOD_mg_L", "COD_mg_L"]
    if len(multi) >= 2 and all(c in multi.columns for c in required_cols):
        # Separate panels avoid making low-magnitude parameters unreadable beside TDS.
        labels = ["TSS", "TDS", "BOD", "COD"]
        for col, label in zip(required_cols, labels):
            up = safe_num(multi.iloc[0], col)
            down = safe_num(multi.iloc[1], col)
            if pd.isna(up) or pd.isna(down):
                st.warning(f"{label}: one or both values are missing; comparison skipped.")
                continue
            fig = go.Figure()
            fig.add_trace(go.Bar(name=str(multi.iloc[0].get("location", "Sample 1")), x=["Upstream"], y=[up], text=[f"{up:g}"], textposition="outside"))
            fig.add_trace(go.Bar(name=str(multi.iloc[1].get("location", "Sample 2")), x=["Downstream"], y=[down], text=[f"{down:g}"], textposition="outside"))
            fig.update_layout(title=f"{label} comparison (mg/L)", barmode="group", showlegend=True)
            st.plotly_chart(chart_config(fig, 300), use_container_width=True)
            if down > up:
                st.warning(f"{label} is higher in the listed downstream sample ({down:g} vs {up:g} mg/L). This comparison alone does not establish the source or cause.")
            elif down < up:
                st.success(f"{label} is lower in the listed downstream sample ({down:g} vs {up:g} mg/L).")
            else:
                st.info(f"{label} is equal in both listed samples ({down:g} mg/L).")
    else:
        st.warning("The multi-parameter dataset does not contain the expected columns or two sample rows.")

    recent = df[(df["date_or_period"] == "2024-02-26") & df["parameter"].str.contains("TDS", case=False, na=False)]
    if len(recent) >= 2:
        som = recent[recent["location"].str.contains("Somanur", case=False, na=False)]["value"]
        ath = recent[recent["location"].str.contains("Athupalayam", case=False, na=False)]["value"]
        if len(som) and len(ath):
            delta = float(ath.iloc[0] - som.iloc[0])
            st.metric("2024 TDS difference (Athupalayam − Somanur)", f"{delta:,.0f} mg/L")
    st.caption("Different parameters have different magnitudes; each parameter is therefore plotted on its own scale.")

elif page == "Abatement plan":
    section_intro("Pollution-abatement plan", "Practical actions linked to the indicators available in the project dataset.")
    actions = [
        ("Industrial effluent control", "Operate and audit industrial effluent treatment plants (IETPs) and common effluent treatment plants (CETPs); routinely verify inlet and outlet quality.", "TSS, BOD, COD, TDS"),
        ("Salt and TDS reduction", "Optimize salt dosing in textile dyeing, segregate high-TDS streams and evaluate feasible water-recovery options.", "TDS, conductivity, chloride, sulphate"),
        ("RO and ZLD performance", "Audit reverse-osmosis recovery, evaporator/crystallizer performance and safe concentrate handling; investigate bypasses or unauthorized discharge.", "TDS, conductivity, recovery rate"),
        ("Municipal sewage management", "Improve sewer connections, sewage interception and treatment capacity before untreated sewage reaches the river.", "BOD, COD, TSS and faecal indicators"),
        ("Monitoring and verification", "Use continuous pH/TDS/DO sensors for screening and confirm findings through accredited laboratory sampling.", "pH, TDS, DO, BOD, COD, TSS"),
    ]
    for title, action, indicators in actions:
        with st.container(border=True):
            st.markdown(f"### {title}")
            st.write(action)
            st.caption(f"Suggested indicators: {indicators}")
    st.warning(
        "These are evidence-informed recommendations for investigation and planning, not site-specific engineering designs "
        "or legal compliance determinations. Implementation requires current sampling, local stakeholder input and qualified review."
    )

else:
    section_intro("Methodology & sources", "Transparent description of the data pipeline, assumptions and evidence.")
    st.subheader("Processing workflow")
    st.markdown(
        "1. **Input:** published/reported observations supplied as CSV files.\n"
        "2. **Validation:** required columns checked; numeric conversion applied to measurement values.\n"
        "3. **Cleaning:** incomplete measurement rows removed, negative values excluded and duplicate record IDs removed when available.\n"
        "4. **Analysis:** descriptive summaries and comparisons between the listed samples.\n"
        "5. **Visualization:** responsive interactive charts and filterable tables.\n"
        "6. **Decision support:** transparent relative-comparison flags and evidence-linked abatement recommendations."
    )
    st.subheader("Data dictionary")
    st.markdown("| Field | Meaning |\n|---|---|\n| `date_or_period` | Sampling date or reporting period |\n| `location` | Reported sampling location |\n| `parameter` | Water-quality indicator |\n| `value` | Reported numeric measurement |\n| `unit` | Measurement unit |\n| `source` / `source_url` | Data provenance, where supplied |\n| `note` | Context or qualification attached to the record |")
    st.subheader("Sources")
    st.markdown(
        "1. **TNUIFSL / Tiruppur City Municipal Corporation**, project report, Table 9; cites CPCB Zonal Office Bengaluru Assessment Report 2014–15. [Open report](https://tnuifsl.com/Disclosures/TNUFIP-TCMC-UGSS-DIEE.pdf)\n"
        "2. **The New Indian Express**, 7 March 2024, reporting TNPCB field measurements dated 26 February 2024. [Open report](https://www.newindianexpress.com/states/tamil-nadu/2024/Mar/07/sewage-discharge-renders-noyyal-river-water-in-tiruppur-unfit-for-drinking)\n"
        "3. **Tamil Nadu Pollution Control Board**, Annual Report 2020–21. [Open annual report](https://tnpcb.gov.in/PDF/Information/annualreports/English/AnnulReport_Eng_2021.pdf)"
    )
    st.subheader("Limitations and responsible interpretation")
    st.markdown(
        "- The dataset is small and combines observations from different dates, locations and reporting contexts.\n"
        "- The 2014–15 samples are not a controlled time series; do not interpret them as a long-term trend.\n"
        "- The current implementation is descriptive and rule-based; it does not contain a trained predictive ML model or validated accuracy score.\n"
        "- TDS alone cannot identify the chemical composition or source of dissolved solids.\n"
        "- Screening flags are prompts for investigation, not regulatory compliance verdicts.\n"
        "- Current field sampling and accredited laboratory confirmation are required for operational or regulatory decisions."
    )
    st.subheader("Technical stack")
    st.write("Python · Pandas · Plotly · Streamlit")

st.divider()
st.caption("Academic prototype | Noyyal River, Tiruppur, Tamil Nadu | Descriptive analytics and decision support")
