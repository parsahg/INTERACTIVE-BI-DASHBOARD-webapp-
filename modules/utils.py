import streamlit as st
from bidi.algorithm import get_display
import arabic_reshaper

def _(text):
    return get_display(arabic_reshaper.reshape(str(text)))

def add_custom_css(path):
    with open(path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def translate_country_name(name):
    mapping = {
        "آذربایجان": "Azerbaijan", "آلمان": "Germany", "آمریکا": "United States",
        "استرالیا": "Australia", "افغانستان": "Afghanistan", "امارات": "United Arab Emirates",
        "انگلستان": "United Kingdom", "بحرین": "Bahrain", "عراق": "Iraq", "قطر": "Qatar"
    }
    return mapping.get(name, name)
