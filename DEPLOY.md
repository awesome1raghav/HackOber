# HACKOBER — The Vault: deployment notes

## 1. Build the upload folder
```
python tools/make_deploy.py
```
This creates `deploy/` with only what the site needs (`index.html`, `assets.js`, `assets/`). Re-run it after every edit to `index.html`.

## 2. Host it (any static host, HTTPS required)
Upload the **contents of `deploy/`** to Netlify Drop, GitHub Pages, Vercel or Firebase Hosting.
HTTPS matters: phones only allow the in-app QR camera on secure pages, and Netlify / GitHub Pages / Vercel give you HTTPS by default.

Open the live link once on a phone and run through it as a team lead before the event.

## 3. Settings (top of the script in `index.html`, block called `CONFIG`)
| Setting | Value now |
|---|---|
| `FEEDBACK_URL` | Your Google Form (read from your QR image) |
| `INSTAGRAM_HANDLE` / `INSTAGRAM_URL` | `@gdgoc_griet` / https://www.instagram.com/gdgoc_griet/ |
| `SITE_URL` | Empty = team QR codes use the page's own address. Only set it if participants reach the site through a different link than the one the team lead opens. |
| `WEBHOOK_URL` | Empty. Optional: a Google Apps Script URL that logs teams and completions. Nothing depends on it. |
| `NEXT_TITLE` / `NEXT_BODY` | The closing "what's next" card |

The QR shown on the last lock is `assets/feedback-qr.png` (your image, unchanged). To swap it, replace that file and run `python tools/make_deploy.py`.

## 4. Testing helpers
* `your-site/?reset` clears saved progress on that phone.
* Progress is saved per phone, so "Start over" is on the first screen.

## 5. Things to know
* Team codes are 7 characters with a typo check. Random codes for ~800 teams collide with odds of about 1 in 3,000; the odds are tiny but not zero.
* A team QR carries the first 64 encoded characters of the team name; the lead always sees the full name.
* Teammates only need internet and a camera (or the code). Fonts and QR libraries load from public CDNs.
* 15 games are built in; each team's lead gets 3 of them, picked from the team code so it is random per team but repeatable. A sample of 45,500 teams showed an even spread across all 15 games and all 455 possible trios.

## 6. Countdown gate
* The site shows only a countdown until **`CONFIG.OPENS_AT`** (currently `2026-10-01T14:30:00+05:30`, i.e. 1 Oct 2026, 2:30 pm India time). Every other screen, deep link and invite link is unreachable until then.
* When the countdown hits zero on a phone that is already open, the "Open the vault" button appears by itself.
* The countdown uses the **website's own clock** (read from the server's `Date` header), not the phone's, so a wrong or changed phone clock can't skip it. If a phone is offline it falls back to its own clock.
* To change the time, edit `OPENS_AT` in `index.html`, then run `python tools/make_deploy.py` and re-upload.

## 7. Secret developer panel
* **Right-click** anywhere (mouse only) on a laptop: enter the developer PIN once and the **whole app opens without waiting for the countdown**. Right-click again to restore the countdown, open diagnostics or close. Preview mode lasts only until the page is refreshed: **a refresh always brings the countdown back** (saved team progress is kept). The PIN is remembered per browser tab, so after a refresh right-click once and choose "Open the whole app".
* Open the diagnostics directly with **7 quick taps in the bottom-left corner** of the screen (phones) or **Ctrl+Shift+D** (laptops).
* It shows the app's status, the countdown and clock sync, this phone's progress, device and browser capabilities, whether the libraries and images loaded, the config, recent screen changes and any errors. **Copy** puts the whole report on the clipboard so it can be pasted into a message.
* Reading the report needs no PIN. Actions that change the app (open the vault early, set a 60-second countdown, load test states, play any game, erase saved data) need the **developer PIN**.
* The default PIN is `hackober-dev`. **Change it before the event:** `python tools/set_dev_pin.py "your new pin"`, then `python tools/make_deploy.py`. Only a hash of the PIN is stored in the page.

## 8. Big moments (vibration + animation)
* **Teammate scans the lead's finish QR** (or taps "My lead has finished"): one unbroken **2.6-second vibration**, a hard screen shake, expanding rings, confetti from three points and a giant "Vault cracked." headline. Then the normal reveal of the sentence continues into the last lock.
* **After the feedback form**: the last word slams in with a stronger shake, five rings, bigger confetti and a heavier vibration pattern.
* **Team card reveal**: the card flies in, overshoots and glows, with rings and a strong buzz.
* Vibration works on Android Chrome only (iPhones ignore it; the animations still play), and only after the person's first tap on the page. The duration is `ms` in `surge({...})` in `index.html`.
