import streamlit as st
import msal
import requests

st.set_page_config(page_title="RAG with SharePoint/OneDrive", layout="centered")

# Azure AD app credentials
client_id = "your_actual_client_id_here"
client_secret = "your_actual_client_secret_here"
tenant_id = "your_actual_tenant_id_here"
redirect_uri = "https://rag-onedrive-instrovate.streamlit.app"

# MSAL setup
authority = f"https://login.microsoftonline.com/{tenant_id}"
scope = ["Files.Read.All", "User.Read"]

def build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
        token_cache=cache
    )

def get_auth_url():
    app = build_msal_app()
    auth_url = app.get_authorization_request_url(scope, redirect_uri=redirect_uri)
    return auth_url

st.title("🔐 RAG App with OneDrive Integration")
st.write("Login with your Microsoft account to access your OneDrive files.")

code = st.query_params().get("code", [None])[0]

if not code:
    if st.button("🔗 Sign in with Microsoft"):
        st.markdown(f"[Click here to authenticate]({get_auth_url()})")
else:
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
                st.markdown(f"- 📄 **{file['name']}**")
        else:
            st.error("Failed to access OneDrive files.")
    else:
        st.error("Login failed. Please try again.")
