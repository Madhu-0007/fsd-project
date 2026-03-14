# 🚗 RidePool Finder — Agent Task File
> Full-stack Flask project | HTML + Bootstrap + CSS + JS + jQuery + SQLite  
> Push to GitHub with clean, human-style commit history

---

## 🗂️ PROJECT OVERVIEW

**App Name:** RidePool Finder  
**Purpose:** A ride-pooling web app where users can post available rides or search for rides to join. Drivers post their route; passengers find and request a seat.  
**Stack:** Flask · Jinja2 · SQLite · Bootstrap 5 · jQuery · Vanilla JS · Minimal CSS

---

## 📁 FOLDER STRUCTURE TO CREATE

```
ridepool-finder/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── (placeholder or empty)
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── post_ride.html
│   ├── search_rides.html
│   ├── ride_detail.html
│   ├── request_success.html
│   └── my_rides.html
├── app.py
├── schema.sql
├── requirements.txt
└── README.md
```

---

## 🗃️ DATABASE SCHEMA (`schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS rides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_name TEXT NOT NULL,
    driver_email TEXT NOT NULL,
    from_location TEXT NOT NULL,
    to_location TEXT NOT NULL,
    ride_date TEXT NOT NULL,
    ride_time TEXT NOT NULL,
    seats_available INTEGER NOT NULL,
    price_per_seat REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ride_id INTEGER NOT NULL,
    passenger_name TEXT NOT NULL,
    passenger_email TEXT NOT NULL,
    seats_requested INTEGER NOT NULL,
    message TEXT,
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ride_id) REFERENCES rides(id)
);
```

---

## ⚙️ BACKEND — `app.py`

Implement the following Flask routes:

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home page — hero section + search bar |
| `/post-ride` | GET | Show post ride form |
| `/post-ride` | POST | Validate + insert ride into DB, redirect to success |
| `/search` | GET | Show search form + results filtered by from/to/date |
| `/ride/<int:id>` | GET | Show single ride detail + request form |
| `/request-ride/<int:ride_id>` | POST | Submit seat request, redirect to success |
| `/success` | GET | Generic success confirmation page |
| `/my-rides` | GET | List all posted rides (no auth needed, show all) |

**Flask setup requirements:**
- Import: `Flask, render_template, request, redirect, url_for, g, flash`
- Use `sqlite3` with `get_db()` helper that uses `g` for connection
- Call `init_db()` on first run using `schema.sql`
- Use `app.secret_key = 'ridepool_secret_2024'`
- Run on `debug=True`

---

## 🌐 FRONTEND TEMPLATES

### `base.html`
- Bootstrap 5 CDN (CSS + JS bundle)
- jQuery 3.7 CDN
- Link to `static/css/style.css` and `static/js/main.js`
- Bootstrap Navbar with brand "🚗 RidePool" and links: Home, Find a Ride, Post a Ride, My Rides
- Navbar collapses on mobile (hamburger menu)
- Flash messages block: loop `get_flashed_messages()` and show as Bootstrap `.alert.alert-success` or `.alert-danger` with dismiss button
- Footer with text "© 2024 RidePool Finder · Made with Flask & Bootstrap"

### `index.html` (Home — extends base)
- Full-width hero section with gradient background (`#1a1a2e` → `#16213e`)
- Heading: "Find Your Perfect Ride" in white, subtitle text
- Inline search form (Bootstrap `.row.g-2`) with:
  - From location (text input)
  - To location (text input)
  - Date (date input, min = today)
  - Submit button → POSTs to `/search` as GET params
- Below hero: 3 Bootstrap cards in a row showing feature highlights (Post a Ride, Find a Ride, Save Money)
- "Browse All Rides" button linking to `/search`

### `post_ride.html` (extends base)
- Page heading: "Post a Ride"
- Bootstrap card with form inside
- Fields (all required unless noted):
  - Driver Name (text)
  - Driver Email (email)
  - From Location (text)
  - To Location (text)
  - Ride Date (date, min=today)
  - Ride Time (time)
  - Seats Available (number, min=1, max=8)
  - Price per Seat ₹ (number, min=0, step=0.01)
  - Notes / Message for passengers (textarea, optional)
