import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yaml
import os
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(__file__).parent / "config.yaml"


@st.cache_data(ttl=5)
def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_file_mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


@st.cache_data(ttl=5)
def load_data(path: str, _mtime: float):
    """Load the Fact_Monthly sheet. _mtime is used to bust the cache when the
    file changes on disk (OneDrive sync)."""
    df = pd.read_excel(path, sheet_name="Fact_Monthly", engine="openpyxl")
    df["Month"] = pd.to_datetime(df["Month"])
    numeric_cols = [
        "AI Use Cases Delivered", "Automation Hours Saved", "Client Engagements",
        "Revenue Influenced (USD)", "Delivery Cost (USD)", "Pipeline Value (USD)",
        "Model Deployments", "Avg Model Accuracy (%)",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


@st.cache_data(ttl=5)
def load_kpis(path: str, _mtime: float):
    raw = pd.read_excel(path, sheet_name="Executive_KPIs", engine="openpyxl")
    kpis = {}
    for _, row in raw.iterrows():
        key = row.iloc[0]
        val = row.iloc[1]
        if pd.notna(key) and key != "Metric":
            kpis[str(key).strip()] = val
    return kpis


# ---------------------------------------------------------------------------
# Access control helpers
# ---------------------------------------------------------------------------

def is_admin(cfg) -> bool:
    """Return True if the current user's EY email is in the admins list."""
    admins = [a.lower().strip() for a in cfg.get("admins", [])]
    current = st.session_state.get("user_email", "").lower().strip()
    return current in admins


def has_access(cfg) -> bool:
    """Return True if user is an admin or an approved viewer."""
    if is_admin(cfg):
        return True
    viewers = [v.lower().strip() for v in cfg.get("viewers", [])]
    current = st.session_state.get("user_email", "").lower().strip()
    return current in viewers


def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(cfg, f, default_flow_style=False)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_usd(val):
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:,.1f}B"
    if val >= 1_000_000:
        return f"${val / 1_000_000:,.1f}M"
    if val >= 1_000:
        return f"${val / 1_000:,.0f}K"
    return f"${val:,.0f}"


def fmt_number(val):
    if val >= 1_000_000:
        return f"{val / 1_000_000:,.1f}M"
    if val >= 1_000:
        return f"{val / 1_000:,.1f}K"
    return f"{val:,.0f}"


# ---------------------------------------------------------------------------
# EY brand color palette
# ---------------------------------------------------------------------------

