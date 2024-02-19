from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Function to initialize the database and create table if not exists
def init_db():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            company TEXT,
            emailsent BOOLEAN DEFAULT FALSE,
            emailsource TEXT,
            emailtype TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Call init_db directly to ensure the DB is initialized before any routes are defined
init_db()

# Route for uploading data
@app.route('/upload', methods=['POST'])
def upload_data():
    if not request.is_json:
        return jsonify({'error': 'Missing JSON in request'}), 400
    data = request.get_json()
    duplicates, inserted = [], []
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    for contact in data:
        email = contact['Email']
        cursor.execute("SELECT id FROM contacts WHERE email = ?", (email,))
        if cursor.fetchone():
            duplicates.append(email)
        else:
            try:
                cursor.execute("INSERT INTO contacts (name, email, company, emailsent, emailsource, emailtype) VALUES (?, ?, ?, ?, ?, ?)",
                               (contact['Name'], email, contact.get('Company', ''), False, contact.get('emailsource', ''), contact.get('emailtype', 'VC')))
                inserted.append(email)
            except sqlite3.IntegrityError as e:
                conn.close()  # Close the connection on error before returning
                return jsonify({'error': 'Failed to insert data', 'sqlite_error': str(e)}), 500
    conn.commit()
    conn.close()
    return jsonify({'inserted': inserted, 'duplicates': duplicates}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)