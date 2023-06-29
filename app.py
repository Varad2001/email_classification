from flask import Flask, request, render_template, jsonify

from email_classification.email_ranker import get_rank
from email_classification.gmail_connector import get_emails_from_gmail
from email_classification.email_entity import Email
from email_classification.exception import EmailClassificationException
from email_classification.logger import logging
from email_classification.config import EMAIL_API
import requests, os
import pickle
from threading import Thread


app = Flask(__name__)

OUTPUT_FILE_DIR = os.path.join(os.getcwd(), "static")
OUTPUT_FILE = 'output.pkl'
os.makedirs(OUTPUT_FILE_DIR, exist_ok=True)
OUTPUT_FILE_PATH = os.path.join(OUTPUT_FILE_DIR, OUTPUT_FILE)


@app.route("/")
def hello():
    if os.path.isfile(OUTPUT_FILE_PATH):
        os.remove(OUTPUT_FILE_PATH)
    return render_template("index.html")


@app.route('/result', methods=['POST'])
def result():
    
    logging.info(">>>>>>>>>>>>>>  Inside /result route ...   <<<<<<<<<<<<<<<")

    if os.path.isfile(OUTPUT_FILE_PATH):
        logging.info(">>> Response found.")

        with open(OUTPUT_FILE_PATH,  'rb') as f:
            unpickler = pickle.Unpickler(f)
            response = unpickler.load()
        
        if response['status'] == 200 :
            sorted_emails = response['sorted_emails']

            logging.info(f">>> Response : {response['message']}")

            return jsonify({
            'response' : 'done',
            'template' : render_template("result.html", sorted_emails=sorted_emails)
            })
        
        elif response['status'] == 401:
            logging.info(f">>> Response : {response['message']}")

            return jsonify({
            'response' : 'done',
            'template' : f"<p>{response['message']} <br> Error : {response['Error']}</p>"
            })
        
        else :
            logging.info(f">>> Response : {response['message']}")

            return jsonify({
            'response' : 'done',
            'template' : f"<p>{response['Error']}</p>"
            })
    
    else :
        logging.info(">>> Response not found.")
        return jsonify({'response' : 'na'})



def get_emails(email, password, num_emails):
        
    logging.info(">>> get_emails thread began...")
    try :
        emails = get_emails_from_gmail(user=email, password=password, email_count=num_emails)
        for email in emails:
            email.rank = get_rank(email)

        logging.info(f">>> Ranks retrieved successfully for given {len(emails)} emails...")

        sorted_emails = sorted(emails, key=lambda email: email.rank, reverse=True)

        logging.info(">>> Returning positive response.... ")

        response = {
                'message': 'Success',
                'status' : 200,
                'sorted_emails' : sorted_emails
            }
        
    except EmailClassificationException as e:

        # if username or password does not match
        if 'AUTHENTICATIONFAILED' in str(e.args[0]):
            response = {
                'message' : "Invalid credentials. Either username or password entered are incorrect.",
                'status' : 401,
                'Error' : str(e.args[0])
            }
        else :
            response =  {
                'message' : "Error occurred . ",
                'status' : 500,
                'Error' : str(e.args[0])
            }

    
    
    with open(OUTPUT_FILE_PATH, 'wb') as f:
        pickle.dump(response, f)
    
    logging.info(f">>> get_emails thread complete. ")



@app.route("/get_emails", methods = ['POST'])
def start_get_emails_process():
    if request.method == 'POST':

        logging.info(">>>>>>>>>>>>>>> Inside  /get_emails api request ... <<<<<<<<<<<<<")

        email = request.form['email']
        password = request.form['password']
        num_emails = int(request.form['num_emails'])

        t = Thread(target=get_emails, args=(email, password, num_emails))
        t.start()
        
        logging.info(f">>> Starting get_emails thread .")

        logging.info(">>>  /get_emails complete.")

        return render_template("emails.html")
    



if __name__ == '__main__':
    app.run(debug=True)
