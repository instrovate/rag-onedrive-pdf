import streamlit as st
import urllib.parse

st.set_page_config(page_title="RAG App with OneDrive", page_icon="🔐")

# ✅ Keep the warning as-is (works fine, not breaking)
params = st.experimental_get_query_params()

st.title("🔐 RAG App with OneDrive Integration")
st.markdown("Login with your Microsoft account to access your OneDrive files.")

st.warning("""
Please replace `st.experimental_get_query_params` with `st.query_params`.  
`st.experimental_get_query_params` will be removed after 2024-04-11.  
Refer to [docs page](https://docs.streamlit.io/) for more information.
""")

# OAuth2 settings
client_id = "1b7ab233-061b-4d2e-9c41-5cce31dcb367"
redirect_uri = "https://rag-onedrive-instrovate.streamlit.app"
response_type = "code"
scope = "Files.Read offline_access openid profile"  # ✅ FIXED: valid scopes

# URL encode all values
auth_url = (
    f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?"
    f"client_id={urllib.parse.quote(client_id)}"
    f"&response_type={urllib.parse.quote(response_type)}"
    f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
    f"&scope={urllib.parse.quote(scope)}"
)

# Sign-in button
if st.button("🔗 Sign in with Microsoft"):
    st.write("Redirecting to Microsoft login...")
    st.markdown(f"[Click here to authenticate]({auth_url})")

# Always show the auth URL below in case button fails
st.markdown(
    f"[Click here to authenticate]({auth_url}) Files.Read"
)
