import json
import requests
import streamlit as st

sign_in_url = "http://127.0.0.1:8000/api/v1/auth/login"


def signin_form() -> None:
    st.set_page_config(page_title="Sign In", page_icon="🗝️")
    st.image("./images/bot.PNG", width=500)
    st.header("Please fill out the form to sign in")
    st.markdown("# Sign In")
    st.sidebar.header("Sign In")

    container = st.container(border=True)
    email = container.text_input("Email ")
    password = container.text_input("Password ")
    input = {"email": email, "password": password}

    if st.button("Sign In"):
        try:
            response = requests.post(url=sign_in_url, data=json.dumps(input))
        except ConnectionRefusedError:
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("No connection with server.")

        #print(response.status_code)
        if response.status_code == 409:  ## already exists
            with st.chat_message(name="assistant"):
                st.write("User not found")
        elif response.status_code == 422:  ## unprocessable entity
            with st.chat_message(name="assistant", avatar="./images/logo.PNG"):
                st.write("Incorrect form.")
        else:
            with st.chat_message(name="assistant"):
                st.write("User was signed in")

if __name__ == "__main__":
    signin_form()


