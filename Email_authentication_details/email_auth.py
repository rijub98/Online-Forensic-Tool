#! C:/Users/riju/AppData/Local/Programs/Python/Python310/python.exe

import sys
import os

import email_auth_helper

# Get the filename from the command argument
filename = sys.argv[1]

src_dir = os.path.join("..", "UPLOADS", "EMAIL_HEADERS")
src_file_path = os.path.join(src_dir, filename)

fields_of_interest = ["Received:", "Date:", "ARC-Authentication-Results:", "Authentication-Results:", "Message-ID:", "From:", "To:", "Subject:", "MIME-Version:", "DKIM-Signature:", "Received: by", "Return-Path:"]

# Call the email header parser to get the field values
field_values, error = email_auth_helper.email_header_parser(src_file_path, fields_of_interest)

if error:
    print(error)

else:
    results, processed_field_vals = email_auth_helper.level_1_authenticator(src_file_path, field_values, fields_of_interest)

    to_print = email_auth_helper.generate_report(filename, results, processed_field_vals, fields_of_interest)
    print(to_print)
