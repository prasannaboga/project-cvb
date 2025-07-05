import os

import streamlit as st
from PIL import Image


st.set_page_config(page_title="Hello Project", layout="wide")
col1, col2 = st.columns([3, 7])


with col1:
  st.markdown(
      """
      <div style="background-color: #e0e0e0; height: 100vh; padding: 10px;">
        <p>This area has a grey background.</p>
      </div>
      """,
      unsafe_allow_html=True,
  )

with col2:
  st.title("Hello Project !!!!")
  st.header("This is a header")
  st.subheader("This is a subheader")
  st.text("This is a text")
  st.markdown("This is a **markdown** text")
  st.success("This is a success message")
  st.info("This is an info message")
  st.warning("This is a warning message")
  st.error("This is an error message")

  exp = ZeroDivisionError("This is an exception message")
  st.exception(exp)

  st.write("This is a write message")
  st.write("This is a write message with a variable:", 548)
  st.write(range(10))

  if st.checkbox("Show/Hide Image"):
    st.image("https://docs.streamlit.io/logo.svg",
             caption="Streamlit Logo", use_container_width=True)

  some_status = st.radio("Select a status", ("Active", "Inactive", "Pending"))
  if some_status == "Active":
    st.success("The status is Active")
  elif some_status == "Inactive":
    st.warning("The status is Inactive")
  else:
    st.info("The status is Pending")

  some_level = st.slider("Select a level", 0, 100, 50)
  st.write("The selected level is:", some_level)
