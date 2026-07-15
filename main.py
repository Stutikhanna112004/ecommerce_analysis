# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import streamlit as st
# import os

# # ---------------------------------------------------------
# # Page Config (First calling page config)
# # ---------------------------------------------------------
# st.set_page_config(
#     page_title="Ecommerce Sales Dashboard",
#     page_icon="🛒",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------------------------------------------------
# # Theme / Palette
# # ---------------------------------------------------------
# PRIMARY = "#6C5CE7"      # violet
# ACCENT = "#00CEC9"       # teal
# WARN = "#FDCB6E"         # amber
# BG_CARD = "#161A2B"
# TEXT_MUTED = "#9AA0B4"

# PALETTE = ["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#74B9FF",
#            "#55EFC4", "#E17055", "#A29BFE", "#81ECEC", "#FAB1A0"]

# sns.set_theme(style="whitegrid")
# plt.rcParams.update({
#     "figure.facecolor": "none",
#     "axes.facecolor": "none",
#     "savefig.facecolor": "none",
#     "axes.edgecolor": "#3A3F55",
#     "axes.labelcolor": "#E4E6F0",
#     "xtick.color": "#B4B8C8",
#     "ytick.color": "#B4B8C8",
#     "text.color": "#E4E6F0",
#     "axes.grid": True,
#     "grid.color": "#2A2E42",
#     "grid.alpha": 0.5,
#     "font.family": "sans-serif",
# })

# # ---------------------------------------------------------
# # Custom CSS — cards, headers, fonts, sidebar polish
# # ---------------------------------------------------------
# st.markdown(f"""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

#     html, body, [class*="css"] {{
#         font-family: 'Inter', sans-serif;
#     }}

#     /* Hide default streamlit chrome */
#     #MainMenu {{visibility: hidden;}}
#     footer {{visibility: hidden;}}

#     /* Page title */
#     .dash-title {{
#         font-family: 'Poppins', sans-serif;
#         font-size: 2.4rem;
#         font-weight: 700;
#         background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0;
#     }}
#     .dash-subtitle {{
#         color: {TEXT_MUTED};
#         font-size: 1rem;
#         margin-top: 0.2rem;
#         margin-bottom: 1.5rem;
#     }}

#     /* KPI cards */
#     .kpi-card {{
#         background: linear-gradient(145deg, #1B2036, #14172A);
#         border: 1px solid #2A2E4A;
#         border-radius: 16px;
#         padding: 1.1rem 1.3rem;
#         box-shadow: 0 4px 18px rgba(0,0,0,0.25);
#         transition: transform 0.15s ease;
#     }}
#     .kpi-card:hover {{
#         transform: translateY(-3px);
#         border-color: {PRIMARY};
#     }}
#     .kpi-label {{
#         color: {TEXT_MUTED};
#         font-size: 0.8rem;
#         font-weight: 500;
#         text-transform: uppercase;
#         letter-spacing: 0.06em;
#         margin-bottom: 0.3rem;
#     }}
#     .kpi-value {{
#         font-family: 'Poppins', sans-serif;
#         font-size: 1.7rem;
#         font-weight: 700;
#         color: #F4F5FA;
#     }}
#     .kpi-icon {{
#         font-size: 1.4rem;
#         margin-bottom: 0.4rem;
#     }}

#     /* Section headers */
#     .section-header {{
#         font-family: 'Poppins', sans-serif;
#         font-size: 1.15rem;
#         font-weight: 600;
#         color: #F4F5FA;
#         border-left: 4px solid {PRIMARY};
#         padding-left: 0.6rem;
#         margin: 1.6rem 0 0.8rem 0;
#     }}

#     /* Chart container card */
#     .chart-card {{
#         background: #12152A;
#         border: 1px solid #22263E;
#         border-radius: 14px;
#         padding: 1rem 1rem 0.4rem 1rem;
#     }}

#     /* Sidebar */
#     section[data-testid="stSidebar"] {{
#         background: #0D0F1C;
#         border-right: 1px solid #22263E;
#     }}
#     section[data-testid="stSidebar"] .stMarkdown h2 {{
#         font-family: 'Poppins', sans-serif;
#         color: {ACCENT};
#     }}

