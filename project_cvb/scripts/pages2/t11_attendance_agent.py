import datetime
import random
import time

import altair as alt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from dateutil.relativedelta import relativedelta
import google.generativeai as genai

from project_cvb.app.models.attendance import Attendance
from project_cvb.config.mongodb_config import initialize_mongodb
from project_cvb.config.settings import Settings  

initialize_mongodb()
settings = Settings()

st.set_page_config(page_title="Chat Agent", layout="wide")
st.title("Chat Agent")

genai.configure(api_key=settings.gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

if "messages" not in st.session_state:
  st.session_state.messages = []

for msg in st.session_state.messages:
  with st.chat_message(msg["role"]):
    st.write(msg["content"])


if prompt := st.chat_input("Ask something"):
  # Save user message
  st.session_state.messages.append({"role": "user", "content": prompt})

  # Display user message
  with st.chat_message("user"):
    st.write(prompt)

  # Build Gemini prompt
  final_prompt = prompt

  chat = model.start_chat(enable_automatic_function_calling=True)
  response = chat.send_message(prompt)
  answer = response.text.strip()

  # Save assistant message
  st.session_state.messages.append({"role": "assistant", "content": response.text})

  # Display assistant message
  with st.chat_message("assistant"):
    st.write(response.text)
