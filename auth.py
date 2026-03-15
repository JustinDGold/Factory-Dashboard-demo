import streamlit as st
import msal
from urllib.parse import urlencode

AUTHORITY = "https://login.microsoftonline.com/{tenant_id}"
SCOPES = ["User.Read"]


def _get_azure_cfg():
    """Read Azure AD settings from Streamlit secrets."""
    try:
        return {
            "client_id": st.secrets["azure"]["client_id"],
            "client_secret": st.secrets["azure"]["client_secret"],
            "tenant_id": st.secrets["azure"]["tenant_id"],
            "redirect_uri": st.secrets["azure"]["redirect_uri"],
        }
    except (KeyError, FileNotFoundError):
        return None


def _build_msal_app(azure_cfg):
    return msal.ConfidentialClientApplication(
        azure_cfg["client_id"],
        authority=AUTHORITY.format(tenant_id=azure_cfg["tenant_id"]),
        client_credential=azure_cfg["client_secret"],
    )


def get_login_url(azure_cfg):
    app = _build_msal_app(azure_cfg)
    flow = app.initiate_auth_code_flow(SCOPES, redirect_uri=azure_cfg["redirect_uri"])
    st.session_state["auth_flow"] = flow
    return flow["auth_uri"]


def handle_callback(azure_cfg):
    """Exchange the authorization code for tokens and return user info."""
    params = st.query_params.to_dict()
    if "code" not in params:
        return None

    flow = st.session_state.get("auth_flow")
    if not flow:
        return None

    app = _build_msal_app(azure_cfg)
    result = app.acquire_token_by_auth_code_flow(flow, params)

    if "error" in result:
        st.error(f"Authentication failed: {result.get('error_description', result['error'])}")
        return None

    claims = result.get("id_token_claims", {})
    return {
        "email": claims.get("preferred_username", "").lower(),
        "name": claims.get("name", ""),
    }


def require_auth():
    """Main auth gate. Returns the authenticated user's email or stops the app.
    Falls back to manual email input if Azure secrets are not configured."""
    azure_cfg = _get_azure_cfg()

    if azure_cfg is None:
        return _fallback_email_auth()

    if "auth_user" in st.session_state and st.session_state["auth_user"]:
        user = st.session_state["auth_user"]
        email = user["email"]
        if not email.endswith("@ey.com"):
            st.error("Access is restricted to EY employees.")
            if st.button("Sign out"):
                _sign_out()
            st.stop()
        return email

    user_info = handle_callback(azure_cfg)
    if user_info:
        st.session_state["auth_user"] = user_info
        st.session_state["user_email"] = user_info["email"]
        st.query_params.clear()
        st.rerun()

    login_url = get_login_url(azure_cfg)
    st.markdown("### Sign in to continue")
    st.markdown(
        f'<a href="{login_url}" target="_self" style="display:inline-block;'
        f"background-color:#FFE600;color:#2E2E38;padding:12px 24px;"
        f'border-radius:6px;font-weight:bold;text-decoration:none;font-size:1rem;">'
        f"Sign in with Microsoft</a>",
        unsafe_allow_html=True,
    )
    st.caption("You will be redirected to your EY Microsoft login.")
    st.stop()


def _fallback_email_auth():
    """Used when Azure AD secrets are not configured (local dev)."""
    email = st.session_state.get("user_email", "").strip()
    if not email:
        st.warning("Please enter your EY email in the sidebar to access the dashboard.")
        st.stop()
    if not email.endswith("@ey.com"):
        st.error("Access is restricted to EY employees. Please enter a valid @ey.com email.")
        st.stop()
    return email


def show_user_info():
    """Display auth status in sidebar."""
    azure_cfg = _get_azure_cfg()
    if azure_cfg and "auth_user" in st.session_state:
        user = st.session_state["auth_user"]
        st.markdown(f"**{user['name']}**")
        st.caption(user["email"])
        if st.button("Sign out", key="signout_btn"):
            _sign_out()
        return True
    return False


def _sign_out():
    for key in ["auth_user", "auth_flow", "user_email"]:
        st.session_state.pop(key, None)
    st.rerun()
