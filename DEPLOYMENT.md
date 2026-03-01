# Deployment Guide: portfolio.enhaq.online

Complete guide from subdomain creation to live site.

---

## Step 1: Create Subdomain on Hostinger

### Via Hostinger Control Panel

1. **Login**
   - Go to: https://hpanel.hostinger.com
   - Sign in

2. **Find Your Hosting Plan**
   - Look for the plan hosting `enhaq.online`
   - Click to open control panel

3. **Navigate to Subdomains**
   - Look for "Subdomains" section (usually under "Advanced" or "Domains")
   - Click "Create Subdomain" or "+ Add Subdomain"

4. **Create Subdomain**
   - **Subdomain name:** `portfolio`
   - **Domain:** `enhaq.online`
   - **Document root:** Let Hostinger auto-generate (usually `/public_html/portfolio`)
   - Click "Create"

5. **Note the Full Path**
   - After creation, Hostinger shows the full server path
   - Example: `/home/u123456/domains/enhaq.online/public_html/portfolio`
   - **Copy this path** — you'll need it for deployment script

6. **Wait for DNS Propagation**
   - Usually takes 15-30 minutes
   - Can take up to 24 hours in rare cases

---

## Step 2: Get FTP Credentials

### Find Existing FTP Account

1. In Hostinger panel, go to **"FTP Accounts"**
2. You should see an existing account (created with hosting)
3. Note:
   - **Username:** (example: `u123456`)
   - **Password:** If you don't know it, reset it
   - **FTP Server:** Usually `ftp.enhaq.online` or IP address shown
   - **Port:** 21 (FTP) or 22 (SFTP)

### Or Create New FTP Account (Optional)

1. Click "Create FTP Account"
2. Fill in:
   - Username: `portfolio-deploy` (or any name)
   - Password: (strong password)
   - Directory: `/public_html/portfolio` (your subdomain path)
3. Save credentials securely

---

## Step 3: Manual Deployment (First Time)

Use FileZilla or any FTP client for first deployment.

### Using FileZilla

1. **Download FileZilla**
   - https://filezilla-project.org
   - Install and open

2. **Connect to Hostinger**
   - **Host:** `ftp.enhaq.online` (or IP from Hostinger)
   - **Username:** Your FTP username
   - **Password:** Your FTP password
   - **Port:** 21
   - Click "Quickconnect"

3. **Navigate Remote Side**
   - In right panel (Remote site), navigate to your subdomain folder
   - Should be: `/public_html/portfolio/` or similar
   - If there's a default `index.html`, delete it

4. **Navigate Local Side**
   - In left panel (Local site), navigate to:
     ```
     ~/.openclaw/workspace/portfolio-tracker/public/
     ```
   - You should see:
     - `index.html`
     - `options.html`

5. **Upload Files**
   - Select both HTML files
   - Drag from left to right (or right-click → Upload)
   - Wait for transfer to complete

6. **Test**
   - Open browser: http://portfolio.enhaq.online
   - Should see your portfolio tracker!

### Troubleshooting Manual Deploy

**"Connection refused"**
- Check FTP hostname (try IP address instead of domain)
- Verify port (21 for FTP, 22 for SFTP)
- Check if FTP is enabled in Hostinger plan

**"Permission denied"**
- FTP user doesn't have write access to that folder
- Use main account or create new FTP user with correct permissions

**"Directory not found"**
- Double-check subdomain document root path
- Some hosts use `/domains/` instead of `/public_html/`

---

## Step 4: Automated Deployment (After First Success)

Once manual deployment works, automate it.

### Configure Deploy Script

1. **Edit deployment script:**
   ```bash
   nano ~/.openclaw/workspace/portfolio-tracker/scripts/deploy.sh
   ```

2. **Fill in your credentials:**
   ```bash
   FTP_HOST="ftp.enhaq.online"          # From Step 2
   FTP_USER="u123456"                   # Your FTP username
   FTP_PASS="your_actual_password"      # Your FTP password
   REMOTE_DIR="/public_html/portfolio"  # From Step 1
   ```