- Submit button: "Post My Ride 🚗"
- jQuery validation on submit (see JS section)

### `search_rides.html` (extends base)
- Top section: compact search/filter form (GET form, same fields as hero search) pre-filled with query params
- Results section:
  - If no rides: Bootstrap `.alert.alert-info` "No rides found. Try different filters."
  - If rides found: Bootstrap card grid (`.row.row-cols-1.row-cols-md-2.row-cols-lg-3.g-4`)
  - Each card shows: From → To, Date & Time, Driver Name, Seats Available badge, Price badge, "View Details" button → `/ride/<id>`
- Use Jinja2 `{% for ride in rides %}` loop

### `ride_detail.html` (extends base)
- Back button → `/search`
- Left column: Ride details card (all fields, route highlight, driver info)
- Right column: "Request a Seat" form
  - Passenger Name (text, required)
  - Passenger Email (email, required)
  - Seats Requested (number, min=1, max=seats_available)
  - Message to driver (textarea, optional)
  - Submit button: "Request Seat ✅"
- Show `seats_available` dynamically as badge — if 0, show "Fully Booked" and disable form
- jQuery validation on request form

### `request_success.html` (extends base)
- Centered success card with ✅ icon
- Message: "Your ride request has been sent!"
- Subtext: "The driver will contact you via email."
- Buttons: "Find Another Ride" → `/search`, "Go Home" → `/`

### `my_rides.html` (extends base)
- Page heading: "All Posted Rides"
- Bootstrap table (`.table.table-hover.table-striped`) listing all rides:
  - Columns: #, From, To, Date, Time, Seats, Price, Driver, Actions
  - Actions: "View" button → `/ride/<id>`
- Empty state message if no rides posted yet

---

## 🎨 STYLES — `static/css/style.css`

Keep it minimal. Only write custom CSS for things Bootstrap can't handle:

```css
/* Color overrides */
:root {
  --primary-dark: #1a1a2e;
  --accent: #e94560;
  --card-hover-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

/* Hero section */
.hero-section {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 420px;
  display: flex;
  align-items: center;
  color: white;
  padding: 60px 0;
}

/* Ride cards hover effect */
.ride-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}
.ride-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--card-hover-shadow);
}

/* Price badge */
.price-badge {
  background-color: #e94560;
  color: white;
  border-radius: 20px;
  padding: 4px 12px;
  font-weight: 600;
}

/* Seat badge */
.seat-badge {
  background-color: #0f3460;
  color: white;
  border-radius: 20px;
  padding: 4px 10px;
}

/* Footer */
footer {
  background: #1a1a2e;
  color: #adb5bd;
  text-align: center;
  padding: 20px;
  margin-top: 60px;
}

/* Form validation error styling */
.field-error {
  border-color: #dc3545 !important;
}
.error-msg {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 4px;
}
```

---

## ⚡ JAVASCRIPT + JQUERY — `static/js/main.js`

Implement the following behaviors:

### 1. Post Ride Form Validation (`#postRideForm`)
On submit (prevent default until valid):
- Driver Name: not empty
- Driver Email: valid email format (regex test)
- From Location: not empty
- To Location: not empty, must differ from From Location (show error "From and To cannot be the same")
- Ride Date: not empty, must be today or future
- Ride Time: not empty
- Seats Available: between 1–8
- Price: >= 0
- Clear all `.field-error` and `.error-msg` on each validation run
- If all valid, submit the form

### 2. Request Ride Form Validation (`#requestRideForm`)
On submit:
- Passenger Name: not empty
- Passenger Email: valid email format
- Seats Requested: >= 1
- If valid, show Bootstrap spinner in the button and submit

### 3. Search Form Auto-submit
- On the search page, when user changes the date picker input, auto-submit the filter form (for quick filtering UX)

### 4. Seat Availability Warning
- On ride detail page: if `seats_available <= 2` (pass this as a data attribute `data-seats`), show a yellow Bootstrap `.alert.alert-warning` "Hurry! Only X seats left."

### 5. Confirmation Toast on Ride Posting
- After page load on `/success`, show a Bootstrap Toast in the bottom-right corner saying "Ride posted successfully! 🎉"

