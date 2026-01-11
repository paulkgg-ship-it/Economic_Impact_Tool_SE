import streamlit as st

st.title("Test App")
st.write("If you see this, Streamlit Cloud is working!")

try:
    from PIL import Image
    st.success("✓ PIL/Pillow working")
except:
    st.error("✗ PIL/Pillow not working")

try:
    import requests
    st.success("✓ requests working")
except:
    st.error("✗ requests not working")

try:
    from data_processor import data_processor
    st.success("✓ data_processor import working")
except Exception as e:
    st.error(f"✗ data_processor failed: {e}")

try:
    from stack_client import StackAIClient
    st.success("✓ stack_client import working")
except Exception as e:
    st.error(f"✗ stack_client failed: {e}")
