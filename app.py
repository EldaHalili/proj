from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Elda2405@'
app.config['MYSQL_DB'] = 'notes_app'
app.config['MYSQL_PORT'] = 3307
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notes', methods=['GET'])
def get_notes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    cur.close()
    return jsonify(notes)

@app.route('/add_note', methods=['POST'])
def create_note():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    title = data.get('note_text')  # Corrected field name
    content = data.get('note_color')  # Corrected field name
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    mysql.connection.commit()
    cur.execute("SELECT LAST_INSERT_ID()")
    note_id = cur.fetchone()[0]
    cur.close()
    return jsonify({"message": "Note created successfully", "note_id": note_id})


@app.route('/delete_note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    # Check if the note with the given note_id exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM notes WHERE id = %s", (note_id,))
    note = cur.fetchone()
    cur.close()

    if not note:
        # If the note doesn't exist, return an error response
        return jsonify({"error": "Note not found"}), 404

    # If the note exists, proceed with the delete operation
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Note deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)