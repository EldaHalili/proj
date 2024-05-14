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

@app.route('/', methods=['GET'])
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
    cur.close()
    return jsonify({"message": "Note created successfully"})

    data = request.json
    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    title = data.get('note_text')
    content = data.get('note_color')
    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Note created successfully"})

if __name__ == '__main__':
    app.run(debug=True)
