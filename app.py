from flask import Flask, request, render_template, jsonify
from email_classification.email_ranker import get_rank
from email_classification.gmail_connector import get_emails_from_gmail
from email_classification.email_entity import Email
import requests
from email_classification.config import EMAIL_API

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    email = request.form['email']
    password = request.form['password']
    num_emails = int(request.form['num_emails'])
    response = requests.post(EMAIL_API, 
                             data={
                                 'email': email,
                                 'password' : password,
                                 'num_emails' : num_emails
                                 })
    response = response.json()
    if response['status'] == 200 :
        return render_template("result.html", sorted_emails=response['sorted_emails'])
    elif response['status'] == 401:
        return f"<p>{response['message']} <br> Error : {response['Error']}</p>"
    else :
        return f"<p>{response['Error']}</p>"



@app.route("/get_emails", methods = ['POST'])
def get_emails():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        num_emails = int(request.form['num_emails'])
        
        try :
            emails = get_emails_from_gmail(user=email, password=password, email_count=num_emails)
            for email in emails:
                email.rank = get_rank(email)

            sorted_emails = sorted(emails, key=lambda email: email.rank, reverse=True)

            return jsonify(
                {
                    'message': 'Success',
                    'status' : 200,
                    'sorted_emails' : sorted_emails
                }
            )
        except Exception as e:
            # if username or password does not match
            if 'AUTHENTICATIONFAILED' in str(e.args[0]):
                return jsonify({
                    'message' : "Invalid credentials. Either username or password entered are incorrect.",
                    'status' : 401,
                    'Error' : str(e)
                })
            else :
                return jsonify({
                    'message' : "Error occurred . ",
                    'status' : 500,
                    'Error' : str(e)
                })

        
    


if __name__ == '__main__':
    app.run(debug=True)
