"""Builds ./deploy with ONLY the files the site needs. Upload the contents of deploy/ to any static host
(Netlify Drop, GitHub Pages, Vercel, Firebase Hosting...). Run: python tools/make_deploy.py"""
import os, shutil, subprocess, sys
root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
subprocess.check_call([sys.executable, os.path.join(root, 'tools', 'build_assets.py')])   # keep assets.js in sync with assets/
out = os.path.join(root, 'deploy')
os.makedirs(os.path.join(out, 'assets'), exist_ok=True)
files = ['index.html', 'assets.js'] + ['assets/' + f for f in ('favicon.png', 'feedback-qr.png', 'hackober-wordmark.webp', 'gdg-lockup.webp')]
for f in files:
    shutil.copyfile(os.path.join(root, f), os.path.join(out, f))
print('deploy/ ready:', ', '.join(files))