EY_COLORS = ["#FFE600", "#00A3E0", "#FF6D00", "#2C973E", "#C893D4", "#E0004D"]


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Factory.AI Partner Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for EY branding
st.markdown("""
<style>
    .main .block-container { padding-top: 1.5rem; }
    div[data-testid="stMetric"] {
        background-color: #1A1A24;
        border: 1px solid #FFE600;
        border-radius: 8px;
        padding: 12px 16px;
    }
    div[data-testid="stMetric"] label { color: #AAAAAA !important; font-size: 0.85rem; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #FFE600 !important; }
    .stSelectbox label, .stMultiSelect label { color: #CCCCCC !important; }
    header[data-testid="stHeader"] { background-color: #2E2E38; }
    .live-indicator {
        display: inline-block;
        width: 8px; height: 8px;
        background: #2C973E;
        border-radius: 50%;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Load config and data
# ---------------------------------------------------------------------------

cfg = load_config()
excel_path = cfg["excel_path"]
mtime = get_file_mtime(excel_path)

if not os.path.exists(excel_path):
    st.error(f"Excel file not found: {excel_path}")
    st.info("Make sure OneDrive is synced and the file path in config.yaml is correct.")
    st.stop()

df = load_data(excel_path, mtime)
kpis = load_kpis(excel_path, mtime)

# ---------------------------------------------------------------------------
# Sidebar: Identity + Filters
# ---------------------------------------------------------------------------

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/34/EY_logo_2019.svg", width=80)
    st.markdown("### Factory.AI Partner Dashboard")

    st.divider()

    # Login via EY email
    email = st.text_input(
        "Your EY email",
        value=st.session_state.get("user_email", ""),
        placeholder="first.last@ey.com",
    )
    if email:
        st.session_state["user_email"] = email.lower().strip()

    user_is_admin = is_admin(cfg)
    if user_is_admin:
        st.success("Role: Admin")
    else:
        st.info("Role: Viewer (read-only)")

    st.divider()
    st.markdown("#### Filters")

    regions = sorted(df["Region"].unique())
    sectors = sorted(df["Sector"].unique())
    offerings = sorted(df["Offering"].unique())
    months = sorted(df["Month"].unique())

    sel_regions = st.multiselect("Region", regions, default=regions)
    sel_sectors = st.multiselect("Sector", sectors, default=sectors)
    sel_offerings = st.multiselect("Offering", offerings, default=offerings)

    min_month = months[0].to_pydatetime()
    today = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    max_data_month = months[-1].to_pydatetime()
    slider_max = max(today, max_data_month)

    date_range = st.slider(
        "Date Range",
        min_value=min_month,
        max_value=slider_max,
        value=(min_month, slider_max),
        format="MMM YYYY",
    )

    st.divider()
    last_modified = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(
        f'<span class="live-indicator"></span> **Live** &nbsp;|&nbsp; Last sync: {last_modified}',
        unsafe_allow_html=True,
    )
    refresh = cfg.get("refresh_interval_seconds", 10)
    st.caption(f"Auto-refresh every {refresh}s")

# ---------------------------------------------------------------------------
# Access gate
# ---------------------------------------------------------------------------

user_email = st.session_state.get("user_email", "").strip()
if not user_email:
    st.warning("Please enter your EY email in the sidebar to access the dashboard.")
    st.stop()

if not has_access(cfg):
    st.error("You do not have access to this dashboard. Ask an admin to grant you access.")
    st.stop()

# ---------------------------------------------------------------------------
# Apply filters
# ---------------------------------------------------------------------------

mask = (
    df["Region"].isin(sel_regions)
    & df["Sector"].isin(sel_sectors)
    & df["Offering"].isin(sel_offerings)
    & (df["Month"] >= pd.Timestamp(date_range[0]))
    & (df["Month"] <= pd.Timestamp(date_range[1]))
)
fdf = df[mask].copy()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.markdown("## Factory.AI Partner Dashboard (USD)")
st.caption("Real-time view powered by OneDrive-synced Excel data")

# ---------------------------------------------------------------------------
# KPI cards row
# ---------------------------------------------------------------------------

k1, k2, k3, k4, k5, k6 = st.columns(6)

total_revenue = fdf["Revenue Influenced (USD)"].sum()
total_cost = fdf["Delivery Cost (USD)"].sum()
total_pipeline = fdf["Pipeline Value (USD)"].sum()
total_use_cases = fdf["AI Use Cases Delivered"].sum()
total_hours = fdf["Automation Hours Saved"].sum()
avg_accuracy = fdf["Avg Model Accuracy (%)"].mean()

k1.metric("Revenue Influenced", fmt_usd(total_revenue))
k2.metric("Delivery Cost", fmt_usd(total_cost))
k3.metric("Pipeline Value", fmt_usd(total_pipeline))
k4.metric("Use Cases Delivered", fmt_number(total_use_cases))
k5.metric("Hours Saved", fmt_number(total_hours))
k6.metric("Avg Model Accuracy", f"{avg_accuracy:.1f}%")

st.divider()

# ---------------------------------------------------------------------------
# Row 1: Revenue over time + Pipeline by Region
# ---------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    monthly_rev = (
        fdf.groupby("Month")["Revenue Influenced (USD)"]
        .sum()
        .reset_index()
    )
    fig = px.area(
        monthly_rev,
        x="Month",
        y="Revenue Influenced (USD)",
        title="Revenue Influenced Over Time",
        color_discrete_sequence=["#FFE600"],
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#333"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    region_pipeline = (
        fdf.groupby("Region")["Pipeline Value (USD)"]
        .sum()
        .reset_index()
        .sort_values("Pipeline Value (USD)", ascending=True)
    )
    fig = px.bar(
        region_pipeline,
        x="Pipeline Value (USD)",
        y="Region",
        orientation="h",
        title="Pipeline Value by Region",
        color="Region",
        color_discrete_sequence=EY_COLORS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#333"),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 2: Use Cases by Offering + Sector Revenue Heatmap
# ---------------------------------------------------------------------------

col3, col4 = st.columns(2)

with col3:
    offering_cases = (
        fdf.groupby("Offering")["AI Use Cases Delivered"]
        .sum()
        .reset_index()
    )
    fig = px.pie(
        offering_cases,
        values="AI Use Cases Delivered",
        names="Offering",
        title="AI Use Cases by Offering",
        color_discrete_sequence=EY_COLORS,
        hole=0.45,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
    )
    st.plotly_chart(fig, use_container_width=True)

with col4:
    heatmap_data = (
        fdf.groupby(["Region", "Sector"])["Revenue Influenced (USD)"]
        .sum()
        .reset_index()
    )
    pivot = heatmap_data.pivot(index="Sector", columns="Region", values="Revenue Influenced (USD)").fillna(0)
    fig = px.imshow(
        pivot.values,
        labels=dict(x="Region", y="Sector", color="Revenue (USD)"),
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        title="Revenue Heatmap: Region x Sector",
        color_continuous_scale=["#1A1A24", "#FFE600"],
        aspect="auto",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 3: Model Deployments Trend + Automation Hours by Sector
# ---------------------------------------------------------------------------

col5, col6 = st.columns(2)

with col5:
    monthly_deploy = (
        fdf.groupby("Month")["Model Deployments"]
        .sum()
        .reset_index()
    )
    fig = px.line(
        monthly_deploy,
        x="Month",
        y="Model Deployments",
        title="Model Deployments Over Time",
        color_discrete_sequence=["#00A3E0"],
        markers=True,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#333"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col6:
    sector_hours = (
        fdf.groupby("Sector")["Automation Hours Saved"]
        .sum()
        .reset_index()
        .sort_values("Automation Hours Saved", ascending=True)
    )
    fig = px.bar(
        sector_hours,
        x="Automation Hours Saved",
        y="Sector",
        orientation="h",
        title="Automation Hours Saved by Sector",
        color="Sector",
        color_discrete_sequence=EY_COLORS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#333"),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Row 4: Revenue vs Cost scatter + Client Engagements trend
# ---------------------------------------------------------------------------

col7, col8 = st.columns(2)

with col7:
    scatter_data = (
        fdf.groupby(["Region", "Offering"])
        .agg({"Revenue Influenced (USD)": "sum", "Delivery Cost (USD)": "sum", "Client Engagements": "sum"})
        .reset_index()
    )
    fig = px.scatter(
        scatter_data,
        x="Delivery Cost (USD)",
        y="Revenue Influenced (USD)",
        size="Client Engagements",
        color="Region",
        symbol="Offering",
        title="Revenue vs Cost (size = Engagements)",
        color_discrete_sequence=EY_COLORS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        xaxis=dict(showgrid=True, gridcolor="#333"),
        yaxis=dict(showgrid=True, gridcolor="#333"),
    )
    st.plotly_chart(fig, use_container_width=True)

with col8:
    monthly_engage = (
        fdf.groupby(["Month", "Region"])["Client Engagements"]
        .sum()
        .reset_index()
    )
    fig = px.line(
        monthly_engage,
        x="Month",
        y="Client Engagements",
        color="Region",
        title="Client Engagements Over Time",
        color_discrete_sequence=EY_COLORS,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#333"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Data table + Admin editing
# ---------------------------------------------------------------------------

st.divider()
st.markdown("### Detailed Data")

if user_is_admin:
    st.markdown("*Admin mode: you can edit data, download exports, and manage access.*")
    csv = fdf.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered CSV", csv, "factory_ai_dashboard_export.csv", "text/csv")

    st.markdown("#### Edit Data")
    edited_df = st.data_editor(
        fdf,
        use_container_width=True,
        height=400,
        num_rows="dynamic",
        key="data_editor",
    )

    if st.button("Save Changes to Excel"):
        full_df = df.copy()
        full_df.update(edited_df)
        new_rows = edited_df.loc[~edited_df.index.isin(df.index)]
        if not new_rows.empty:
            full_df = pd.concat([full_df, new_rows], ignore_index=True)
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            full_df.to_excel(writer, sheet_name="Fact_Monthly", index=False)
        st.success("Changes saved to Excel. Dashboard will refresh automatically.")
        load_data.clear()
        load_kpis.clear()
        time.sleep(1)
        st.rerun()
else:
    with st.expander("View raw data", expanded=False):
        st.dataframe(fdf, use_container_width=True, height=400)

# ---------------------------------------------------------------------------
# Admin-only: manage access
# ---------------------------------------------------------------------------

if user_is_admin:
    st.divider()
    st.markdown("### Admin: Manage Access")

    tab_viewers, tab_admins = st.tabs(["Viewers", "Admins"])

    # --- Viewers tab ---
    with tab_viewers:
        st.caption("Viewers have read-only access to the dashboard.")
        current_viewers = cfg.get("viewers", [])
        if current_viewers:
            st.markdown("**Current viewers:**")
            for v in current_viewers:
                st.text(f"  {v}")
        else:
            st.info("No viewers added yet. All access is currently admin-only.")

        new_viewer = st.text_input("Add viewer email", placeholder="first.last@ey.com", key="add_viewer")
        if st.button("Add Viewer") and new_viewer:
            normalized = new_viewer.lower().strip()
            if not normalized.endswith("@ey.com"):
                st.warning("Please enter a valid @ey.com email address.")
            elif normalized in [a.lower().strip() for a in cfg.get("admins", [])]:
                st.warning("This user is already an admin.")
            elif normalized not in [v.lower().strip() for v in current_viewers]:
                current_viewers.append(normalized)
                cfg["viewers"] = current_viewers
                save_config(cfg)
                st.success(f"Added {normalized} as viewer")
                load_config.clear()
                st.rerun()
            else:
                st.warning("Email already in viewers list.")

        if current_viewers:
            remove_viewer = st.selectbox("Remove viewer", current_viewers, key="rm_viewer")
            if st.button("Remove Viewer"):
                current_viewers.remove(remove_viewer)
                cfg["viewers"] = current_viewers
                save_config(cfg)
                st.success(f"Removed {remove_viewer}")
                load_config.clear()
                st.rerun()

    # --- Admins tab ---
    with tab_admins:
        st.caption("Admins can edit data, export, and manage all user access.")
        current_admins = cfg.get("admins", [])
        st.markdown("**Current admins:**")
        for a in current_admins:
            st.text(f"  {a}")

        new_admin = st.text_input("Add admin email", placeholder="first.last@ey.com", key="add_admin")
        if st.button("Add Admin") and new_admin:
            normalized = new_admin.lower().strip()
            if not normalized.endswith("@ey.com"):
                st.warning("Please enter a valid @ey.com email address.")
            elif normalized not in [a.lower().strip() for a in current_admins]:
                current_admins.append(normalized)
                cfg["admins"] = current_admins
                # Remove from viewers if they were a viewer
                viewers = cfg.get("viewers", [])
                cfg["viewers"] = [v for v in viewers if v.lower().strip() != normalized]
                save_config(cfg)
                st.success(f"Added {normalized} as admin")
                load_config.clear()
                st.rerun()
            else:
                st.warning("Email already in admins list.")

        if len(current_admins) > 1:
            remove_admin = st.selectbox("Remove admin", current_admins, key="rm_admin")
            if st.button("Remove Admin"):
                if remove_admin.lower().strip() == st.session_state.get("user_email", "").lower().strip():
                    st.warning("You cannot remove yourself.")
                else:
                    current_admins.remove(remove_admin)
                    cfg["admins"] = current_admins
                    save_config(cfg)
                    st.success(f"Removed {remove_admin}")
                    load_config.clear()
                    st.rerun()

# ---------------------------------------------------------------------------
# Auto-refresh: re-run every N seconds to pick up Excel changes
# ---------------------------------------------------------------------------

time.sleep(cfg.get("refresh_interval_seconds", 10))
st.rerun()
