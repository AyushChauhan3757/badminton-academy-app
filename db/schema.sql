CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  admission_date DATE NOT NULL,
  batch TEXT NOT NULL,
  timing TEXT NOT NULL,
  fees INTEGER NOT NULL,
  is_custom_fee INTEGER DEFAULT 0,
  guardian_name TEXT,
  phone TEXT
);

CREATE TABLE IF NOT EXISTS gym_members (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT,
  joining_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS coaches (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT,
  salary INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS payments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  payer_type TEXT NOT NULL,
  payer_id INTEGER NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  paid_on DATE NOT NULL,
  marked_by TEXT NOT NULL,
  UNIQUE(payer_type, payer_id, month, year)
);

CREATE INDEX IF NOT EXISTS idx_payments_lookup ON payments(payer_id, month, year);

CREATE TABLE IF NOT EXISTS salary_payouts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  coach_id INTEGER NOT NULL REFERENCES coaches(id),
  month INTEGER NOT NULL,
  year INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  paid_on DATE NOT NULL,
  UNIQUE(coach_id, month, year)
);

CREATE TABLE IF NOT EXISTS transactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,
  category TEXT NOT NULL,
  amount INTEGER NOT NULL,
  date DATE NOT NULL,
  description TEXT
);