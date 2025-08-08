import streamlit as st
import requests

st.set_page_config(page_title="Mcp App")
st.title("Mcp App")



if st.button("Run Google Search for 'streamlit'"):
    try:
        # Replace with your MCP server's actual URL and endpoint
        response = requests.post("http://localhost:8000/tools/google_search_streamlit/execute")
        result = response.json()
        if result["status"] == "success":
            st.success(f"Search completed successfully! Page title: {result['page_title']}")
        else:
            st.error(f"Error: {result['message']}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
