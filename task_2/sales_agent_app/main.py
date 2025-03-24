import streamlit as st
import config
from sales_agent import ai_sales_agent
from product_catalog import get_recommendation, detect_categories

# Streamlit UI
st.set_page_config(page_title="AI Sales Agent", page_icon="🛒")
st.title("🛍️ AI Sales Agent")

st.write("Ask me anything about our products, recommendations, purchases, or support!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_button_click" not in st.session_state:
    st.session_state.last_button_click = None

if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

if "cart" not in st.session_state:
    st.session_state.cart = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Category buttons - outside of chat messages
if "temp_categories" in st.session_state and st.session_state.temp_categories:
    st.write("**Product Categories:**")
    num_cols = min(3, len(st.session_state.temp_categories))
    cols = st.columns(num_cols)

    for i, category in enumerate(st.session_state.temp_categories):
        if cols[i % num_cols].button(f"View {category.title()} Products", key=f"{category}_{len(st.session_state.messages)}"):
            st.session_state.selected_category = category
            st.session_state.last_button_click = category
            st.session_state.temp_categories = []
            st.rerun()

# Handle category selection from button click
if st.session_state.selected_category:
    category = st.session_state.selected_category
    products = get_recommendation(category)
    product_list = "\n".join(
        [f"- {product['name']} (${product['price']})" for product in products])
    response = f"Here are our top {category} products:\n{product_list}\n\nCan I help you with more details on any of these products?"

    # Add response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

    # Reset the selection
    st.session_state.selected_category = None
    st.rerun()

# Reset chat button
if st.button("Reset Chat"):
    st.session_state.messages = []
    st.session_state.cart = []
    st.rerun()

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Detect categories in user input
    detected_categories = detect_categories(user_input)

    # Store detected categories temporarily
    st.session_state.temp_categories = detected_categories

    # Maintain conversation history for AI
    chat_history = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    # Get AI response if no button was clicked
    if not st.session_state.last_button_click:
        with st.spinner("AI is typing..."):
            response = ai_sales_agent(user_input, chat_history)

        # Add response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})

    # Reset button click tracker
    st.session_state.last_button_click = None
    st.rerun()