### 6. Navbar Active Link Highlighting
- Use jQuery to add `.active` class to the nav link whose href matches `window.location.pathname`

---

## 📦 `requirements.txt`

```
Flask==3.0.3
```

---

## 📝 `README.md`

Write a clean, complete README with these sections:

```markdown
# 🚗 RidePool Finder

A full-stack ride-pooling web application where users can post available rides and find rides to join.

## 🛠 Tech Stack
- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML5, Bootstrap 5, jQuery 3.7, Vanilla JS
- **Templating:** Jinja2

## ✨ Features
- Post a ride with route, date, time, seats, and price
- Search rides by origin, destination, and date
- View detailed ride info and request a seat
- Client-side form validation with jQuery
- Flash message feedback
- Fully responsive (Bootstrap grid)

## 🚀 Setup Instructions

1. Clone the repo
   git clone https://github.com/YOUR_USERNAME/ridepool-finder.git
   cd ridepool-finder

2. Create a virtual environment
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Run the app
   python app.py

5. Open in browser
   http://127.0.0.1:5000

## 📁 Project Structure
(include tree of folders)

## 📸 Screenshots
(add after running locally)
```

---

## 🗂️ GIT COMMIT SEQUENCE
When making each git commit, set a fake author date to simulate 
building over 3 days. Use this format:

Day 1 commits → GIT_AUTHOR_DATE="2025-03-12T10:00:00" GIT_COMMITTER_DATE="2025-03-12T10:00:00" git commit -m "..."
Day 2 commits → GIT_AUTHOR_DATE="2025-03-13T14:00:00" GIT_COMMITTER_DATE="2025-03-13T14:00:00" git commit -m "..."
Day 3 commits → GIT_AUTHOR_DATE="2025-03-14T11:00:00" GIT_COMMITTER_DATE="2025-03-14T11:00:00" git commit -m "..."

Vary the times slightly within each day — don't make every 
commit exactly on the hour. Spread them 20-40 mins apart 
to look natural.

Initialize git and push with these commits **in order**. Write them exactly as shown — these should read like a real developer's history:

```
git init
git remote add origin https://github.com/Madhu-0007/fsd-project.git

# Commit 1
git add README.md
git commit -m "initial commit: add project README with setup instructions"

# Commit 2
git add schema.sql requirements.txt
git commit -m "add database schema and requirements"

# Commit 3
git add app.py
git commit -m "feat: set up Flask app with routes and SQLite integration"

# Commit 4
git add templates/base.html
git commit -m "feat: add base template with Bootstrap navbar and footer"

# Commit 5
git add templates/index.html
git commit -m "feat: add home page with hero section and search form"

# Commit 6
git add templates/post_ride.html templates/request_success.html
git commit -m "feat: add post ride form and success confirmation page"

# Commit 7
git add templates/search_rides.html templates/ride_detail.html
git commit -m "feat: add ride search results and ride detail with request form"

# Commit 8
git add templates/my_rides.html
git commit -m "feat: add my rides page with full rides table"

# Commit 9
git add static/css/style.css
git commit -m "style: add custom CSS for hero, cards, badges and form errors"

# Commit 10
git add static/js/main.js
git commit -m "feat: add jQuery form validation, seat warning, and toast notification"

# Commit 11 (final)
git add .
git commit -m "chore: final cleanup"

git push -u origin main
```

---

## ✅ ACCEPTANCE CRITERIA

Before marking done, verify:

- [ ] App runs with `python app.py` without errors
- [ ] SQLite DB is created automatically on first run
- [ ] Can post a ride → appears in search and my-rides
- [ ] Search filters by from/to/date correctly
- [ ] Ride detail page shows correct info
- [ ] Seat request form submits and shows success page
- [ ] jQuery validation catches all empty/invalid fields
- [ ] Navbar highlights active page
- [ ] Fully responsive on mobile (Bootstrap grid)
- [ ] GitHub repo has all 11 commits in correct order
- [ ] README is complete and accurate

---

## 🚫 DO NOT

- Do not use React, Vue, or any JS framework
- Do not add authentication/login (out of scope)
- Do not use external CSS frameworks other than Bootstrap 5
- Do not write more than ~50 lines of custom CSS
- Do not use any paid APIs or external services