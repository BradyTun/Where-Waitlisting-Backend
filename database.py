import sqlite3
from models import WaitlistEntry

def init_db():
    conn = sqlite3.connect('waitlist.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS waitlist
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  email TEXT,
                  profession TEXT,
                  meetupPlaces TEXT,
                  frequency TEXT,
                  interests TEXT,
                  reason TEXT)''')
    conn.commit()
    conn.close()

def add_entry(entry: WaitlistEntry):
    conn = sqlite3.connect('waitlist.db')
    c = conn.cursor()
    c.execute("INSERT INTO waitlist (name, email, profession, meetupPlaces, frequency, interests, reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (entry.name, entry.email, entry.profession, ','.join(entry.meetupPlaces), entry.frequency, entry.interests, entry.reason))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect('waitlist.db')
    c = conn.cursor()
    c.execute("SELECT * FROM waitlist")
    rows = c.fetchall()
    conn.close()
    entries = []
    for row in rows:
        entries.append({
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'profession': row[3],
            'meetupPlaces': row[4].split(','),
            'frequency': row[5],
            'interests': row[6],
            'reason': row[7]
        })
    return entries