#     hr {{
#         border-color: #22263E !important;
#     }}
# </style>
# """, unsafe_allow_html=True)

# # ---------------------------------------------------------
# # Data Load + Clean (Load Dataset)
# # ---------------------------------------------------------
# DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


# @st.cache_data
# def load_data(path):
#     df = pd.read_csv(path, encoding="latin1")
#     df = df.dropna(subset=["Description"])

#     df["IsCancelled"] = df["InvoiceNo"].astype(str).str.startswith("C")

#     df_clean = df[
#         (~df["IsCancelled"]) &
#         (df["Quantity"] > 0) &
#         (df["UnitPrice"] > 0)
#     ].copy()

#     df_clean["InvoiceDate"] = pd.to_datetime(
#         df_clean["InvoiceDate"], format="%m/%d/%Y %H:%M"
#     )
#     df_clean["TotalPrice"] = np.multiply(df_clean["Quantity"], df_clean["UnitPrice"])
#     df_clean["Year"] = df_clean["InvoiceDate"].dt.year
#     df_clean["Month"] = df_clean["InvoiceDate"].dt.month
#     df_clean["Hour"] = df_clean["InvoiceDate"].dt.hour
#     df_clean["DayOfWeek"] = df_clean["InvoiceDate"].dt.day_name()
#     df_clean["YearMonth"] = df_clean["InvoiceDate"].dt.to_period("M").astype(str)

#     return df_clean


# df_clean = load_data(DATA_PATH)

# # ---------------------------------------------------------
# # Sidebar Filters
# # ---------------------------------------------------------
# st.sidebar.markdown("## 🎛️ Filters")
# st.sidebar.markdown("Refine the dashboard view below.")
# st.sidebar.markdown("---")

# countries = sorted(df_clean["Country"].unique().tolist())
# selected_countries = st.sidebar.multiselect(
#     "🌍 Country", options=countries, default=countries
# )

# min_date = df_clean["InvoiceDate"].min().date()
# max_date = df_clean["InvoiceDate"].max().date()
# date_range = st.sidebar.date_input(
#     "📅 Date Range", value=(min_date, max_date),
#     min_value=min_date, max_value=max_date
# )

# st.sidebar.markdown("---")
# st.sidebar.caption(f"Dataset spans **{min_date}** → **{max_date}**")
# st.sidebar.caption(f"{len(countries)} countries in view")

# # Filters apply karna
# mask = df_clean["Country"].isin(selected_countries)
# if len(date_range) == 2:
#     start_date, end_date = date_range
#     mask &= (df_clean["InvoiceDate"].dt.date >= start_date) & \
#             (df_clean["InvoiceDate"].dt.date <= end_date)

# filtered = df_clean[mask]

# # ---------------------------------------------------------
# # Title
# # ---------------------------------------------------------
# st.markdown('<div class="dash-title">🛒 Ecommerce Sales Dashboard</div>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="dash-subtitle">Interactive view of revenue, products, customers and trends.</div>',
#     unsafe_allow_html=True
# )

# # ---------------------------------------------------------
# # KPI Cards (top metrics row)
# # ---------------------------------------------------------
# total_revenue = filtered["TotalPrice"].sum()
# total_orders = filtered["InvoiceNo"].nunique()
# total_customers = filtered["CustomerID"].nunique()
# avg_order_value = filtered.groupby("InvoiceNo")["TotalPrice"].sum().mean()

# kpis = [
#     ("💰", "Total Revenue", f"£{total_revenue:,.0f}"),
#     ("📦", "Total Orders", f"{total_orders:,}"),
#     ("👥", "Total Customers", f"{total_customers:,}"),
#     ("🧾", "Avg Order Value", f"£{avg_order_value:,.2f}"),
# ]

# cols = st.columns(4)
# for col, (icon, label, value) in zip(cols, kpis):
#     with col:
#         st.markdown(f"""
#         <div class="kpi-card">
#             <div class="kpi-icon">{icon}</div>
#             <div class="kpi-label">{label}</div>
#             <div class="kpi-value">{value}</div>
#         </div>
#         """, unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)


# def styled_fig(figsize=(6, 4)):
#     """Create a matplotlib fig/ax pair matching the dark theme."""
#     fig, ax = plt.subplots(figsize=figsize)
#     for spine in ["top", "right"]:
#         ax.spines[spine].set_visible(False)
#     return fig, ax


