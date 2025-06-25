import streamlit as st
import requests
import msal
import os

# Load secrets from Streamlit Cloud settings
client_id = st.secrets["client_id"]
client_secret = st.secrets["client_secret"]
tenant_id = st.secrets["tenant_id"]
redirect_uri = st.secrets["redirect_uri"]

# Microsoft scopes
scope = ["Files.Read"]

def build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret,
        token_cache=cache,
    )

def get_auth_url():
    app = build_msal_app()
    auth_url = app.get_authorization_request_url(scope, redirect_uri=redirect_uri)
    return auth_url

# --- Streamlit App UI ---
st.set_page_config(page_title="🔐 RAG App with OneDrive", layout="centered")
st.title("🔐 RAG App with OneDrive Integration")
st.write("Login with your Microsoft account to access your OneDrive files.")

# --- Extract auth code from URL ---
params = st.experimental_get_query_params()
code = st.query_params.get("code", [None])[0]


if not code:
    if st.button("🔗 Sign in with Microsoft"):
        st.markdown(f"[Click here to authenticate]({get_auth_url()})")
else:
    # Exchange code for access token
    app = build_msal_app()
    result = app.acquire_token_by_authorization_code(code, scopes=scope, redirect_uri=redirect_uri)

    if "access_token" in result:
        access_token = result["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # Get OneDrive root files
        drive_response = requests.get("https://graph.microsoft.com/v1.0/me/drive/root/children", headers=headers)

        if drive_response.status_code == 200:
            files = drive_response.json().get("value", [])
            st.success("✅ Login successful! Here are your OneDrive files:")
            for file in files:
                st.write(f"📄 {file['name']}")
        else:
            st.error(f"❌ Failed to fetch files: {drive_response.status_code}")
    else:
        st.error("❌ Failed to authenticate. Please try again.")
