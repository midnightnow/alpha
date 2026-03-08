# 🆘 How to Push to GitHub

If you are struggling to get the code to GitHub, follow these 3 steps exactly.

### Step 1: Open Terminal
Look for "Terminal" in your editor menu (usually `Ctrl + ~` or `Cmd + J`).

### Step 2: Run the Sync Wizard
Copy the line below, paste it into the terminal, and hit Enter:

```bash
sh git_sync.sh
```

### Step 3: Authenticate
1. The script will ask for your **Repo URL**. Paste: `https://github.com/midnightnow/mathman-flatland.git` (or whatever you named it).
2. If it asks for a **Username**, type your GitHub username.
3. If it asks for a **Password**, you likely need a **Personal Access Token** if 2FA is on, or your normal password if not.

---

### Manual Fallback
If the script fails, run these 3 commands one by one:

1. `git add .`
2. `git commit -m "Manual upload"`
3. `git push origin main`
