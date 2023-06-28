import imaplib
import email
from email.utils import parseaddr
from email_classification.email_entity import Email
from email_classification.utils import extract_date_and_time
from email_classification.logger import logging


def get_emails_from_gmail(user, password, email_count ) -> list[Email]:

    # Connect to the Gmail IMAP server and login with your credentials
    imap_url = 'imap.gmail.com'

    my_mail = imaplib.IMAP4_SSL(imap_url)
    my_mail.login(user, password)

    # Select the folder from which you want to retrieve emails
    my_mail.select('Inbox')

    # Use the search method to find specific emails
    status, data = my_mail.search(None, 'ALL')
    email_ids = data[0].split()

    emails = []

    # Loop through the email ids and fetch the email using the RFC822 protocol
    for email_id in email_ids[:email_count]:

        status, data = my_mail.fetch(email_id, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        
        # Get the From, Date, and Subject fields of the email
        from_field = email_message['From']
        date_field = email_message['Date']
        subject_field = email_message['Subject']

        # Parse the From field to extract the sender's name and email
        sender_name, sender_email = parseaddr(from_field)

        # Get the Message-ID field of the email
        message_id = email_message['Message-ID'].strip('<>')
        
        # Construct a URL to view the email in your browser
        url = f'https://mail.google.com/mail/u/0/#search/rfc822msgid:{message_id}'
        
        # Print the From, Date, and Subject fields
        #print(f'From: {from_field}')
        #print(f'Date: {extract_date_and_time(date_field)}')
        #print(f'Subject: {subject_field}')

        # Print the sender's name and email
        #print(f'Sender name: {sender_name}')
        #print(f'Sender email: {sender_email}')
        
        # Check if the email is multipart
        if email_message.is_multipart():
            # Loop through the parts of the email
            for part in email_message.walk():
                # Get the content type of the part
                content_type = part.get_content_type()
                # Check if the content type is text/plain or text/html
                if content_type == 'text/plain' or content_type == 'text/html':
                    # Get the payload of the part
                    payload = part.get_payload(decode=True)
                    # Decode the payload and print it
                    message_body = payload.decode(part.get_content_charset())
                    # print(f'Message: {message_body}')
        else:
            # Get the payload of the email
            payload = email_message.get_payload(decode=True)
            # Decode the payload and print it
            message_body = payload.decode(email_message.get_content_charset())
            # print(f'Message: {message_body}')

        an_email = Email(
            sender_email_address=sender_email,
            subject=subject_field,
            date_time=extract_date_and_time(date_field),
            contents=message_body, 
            url = url
        )

        emails.append(an_email)

    return emails


"""try :     
    emails = get_emails_from_gmail("sfsfs", "dfs",3)
    for email in emails :
        print(email.sender_email_address)
        print(email.subject)
        print(email.date_time)
except Exception as e:
    if 'AUTHENTICATIONFAILED' in str(e.args[0]):
        print("Login failed.")
    else :
        raise Exception(e)"""



