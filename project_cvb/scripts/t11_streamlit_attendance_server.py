import datetime
import time

import streamlit as st

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb
from project_cvb.config.settings import Settings

st.set_page_config(page_title="Demo App", layout="wide")
st.title("App")


@st.cache_data
def get_employee_ids():
  return Attendance.objects().distinct("employee_id")


@st.cache_data
def get_status_values():
  return Attendance._fields["status"].choices


def paginate(queryset, page, page_size):
  time.sleep(0.7)
  total_records = queryset.count()
  if total_records == 0:
    return [], 1, 1, 0
  total_pages = (total_records + page_size - 1) // page_size
  page = min(max(1, page), total_pages)
  results = queryset.skip((page - 1) * page_size).limit(page_size)
  return list(results), page, total_pages, total_records


initialize_mongodb()
page_size = 25
page = st.session_state.get("page_number", 1)
field_map = {
    "Employee ID": "employee_id",
    "Day": "day",
    "Check In": "check_in",
    "Check Out": "check_out",
    "Status": "status"
}

min_day = datetime.date(2025, 7, 1)
max_day = datetime.date(2025, 7, 31)
employee_ids = get_employee_ids()
status_values = get_status_values()

query_params = st.query_params
selected_employee = query_params.get("employee", "All")
selected_status = query_params.get("status", "All")

with st.sidebar:
  st.header("Will come with somename")

with st.expander("Filters", expanded=True):
  filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 3])
  with filter_col1:
    employee_columns = ["All"] + sorted(employee_ids)
    selected_employee = st.selectbox(
        "Employee", employee_columns, index=employee_columns.index(selected_employee))
  with filter_col2:
    status_options = ["All"] + sorted(status_values)
    selected_status = st.selectbox(
        "Status", status_options, index=status_options.index(selected_status))
  with filter_col3:
    selected_day = st.date_input(
        "Day", value=(min_day, max_day), format="YYYY-MM-DD")

  st.query_params["employee"] = selected_employee
  st.query_params["status"] = selected_status

  sort_col1, sort_col2 = st.columns([1, 1])
  with sort_col1:
    columns = ["Employee ID", "Day", "Check In", "Check Out", "Status"]
    sort_column = st.selectbox("Sort by", columns, index=1)

  with sort_col2:
    sort_direction = st.selectbox(
        "Order", ["Desc", "Asc"], label_visibility="hidden")

# Sorting
sort_field = field_map[sort_column]
order_by = f"-{sort_field}" if sort_direction == "Desc" else sort_field

queryset = Attendance.objects()
if selected_employee != "All":
  queryset = queryset.filter(employee_id=selected_employee)
if selected_status != "All":
  queryset = queryset.filter(status=selected_status)
if isinstance(selected_day, tuple) and len(selected_day) == 2:
  queryset = queryset.filter(
      day__gte=selected_day[0], day__lte=selected_day[1])
else:
  queryset = queryset.filter(day=selected_day)

with st.spinner("Loading data...", show_time=True):
  attendances, page, total_pages, total_records = paginate(
      queryset.order_by(order_by), page, page_size)
data = [
    {
        "Employee ID": a.employee_id,
        "Day": a.day,
        "Check In": a.check_in,
        "Check Out": a.check_out,
        "Status": a.status
    }
    for a in attendances
]

st.dataframe(data, use_container_width=True)

paginate_text, page_stepper = st.columns([4, 1])
with paginate_text:
  st.caption(f"Page {page} of {total_pages} ({total_records} records)")

with page_stepper:
  new_page = st.number_input(
      "Page",
      min_value=1,
      max_value=max(1, total_pages),
      value=page,
      step=1,
      key="page_number",
      label_visibility="collapsed",
  )
  if page != 1 and new_page >= max(1, total_pages):
    st.warning("You have reached the last page.")
