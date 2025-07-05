import streamlit as st
import gspread

gc = gspread.service_account('credentials.json')
sheet = gc.open("YouTube_Videos").sheet1

st.title("YouTube Upload Status")
st.write(sheet.get_all_records())
