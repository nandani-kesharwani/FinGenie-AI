from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
import mysql.connector
from ai import ask_ai
from config import DB_CONFIG, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)

def login_required():
    if 'user_id' not in session:
        return False
    return True

# Database Connection
db = mysql.connector.connect(**DB_CONFIG)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        query = "SELECT * FROM users WHERE email=%s"
        cursor.execute(query, (email,))

        user = cursor.fetchone()

        if user:

            stored_password = user[3]

            if bcrypt.check_password_hash(stored_password, password):
                session['user_id'] = user[0]
                session['fullname'] = user[1]

                return redirect(url_for('dashboard'))

            else:

                return "Incorrect Password"

        else:

            return "User Not Found"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():

    if not login_required():
        return redirect(url_for('login'))

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=%s",
        (session['user_id'],)
    )
    total_income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=%s",
        (session['user_id'],)
    )
    total_expense = cursor.fetchone()[0] or 0

    # Savings
    savings = total_income - total_expense

    # Income History
    cursor.execute("""
        SELECT id, source, amount, income_date
        FROM income
        WHERE user_id=%s
        ORDER BY income_date DESC
    """, (session['user_id'],))

    income_history = cursor.fetchall()

    # Expense History
    cursor.execute("""
        SELECT id, category, amount, expense_date
        FROM expenses
        WHERE user_id=%s
        ORDER BY expense_date DESC
    """, (session['user_id'],))

    expense_history = cursor.fetchall()

    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expense=total_expense,
        savings=savings,
        income_history=income_history,
        expense_history=expense_history
    )

@app.route('/reports')
def reports():

    if not login_required():
        return redirect(url_for('login'))

    # Total Income
    cursor.execute(
        "SELECT SUM(amount) FROM income WHERE user_id=%s",
        (session['user_id'],)
    )
    total_income = cursor.fetchone()[0] or 0

    # Total Expense
    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE user_id=%s",
        (session['user_id'],)
    )
    total_expense = cursor.fetchone()[0] or 0

    savings = total_income - total_expense

    # Expense Category Data
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        WHERE user_id=%s
        GROUP BY category
    """, (session['user_id'],))

    expense_data = cursor.fetchall()

    categories = [row[0] for row in expense_data]
    amounts = [float(row[1]) for row in expense_data]

    return render_template(
        "reports.html",
        total_income=total_income,
        total_expense=total_expense,
        savings=savings,
        categories=categories,
        amounts=amounts
    )

@app.route('/add_income', methods=['GET', 'POST'])
def add_income():

    if not login_required():
        return redirect(url_for('login'))

    if request.method == 'POST':

        source = request.form['source']
        amount = request.form['amount']
        income_date = request.form['income_date']
        user_id = session['user_id']

        query = """
INSERT INTO income (user_id, source, amount, income_date)
VALUES (%s, %s, %s, %s)
"""

        cursor.execute(query, (user_id,source, amount, income_date))
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_income.html')

@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():

    if not login_required():
        return redirect(url_for('login'))

    if request.method == 'POST':

        category = request.form['category']
        amount = request.form['amount']
        expense_date = request.form['expense_date']
        user_id = session['user_id']

        query = """
INSERT INTO expenses (user_id, category, amount, expense_date)
VALUES (%s, %s, %s, %s)
"""

        cursor.execute(query, (user_id, category, amount, expense_date))
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_expense.html')

@app.route('/delete_income/<int:id>')
def delete_income(id):

    query = "DELETE FROM income WHERE id=%s AND user_id=%s"

    cursor.execute(query, (id, session['user_id']))
    db.commit()

    return redirect(url_for('dashboard'))

@app.route('/delete_expense/<int:id>')
def delete_expense(id):

    query = "DELETE FROM expenses WHERE id=%s AND user_id=%s"

    cursor.execute(query, (id, session['user_id']))
    db.commit()

    return redirect(url_for('dashboard'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        query = """
        INSERT INTO users (fullname, email, password)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (fullname, email, hashed_password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))

@app.route('/ai_advisor', methods=['GET', 'POST'])
def ai_advisor():

    if not login_required():
        return redirect(url_for('login'))

    answer = ""

    if request.method == "POST":

        question = request.form["question"]

        # Get Total Income
        cursor.execute(
            "SELECT SUM(amount) FROM income WHERE user_id=%s",
            (session['user_id'],)
        )
        total_income = cursor.fetchone()[0] or 0

        # Get Total Expense
        cursor.execute(
            "SELECT SUM(amount) FROM expenses WHERE user_id=%s",
            (session['user_id'],)
        )
        total_expense = cursor.fetchone()[0] or 0

        # Calculate Savings
        savings = total_income - total_expense

        # Get Expense Category Summary
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            WHERE user_id=%s
            GROUP BY category
            ORDER BY SUM(amount) DESC
        """, (session['user_id'],))

        expense_categories = cursor.fetchall()

        try:
            answer = ask_ai(
                question,
                total_income,
                total_expense,
                savings,
                expense_categories
            )

        except Exception as e:
            answer = f"AI Error: {e}"

    return render_template(
        "ai_advisor.html",
        answer=answer
    )

if __name__ == '__main__':
    app.run(debug=True)