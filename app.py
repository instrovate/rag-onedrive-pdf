import streamlit as st
import requests
import os

# ---------------------------------------------
# App Title & Instructions
# ---------------------------------------------
st.set_page_config(page_title="RAG App with OneDrive", page_icon="🔐")
st.title("🔐 RAG App with OneDrive Integration")
st.write("Login with your Microsoft account to access your OneDrive files.")

# ---------------------------------------------
# OAuth App Registration (replace with yours)
# ---------------------------------------------
CLIENT_ID = st.secrets["client_id"]
CLIENT_SECRET = st.secrets["client_secret"]
REDIRECT_URI = st.secrets["redirect_uri"]
AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
SCOPES = "offline_access Files.Read"

# ---------------------------------------------
# Get Authorization Code from URL
# ---------------------------------------------
query_params = st.experimental_get_query_params()
code = query_params.get("code", [None])[0]

if not code:
    auth_link = (
        f"{AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_mode=query"
        f"&scope={SCOPES}"
    )
    if st.button("🔗 Sign in with Microsoft"):
        st.markdown(f"[Click here to authenticate]({auth_link})", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------
# Exchange Code for Access Token
# ---------------------------------------------
st.info("Authorizing with Microsoft...")
try:
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    }
    response = requests.post(TOKEN_URL, data=token_data)
    response.raise_for_status()
    token_json = response.json()
    access_token = token_json["access_token"]
    st.success("✅ Login successful! You can now access OneDrive files.")
except Exception as e:
    st.error("❌ Token exchange failed.")
    st.exception(e)
    st.stop()

# ---------------------------------------------
# Optional: Fetch & List OneDrive Files
# ---------------------------------------------
headers = {"Authorization": f"Bearer {access_token}"}
files_url = "https://graph.microsoft.com/v1.0/me/drive/root/children"

try:
    response = requests.get(files_url, headers=headers)
    response.raise_for_status()
    files = response.json().get("value", [])
    file_names = [file["name"] for file in files]
    selected_file = st.selectbox("📁 Select a file from your OneDrive:", file_names)
    st.success(f"✅ Selected: {selected_file}")
except Exception as e:
    st.error("❌ Failed to fetch OneDrive files.")
    st.exception(e)
