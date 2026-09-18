import streamlit as st
import pandas as pd


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="MPLADS AI Dashboard",
    page_icon="🏛️",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("🏛️ MPLADS AI")

st.subheader(
    "Smart Anomaly & Efficiency Detection System"
)

st.write(
    "AI-assisted system for detecting potential anomalies, "
    "high-risk patterns and inefficiencies in MPLADS works."
)


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/mplads_ml_results.csv"
)


# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filters")

states = sorted(
    df["State"].dropna().unique()
)

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All States"] + states
)

risk_options = [
    "All Risk Levels",
    "Low",
    "Medium",
    "High"
]

selected_risk = st.sidebar.selectbox(
    "Select Risk Level",
    risk_options
)

ml_options = [
    "All",
    "Potential Anomaly",
    "Normal"
]

selected_ml = st.sidebar.selectbox(
    "ML Anomaly",
    ml_options
)


# ==========================================
# APPLY FILTERS
# ==========================================

filtered_df = df.copy()

if selected_state != "All States":
    filtered_df = filtered_df[
        filtered_df["State"] == selected_state
    ]

if selected_risk != "All Risk Levels":
    filtered_df = filtered_df[
        filtered_df["Risk Level"] == selected_risk
    ]

if selected_ml != "All":
    filtered_df = filtered_df[
        filtered_df["ML Anomaly"] == selected_ml
    ]


st.sidebar.write(
    f"Showing {len(filtered_df):,} projects"
)
# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

st.header("📌 Executive Summary")

st.write(
    "Quick overview of MPLADS project implementation "
    "and detected risk patterns."
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.info(
        f"📁 **{len(filtered_df):,} projects** "
        f"are currently being analyzed."
    )

    st.info(
        f"💰 Total completed works value is "
        f"**₹{filtered_df['Final Amount (₹)'].sum():,.0f}**."
    )


with summary_col2:

    st.warning(
        f"🔴 **{(filtered_df['Risk Level'] == 'High').sum():,}** "
        f"projects are classified as high risk."
    )

    st.warning(
        f"🤖 **{(filtered_df['ML Anomaly'] == 'Potential Anomaly').sum():,}** "
        f"projects are identified as potential anomalies by ML."
    )

# ==========================================
# KEY METRICS
# ==========================================

total_projects = len(filtered_df)

total_amount = filtered_df[
    "Final Amount (₹)"
].sum()

high_risk = (
    filtered_df["Risk Level"] == "High"
).sum()

medium_risk = (
    filtered_df["Risk Level"] == "Medium"
).sum()

ml_anomalies = (
    filtered_df["ML Anomaly"] == "Potential Anomaly"
).sum()


col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📁 Total Projects",
    f"{total_projects:,}"
)

col2.metric(
    "💰 Total Amount",
    f"₹{total_amount:,.0f}"
)

col3.metric(
    "🔴 High Risk",
    f"{high_risk:,}"
)

col4.metric(
    "🟡 Medium Risk",
    f"{medium_risk:,}"
)

col5.metric(
    "🤖 ML Anomalies",
    f"{ml_anomalies:,}"
)


st.divider()


# ==========================================
# STATE-WISE ANALYSIS
# ==========================================

st.header("🗺️ State-wise Analysis")

state_analysis = (
    filtered_df
    .groupby("State")
    .agg(
        Projects=("Work ID", "count"),

        Total_Amount=(
            "Final Amount (₹)",
            "sum"
        ),

        High_Risk=(
            "Risk Level",
            lambda x: (x == "High").sum()
        ),

        Potential_Anomalies=(
            "ML Anomaly",
            lambda x: (
                x == "Potential Anomaly"
            ).sum()
        )
    )
    .reset_index()
)

state_analysis = state_analysis.sort_values(
    "Projects",
    ascending=False
)

st.dataframe(
    state_analysis,
    width="stretch"
)


# ==========================================
# STATE-WISE PROJECT CHART
# ==========================================

st.subheader("📊 Projects by State")

state_chart = state_analysis.head(15)

st.bar_chart(
    state_chart,
    x="State",
    y="Projects"
)


# ==========================================
# PROJECT FLAG EXPLANATION
# ==========================================

st.header("🔍 Why is this project flagged?")

st.write(
    "Select a project to understand why the system "
    "has marked it as a potential anomaly or high-risk project."
)


