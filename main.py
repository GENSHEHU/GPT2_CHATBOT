import streamlit as st
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Page configuration
st.set_page_config(page_title="GPT-2 CHATBOT")

# Loading model and tokenizer
@st.cache_resource
def load_model():
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    
    # Add padding token if it is not existing
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    return model, tokenizer

# Response generation function
def generate_response(user_input, model, tokenizer, max_length=150):
    # Preparing the input
    input_text = user_input + tokenizer.eos_token
    
    # Encoding input
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    
    # Generating response
    outputs = model.generate(
        inputs, 
        max_length=max_length, 
        num_return_sequences=1, 
        no_repeat_ngram_size=2,
        temperature=0.5,
        top_k=50,
        top_p=0.95,
        do_sample=True
    )
    
    # Decoding and cleaning response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Removing the original input from the response
    response = response[len(input_text):].strip()
    
    return response

# Main Streamlit app
def main():
    # Load model
    model, tokenizer = load_model()
    
    # App title and description
    st.title("GPT-2 CHATBOT")
    st.markdown("Chat with GPT-2 CHATBOT!")
    
    # Initializing chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat input
    user_input = st.chat_input("Enter your message:")
    
    # Processing user input
    if user_input:
        # Adding user message to chat history
        st.session_state.chat_history.append({
            "role": "user", 
            "content": user_input
        })
        
        # Generating AI response
        try:
            ai_response = generate_response(user_input, model, tokenizer)
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": ai_response
            })
        except Exception as e:
            st.error(f"Error generating response: {e}")
    
    # Displaying chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            with st.chat_message("user"):
                st.write(message['content'])
        else:
            with st.chat_message("assistant"):
                st.write(message['content'])
    
    # Additional information
    st.sidebar.header("About")
    st.sidebar.info(
        "This chatbot uses GPT-2 to generate responses. "
        "Responses are generated in real-time using pre-trained weights."
    )


if __name__ == "__main__":
    main()