# 2_Aggregated_Attendance.py

import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from dateutil.relativedelta import relativedelta

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb

import altair as alt

initialize_mongodb()

st.set_page_config(page_title="Aggregated Attendance", layout="wide")
st.title("Aggregated Attendance")

with st.expander("Filters", expanded=True):
  months = (
      "All",
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
  )
  years = range(2024, 2026)

  today = datetime.date.today()
  current_month = today.month
  current_year = today.year

  month_col1, year_col2 = st.columns([2, 2])
  with month_col1:
    selected_month = st.selectbox("Month", months, index=current_month)
  with year_col2:
    selected_year = st.selectbox(
        "Year", years, index=years.index(current_year))

  if selected_month == "All":
    start_date = datetime.date(selected_year, 1, 1)
    end_date = datetime.date(selected_year, 12, 31)
  else:
    month_index = months.index(selected_month)
    start_date = datetime.date(selected_year, month_index, 1)
    next_month = start_date + relativedelta(months=1)
    end_date = next_month - datetime.timedelta(days=1)

  filter_date_range = (start_date, end_date)
  st.caption(
      f"Filtering from **{filter_date_range[0]}** to **{filter_date_range[1]}**")

pipeline = [
    {
        "$match": {
            "day": {
                "$gte": datetime.datetime.combine(start_date, datetime.time.min),
                "$lte": datetime.datetime.combine(end_date, datetime.time.max),
            }
        }
    },
    {
        "$group": {
            "_id": {
                "employee_id": "$employee_id",
                "status": "$status",
            },
            "count": {"$sum": 1},
        }
    }
]
results = list(Attendance.objects.aggregate(*pipeline))
records = [
    {
        "employee_id": r["_id"]["employee_id"],
        "status": r["_id"]["status"],
        "count": r["count"]
    }
    for r in results
]

df = pd.DataFrame(records)
all_statuses = Attendance._fields["status"].choices
if not df.empty:
  summary = (
      df.pivot_table(
          index="employee_id", columns="status", values="count", fill_value=0
      )
      .reindex(columns=all_statuses, fill_value=0)
      .reset_index()
  )
else:
  summary = pd.DataFrame(columns=["employee_id"] + list(all_statuses))
st.dataframe(summary, use_container_width=True)

data = {
    "status": ["present", "absent", "leave", "holiday", "weekend"],
    "count": [19, 0, 2, 2, 7],
}

df = pd.DataFrame(data)
df["percentage"] = df["count"] / df["count"].sum() * 100
df_nonzero = df[df["count"] > 0]

chart = alt.Chart(df_nonzero).mark_bar().encode(
    x=alt.X("count:Q", stack="normalize"),  
    color=alt.Color("status:N", scale=alt.Scale(
        domain=["present", "absent", "leave", "holiday", "weekend"],
        range=["#22c55e", "#ef4444", "#facc15", "#3b82f6", "#a855f7"]
    )),
    tooltip=[
        alt.Tooltip("status:N"),
        alt.Tooltip("count:Q"),
        alt.Tooltip("percentage:Q", format=".2f")
    ]
).properties(
    height=50,
    width=600
)

st.altair_chart(chart)
