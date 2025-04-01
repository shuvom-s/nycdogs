# Deploying NYC Dogs App to Netlify

This guide explains how to deploy the NYC Dogs Geographic Distribution app to Netlify, making it available on the web for anyone to use.

## Prerequisites

- Git installed on your computer
- Node.js and npm installed (for Netlify CLI)
- A GitHub account (optional, but recommended)
- A Netlify account (free tier is fine)

## Option 1: Using Netlify CLI (Recommended for testing)

### Step 1: Install Netlify CLI

```bash
npm install -g netlify-cli
```

### Step 2: Build the static site

```bash
# Run the build script to generate the static site
python build_netlify.py
```

This will create a `netlify_build` directory with all the necessary files for deployment.

### Step 3: Deploy to Netlify

```bash
# Navigate to the build directory
cd netlify_build

# Start the deployment process
netlify deploy
```

Follow the prompts:
- Choose "Create & configure a new site"
- Select your team
- Optionally, provide a custom site name or accept the generated one
- For the publish directory, enter `.` (the current directory)

### Step 4: Preview and deploy production

The previous step creates a draft URL for preview. Once you've verified everything looks good:

```bash
netlify deploy --prod
```

Your site is now live at the URL provided by Netlify!

## Option 2: Deploying via GitHub (Recommended for continuous integration)

### Step 1: Push your code to GitHub

```bash
# Initialize Git repository if not already done
git init
git add .
git commit -m "Initial commit"

# Create a GitHub repository and push to it
git remote add origin https://github.com/YOUR_USERNAME/nyc-dogs-map.git
git push -u origin main
```

### Step 2: Connect to Netlify

1. Go to [Netlify](https://app.netlify.com/)
2. Click "New site from Git"
3. Choose GitHub as your provider
4. Authorize Netlify to access your GitHub account
5. Select your repository

### Step 3: Configure build settings

Configure the build settings:
- Build command: `python build_netlify.py`
- Publish directory: `netlify_build`

### Step 4: Deploy

Click "Deploy site" and Netlify will build and deploy your site.

## Handling Large Files

The NYC dogs dataset and map files can be quite large. If you encounter issues with file size:

1. Consider reducing the number of maps generated (modify build_netlify.py to limit to top 10-20 breeds/names)
2. Use Git LFS (Large File Storage) for files over 100MB if using GitHub
3. For very large datasets, consider hosting the data files separately and loading them via API

## Customizing Your Netlify Site

- Custom domain: In the Netlify dashboard, go to Site settings > Domain management
- Environment variables: Site settings > Build & deploy > Environment
- Forms and functions: These are advanced Netlify features you can explore in their documentation

## Troubleshooting

- If maps don't load, check browser console for path errors
- Ensure all file paths in the HTML are relative, not absolute
- Check Netlify build logs for any Python dependency issues
- For large datasets, you might need to use Netlify Large Media or external storage 