project_ids = filtered_df[
    "Work ID"
].astype(str).tolist()


if len(project_ids) > 0:

    selected_project = st.selectbox(
        "Select Work ID",
        project_ids
    )

    project = filtered_df[
        filtered_df["Work ID"].astype(str)
        == selected_project
    ].iloc[0]


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Risk Score",
        project["Risk Score"]
    )


    col2.metric(
        "Risk Level",
        project["Risk Level"]
    )


    col3.metric(
        "ML Status",
        project["ML Anomaly"]
    )


    st.write("### 📌 Detection Reason")


    st.info(
        project["Risk Reason"]
    )


    st.write("### 📋 Project Details")


    st.write(
        f"**MP Name:** {project['MP Name']}"
    )


    st.write(
        f"**State:** {project['State']}"
    )


    st.write(
        f"**Final Amount:** "
        f"₹{project['Final Amount (₹)']:,.0f}"
    )


else:

    st.info(
        "No projects available for the selected filters."
    )


# ==========================================
# RISK DISTRIBUTION
# ==========================================

st.header("📊 Risk Distribution")

risk_counts = (
    filtered_df["Risk Level"]
    .value_counts()
)

st.bar_chart(
    risk_counts
)


# ==========================================
# ML ANOMALY DISTRIBUTION
# ==========================================

st.header("🤖 ML Anomaly Detection")

ml_counts = (
    filtered_df["ML Anomaly"]
    .value_counts()
)

st.bar_chart(
    ml_counts
)


# ==========================================
# POTENTIAL ANOMALIES
# ==========================================

st.header("🚨 Potential Anomalies")

anomaly_df = filtered_df[
    filtered_df["ML Anomaly"]
    == "Potential Anomaly"
]


if len(anomaly_df) > 0:

    st.dataframe(
        anomaly_df[
            [
                "Work ID",
                "MP Name",
                "State",
                "Final Amount (₹)",
                "Risk Score",
                "Risk Level",
                "Risk Reason",
                "ML Anomaly"
            ]
        ],
        width="stretch"
    )

else:

    st.info(
        "No potential anomalies found "
        "for the selected filters."
    )


# ==========================================
# HIGH RISK PROJECTS
# ==========================================

st.header("🔴 High Risk Projects")

high_risk_df = filtered_df[
    filtered_df["Risk Level"] == "High"
]


if len(high_risk_df) > 0:

    st.dataframe(
        high_risk_df[
            [
                "Work ID",
                "MP Name",
                "State",
                "Final Amount (₹)",
                "Risk Score",
                "Risk Level",
                "Risk Reason"
            ]
        ],
        width="stretch"
    )

else:

    st.info(
        "No high-risk projects found "
        "for the selected filters."
    )


# ==========================================
# ALL PROJECTS
# ==========================================

st.header("🔎 All Projects")

st.dataframe(
    filtered_df[
        [
            "Work ID",
            "MP Name",
            "State",
            "Final Amount (₹)",
            "Risk Score",
            "Risk Level",
            "Risk Reason",
            "ML Anomaly"
        ]
    ],
    width="stretch"
)


# ==========================================
# DOWNLOAD REPORT
# ==========================================

st.header("📥 Download Report")

download_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Filtered Report",
    data=download_data,
    file_name="MPLADS_AI_Filtered_Report.csv",
    mime="text/csv",
    width="stretch"
)
# ==========================================
# DATA & MODEL LIMITATIONS
# ==========================================

st.header("⚠️ Data & Model Limitations")

st.write(
    "The following points should be considered while interpreting "
    "the detected risk patterns:"
)

st.markdown("""
- ⚠️ **Potential anomaly does not mean confirmed fraud.**
  Every flagged case requires human verification.

- 🔗 **Payment data limitation:** Payment information is available
  at MP/Constituency/State level in the available expenditure data,
  so it is not directly linked to every individual Work ID.

- 🤖 **ML model:** The Isolation Forest model is a prototype
  anomaly-detection approach and is not an official government
  fraud-detection model.

- 📊 **Risk score:** The current risk score is a prototype
  prioritization mechanism, not an official MPLADS risk rating.

- 🧑‍💼 **Human-in-the-loop:** Final decisions should be made by
  authorized officials after checking supporting records.
""")

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "⚠️ This system identifies potential anomalies "
    "and risk patterns for human verification. "
    "An anomaly does not automatically indicate fraud."
)