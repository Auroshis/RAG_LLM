import streamlit as st
from ChatBot import rag

# Initialize the ChatPDF object (replace 'your_pdf.pdf' with your actual file path)
chatpdf = ChatBot()
chatpdf.ingest("your_pdf.pdf")

def main():
  """ Creates a chat interface for interacting with the ChatPDF object """
  
  # Chat history
  chat_history = []

  # Title and description
  st.title("Chat with your PDF")
  st.write("Ask questions about the content of the uploaded PDF.")

  # Text input for user query
  user_input = st.text_input("You: ", key="user_input")

  # Process user input on button click or Enter key press
  if user_input or st.button("Ask"):
    # Get response from ChatPDF
    response = chatpdf.ask(user_input)
    
    # Update chat history
    chat_history.append({"user": user_input, "bot": response})
    st.session_state["chat_history"] = chat_history

    # Clear user input for next question
    st.text_input("", value="", key="user_input")  # Clear input field

  # Display chat history
  for message in st.session_state["chat_history"]:
    st.write(f"{message['user']}: {message['bot']}")

if __name__ == "__main__":
  main()
