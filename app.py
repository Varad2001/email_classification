from flask import Flask, request, render_template
from email_classification.email_ranker import get_rank
from email_classification.gmail_connector import get_emails_from_gmail
from email_classification.email_entity import Email

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    email = request.form['email']
    password = request.form['password']
    num_emails = int(request.form['num_emails'])
    
    emails = get_emails_from_gmail(user=email, password=password, email_count=num_emails)

    for email in emails:
        email.rank = get_rank(email)

    sorted_emails = sorted(emails, key=lambda email: email.rank, reverse=True)

    return render_template("result.html", sorted_emails= sorted_emails)

if __name__ == '__main__':
    app.run(debug=True)