3. **Save and exit** (Ctrl+X, Y, Enter in nano)

### Test Automated Deploy

```bash
cd ~/.openclaw/workspace/portfolio-tracker
./scripts/deploy.sh
```

Should output:
```
🚀 Deploying portfolio.enhaq.online...
📦 Regenerating site...
✅ Site generated
📤 Uploading to Hostinger...
[upload progress]
✅ Deployment successful!
🌐 Visit: http://portfolio.enhaq.online
```

### Secure Your Password (Optional)

Instead of hardcoding password in script:

1. **Create secure config file:**
   ```bash
   echo 'FTP_PASS="your_password"' > ~/.openclaw/workspace/.secrets/ftp.env
   chmod 600 ~/.openclaw/workspace/.secrets/ftp.env
   ```

2. **Update deploy.sh to read from file:**
   ```bash
   source ~/.openclaw/workspace/.secrets/ftp.env
   ```

---

## Step 5: Update Workflow

After deployment is working:

1. **Edit data** (add holdings/trades)
2. **Regenerate site:**
   ```bash
   python3 scripts/generate.py
   ```
3. **Deploy:**
   ```bash
   ./scripts/deploy.sh
   ```

### Or One-Line Update:

```bash
python3 scripts/generate.py && ./scripts/deploy.sh
```

---

## DNS & SSL Setup

### Enable HTTPS (SSL Certificate)

1. In Hostinger panel, go to **"SSL"**
2. Find `portfolio.enhaq.online`
3. Click "Install SSL" or "Enable"
4. Hostinger provides free Let's Encrypt SSL
5. Wait 5-10 minutes for activation
6. Site will be accessible via: **https://portfolio.enhaq.online**

### Force HTTPS (Optional)

Create `.htaccess` file in subdomain root:

```apache
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

Upload via FTP to `/public_html/portfolio/.htaccess`

---

## Alternative: Deploy via Git (Advanced)

If you prefer Git-based workflow:

1. **Initialize Git repo:**
   ```bash
   cd ~/.openclaw/workspace/portfolio-tracker
   git init
   git add .
   git commit -m "Initial portfolio tracker"
   ```

2. **Push to GitHub/GitLab**
   ```bash
   git remote add origin https://github.com/yourusername/portfolio-tracker.git
   git push -u origin main
   ```

3. **Set up Git deployment on Hostinger:**
   - Hostinger supports Git deployment in some plans
   - Or use GitHub Actions to deploy via FTP

---

## Checklist

- [ ] Subdomain created: portfolio.enhaq.online
- [ ] DNS propagated (site accessible)
- [ ] FTP credentials obtained
- [ ] First manual deployment successful
- [ ] Automated deploy script configured
- [ ] SSL certificate installed
- [ ] Site live and functional

---

## Quick Reference

**Generate site:**
```bash
cd ~/.openclaw/workspace/portfolio-tracker
python3 scripts/generate.py
```

**Deploy:**
```bash
./scripts/deploy.sh
```

**Add holding:**
```bash
python3 scripts/add-holding.py --ticker RACE --name Ferrari ...
```

**Add trade:**
```bash
python3 scripts/add-trade.py --ticker SPY --type P1 ...
```

**Full workflow:**
```bash
# Make changes to data
# Then:
python3 scripts/generate.py && ./scripts/deploy.sh
```

---

## Need Help?

**FTP not working?**
- Try SFTP (port 22) instead of FTP (port 21)
- Use IP address instead of hostname
- Check firewall/security settings

**Subdomain not resolving?**
- Wait longer (DNS can take 24h)
- Check Hostinger DNS settings
- Verify subdomain was created successfully

**Files not showing?**
- Check remote directory path is correct
- Verify file permissions (755 for folders, 644 for files)
- Clear browser cache

**Script errors?**
- Ensure `lftp` is installed: `brew install lftp`
- Check credentials are correct in deploy.sh
- Test FTP connection manually with FileZilla first
