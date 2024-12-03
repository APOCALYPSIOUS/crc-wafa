import streamlit as st
from main import perform_query_and_get_response


def main():
    # Set the page configuration
    st.set_page_config(page_title="CRC Demo")

    # App title
    st.title("CRC Demo")
    st.write("Welcome to the CRC Demo chat app! Ask your questions below.")

    # Initialize session state to store messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    # User input section
    if user_input := st.chat_input("Type your message"):
        # Add the user input to the messages list
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display the user input in the chat
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get the last 10 conversations excluding the latest user input
        conversation_history = st.session_state.messages[:-1][-10:]

        # Process the response and display it
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:

                    # Pass the user input and the conversation history
                    response = perform_query_and_get_response(user_input)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
