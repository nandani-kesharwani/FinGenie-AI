# 💰 FinGenie AI

FinGenie AI is an AI-powered personal financial management web application designed to help users track their income, expenses, savings, and financial habits in one place.

The project combines a Flask-based web application with MySQL for financial data management and a local AI advisor powered by Ollama and Llama 3.2.

---

## 🎯 Objectives

- Track personal income and expenses.
- Calculate total income, expenses, and savings.
- Maintain separate financial records for each user.
- Provide graphical financial reports.
- Analyze expenses by category.
- Provide AI-powered financial guidance.
- Support simple English and Hinglish financial queries.
- Protect user passwords using password hashing.
- Keep AI processing local using Ollama.

---

## ✨ Features

### 👤 User Authentication
- User registration
- Secure login
- Logout
- Password hashing using Flask-Bcrypt
- Session-based user authentication

### 💵 Income Management
- Add income records
- View income history
- Delete income records
- Calculate total income

### 💸 Expense Management
- Add expense records
- View expense history
- Delete expense records
- Categorize expenses
- Calculate total expenses

### 📊 Financial Reports
- Total income
- Total expenses
- Total savings
- Income vs expense bar chart
- Expense category pie chart

### 🤖 AI Financial Advisor
FinGenie AI provides simple financial guidance using a locally running Llama 3.2 model through Ollama.

Users can ask questions such as:

- How can I save more money?
- How much should I save every month?
- What is SIP?
- How can I reduce my expenses?
- Mere expenses bahut zyada hain, kya karu?

The AI can use the user's financial summary to provide personalized suggestions.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application backend |
| MySQL | Database |
| SQL | Database operations |
| HTML | Web page structure |
| CSS | Styling |
| Bootstrap | Responsive UI |
| JavaScript | Client-side functionality |
| Chart.js | Financial charts |
| Flask-Bcrypt | Password hashing |
| Jinja2 | Dynamic HTML templates |
| Ollama | Local AI runtime |
| Llama 3.2 | AI financial advisor |

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
HTML / Bootstrap Frontend
  │
  ▼
Flask Application
  │
  ├──────────────► MySQL Database
  │                  │
  │                  ├── Users
  │                  ├── Income
  │                  └── Expenses
  │
  └──────────────► AI Advisor
                       │
                       ▼
                    Ollama
                       │
                       ▼
                   Llama 3.2

                   