# Avni Badminton Academy

A full-stack management app built to replace a paper attendance/fee register at a real badminton academy. Built as both a working business tool and a portfolio project.

**Live demo:** _add your Streamlit Community Cloud URL here once deployed_

---

## Overview

Avni Badminton Academy handles day-to-day academy operations: student and gym-member rosters, monthly fee tracking, coach salaries, and a full financial activity log — all backed by a real database, accessible from any device.

Two roles are supported:
- **Admin** — full access: manage students, gym members, and coaches; track and mark fees/salaries paid; view financial totals and a full activity log.
- **Coach** — shared login for the academy's coaches: view rosters, mark student/gym fees as paid, and follow up on students who missed last month's payment. No access to financial totals or salary figures.

## Features

- **Dashboard** — lifetime and monthly totals (fees received, expenses paid, profit), plus a live activity log of every payment and transaction
- **Fees tracking** — a live "who hasn't paid this month" checklist for students and gym members, recalculated automatically as the calendar rolls over — no manual resets needed
- **Missed-payment follow-up** — a dedicated view for anyone who missed last month's fee, with one-click "mark as paid" or "remove" actions
- **Coach salaries** — admin-managed salary figures with one-click monthly payout tracking, kept separate from what coaches themselves can see
- **Full roster management** — add/edit/delete students, gym members, and coaches, with search, filters, and pagination
- **Activity log** — a searchable, filterable, paginated record of every fee payment, salary payout, and expense
- **Role-based access** — a simple two-role auth model with session timeout and a distinct read/write permission set for coaches vs. admin
- **Mobile-friendly** — fully responsive, used day-to-day on both a desktop and a phone at the academy

## Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend & app logic | [Streamlit](https://streamlit.io) (Python) | Single codebase for UI and logic, fast to build and iterate |
| Database | [Turso](https://turso.tech) (libSQL / SQLite-compatible) | Generous free tier, no cold-start/sleep behavior unlike other free-tier hosted Postgres options |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) | Free, deploys directly from GitHub |

The database is stress-tested to comfortably handle 1,000+ students over 5-10 years of operation on Turso's free tier, with headroom to spare.

## Project Structure

```
├── app.py                  # Entry point — auth, routing, global styling
├── constants.py             # Batch fees/timings, roles, idle timeout
├── db/
│   ├── connection.py        # Shared Turso connection helper
│   ├── schema.sql           # Full table schema
│   ├── students.py          # Student CRUD
│   ├── gym_members.py       # Gym member CRUD
│   ├── coaches.py           # Coach CRUD
│   ├── payments.py          # Fee pending/paid/missed-last-month queries + mark-paid writes
│   ├── salary.py            # Coach salary status + payout writes
│   ├── overview.py          # Dashboard totals + recent activity log
│   └── log.py                # Full activity log queries (paginated, filtered, searchable)
├── pages_admin/              # Admin-only pages (Overview, Pending, Students, Gym, Coaches, Log)
├── pages_coach/               # Coach-only pages (Fees Pending, Students Roster, Gym Roster)
├── utils/
│   ├── auth.py                # Session/role guard, idle timeout
│   ├── header.py              # Shared per-page header component
│   ├── styling.py             # Centralized theme/CSS
│   └── ui_helpers.py          # Shared render helpers (pills, toasts, dialog kit)
├── scripts/
│   └── init_db.py             # One-time/idempotent table creation script
└── requirements.txt
```

## Running Locally

1. Clone the repo and install dependencies:
```bash
   pip install -r requirements.txt
```
2. Create a [Turso](https://turso.tech) database and grab its connection URL + auth token.
3. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in:
```toml
   TURSO_DATABASE_URL = "https://your-database-url.turso.io"
   TURSO_AUTH_TOKEN = "your-auth-token"
   ADMIN_PASSWORD = "your-admin-password"
   COACH_PASSWORD = "your-coach-password"
```
4. Initialize the database tables:
```bash
   python scripts/init_db.py
```
5. Run the app:
```bash
   streamlit run app.py
```

## Notes

This is a real, actively-used tool for a family-run academy — the codebase prioritizes clean, understandable code and correct business logic (append-only payment history, no destructive resets, confirm-before-write on every financial action) over unnecessary complexity or premature optimization. A handful of deliberate v1 scope decisions are worth calling out:

- **No export/backup or audit-trail feature** — if a correction is ever needed after the fact, it's made directly in the Turso dashboard, treated as a rare, manual fallback rather than app functionality.
- **No multi-month arrears tracking** — the "missed last month" view only looks one month back, on the assumption that people either pay by month-end or leave; catching someone who slips past two consecutive months is an accepted manual/awareness gap for v1.
- **Batch fees and timings are hardcoded Python constants, not a database table** — there are only ever a handful of batches, and they change rarely enough that a join would add complexity without real benefit.
- **All dates are computed against IST explicitly in code**, regardless of what timezone the hosting server itself runs in, since the app is used exclusively by one academy in one timezone.

Built and maintained as a solo project — issues and suggestions are welcome, but this is primarily a working tool for one specific academy rather than a general-purpose product.