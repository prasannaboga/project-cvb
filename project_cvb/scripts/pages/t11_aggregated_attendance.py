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

all_statuses = ["present", "absent", "leave", "holiday", "weekend"]
status_order_map = {status: i for i, status in enumerate(all_statuses)}
status_color_map = {
    "present": "#22c55e",
    "absent": "#ef4444",
    "leave": "#facc15",
    "holiday": "#3b82f6",
    "weekend": "#a855f7"
}

df = pd.DataFrame(records)
if not df.empty:
  aggregate_records = (
      df.pivot_table(
          index="employee_id", columns="status", values="count", fill_value=0
      )
      .reindex(columns=all_statuses, fill_value=0)
      .reset_index()
  )
else:
  aggregate_records = pd.DataFrame(
      columns=["employee_id"] + list(all_statuses))

for _, row in aggregate_records.iterrows():
  st.divider()
  name_col, daily_time_col, summary_col = st.columns([1, 3, 1])

  name_col.write(row["employee_id"])

  status_data = pd.DataFrame({
      "status": all_statuses,
      "count": [row["present"], row["absent"], row["leave"], row["holiday"], row["weekend"]],
  })
  status_data["percentage"] = status_data["count"] / \
      status_data["count"].sum() * 100
  status_data['order'] = status_data['status'].map(status_order_map)

  status_chart = alt.Chart(status_data).mark_bar().encode(
      x=alt.X("count:Q", stack="normalize", axis=None),
      order=alt.Order("order:Q"),
      color=alt.Color("status:N", sort=all_statuses, scale=alt.Scale(domain=all_statuses,
                                                                     range=[status_color_map[s] for s in all_statuses]), legend=None),
      tooltip=[
          alt.Tooltip("status:N", title="Status"),
          alt.Tooltip("count:Q", title="Count"),
          alt.Tooltip("percentage:Q", title="Percentage", format=".2f")
      ]
  ).properties(
      height=45,
      width="container"
  )
  summary_col.altair_chart(status_chart, use_container_width=True)

st.divider()
