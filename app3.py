import streamlit as st
from neo4j import GraphDatabase
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Neo4j LOCAL Connection
uri = "bolt://localhost:7687"
username = "neo4j"
password = "Pooja@2005"  # Replace with your password

driver = GraphDatabase.driver(uri, auth=(username, password))

# --- Data Fetching Functions ---

def get_all_sessions():
    query = """
    MATCH (e:Employee)-[r:USED]->(d:Device)
    RETURN e.name AS EmployeeName, r.login_time AS LoginTime,
           r.logout_time AS LogoutTime, r.final_total_risk AS Risk
    ORDER BY Risk DESC
    """
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

def get_top_risky_employees():
    query = """
    MATCH (e:Employee)-[r:USED]->(:Device)
    RETURN e.name AS Employee, max(r.final_total_risk) AS MaxRisk
    ORDER BY MaxRisk DESC
    LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return pd.DataFrame([record.data() for record in result])

# --- UI Helper: Colored Card ---
def colored_card(title, value, subtitle, color):
    st.markdown(
        f"""
        <div style="background-color:{color}; padding:1.5rem; border-radius:10px; 
             box-shadow: 0px 4px 10px rgba(0,0,0,0.25); text-align:center;">
            <h3 style="color:white;">{title}</h3>
            <h1 style="color:white;">{value}</h1>
            <p style="color:white;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- UI Helper: Gauge Chart ---
def show_risk_gauge(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Avg Risk Score (All Sessions)"},
        gauge={
            'axis': {'range': [0, 3]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [0, 1], 'color': "green"},
                {'range': [1, 2.1], 'color': "yellow"},
                {'range': [2.1, 3], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

# --- Streamlit Page Config ---
st.set_page_config(page_title="Insider Threat Dashboard", page_icon="🚨", layout="wide")
st.title("🚨 Insider Threat Detection Dashboard")

# --- Fetch Data (with Spinner) ---
with st.spinner("Loading data from Neo4j..."):
    all_sessions = get_all_sessions()

total_session_count = len(all_sessions)
avg_risk = round(sum([s['Risk'] for s in all_sessions]) / total_session_count, 2) if total_session_count > 0 else 0

# --- Color Logic for Risk ---
avg_risk_color = "#28a745"
if avg_risk >= 2.1:
    avg_risk_color = "#dc3545"
elif avg_risk >= 1.2:
    avg_risk_color = "#ffc107"

# --- KPI Cards ---
col1, col2, col3 = st.columns(3)
with col1:
    colored_card("Total Sessions", total_session_count, "All user-device session logs", "#0d6efd")
with col2:
    colored_card("Suspicious Sessions", sum(1 for s in all_sessions if s['Risk'] >= 2.1), "Flagged as risky", "#dc3545")
with col3:
    colored_card("Avg Risk Score", avg_risk, "Across all sessions", avg_risk_color)

# --- Gauge Chart ---
if total_session_count > 0:
    show_risk_gauge(avg_risk)

st.markdown("---")

# --- Top 5 Riskiest Employees ---
st.subheader("Top 5 Employees by Highest Session Risk")
risky_df = get_top_risky_employees()
if not risky_df.empty:
    fig = px.bar(risky_df, x="Employee", y="MaxRisk",
                 color="MaxRisk", color_continuous_scale="Reds",
                 title="Top 5 Employees by Max Individual Risk")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No risky employee data available.")

# --- Risk Level Breakdown ---
st.markdown("---")
st.subheader("Risk Level Breakdown (All Sessions)")

if all_sessions:
    df = pd.DataFrame(all_sessions)

    # Risk Labeling
    def tag_risk(risk):
        if risk >= 2.1:
            return "🔴 HIGH"
        elif 1.2 <= risk < 2.1:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"

    df["Risk_Level"] = df["Risk"].apply(tag_risk)

    # Risk Filter
    risk_filter = st.selectbox("Filter by Risk Level", ["All", "🔴 HIGH", "🟡 MEDIUM", "🟢 LOW"])
    if risk_filter != "All":
        df = df[df["Risk_Level"] == risk_filter]

    # Donut Chart
    risk_counts = df["Risk_Level"].value_counts().reindex(["🔴 HIGH", "🟡 MEDIUM", "🟢 LOW"], fill_value=0)
    labels = ["🔴 HIGH", "🟡 MEDIUM", "🟢 LOW"]
    sizes = [risk_counts[label] for label in labels]
    colors = ["#ff4c4c", "#ffd93b", "#28a745"]

    fig, ax = plt.subplots()
    ax.pie(
        sizes, labels=labels, colors=colors, startangle=140,
        autopct=lambda p: f'{p:.1f}%' if p > 0 else '',
        wedgeprops=dict(width=0.3, edgecolor='black')
    )
    ax.axis('equal')
    st.pyplot(fig)

    # Data Table
    st.markdown("---")
    with st.expander("📄 View All Session Details (Total 500)"):
        st.dataframe(df.head(500), use_container_width=True)
else:
    st.info("No session data available.")

# --- Clean Exit ---
if driver:
    driver.close()
