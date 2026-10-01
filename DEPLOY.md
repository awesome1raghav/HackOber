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
* The site shows only the **HACKOBER wordmark and the timers** until **`CONFIG.OPENS_AT`** (currently `2026-10-01T13:30:00+05:30`, i.e. 1 Oct 2026, **1:30 pm** India time). Every other screen, deep link and invite link is unreachable until then.
* "The event is over. Almost." appears only in the **last 10 minutes** of the main countdown.
* Once the countdown reaches zero, the gate returns to its full look (logo, tagline) with the "Open the vault" button.
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

## 9. Team size, names and each person's part
* Team size is **2 to 4** people, the lead included (`MIN_TEAM` / `MAX_TEAM` in `CONFIG`).
* The **lead types their own name** when creating the team. Each **teammate types their own name** after joining.
* Everyone is also asked for **their part in the hackathon**: a **role** (required, up to 32 characters, with six quick-pick chips such as "Full-Stack Developer" or "UI/UX Designer") and **what they worked on** (optional, up to 72 characters; a chip fills a matching suggestion that can be edited). Both appear on the team card.
* Because there is no server, names and parts travel by QR: a teammate's **name pass** (shown in their waiting room) is scanned by the lead, and the lead's **finish code** then carries the lead's and every teammate's name, role and "what they worked on" to all phones. Every card shows **Team lead + Members**, each with their part.
* A teammate's own name and part are always on their own card, even if the lead never scanned their pass. Phones that joined before this update have no part saved; a teammate in that state is asked for it the next time the app resumes, and anyone without a part still gets a "Vault cracked" tile on the card.
* Everything is shown in full on the phone that typed it. Inside a QR, each name is limited to about 36 characters, a role to 30 and "what they worked on" to 56; a longer "what they worked on" is shortened by dropping whole trailing items ("A, B, C" becomes "A, B"). A worst case 4-person finish code (every field at its limit) is a 81-module QR; a typical one is 61 modules. Both decode with OpenCV down to the size the QR is shown at on a phone.

## 10. Round 1 timer
* Under the main countdown there is a second, smaller timer, **"Round 1 ends in"**, counting down to **`CONFIG.ROUND1_ENDS_AT`** (currently `2026-10-01T13:00:00+05:30`, 1:00 pm India time).
* When it reaches zero it changes to **"Round 1 has ended"** and stays that way until the vault opens. If its time is not before the main countdown's time, the timer hides itself.
* It uses the same server-corrected clock as the main countdown. To change either time, edit `ROUND1_ENDS_AT` or `OPENS_AT` in `index.html`, run `python tools/make_deploy.py` and re-upload.

## 11. The team card (made to be posted on LinkedIn)
* "Poster Clean" design on a pure white page (1080 x 1350, the 4:5 portrait LinkedIn shows in full): the exact GDG lockup, "Google Developer's Day" and the HACKOBER wordmark; **TEAM OF N** between two orange dashes; the team name in large black type with a short orange rule; then **one soft rounded row per person**: an orange number badge (01 to 04), the name, a peach **Team Lead** or **Member** pill, and on the right an icon tile with the person's **role** in bold and **what they worked on** in grey; finally an orange rule, **TEAM CODE** (code in orange) and `@gdgoc_griet | #HACKOBER #GDGoC`.
* The icon follows the role: `</>` for developers, a presentation board for presenters and pitch roles, a layout icon for designers, a chip for AI/ML, a magnifier for research and testing, a spark for anything else.
* Colour reasoning: neutral white and cool grey (~70%) give the orange room to glow; brand orange (~20%) carries energy and courage and marks what matters (badges, rules, team code); near-black ink (~10%) is orange's strongest contrast, so names read instantly and feel trustworthy. A pale peach tint links the pills and icon tiles to the brand without adding a new hue.
* The layout measures itself: the team name shrinks and wraps to two lines, row height and text size step down for 3 and 4 people, long names wrap, and very long roles or descriptions end with "..." instead of colliding. Checked with 2, 3 and 4 people, a 70-character team name, 38-character names and maximum-length roles and descriptions.
* **Post on LinkedIn** (next to "Download card"): on **phones** it opens the share sheet with the card image attached, so choosing LinkedIn opens its post box with the card already in it (the caption is copied too, in case the LinkedIn app drops the text). On **computers** it copies the card to the clipboard and opens LinkedIn's post box with the caption already typed; the person presses **Ctrl+V** (Cmd+V on a Mac) once to attach the card. If the browser blocks clipboard images, the card is saved instead and the sheet says to attach it with the image icon. LinkedIn offers no way for a web page to attach a picture by itself, which is why these two routes are used.
* The caption names everyone with their role, for example "Hima Charan (Full-Stack Developer), Raghav (UI/UX & Presentation) and Asha Rao (Researcher)".