# def render_chart(container, title, plot_fn):
#     with container:
#         st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
#         st.markdown('<div class="chart-card">', unsafe_allow_html=True)
#         plot_fn()
#         st.markdown('</div>', unsafe_allow_html=True)


# # ---------------------------------------------------------
# # Row 1: Monthly Trend + Top Countries
# # ---------------------------------------------------------
# row1_col1, row1_col2 = st.columns(2)


# def plot_monthly_trend():
#     monthly_sales = filtered.groupby("YearMonth")["TotalPrice"].sum()
#     fig, ax = styled_fig()
#     ax.plot(monthly_sales.index, monthly_sales.values, marker="o",
#             color=PRIMARY, linewidth=2.2, markersize=5,
#             markerfacecolor=ACCENT, markeredgecolor="none")
#     ax.fill_between(range(len(monthly_sales)), monthly_sales.values, alpha=0.08, color=PRIMARY)
#     ax.set_xlabel("Year-Month")
#     ax.set_ylabel("Revenue (£)")
#     plt.xticks(rotation=45)
#     st.pyplot(fig, transparent=True)


# def plot_top_countries():
#     country_revenue = (
#         filtered.groupby("Country")["TotalPrice"].sum()
#         .sort_values(ascending=False).head(10)
#     )
#     fig, ax = styled_fig()
#     sns.barplot(x=country_revenue.values, y=country_revenue.index,
#                 hue=country_revenue.index, palette=PALETTE, legend=False, ax=ax)
#     ax.set_xlabel("Revenue (£)")
#     ax.set_ylabel("")
#     st.pyplot(fig, transparent=True)


# render_chart(row1_col1, "📈 Monthly Revenue Trend", plot_monthly_trend)
# render_chart(row1_col2, "🌍 Top 10 Countries by Revenue", plot_top_countries)

# # ---------------------------------------------------------
# # Row 2: Top Products + Order Value Distribution
# # ---------------------------------------------------------
# row2_col1, row2_col2 = st.columns(2)


# def plot_top_products():
#     top_products = (
#         filtered.groupby("Description")["TotalPrice"].sum()
#         .sort_values(ascending=False).head(10)
#     )
#     fig, ax = styled_fig()
#     sns.barplot(x=top_products.values, y=top_products.index,
#                 hue=top_products.index, palette=PALETTE, legend=False, ax=ax)
#     ax.set_xlabel("Revenue (£)")
#     ax.set_ylabel("")
#     st.pyplot(fig, transparent=True)


# def plot_order_distribution():
#     order_values = filtered.groupby("InvoiceNo")["TotalPrice"].sum().values
#     fig, ax = styled_fig()
#     sns.histplot(order_values, bins=50, kde=True, color=ACCENT, ax=ax,
#                  edgecolor="none", alpha=0.7)
#     ax.set_xlim(0, 1000)
#     ax.set_xlabel("Order Value (£)")
#     ax.set_ylabel("Count")
#     st.pyplot(fig, transparent=True)


# render_chart(row2_col1, "🏆 Top 10 Products by Revenue", plot_top_products)
# render_chart(row2_col2, "📊 Order Value Distribution", plot_order_distribution)

# # ---------------------------------------------------------
# # Row 3: Sales by Day of Week + Hour
# # ---------------------------------------------------------
# row3_col1, row3_col2 = st.columns(2)

# day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
#              "Friday", "Saturday", "Sunday"]


# def plot_sales_by_day():
#     sales_by_day = filtered.groupby("DayOfWeek")["TotalPrice"].sum().reindex(day_order)
#     fig, ax = styled_fig()
#     sns.barplot(x=sales_by_day.index, y=sales_by_day.values,
#                 hue=sales_by_day.index, palette=PALETTE, legend=False, ax=ax)
#     plt.xticks(rotation=45)
#     ax.set_xlabel("")
#     ax.set_ylabel("Revenue (£)")
#     st.pyplot(fig, transparent=True)


