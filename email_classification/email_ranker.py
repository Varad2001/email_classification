import os, sys
import pickle
from email_classification.email_entity import Email
from sklearn.feature_extraction.text import CountVectorizer
from email_classification.config import EMAIL_RANKER_MODEL_PATH


def get_rank(an_email):

    with open(EMAIL_RANKER_MODEL_PATH, 'rb') as f:
        features = pickle.load(f)

    volume_feature = features['volume_feature']
    similar_threads_data = features['similar_thread_feature']
    thread_activity = features['thread_activity_feature']
    term_weights = features['term_weights']
    msg_weights = features['msg_weights']

    # 1st weight : based on the freq of the sender 
    if an_email.sender_email_address in list(volume_feature.index):
        email_freq_wt = volume_feature[an_email.sender_email_address]
    else :
        email_freq_wt = 1
    #print(f"Email freq weight : {email_freq_wt}")

    # 2nd weight : if the sender is in threads
    sender_in_thread = similar_threads_data[similar_threads_data['sender_email_address'] == an_email.sender_email_address]
    if len(sender_in_thread):
        sender_in_thread_wt = sender_in_thread['weights'].values[0]
    else :
        sender_in_thread_wt = 1
    #print(f"Sender in thread weight : {sender_in_thread_wt}")

    # 3rd weight : if the subject is part of a thread
    # convert to lowercase
    thread_activity['Thread_subject'] = thread_activity['Thread_subject'].map(lambda x : x.lower())

    if an_email.subject.lower() in list(thread_activity['Thread_subject']):
        subject_in_thread_wt = thread_activity[thread_activity['Thread_subject'] == an_email.subject]['Weight'].values[0]
    else :
        subject_in_thread_wt = 1
    #print(f"Subject in thread weight : {subject_in_thread_wt}")

    # 4th weight : terms in the subject 
    text = [an_email.subject]
    count_vec = CountVectorizer(stop_words='english')
    count_matrix = count_vec.fit_transform(text)
    terms = count_vec.get_feature_names_out()

    wts = [term_weights[term_weights['term'] == x]['weight'].values[0] for x in terms if len(term_weights[term_weights['term'] == x])]
    if len(wts):
        subject_terms_wt = sum(wts) / len(wts)
    else :
        subject_terms_wt = 1

    #print(f"Terms in subject weight : {subject_terms_wt}")

    # 5th weight : terms in the message
    text = [an_email.contents]
    count_vec = CountVectorizer(stop_words='english')
    count_matrix = count_vec.fit_transform(text)
    terms = count_vec.get_feature_names_out()

    wts = [msg_weights[msg_weights['term'] == x]['weight'].values[0] for x in terms if len(msg_weights[msg_weights['term'] == x])]
    if len(wts):
        content_terms_wt = sum(wts) / len(wts)
    else :
        content_terms_wt = 1

    #print(content_terms_wt)

    rank = email_freq_wt * sender_in_thread_wt * subject_in_thread_wt * subject_terms_wt * content_terms_wt

    return rank

    
    

