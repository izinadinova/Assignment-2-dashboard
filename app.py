"""Assignment 2: four linked views of the ISLP Auto data."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Auto Explorer", page_icon="🚗", layout="wide")

# Read the same complete Auto data used in the notebook.
auto = pd.read_csv(Path(__file__).with_name("Auto.csv"))
auto["Origin"] = auto["origin"].map({1: "American", 2: "European", 3: "Japanese"})
auto["Model year"] = auto["year"] + 1900

st.title("Auto Explorer")
st.write("How do fuel economy, weight and engine groups differ by car origin?")
st.caption("Assignment 2 · Inzhumarzhan Zinadinova · ISLP Auto · 392 historical cars, model years 1970–1982")

# These filters select one table. Every chart below uses that same table.
st.sidebar.header("Choose the cars")
origin = st.sidebar.selectbox("Car origin", ["All origins", "American", "European", "Japanese"])
years = st.sidebar.slider("Model year", 1970, 1982, (1970, 1982))
data = auto[auto["Model year"].between(years[0], years[1])].copy()
if origin != "All origins":
    data = data[data["Origin"] == origin].copy()
st.sidebar.caption("Both filters change all four charts together. Hover over a chart to see values.")

if data.empty:
    st.info("No cars match these filters. Choose another origin or a wider year range.")
    st.stop()

st.subheader(f"{origin} · {years[0]}–{years[1]} · {len(data)} cars")
one, two, three = st.columns(3)
one.metric("Cars selected", len(data))
two.metric("Mean fuel economy", f"{data['mpg'].mean():.2f} mpg")
three.metric("Mean weight", f"{data['weight'].mean():,.0f} lb")
st.caption("MPG means miles per US gallon. A higher MPG value means better fuel economy.")

left, right = st.columns(2)
with left:
    st.markdown("#### 1. Fuel economy distribution")
    hist = px.histogram(data, x="mpg", color_discrete_sequence=["#2563a6"],
                        labels={"mpg": "Fuel economy (mpg)"})
    hist.update_traces(xbins={"start": 5, "end": 50, "size": 5})
    hist.update_layout(yaxis_title="Cars", height=350, showlegend=False)
    hist.update_xaxes(range=[5, 50])
    st.plotly_chart(hist, width="stretch", key="mpg_histogram")
    st.caption("The histogram shows how many selected cars fall in each 5-mpg band.")

with right:
    st.markdown("#### 2. Weight and fuel economy")
    scatter = px.scatter(data, x="weight", y="mpg", hover_name="name", color="Origin",
                         labels={"weight": "Weight (lb)", "mpg": "Fuel economy (mpg)"},
                         color_discrete_map={"American": "#2563a6", "European": "#dc8833", "Japanese": "#208777"})
    scatter.update_traces(marker={"size": 7, "opacity": 0.7})
    scatter.update_layout(height=350, legend_title_text="Origin")
    scatter.update_xaxes(range=[1400, 5300]); scatter.update_yaxes(range=[5, 50])
    st.plotly_chart(scatter, width="stretch", key="weight_mpg")
    st.caption("Each point is one car. A downward pattern means heavier cars tend to have lower MPG.")

left, right = st.columns(2)
with left:
    st.markdown("#### 3. Mean fuel economy by model year")
    yearly = data.groupby("Model year", as_index=False)["mpg"].mean()
    line = px.line(yearly, x="Model year", y="mpg", markers=True,
                   labels={"mpg": "Mean fuel economy (mpg)"}, color_discrete_sequence=["#208777"])
    line.update_layout(height=350)
    line.update_xaxes(range=[1969.5, 1982.5], dtick=2); line.update_yaxes(range=[5, 50])
    st.plotly_chart(line, width="stretch", key="year_mpg")
    st.caption("The line compares different model-year groups. It does not follow the same car over time.")

with right:
    st.markdown("#### 4. Fuel economy by engine cylinders")
    data["Cylinder group"] = data["cylinders"].astype(str)
    box = px.box(data, x="Cylinder group", y="mpg", points=False,
                  category_orders={"Cylinder group": ["3", "4", "5", "6", "8"]},
                  labels={"mpg": "Fuel economy (mpg)"}, color_discrete_sequence=["#208777"])
    box.update_layout(height=350, xaxis_title="Cylinders")
    box.update_yaxes(range=[5, 50])
    st.plotly_chart(box, width="stretch", key="cylinders_mpg")
    st.caption("The boxplot compares the median and spread of MPG across cylinder groups.")

st.divider()
st.write(f"For this selection, mean fuel economy is {data['mpg'].mean():.2f} mpg across {len(data)} cars.")
st.caption("Source: ISLP Auto, complete course CSV. The data are historical and show associations, not causes.")
with st.expander("Show the selected data"):
    st.dataframe(data[["name", "Origin", "Model year", "cylinders", "weight", "horsepower", "mpg"]], hide_index=True)
st.markdown("[ISLP source and variable definitions](https://intro-stat-learning.github.io/ISLP/datasets/Auto.html)")
