# Building and Deploying a Live Dashboard with Factory.AI

**A Step-by-Step Guide for EY Professionals**

---

## What You Will Build

A live, interactive dashboard that:

- Visualizes data from an Excel file you already maintain
- Updates automatically when your Excel file changes
- Is accessible to everyone at EY via a simple web link
- Gives you admin control over who can edit data
- Is secured with Microsoft SSO — users sign in with their real EY account

**Time required:** ~30 minutes (including SSO setup)

**Technical experience required:** None. Factory.AI builds the code for you.

---

## What You Need Before Starting

| Item | Where to Get It |
|------|----------------|
| Factory.AI CLI (Droid) | Pre-installed on your machine, or visit [factory.ai](https://factory.ai) |
| A GitHub account | [github.com](https://github.com) (free) |
| A Streamlit Community Cloud account | [streamlit.io/cloud](https://streamlit.io/cloud) (free, sign in with GitHub) |
| Your data in an Excel file (.xlsx) | Any Excel file on your machine or OneDrive |
| Azure AD app registration (for SSO) | Request from your IT team — see Step 8 and the email template below |

> **Start the Azure request early.** Step 8 requires your IT team to register an app in Azure, which may take a day or two. Send them the request now (template below) so it is ready by the time you reach Step 8. The dashboard works without SSO while you wait, but SSO is required before sharing sensitive data.

### Email Template — Send This to Your IT Team Now

> Hi,
>
> I am building an internal Streamlit dashboard and need an Azure AD (Microsoft Entra ID) app registration to enable Microsoft SSO. Could you help with the following?
>
> 1. Register a new app called "Factory AI Dashboard"
> 2. Set supported account types to "Accounts in this organizational directory only"
> 3. Add a Web redirect URI (I will provide the URL once deployed — placeholder: https://placeholder.streamlit.app)
> 4. Create a client secret
> 5. Add the Microsoft Graph "User.Read" delegated permission and grant admin consent
> 6. Send me the Application (client) ID, Directory (tenant) ID, and client secret value
>
> Thank you!

---

## Step 1: Open Factory.AI

Open your terminal (on Mac: search "Terminal" in Spotlight).

Type the following and press Enter:

```
droid
```

You should see the Factory.AI prompt appear. This is where you will give instructions in plain English.

> **Tip:** Think of Factory.AI as a colleague who writes code. You describe what you want; it builds it.

---

## Step 2: Tell Factory.AI About Your Dashboard

Type a message like the one below. Replace the details with your own:

```
Create a Streamlit dashboard using the Excel file at
"/Users/YourName/OneDrive - EY/my_data_file.xlsx"
as the data source. Make it update live when the Excel file changes.
Use EY branding (dark theme, yellow accents). Include KPI cards,
charts, and filters. Add role-based access so only admins can edit
and everyone at EY with an @ey.com email can view.
Include Microsoft SSO authentication using Azure AD so users
sign in with their real EY Microsoft account. Fall back to
manual email input if Azure secrets are not yet configured.
```

> **How to find your Excel file path:**
> 1. Open Finder
> 2. Navigate to your Excel file
> 3. Right-click the file > Hold the Option key > Click "Copy as Pathname"
> 4. Paste it into your message above

Factory.AI will:
- Read your Excel file to understand the data
- Build the full dashboard application
- Create all necessary configuration files

**Wait for it to finish.** It will tell you when it is done.

---

## Step 3: Test Your Dashboard Locally

Factory.AI will typically launch the dashboard for you. If not, type:

```
run the streamlit app
```

Your browser will open with your dashboard. Verify:

- [ ] The charts display your data correctly
- [ ] The filters work (Region, Date Range, etc.)
- [ ] The KPI numbers look reasonable

> **Want changes?** Just tell Factory.AI in plain English:
> - "Make the title bigger"
> - "Add a bar chart showing revenue by region"
> - "Change the color scheme"
> - "Add a download button for the data"

---

## Step 4: Create a GitHub Repository

Tell Factory.AI:

```
push this code to GitHub and create a new repo called "My Dashboard Name"
```

Factory.AI will:
1. Create a new repository on GitHub
2. Upload all the code
3. Give you the repository URL

**Save this URL.** You will need it in the next step.

---

## Step 5: Deploy to Streamlit Community Cloud

This is how you make the dashboard accessible to everyone at EY via a web link.

### 5a. Sign in to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Continue with GitHub"**
3. Sign in with your GitHub account
4. Authorize Streamlit to access your repositories

### 5b. Deploy Your App

1. Click **"New app"** (top right)
2. Fill in:
   - **Repository:** Select your dashboard repo (e.g., `YourName/My-Dashboard-Name`)
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Deploy"**

### 5c. Wait for Deployment

- Streamlit will install dependencies and start your app
- This takes 2-3 minutes the first time
- You will see a live URL like: `https://my-dashboard-name-xyz.streamlit.app`

> **If you see an error:** Copy the error message, go back to Factory.AI, paste it, and say "fix this error." Then tell Factory.AI to push the fix to GitHub. Streamlit Cloud will automatically redeploy.

---

## Step 6: Share With Your Team

Your dashboard is now live. You can share the Streamlit URL with your team to start testing. For non-sensitive data, this is ready to use now. For sensitive data, complete Step 8 (SSO activation) before sharing broadly.

**There are two roles:**

| Role | Who Gets It | What They Can Do |
|------|------------|-----------------|
| **Viewer** | Anyone with an @ey.com email | View charts, use filters, explore data |
| **Admin** | Only people you specifically grant access to | Everything a viewer can do, PLUS: edit data directly in the app, download CSV exports, save changes back to Excel, and add or remove other admins |

> **You are the first admin.** Your email is set as admin by default when Factory.AI builds the app. Everyone else starts as a viewer.

### How to Give Someone Admin Access

1. Open the dashboard and sign in with your @ey.com email (you must already be an admin)
2. Scroll to the bottom of the page to the **"Admin: Manage Admins"** section
3. In the **"Add admin email"** field, enter the person's full @ey.com email address
4. Click **"Add Admin"**
5. The person will have admin access immediately on their next page load

### How to Remove Admin Access

1. Scroll to the **"Admin: Manage Admins"** section
2. Use the **"Remove admin"** dropdown to select the person
3. Click **"Remove Admin"**
4. They will revert to viewer access immediately

> **Note:** You cannot remove yourself as admin. There must always be at least one admin.

### What Each Role Sees

| Feature | Viewer | Admin |
|---------|--------|-------|
| View all charts and KPIs | Yes | Yes |
| Use filters (Region, Sector, Date, etc.) | Yes | Yes |
| View raw data table | Yes (read-only, in expandable section) | Yes (editable, always visible) |
| Edit data directly in the app | No | Yes |
| Save changes back to Excel | No | Yes |
| Download data as CSV | No | Yes |
| Add/remove admins | No | Yes |

---

## Step 7: Keep Your Dashboard Updated

### If your Excel file is in the GitHub repo:

When you update your Excel file:

1. Open Factory.AI
2. Say: `copy the latest version of my Excel file into the data folder and push to GitHub`
3. Streamlit Cloud will automatically redeploy with the new data (takes ~1 minute)

### If you want to make dashboard changes:

1. Open Factory.AI
2. Describe what you want changed (e.g., "add a new chart showing quarterly trends")
3. Say: `push the changes to GitHub`
4. Streamlit Cloud picks up the changes automatically

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"ModuleNotFoundError"** on Streamlit Cloud | A Python package is missing. Tell Factory.AI: "add [package name] to requirements.txt and push to GitHub" |
| **"Excel file not found"** on Streamlit Cloud | The Excel file is not in the repo. Tell Factory.AI: "copy my Excel file into the data folder in the repo and push" |
| **Dashboard looks broken after changes** | Go back to Factory.AI, paste the error, and say "fix this." Then push to GitHub. |
| **Charts show wrong data** | Check your Excel file for blank rows, text in numeric columns, or merged cells. Clean the data and re-push. |
| **Can't access Streamlit Cloud** | Make sure you signed up at [streamlit.io/cloud](https://streamlit.io/cloud) with the same GitHub account that owns the repo. |

---

## Quick Reference

| Task | What to Tell Factory.AI |
|------|------------------------|
| Build a dashboard | "Create a Streamlit dashboard using [file path]" |
| Change a chart | "Change the bar chart to a line chart" |
| Add a filter | "Add a filter for [column name]" |
| Fix an error | Paste the error and say "fix this" |
| Push to GitHub | "Push the changes to GitHub" |
| Create a new repo | "Push this to GitHub and create a repo called [name]" |

---

## Step 8: Activate Microsoft SSO

Your dashboard already has SSO built in from Step 2. Now you activate it by pasting the three values your IT team provided (from the request you sent before starting).

> **Why this step is essential:** Without SSO, anyone can type any @ey.com email into the dashboard with no verification. SSO forces users to sign in with their real EY Microsoft account — the same login they use for Outlook and Teams. This is required before sharing any sensitive data.

> **No code changes needed.** You are only pasting configuration values. The SSO code is already in your app.

### What You Need

If your IT team has already responded to the email you sent at the start of this guide, you should have the three values (client_id, tenant_id, client_secret) ready to go. If not, follow the steps below to complete the registration yourself, or share this section with your IT contact.

### 8a. Register an App in Microsoft Entra ID (Azure AD)

1. Go to [portal.azure.com](https://portal.azure.com) and sign in with your EY account
2. In the top search bar, type **"App registrations"** and click on it
3. Click **"+ New registration"**
4. Fill in:
   - **Name:** `Factory AI Dashboard`
   - **Supported account types:** Select **"Accounts in this organizational directory only"** (this restricts login to EY employees only)
   - **Redirect URI:**
     - Platform: **Web**
     - URI: Your Streamlit Cloud URL (e.g., `https://my-dashboard-xyz.streamlit.app`)
5. Click **Register**

### 8b. Copy Your Two IDs

After registration, you will land on the app's **Overview** page. Copy these two values and save them somewhere safe:

| Field on Screen | What to Save It As |
|----------------|-------------------|
| Application (client) ID | `client_id` |
| Directory (tenant) ID | `tenant_id` |

### 8c. Create a Client Secret

1. In the left sidebar of your app registration, click **"Certificates & secrets"**
2. Click **"+ New client secret"**
3. Enter a description (e.g., `streamlit-dashboard`)
4. Choose an expiry period (e.g., 12 months)
5. Click **Add**
6. **Immediately copy the value in the "Value" column** — this is your `client_secret`

> **Important:** The secret value is only shown once. If you navigate away without copying it, you will need to create a new one.

### 8d. Add API Permissions

1. In the left sidebar, click **"API permissions"**
2. Click **"+ Add a permission"**
3. Select **"Microsoft Graph"**
4. Select **"Delegated permissions"**
5. Search for **"User.Read"** and check the box
6. Click **"Add permissions"**
7. Click the **"Grant admin consent for EY"** button (this requires admin privileges)

> **If you do not see the "Grant admin consent" button:** You need someone with a higher admin role to click it for you. Send them a link to this app registration page.

### 8e. Add Your Three Values to Streamlit Cloud

This is the final step. No code changes are needed — you are just entering configuration.

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Find your app and click the three-dot menu (⋯) > **Settings**
3. Click the **"Secrets"** tab
4. Paste the following, replacing the placeholder values with your actual values:

```toml
[azure]
client_id = "paste-your-application-client-id-here"
client_secret = "paste-your-client-secret-value-here"
tenant_id = "paste-your-directory-tenant-id-here"
redirect_uri = "https://your-app-name.streamlit.app"
```

5. Click **Save**
6. Click **"Reboot app"** (or go to the Manage app menu and reboot)

### 8f. Verify It Works

1. Open your dashboard URL in a private/incognito browser window
2. You should see a **"Sign in with Microsoft"** button instead of a text field
3. Click it — you will be redirected to Microsoft's login page
4. Sign in with your EY account
5. You should be returned to the dashboard, now showing your name and email

> **If you see an error after signing in:** The most common cause is the redirect URI not matching exactly. Go back to your app registration in Azure Portal > **Authentication** and verify the redirect URI matches your Streamlit Cloud URL exactly (including https:// and no trailing slash).

### What Changes for Users

| Before SSO | After SSO |
|-----------|-----------|
| Users type their email into a text box | Users click "Sign in with Microsoft" |
| No verification — anyone can type any email | Microsoft verifies their identity |
| Only suitable for non-sensitive data | Suitable for sensitive and confidential data |
| No audit trail | Microsoft logs all sign-ins |

### Reminder

If your IT team has not yet responded to the email you sent at the beginning of this guide, follow up and provide them with your Streamlit Cloud URL (from Step 5) as the redirect URI. You can also share the `AZURE_SSO_SETUP.md` file from your GitHub repository for full technical details.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"ModuleNotFoundError"** on Streamlit Cloud | A Python package is missing. Tell Factory.AI: "add [package name] to requirements.txt and push to GitHub" |
| **"Excel file not found"** on Streamlit Cloud | The Excel file is not in the repo. Tell Factory.AI: "copy my Excel file into the data folder in the repo and push" |
| **Dashboard looks broken after changes** | Go back to Factory.AI, paste the error, and say "fix this." Then push to GitHub. |
| **Charts show wrong data** | Check your Excel file for blank rows, text in numeric columns, or merged cells. Clean the data and re-push. |
| **Can't access Streamlit Cloud** | Make sure you signed up at [streamlit.io/cloud](https://streamlit.io/cloud) with the same GitHub account that owns the repo. |
| **SSO: "AADSTS50011" redirect URI error** | The redirect URI in Azure does not match your Streamlit URL exactly. Fix it in Azure Portal > App registration > Authentication. |
| **SSO: "Authentication failed"** | The client secret may have expired. Create a new one in Azure Portal and update Streamlit Cloud secrets. |
| **SSO: "Grant admin consent" button missing** | You need a Global Administrator or Privileged Role Administrator to grant consent. Ask your IT admin. |

---

## Quick Reference

| Task | What to Tell Factory.AI |
|------|------------------------|
| Build a dashboard | "Create a Streamlit dashboard using [file path]" |
| Change a chart | "Change the bar chart to a line chart" |
| Add a filter | "Add a filter for [column name]" |
| Fix an error | Paste the error and say "fix this" |
| Push to GitHub | "Push the changes to GitHub" |
| Create a new repo | "Push this to GitHub and create a repo called [name]" |

---

*Built with [Factory.AI](https://factory.ai) — the AI software engineering platform.*
