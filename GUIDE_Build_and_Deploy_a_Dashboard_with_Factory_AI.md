# Building and Deploying a Live Dashboard with Factory.AI

**A Step-by-Step Guide for EY Professionals**

---

## What You Will Build

A live, interactive dashboard that:

- Visualizes data from an Excel file you already maintain
- Updates automatically when your Excel file changes
- Is accessible to everyone at EY via a simple web link
- Gives you admin control over who can edit data

**Time required:** ~20 minutes

**Technical experience required:** None. Factory.AI builds the code for you.

---

## What You Need Before Starting

| Item | Where to Get It |
|------|----------------|
| Factory.AI CLI (Droid) | Pre-installed on your machine, or visit [factory.ai](https://factory.ai) |
| A GitHub account | [github.com](https://github.com) (free) |
| A Streamlit Community Cloud account | [streamlit.io/cloud](https://streamlit.io/cloud) (free, sign in with GitHub) |
| Your data in an Excel file (.xlsx) | Any Excel file on your machine or OneDrive |

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

Your dashboard is now live. Share the Streamlit URL with anyone at EY.

**Access works like this:**

| Who | What They Can Do |
|-----|-----------------|
| Anyone with an @ey.com email | View the dashboard, use filters, explore data |
| Admins (emails you configure) | Edit data directly, download exports, manage other admins |

### To add an admin:

1. Open the dashboard and sign in with your @ey.com email
2. Scroll to the bottom: **"Admin: Manage Admins"**
3. Enter the new admin's @ey.com email
4. Click **"Add Admin"**

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

## Optional: Add Microsoft SSO (Real Login Validation)

If you want users to sign in with their actual EY Microsoft account instead of typing their email, you will need help from your IT team. See the `AZURE_SSO_SETUP.md` file in your repository for detailed instructions to share with them.

> **Note:** The dashboard works perfectly without SSO. This is an optional security enhancement.

---

*Built with [Factory.AI](https://factory.ai) — the AI software engineering platform.*
