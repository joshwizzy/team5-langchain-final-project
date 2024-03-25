from dotenv import load_dotenv, find_dotenv
import streamlit as st


def launch_app():
    print('launching app')
    st.title('Github Issues PM Assistant')


if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    launch_app()
