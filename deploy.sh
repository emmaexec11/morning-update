#!/bin/bash

# Morning Update Dashboard - Quick Deploy Script

echo "🚀 Deploying Morning Update Dashboard..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "initial morning update dashboard"
    echo "✅ Git repository initialized"
    echo ""
    echo "📋 Next steps:"
    echo "1. Create GitHub repo: https://github.com/new"
    echo "2. Name it: morning-update"  
    echo "3. Run: git remote add origin https://github.com/YOUR-USERNAME/morning-update.git"
    echo "4. Run: git push -u origin main"
    echo "5. Deploy on Cloudflare Pages: https://dash.cloudflare.com"
else
    # We're already in a git repo, just push changes
    echo "📤 Pushing changes to GitHub..."
    git add .
    
    # Get commit message from user or use default
    if [ -z "$1" ]; then
        COMMIT_MSG="update morning dashboard"
    else
        COMMIT_MSG="$1"
    fi
    
    git commit -m "$COMMIT_MSG"
    git push
    
    echo "✅ Changes pushed! Dashboard will update in ~30 seconds"
    echo "🔗 Check your live URL on Cloudflare Pages"
fi

echo ""
echo "⚡ Morning Update Dashboard deployment complete!"