# def plot_sales_by_hour():
#     sales_by_hour = filtered.groupby("Hour")["TotalPrice"].sum()
#     fig, ax = styled_fig()
#     ax.plot(sales_by_hour.index, sales_by_hour.values, marker="o",
#             color=WARN, linewidth=2.2, markersize=5,
#             markerfacecolor=PRIMARY, markeredgecolor="none")
#     ax.fill_between(sales_by_hour.index, sales_by_hour.values, alpha=0.08, color=WARN)
#     ax.set_xlabel("Hour")
#     ax.set_ylabel("Revenue (£)")
#     st.pyplot(fig, transparent=True)


# render_chart(row3_col1, "📅 Revenue by Day of Week", plot_sales_by_day)
# render_chart(row3_col2, "🕒 Revenue by Hour of Day", plot_sales_by_hour)

# # ---------------------------------------------------------
# # Row 4: Top Customers Table
# # ---------------------------------------------------------
# st.markdown('<div class="section-header">👤 Top 10 Customers by Spend</div>', unsafe_allow_html=True)
# customer_summary = filtered.groupby("CustomerID").agg(
#     TotalSpent=("TotalPrice", "sum"),
#     NumOrders=("InvoiceNo", "nunique"),
#     AvgOrderValue=("TotalPrice", "mean"),
#     LastPurchase=("InvoiceDate", "max")
# ).sort_values("TotalSpent", ascending=False).head(10)

# st.dataframe(
#     customer_summary.style
#         .format({"TotalSpent": "£{:,.2f}", "AvgOrderValue": "£{:,.2f}"})
#         .background_gradient(subset=["TotalSpent"], cmap="Purples"),
#     use_container_width=True
# )

# # ---------------------------------------------------------
# # Raw Data (optional expandable section)
# # ---------------------------------------------------------
# with st.expander("🔍 Raw Filtered Data Insight"):
#     st.dataframe(filtered.head(500), use_container_width=True)

# st.markdown(
#     f'<p style="text-align:center; color:{TEXT_MUTED}; margin-top:2rem; font-size:0.8rem;">'
#     'Built with Streamlit · Ecommerce Sales Dashboard</p>',
#     unsafe_allow_html=True
# )


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------------------------------------------------
# Page Config (First calling page config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Ecommerce Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Theme / Palette
# ---------------------------------------------------------
PRIMARY = "#6C5CE7"      # violet
ACCENT = "#00CEC9"       # teal
WARN = "#FDCB6E"         # amber
DANGER = "#FF6B6B"       # coral (used for predicted point)
TEXT_MUTED = "#9AA0B4"

PALETTE = ["#6C5CE7", "#00CEC9", "#FD79A8", "#FDCB6E", "#74B9FF",
           "#55EFC4", "#E17055", "#A29BFE", "#81ECEC", "#FAB1A0"]

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.facecolor": "none",
    "axes.facecolor": "none",
    "savefig.facecolor": "none",
    "axes.edgecolor": "#3A3F55",
    "axes.labelcolor": "#E4E6F0",
    "xtick.color": "#B4B8C8",
    "ytick.color": "#B4B8C8",
    "text.color": "#E4E6F0",
    "axes.grid": True,
    "grid.color": "#2A2E42",
    "grid.alpha": 0.5,
    "font.family": "sans-serif",
})

# ---------------------------------------------------------
# Custom CSS — cards, headers, fonts, sidebar polish
# ---------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .dash-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }}
    .dash-subtitle {{
        color: {TEXT_MUTED};
        font-size: 1rem;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }}

    .kpi-card {{
        background: linear-gradient(145deg, #1B2036, #14172A);
        border: 1px solid #2A2E4A;
        border-radius: 16px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        transition: transform 0.15s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-3px);
        border-color: {PRIMARY};
    }}
    .kpi-label {{
        color: {TEXT_MUTED};
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }}
    .kpi-value {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: #F4F5FA;
    }}
    .kpi-icon {{
        font-size: 1.4rem;
        margin-bottom: 0.4rem;
    }}

    .section-header {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.15rem;
        font-weight: 600;
        color: #F4F5FA;
        border-left: 4px solid {PRIMARY};
        padding-left: 0.6rem;
        margin: 1.6rem 0 0.8rem 0;
    }}

    .chart-card {{
        background: #12152A;
        border: 1px solid #22263E;
        border-radius: 14px;
        padding: 1rem 1rem 0.4rem 1rem;
    }}

    .predict-card {{
        background: linear-gradient(145deg, #1B2036, #14172A);
        border: 1px solid {PRIMARY};
        border-radius: 14px;
        padding: 1rem 1.3rem;
        margin-bottom: 1rem;
    }}

    section[data-testid="stSidebar"] {{
        background: #0D0F1C;
        border-right: 1px solid #22263E;
    }}
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {{
        font-family: 'Poppins', sans-serif;
        color: {ACCENT};
    }}

    hr {{
        border-color: #22263E !important;
    }}

    div.stButton > button {{
        background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        width: 100%;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Load + Clean (Load Dataset)
# ---------------------------------------------------------
# Built relative to this file so it works both locally and on Streamlit Cloud,
# regardless of what the current working directory happens to be.
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.csv")


@st.cache_data
def load_data(path):
    df = pd.read_csv(path, encoding="latin1")
    df = df.dropna(subset=["Description"])

    df["IsCancelled"] = df["InvoiceNo"].astype(str).str.startswith("C")

    df_clean = df[
        (~df["IsCancelled"]) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ].copy()

    df_clean["InvoiceDate"] = pd.to_datetime(
        df_clean["InvoiceDate"], format="%m/%d/%Y %H:%M"
    )
    df_clean["TotalPrice"] = np.multiply(df_clean["Quantity"], df_clean["UnitPrice"])
    df_clean["Year"] = df_clean["InvoiceDate"].dt.year
    df_clean["Month"] = df_clean["InvoiceDate"].dt.month
    df_clean["Hour"] = df_clean["InvoiceDate"].dt.hour
    df_clean["DayOfWeek"] = df_clean["InvoiceDate"].dt.day_name()
    df_clean["YearMonth"] = df_clean["InvoiceDate"].dt.to_period("M").astype(str)

    return df_clean


df_clean = load_data(DATA_PATH)


# ---------------------------------------------------------
# Train Prediction Model (Linear Regression)
# ---------------------------------------------------------
@st.cache_resource
def train_prediction_model(df):
    cust_summary = df.groupby("CustomerID").agg(
        TotalSpent=("TotalPrice", "sum"),
        NumOrders=("InvoiceNo", "nunique"),
        AvgOrderValue=("TotalPrice", "mean"),
    ).reset_index().dropna()

    X = cust_summary[["NumOrders", "AvgOrderValue"]]
    y = cust_summary["TotalSpent"]

    model = LinearRegression()
    model.fit(X, y)

    r2 = r2_score(y, model.predict(X))

    return model, cust_summary, r2


pred_model, cust_summary_full, model_r2 = train_prediction_model(df_clean)

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.markdown("## 🎛️ Filters")
st.sidebar.markdown("Refine the dashboard view below.")
st.sidebar.markdown("---")

countries = sorted(df_clean["Country"].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "🌍 Country", options=countries, default=countries
)

min_date = df_clean["InvoiceDate"].min().date()
max_date = df_clean["InvoiceDate"].max().date()
date_range = st.sidebar.date_input(
    "📅 Date Range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date
)

# Filters apply karna
mask = df_clean["Country"].isin(selected_countries)
if len(date_range) == 2:
    start_date, end_date = date_range
    mask &= (df_clean["InvoiceDate"].dt.date >= start_date) & \
            (df_clean["InvoiceDate"].dt.date <= end_date)

filtered = df_clean[mask]

# ---------------------------------------------------------
# Sidebar: Spend Prediction Tool
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔮 Predict Customer Spend")
st.sidebar.caption("Enter customer details below.")

input_orders = st.sidebar.number_input(
    "Number of Orders", min_value=1, max_value=500, value=5, step=1
)
input_aov = st.sidebar.number_input(
    "Average Order Value (£)", min_value=1.0, max_value=10000.0, value=250.0, step=10.0
)
predict_btn = st.sidebar.button("✨ Predict Total Spend")

if predict_btn:
    input_data = pd.DataFrame(
        {"NumOrders": [input_orders], "AvgOrderValue": [input_aov]}
    )
    prediction = pred_model.predict(input_data)[0]
    st.session_state["prediction"] = prediction
    st.session_state["input_orders"] = input_orders
    st.session_state["input_aov"] = input_aov

# ---------------------------------------------------------
# Title
# ---------------------------------------------------------
st.markdown('<div class="dash-title">🛒 Ecommerce Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="dash-subtitle">Interactive view of revenue, products, customers and trends.</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Prediction Result Banner (agar prediction ho chuki hai)
# ---------------------------------------------------------
if "prediction" in st.session_state:
    st.markdown(f"""
    <div class="predict-card">
        🔮 Predicted Total Spend for <b>{st.session_state['input_orders']}</b> orders
        @ <b>£{st.session_state['input_aov']:,.2f}</b> avg order value =
        <span style="color:{ACCENT}; font-size:1.2rem; font-weight:700;">
            £{st.session_state['prediction']:,.2f}
        </span>
        <span style="color:{TEXT_MUTED};"> (Model R²: {model_r2:.2f})</span>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# KPI Cards (top metrics row)
# ---------------------------------------------------------
total_revenue = filtered["TotalPrice"].sum()
total_orders = filtered["InvoiceNo"].nunique()
total_customers = filtered["CustomerID"].nunique()
avg_order_value = filtered.groupby("InvoiceNo")["TotalPrice"].sum().mean()

kpis = [
    ("💰", "Total Revenue", f"£{total_revenue:,.0f}"),
    ("📦", "Total Orders", f"{total_orders:,}"),
    ("👥", "Total Customers", f"{total_customers:,}"),
    ("🧾", "Avg Order Value", f"£{avg_order_value:,.2f}"),
]

cols = st.columns(4)
for col, (icon, label, value) in zip(cols, kpis):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


def styled_fig(figsize=(6, 4)):
    """Create a matplotlib fig/ax pair matching the dark theme."""
    fig, ax = plt.subplots(figsize=figsize)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    return fig, ax


def render_chart(container, title, plot_fn):
    with container:
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        plot_fn()
        st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------
# Row 1: Monthly Trend + Top Countries
# ---------------------------------------------------------
row1_col1, row1_col2 = st.columns(2)


def plot_monthly_trend():
    monthly_sales = filtered.groupby("YearMonth")["TotalPrice"].sum()
    fig, ax = styled_fig()
    ax.plot(monthly_sales.index, monthly_sales.values, marker="o",
            color=PRIMARY, linewidth=2.2, markersize=5,
            markerfacecolor=ACCENT, markeredgecolor="none")
    ax.fill_between(range(len(monthly_sales)), monthly_sales.values, alpha=0.08, color=PRIMARY)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Revenue (£)")
    plt.xticks(rotation=45)
    st.pyplot(fig, transparent=True)


def plot_top_countries():
    country_revenue = (
        filtered.groupby("Country")["TotalPrice"].sum()
        .sort_values(ascending=False).head(10)
    )
    fig, ax = styled_fig()
    sns.barplot(x=country_revenue.values, y=country_revenue.index,
                hue=country_revenue.index, palette=PALETTE, legend=False, ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    st.pyplot(fig, transparent=True)


render_chart(row1_col1, "📈 Monthly Revenue Trend", plot_monthly_trend)
render_chart(row1_col2, "🌍 Top 10 Countries by Revenue", plot_top_countries)

# ---------------------------------------------------------
# Row 2: Top Products + Order Value Distribution
# ---------------------------------------------------------
row2_col1, row2_col2 = st.columns(2)


def plot_top_products():
    top_products = (
        filtered.groupby("Description")["TotalPrice"].sum()
        .sort_values(ascending=False).head(10)
    )
    fig, ax = styled_fig()
    sns.barplot(x=top_products.values, y=top_products.index,
                hue=top_products.index, palette=PALETTE, legend=False, ax=ax)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    st.pyplot(fig, transparent=True)


def plot_order_distribution():
    order_values = filtered.groupby("InvoiceNo")["TotalPrice"].sum().values
    fig, ax = styled_fig()
    sns.histplot(order_values, bins=50, kde=True, color=ACCENT, ax=ax,
                 edgecolor="none", alpha=0.7)
    ax.set_xlim(0, 1000)
    ax.set_xlabel("Order Value (£)")
    ax.set_ylabel("Count")
    st.pyplot(fig, transparent=True)


render_chart(row2_col1, "🏆 Top 10 Products by Revenue", plot_top_products)
render_chart(row2_col2, "📊 Order Value Distribution", plot_order_distribution)

# ---------------------------------------------------------
# Row 3: Sales by Day of Week + Hour
# ---------------------------------------------------------
row3_col1, row3_col2 = st.columns(2)

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]


def plot_sales_by_day():
    sales_by_day = filtered.groupby("DayOfWeek")["TotalPrice"].sum().reindex(day_order)
    fig, ax = styled_fig()
    sns.barplot(x=sales_by_day.index, y=sales_by_day.values,
                hue=sales_by_day.index, palette=PALETTE, legend=False, ax=ax)
    plt.xticks(rotation=45)
    ax.set_xlabel("")
    ax.set_ylabel("Revenue (£)")
    st.pyplot(fig, transparent=True)


def plot_sales_by_hour():
    sales_by_hour = filtered.groupby("Hour")["TotalPrice"].sum()
    fig, ax = styled_fig()
    ax.plot(sales_by_hour.index, sales_by_hour.values, marker="o",
            color=WARN, linewidth=2.2, markersize=5,
            markerfacecolor=PRIMARY, markeredgecolor="none")
    ax.fill_between(sales_by_hour.index, sales_by_hour.values, alpha=0.08, color=WARN)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Revenue (£)")
    st.pyplot(fig, transparent=True)


render_chart(row3_col1, "📅 Revenue by Day of Week", plot_sales_by_day)
render_chart(row3_col2, "🕒 Revenue by Hour of Day", plot_sales_by_hour)

# ---------------------------------------------------------
# Row 4: Top Customers Table
# ---------------------------------------------------------
st.markdown('<div class="section-header">👤 Top 10 Customers by Spend</div>', unsafe_allow_html=True)
customer_summary = filtered.groupby("CustomerID").agg(
    TotalSpent=("TotalPrice", "sum"),
    NumOrders=("InvoiceNo", "nunique"),
    AvgOrderValue=("TotalPrice", "mean"),
    LastPurchase=("InvoiceDate", "max")
).sort_values("TotalSpent", ascending=False).head(10)

st.dataframe(
    customer_summary.style
        .format({"TotalSpent": "£{:,.2f}", "AvgOrderValue": "£{:,.2f}"})
        .background_gradient(subset=["TotalSpent"], cmap="Purples"),
    use_container_width=True
)

# ---------------------------------------------------------
# Row 5: Prediction vs Existing Customers (agar prediction ho chuki hai)
# ---------------------------------------------------------
if "prediction" in st.session_state:
    st.markdown('<div class="section-header">🔮 Your Predicted Customer vs Existing Customers</div>',
                unsafe_allow_html=True)

    comparison_df = cust_summary_full[["CustomerID", "NumOrders", "AvgOrderValue", "TotalSpent"]].copy()
    comparison_df["Type"] = "Existing Customer"

    new_row = pd.DataFrame({
        "CustomerID": ["Your Input"],
        "NumOrders": [st.session_state["input_orders"]],
        "AvgOrderValue": [st.session_state["input_aov"]],
        "TotalSpent": [st.session_state["prediction"]],
        "Type": ["Predicted (You)"]
    })

    combined = pd.concat([comparison_df, new_row], ignore_index=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    fig, ax = styled_fig(figsize=(10, 5))
    sns.scatterplot(
        data=combined, x="NumOrders", y="TotalSpent", hue="Type",
        palette={"Existing Customer": "#3D4266", "Predicted (You)": DANGER},
        s=110, ax=ax, edgecolor="none"
    )
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Total Spend (£)")
    ax.legend(frameon=False, labelcolor="#E4E6F0")
    st.pyplot(fig, transparent=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# Raw Data (optional expandable section)
# ---------------------------------------------------------
with st.expander("🔍 Raw Filtered Data Insight"):
    st.dataframe(filtered.head(500), use_container_width=True)

st.markdown(
    f'<p style="text-align:center; color:{TEXT_MUTED}; margin-top:2rem; font-size:0.8rem;">'
    'Built with Streamlit · Ecommerce Sales Dashboard</p>',
    unsafe_allow_html=True
)