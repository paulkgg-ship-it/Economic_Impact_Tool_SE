import streamlit as st

st.title("✅ Streamlit Works!")
st.write("If you see this, the basic deployment is working.")

# Test imports one by one
st.write("---")
st.write("Testing imports...")

try:
    import os
    st.success("✓ os")
except Exception as e:
    st.error(f"✗ os: {e}")

try:
    import json
    st.success("✓ json")
except Exception as e:
    st.error(f"✗ json: {e}")

try:
    import pandas
    st.success("✓ pandas")
except Exception as e:
    st.error(f"✗ pandas: {e}")

try:
    from PIL import Image
    st.success("✓ PIL/Pillow")
except Exception as e:
    st.error(f"✗ PIL: {e}")

try:
    import requests
    st.success("✓ requests")
except Exception as e:
    st.error(f"✗ requests: {e}")

try:
    import markdown
    st.success("✓ markdown")
except Exception as e:
    st.error(f"✗ markdown: {e}")

try:
    import weasyprint
    st.success("✓ weasyprint")
except Exception as e:
    st.error(f"✗ weasyprint: {e}")

st.write("---")
st.write("Testing local imports...")

try:
    from stack_client import StackAIClient
    st.success("✓ stack_client")
except Exception as e:
    st.error(f"✗ stack_client: {e}")

try:
    from data_processor import data_processor
    st.success("✓ data_processor")
except Exception as e:
    st.error(f"✗ data_processor: {e}")

try:
    from pdf_generator import generate_pdf_from_markdown
    st.success("✓ pdf_generator")
except Exception as e:
    st.error(f"✗ pdf_generator: {e}")

st.write("---")
st.write("Testing secrets...")

try:
    api_key = st.secrets.get("STACK_AI_API_KEY", "NOT_FOUND")
    flow_id = st.secrets.get("STACK_AI_FLOW_ID", "NOT_FOUND")
    
    if api_key != "NOT_FOUND":
        st.success(f"✓ STACK_AI_API_KEY found (starts with: {api_key[:10]}...)")
    else:
        st.error("✗ STACK_AI_API_KEY not found")
    
    if flow_id != "NOT_FOUND":
        st.success(f"✓ STACK_AI_FLOW_ID found (starts with: {flow_id[:10]}...)")
    else:
        st.error("✗ STACK_AI_FLOW_ID not found")
        
except Exception as e:
    st.error(f"✗ Secrets error: {e}")

st.balloons()
