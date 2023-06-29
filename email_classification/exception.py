import os, sys

def error_msg_detail(error, error_details : sys):
    _, _, exc_tb = error_details.exc_info()

    file_name = exc_tb.tb_frame.f_code.co_filename
    error_msg = "Error occured in script name [{0}] : line no [{1}] : error : [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error))
    
    return error_msg

class EmailClassificationException(Exception):
    def __init__(self, error_msg, error_detail : sys):
        self.error_message = error_msg_detail(
            error_msg, error_details = error_detail
        )

    def __str__(self):
        return self.error_message
    