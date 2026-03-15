# Azure AD SSO Setup for Factory.AI Dashboard

## Step 1: Register an App in Azure AD (Microsoft Entra ID)

1. Go to [Azure Portal](https://portal.azure.com) > **Microsoft Entra ID** > **App registrations** > **New registration**
2. Name: `Factory AI Dashboard`
3. Supported account types: **Accounts in this organizational directory only** (EY tenant)
4. Redirect URI:
   - Platform: **Web**
   - URI: `https://factory-dashboard-demo-ey.streamlit.app` (your Streamlit Cloud URL)
   - For local dev, also add: `http://localhost:8501`
5. Click **Register**

## Step 2: Get Your Credentials

From the app registration page:
- **Application (client) ID** → this is your `client_id`
- **Directory (tenant) ID** → this is your `tenant_id`

## Step 3: Create a Client Secret

1. Go to **Certificates & secrets** > **New client secret**
2. Description: `streamlit-dashboard`
3. Expiry: choose your preference
4. Copy the **Value** immediately (shown only once) → this is your `client_secret`

## Step 4: Configure API Permissions

1. Go to **API permissions** > **Add a permission**
2. Select **Microsoft Graph** > **Delegated permissions**
3. Add: `User.Read`
4. Click **Grant admin consent for EY**

## Step 5: Add Secrets to Streamlit Cloud

1. Go to your app on [Streamlit Cloud](https://share.streamlit.io)
2. Click **Settings** > **Secrets**
3. Paste:

```toml
[azure]
client_id = "YOUR_APPLICATION_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
tenant_id = "YOUR_EY_TENANT_ID"
redirect_uri = "https://factory-dashboard-demo-ey.streamlit.app"
```

4. Save and reboot the app.

## How It Works

- Users see a **"Sign in with Microsoft"** button
- They authenticate with their EY Microsoft account
- The app verifies their email ends with `@ey.com`
- If Azure secrets are not configured, the app falls back to manual email input (no SSO)
