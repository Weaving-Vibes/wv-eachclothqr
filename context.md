# London Pie — Fabric Page Context

## Project Overview
A mobile-first fabric showcase page for **Weaving Vibes** (B2B hemp textile manufacturer, Mumbai).
Built for a **5-day exhibition** where visitors scan a QR code → land on this page → can request a free swatch.

**Stack:** Pure HTML/CSS/JS → hosted on GitHub Pages (free)
**Form submission:** JS `fetch POST` → Google Apps Script → Google Sheets (enquiry log)

---

## File Structure
```
london-pie/
├── index.html              ← main page
└── static/
    ├── fabric-hero.png     ← hero background image
    ├── woman-lifestyle.png ← women's wear lifestyle image
    └── man-lifestyle.png   ← men's wear lifestyle image
```

---

## Page Sections (top to bottom)

| Section | Description |
|---|---|
| **Nav** | Fixed top bar — "Weaving Vibes" logo + "100% Hemp" pill |
| **Hero** | Full-screen image with overlay, fabric name, spec pills, scroll hint |
| **About** | Dark green bg — fabric story, blockquote, tags |
| **Lifestyle (Women)** | Image LEFT (55%) · Text RIGHT (45%) — use cases, all-season, skin-kind, low MOQ |
| **Lifestyle (Men)** | Image RIGHT (55%) · Text LEFT (45%) — use cases, durability, global exports, customisable |
| **Colors** | Horizontal scroll — 9 color swatches with names |
| **Numbers** | Stats grid (4 cards) + animated ticker |
| **CTA** | "Request a free sample" button → opens modal |
| **Footer** | Logo, tagline, links (Website / Email / Instagram) |
| **Modal** | Bottom sheet form → submits to Google Sheets |

---

## Fabric Details — London Pie

| Property | Value |
|---|---|
| Material | 100% Hemp |
| GSM | 120–130 |
| Weave | Plain Weave |
| Width | 58" |
| Dye | Azo-Free |
| Collection | 2025 |

### Available Colors (9)
| Name | Hex |
|---|---|
| Molten Lava | `#6B1F2A` |
| Illuminating | `#E8C84A` |
| Copper Coin | `#8B4A2E` |
| Candy Pink | `#F0B8C0` |
| Bleached Aqua | `#B8D4D8` |
| Mock Orange | `#E8A882` |
| Blue Ribbon | `#1A2E5C` |
| Lime Cream | `#D8E8C8` |
| Woodbine | `#6B7A3A` |

---

## Design System

### Fonts
- **Display:** Cormorant Garamond (serif) — headings, titles
- **Body:** Jost (sans-serif) — labels, body text, buttons

### Colors
```css
--green:      #2C4A2E
--green-dark: #1a2e1b
--green-mid:  #3d6640
--green-light:#e8efe8
--cream:      #f5f0e8
--cream-dark: #ede5d6
--gold:       #b5913a
--gold-light: #d4af6a
--text-dark:  #1c1c1a
--text-mid:   #4a4a45
--text-light: #7a7a72
```

### Layout
- `max-width: 480px` centered — mobile-first
- Lifestyle blocks: `display: flex`, 55% image / 45% text
- `.lifestyle-block.reverse` → `flex-direction: row-reverse` for alternating layout

---

## Form Fields (Modal)
| Field | ID | Required |
|---|---|---|
| Name | `f-name` | ✅ |
| Brand / Company | `f-brand` | ❌ |
| Email | `f-email` | ✅ |
| WhatsApp | `f-phone` | ✅ |
| City | `f-city` | ❌ |
| Colour Preference | `f-color` | ❌ |

### Data sent to Google Sheets
`name, brand, email, phone, city, color, fabric (hardcoded: "London Pie"), timestamp`

### Apps Script URL
```js
const SHEET_URL = 'https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec'; // 🔁 Replace
```

---

## Animations
- **Scroll fade-up:** `.fade-up` → `.fade-up.visible` via `IntersectionObserver` (threshold 0.15)
- **Ticker:** CSS `@keyframes ticker` — 18s linear infinite, duplicated items for seamless loop
- **Scroll hint:** CSS `@keyframes bounce` — 2s infinite on hero
- **Modal:** slide-up from bottom via `translateY(100%) → translateY(0)`

---

## Deployment Plan
- **Host:** GitHub Pages (`vansh7206.github.io/wv-fabrics/london-pie/`)
- **DB:** Google Sheets (enquiry log via Apps Script webhook)
- **QR:** One QR per fabric → points to its GitHub Pages URL
- **Scale:** 100–200 visitors/day × 5 days — well within all free tier limits

---

## TODO Before Launch
- [ ] Replace `YOUR_SCRIPT_ID` in `submitForm()` with actual Apps Script deployment URL
- [ ] Add real images to `static/` folder (hero, woman, man)
- [ ] Deploy to GitHub Pages
- [ ] Generate QR codes (one per fabric page)
- [ ] Test form → Sheets flow end to end