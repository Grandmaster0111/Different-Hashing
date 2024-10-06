import streamlit as st

# Define a sidebar for navigation
st.title("Choose Hashing method")


if st.button("Linear Hashing"):
    st.switch_page('pages/linearhash.py')
elif st.button("Extendible Hashing"):
    st.switch_page('pages/Extenhash.py')
elif st.button("Bitmap Hashing"):
    st.switch_page('pages/bitmaphash.py')

