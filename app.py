from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  amount REAL, 
                  category TEXT, 
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()

    # HTML Template inside Python
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expense Tracker</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f4f4f4; }}
            .delete-btn {{ color: red; text-decoration: none; }}
        </style>
    </head>
    <body>
        <h2>Expense Tracker</h2>
        <form action="/add" method="post">
            <label>Amount:</label>
            <input type="number" name="amount" required>
            <label>Category:</label>
            <input type="text" name="category" required>
            <label>Description:</label>
            <input type="text" name="description" required>
            <button type="submit">Add Expense</button>
        </form>

        <h3>Expense List</h3>
        <table>
            <tr>
                <th>ID</th>
                <th>Amount</th>
                <th>Category</th>
                <th>Description</th>
                <th>Action</th>
            </tr>
            {''.join(f"<tr><td>{exp[0]}</td><td>{exp[1]}</td><td>{exp[2]}</td><td>{exp[3]}</td><td><a class='delete-btn' href='/delete/{exp[0]}'>Delete</a></td></tr>" for exp in expenses)}
        </table>
    </body>
    </html>
    '''

@app.route('/add', methods=["POST"])
def add_expense():
    amount = request.form["amount"]
    category = request.form["category"]
    description = request.form["description"]

    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)", 
              (amount, category, description))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
