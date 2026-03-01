#!/bin/bash
# Deploy portfolio site to Hostinger

# Configuration - FILL THESE IN
FTP_HOST="ftp.enhaq.online"          # Your FTP hostname
FTP_USER="u123456"                   # Your FTP username
FTP_PASS="your_password_here"        # Your FTP password
REMOTE_DIR="/public_html/portfolio.enhaq.online"  # Remote directory path

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Deploying portfolio.enhaq.online...${NC}\n"

# Check if credentials are configured
if [ "$FTP_PASS" = "your_password_here" ]; then
    echo -e "${RED}❌ Deployment not configured!${NC}"
    echo ""
    echo "Edit this script and fill in:"
    echo "  FTP_HOST='ftp.enhaq.online'"
    echo "  FTP_USER='your_username'"
    echo "  FTP_PASS='your_password'"
    echo "  REMOTE_DIR='/path/to/portfolio/folder'"
    echo ""
    exit 1
fi

# Change to project root
cd "$(dirname "$0")/.." || exit

# Regenerate site
echo "📦 Regenerating site..."
python3 scripts/generate.py
echo ""

# Upload via FTP using lftp
echo -e "${YELLOW}📤 Uploading to Hostinger...${NC}"

# Check if lftp is installed
if ! command -v lftp &> /dev/null; then
    echo -e "${YELLOW}Installing lftp...${NC}"
    # Try homebrew first (macOS/Linux with brew)
    if command -v brew &> /dev/null; then
        brew install lftp
    # Try apt (Debian/Ubuntu)
    elif command -v apt-get &> /dev/null; then
        sudo apt-get install -y lftp
    else
        echo -e "${RED}❌ Cannot install lftp. Please install manually.${NC}"
        exit 1
    fi
fi

# Upload using lftp (mirror with delete)
lftp -c "
set ftp:ssl-allow no
open -u $FTP_USER,$FTP_PASS $FTP_HOST
mirror -R --delete --verbose public/ $REMOTE_DIR/
bye
"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo "🌐 Visit: http://portfolio.enhaq.online"
else
    echo ""
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi
