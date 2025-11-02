import streamlit as st

# Inject custom CSS with full animations & polish
st.markdown("""
<style>
/* ===================== GLOBAL ===================== */
html, body, [class*="css"] {
    font-family: 'Inter', 'Poppins', sans-serif;
    background-color: #0f1117 !important;
    color: #e5e7eb !important;
    scroll-behavior: smooth;
    transition: background 0.4s ease, color 0.4s ease;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    border-radius: 8px;
}
::-webkit-scrollbar-track { background: #1a1c24; }

/* ===================== SIDEBAR ===================== */
section[data-testid="stSidebar"] {
    background: rgba(20, 22, 30, 0.9);
    backdrop-filter: blur(14px);
    border-right: 1px solid rgba(255,255,255,0.05);
    transition: all 0.3s ease-in-out;
}

section[data-testid="stSidebar"]:hover {
    background: rgba(26, 28, 36, 0.95);
    box-shadow: 4px 0 25px rgba(99,102,241,0.15);
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ===================== HEADER ===================== */
header[data-testid="stHeader"] {
    background: rgba(15, 17, 23, 0.85);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    box-shadow: 0 2px 15px rgba(0,0,0,0.3);
}

/* ===================== MAIN CONTENT ===================== */
main {
    background: radial-gradient(circle at top left, #181b22, #0f1117) !important;
    animation: fadeIn 0.7s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ===================== CARDS / CONTAINERS ===================== */
.stMarkdown, .stPlotlyChart, .stDataFrame, div[data-testid="stMetricValue"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem 1.3rem;
    box-shadow: 0 4px 25px rgba(0,0,0,0.2);
    transition: all 0.25s ease;
}

.stMarkdown:hover, .stPlotlyChart:hover, .stDataFrame:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(99,102,241,0.2);
}

/* Metric pulse animation */
div[data-testid="stMetricValue"] {
    position: relative;
    animation: pulseMetric 3s infinite;
}
@keyframes pulseMetric {
    0% { box-shadow: 0 0 0 rgba(99,102,241,0.0); }
    50% { box-shadow: 0 0 25px rgba(99,102,241,0.3); }
    100% { box-shadow: 0 0 0 rgba(99,102,241,0.0); }
}

/* ===================== BUTTONS ===================== */
div.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: #fff !important;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.3rem;
    transition: all 0.25s ease;
    font-weight: 500;
    box-shadow: 0 0 15px rgba(99,102,241,0.2);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #818cf8, #c084fc);
    box-shadow: 0 0 25px rgba(139, 92, 246, 0.5);
    transform: translateY(-2px);
}
div.stButton > button:active {
    transform: scale(0.98);
}

/* ===================== TABS ===================== */
div[data-baseweb="tab-list"] {
    gap: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
button[data-baseweb="tab"] {
    color: #9ca3af !important;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.5rem 1.1rem;
    transition: all 0.2s ease;
    font-weight: 500;
}
button[data-baseweb="tab"]:hover {
    background: rgba(255,255,255,0.1);
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: white !important;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    box-shadow: 0 0 18px rgba(99,102,241,0.3);
}

/* ===================== CHARTS ===================== */
div[data-testid="stPlotlyChart"] {
    border-radius: 16px;
    padding: 1rem;
}

/* ===================== ANIMATED GLOW HEADINGS ===================== */
h1, h2, h3 {
    background: linear-gradient(90deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientFlow 6s infinite linear;
    background-size: 200% 200%;
}
@keyframes gradientFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ===================== TOOLTIP / HOVER EFFECTS ===================== */
[data-testid="stSidebar"] .stMarkdown:hover {
    filter: brightness(1.1);
}

/* ===================== FOOTER ===================== */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)









import sys, os
# Add the directory containing 'modules' to the Python path
sys.path.append(os.path.abspath(os.path.dirname("module")))



import streamlit as st
from modules.data_loader import load_data, match_dataframes
from modules.charts import (
    show_treemap, show_line_chart, show_bar_chart,
    show_pie_chart, show_map, show_divergence, show_scatter
)

# Sidebar menu
with st.sidebar:
    selected = st.radio(
        "📊 Choose a visualization",
        ["Treemap", "Line Chart", "Bar Plot", "Pie Chart", "Map", "Divergence", "Scatterplot"]
    )


# Load data once
sader1402, sader1403 = load_data("/home/parsahg/Desktop/saderat1.xlsx")
matched_data = match_dataframes(sader1402, sader1403)

# Route to the right visualization
if selected == "Treemap":
    show_treemap(sader1402, sader1403, matched_data)
elif selected == "Line Chart":
    show_line_chart(sader1402, sader1403, matched_data)
elif selected == "Bar Plot":
    show_bar_chart(sader1402, sader1403, matched_data)
elif selected == "Pie Chart":
    show_pie_chart(sader1402, sader1403, matched_data)
elif selected == "Map":
    show_map(sader1402, sader1403, matched_data)
elif selected == "Divergence":
    show_divergence(sader1402, sader1403, matched_data)
elif selected == "Scatterplot":
    show_scatter(sader1402, sader1403, matched_data)
