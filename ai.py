import requests

def ask_ai(question, income, expense, savings, categories):

    category_text = ""

    for category, amount in categories:
        category_text += f"- {category}: ₹{amount}\n"

    prompt = f"""
You are FinGenie AI, a friendly personal financial advisor for Indian users.

Rules:
- Reply in simple Hinglish.
- Talk like chatting on WhatsApp.
- Never use difficult Hindi words.
- Keep answers short (4-8 lines).
- Use emojis naturally.
- Give practical financial advice.
- If user asks in English, reply in English.
- If user asks in Hinglish, reply in Hinglish.
- Always explain finance in simple language.
- Treat SIP as Systematic Investment Plan only.
- Use correct words and languages.

User Financial Data:
Total Income: ₹{income}
Total Expense: ₹{expense}
Savings: ₹{savings}
Expense Category Breakdown:

{category_text}

Use these categories while giving personalized advice.
Mention the highest expense category if relevant.

Use the user's financial data while giving advice.
If expenses are high compared to income, suggest reducing unnecessary expenses.
If savings are low, encourage better budgeting.
If savings are good, appreciate the user and suggest investment ideas.

User Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]