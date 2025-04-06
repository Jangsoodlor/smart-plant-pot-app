import streamlit as st

if __name__ == "__main__":
    welcome = ""
    with open("README.md", "r") as file:
        for line in file:
            welcome += line

    st.markdown(welcome)
