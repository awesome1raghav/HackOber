"""Sets the developer PIN for the secret diagnostics panel.
Usage:  python tools/set_dev_pin.py "my new pin"
It stores only the SHA-256 hash of the PIN in index.html (CONFIG.DEV_PIN_HASH), never the PIN itself.
Then run:  python tools/make_deploy.py"""
import hashlib, os, re, sys
if len(sys.argv) != 2 or len(sys.argv[1]) < 6:
    sys.exit('Usage: python tools/set_dev_pin.py "<pin, at least 6 characters>"')
h = hashlib.sha256(sys.argv[1].encode('utf-8')).hexdigest()
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
src = open(path, encoding='utf-8').read()
new, n = re.subn(r'(DEV_PIN_HASH:\s*")[0-9a-f]{64}(")', lambda m: m.group(1) + h + m.group(2), src)
if n != 1: sys.exit('Could not find DEV_PIN_HASH in index.html')
open(path, 'w', encoding='utf-8', newline='').write(new)
print('Developer PIN updated. Now run: python tools/make_deploy.py')
