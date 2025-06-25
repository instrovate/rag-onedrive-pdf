import streamlit as st
import requests
import msal
from urllib.parse import urlparse, parse_qs

# Constants for Microsoft App
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "https://rag-onedrive-instrovate.streamlit.app/"
authority_url = "https://login.microsoftonline.com/common"
scope = ["Files.Read", "User.Read"]

def build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret,
        token_cache=cache
    )

def get_auth_url():
    app = build_msal_app()
    return app.get_authorization_request_url(scopes=scope, redirect_uri=redirect_uri)

# UI
st.title("🔐 RAG App with OneDrive Integration")
st.write("Login with your Microsoft account to access your OneDrive files.")

# Step 1: Check if there's a "code" parameter in the current URL manually
query_params = st.experimental_get_query_params()
code = query_params.get("code", [None])[0]

# Step 2: If there's no code, show login button
if not code:
    if st.button("🔗 Sign in with Microsoft"):
        auth_url = get_auth_url()
        st.markdown(f"[Click here to authenticate]({auth_url})")

# Step 3: If code exists, proceed with token exchange
else:
    st.info("🔄 Logging you in...")
    app = build_msal_app()
    result = app.acquire_token_by_authorization_code(code, scopes=scope, redirect_uri=redirect_uri)

    if "access_token" in result:
        access_token = result["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        drive_response = requests.get("https://graph.microsoft.com/v1.0/me/drive/root/children", headers=headers)

        if drive_response.status_code == 200:
            files = drive_response.json().get("value", [])
            st.success("✅ Login successful! Here are your OneDrive files:")
            for file in files:
                st.write(f"📄 {file['name']}")
        else:
            st.error("❌ Failed to access OneDrive.")
    else:
        st.error("⚠️ Authentication failed. Please try again.")
