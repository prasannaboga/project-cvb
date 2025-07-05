import streamlit as st
import time

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb
from project_cvb.config.settings import Settings


def paginate(queryset, page, page_size):
  total_records = queryset.count()
  total_pages = (total_records + page_size - 1) // page_size
  page = min(max(1, page), total_pages)
  results = queryset.skip((page - 1) * page_size).limit(page_size)
  return list(results), page, total_pages, total_records


st.set_page_config(page_title="Demo App", layout="wide")
st.title("App")

initialize_mongodb()
page_size = 25
page = st.session_state.get("page_number", 1)

employee_ids = Attendance.objects().distinct("employee_id")
selected_employee = st.selectbox(
    "Filter by Employee", ["All"] + sorted(employee_ids)
)

sort_col1, sort_col2 = st.columns([1, 1])
with sort_col1:
  columns = ["Employee ID", "Day", "Check In", "Check Out", "Status"]
  sort_column = st.selectbox("Sort by", columns, index=1)

with sort_col2:
  sort_direction = st.selectbox(
      "Order", ["Desc", "Asc"], label_visibility="hidden")

field_map = {
    "Employee ID": "employee_id",
    "Day": "day",
    "Check In": "check_in",
    "Check Out": "check_out",
    "Status": "status"
}
sort_field = field_map[sort_column]
order_by = f"-{sort_field}" if sort_direction == "Desc" else sort_field

queryset = Attendance.objects()
if selected_employee != "All":
  queryset = queryset.filter(employee_id=selected_employee)

with st.spinner("Loading data...", show_time=True):
  attendances, page, total_pages, total_records = paginate(
      queryset.order_by(order_by),
      page,
      page_size
  )
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
      label_visibility="collapsed"
  )
  if page !=1 and new_page >= max(1, total_pages):
    st.warning("You have reached the last page.")
