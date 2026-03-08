# ⚾ Little League Rules Assistant

A chatbot that answers questions about your little league rules, powered by Claude AI.

---

## Deployment Guide (Vercel)

### Step 1: Get a Claude API Key
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in and click **API Keys** in the left sidebar
3. Click **Create Key**, give it a name, and copy it somewhere safe
4. Go to **Billing** and add a credit card (costs will be under $1/month for typical use)

### Step 2: Put this project on GitHub
1. Create a free account at [github.com](https://github.com)
2. Click the **+** icon → **New repository**, name it `little-league-bot`, click **Create**
3. Upload ALL these files to the repo — including your **`rules.pdf`** renamed exactly as `rules.pdf`

   Your repo should contain:
   ```
   app.py
   vercel.json
   requirements.txt
   rules.pdf          ← your league rulebook PDF goes here
   templates/
       index.html
   ```

### Step 3: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com) and sign up with your GitHub account
2. Click **Add New → Project**
3. Find and select your `little-league-bot` repository, click **Import**
4. Before clicking Deploy, click **Environment Variables** and add:
   - **Key:** `ANTHROPIC_API_KEY`
   - **Value:** *(paste your API key from Step 1)*
5. Click **Deploy** — Vercel will give you a public URL like `https://little-league-bot.vercel.app`

### Step 4: Share the link!
Send the URL to your coaches and parents. That's it — they can start asking questions immediately.

---

## Updating the Rules
If your rulebook changes next season:
1. Replace `rules.pdf` in your GitHub repo with the new file
2. Vercel will automatically redeploy within a minute or two

## Estimated Monthly Cost
With ~15 users asking ~10 questions each: **approx. $0.50–$1.00/month**

## Troubleshooting
- **"The rules PDF hasn't been added"** → Make sure `rules.pdf` is in the root of your GitHub repo
- **"Invalid API key"** → Double-check the `ANTHROPIC_API_KEY` environment variable in Vercel settings
- **Bot gives wrong answers** → Make sure your PDF has selectable text (not a scanned image). Try opening it and copying text to verify.
