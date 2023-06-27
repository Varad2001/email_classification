import os
from email_classification.gmail_connector import get_emails_from_gmail
from email_classification.email_ranker import get_rank


if __name__ == '__main__' :

    emails = get_emails_from_gmail(4)
    for email in emails:
        email.rank = get_rank(email)

    sorted_emails = sorted(emails, key=lambda email: email.rank, reverse=True)
    for an_email in sorted_emails:
        print(an_email.sender_email_address)
        print(an_email.subject)
        print()
