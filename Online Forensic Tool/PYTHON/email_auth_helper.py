import os
import sys

from datetime import datetime
from email.parser import BytesParser
from email.policy import default

# Get the names of all the fields present in an email's headers
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns a list of the names of all fields found in the email header file
#
def get_all_fieldnames(filename):

    # First find all the fields present in the email headers
    with open(filename, "rb") as fp:
        headers = BytesParser(policy=default).parse(fp, headersonly=True)

    fields = []
    # Add each field name to a list
    for j in headers:
        field_name = (j + ":")
        # add to the list only if it is not already added
        if field_name not in fields:
            fields.append(j + ":")

    return fields


# Get the values of the fields of interest present in an email's headers
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns the list of values for all the fields of interest found in the header
#
def get_all_fieldvalues(filename, fields_of_interest):

    field_values = [[] for i in range(len(fields_of_interest))]
    
    # We get all the field names present in the email header
    all_field_names = get_all_fieldnames(filename)

    # Parse the file looking for the fields of interest
    with open(filename, "r") as fp:
        temp = ""
        populating_field_index = -1
        for line in fp:
            # Get all the words in the current line
            words = line.split()

            # If the line is not empty
            if len(words) != 0:

                # If we are starting a new field, then record the previous value
                if words[0] in all_field_names:

                    # If we are currently recording a value
                    if populating_field_index != -1:
                        field_values[populating_field_index].append(temp)
                        temp = ""
                        populating_field_index = -1

                    # If we are starting a field of interest
                    if words[0] in fields_of_interest:
                        if (words[0] == "Received:") and (words[1] == "by"):
                            populating_field_index = fields_of_interest.index("Received: by")
                        else:
                            populating_field_index = fields_of_interest.index(words[0])
                        temp = line
                else:
                    # If we are currently recording a value
                    if populating_field_index != -1:
                        temp += line

    return field_values


# Main entry point function for the email header parser
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns the list of values for all the fields of interest found in the header
#
def email_header_parser(filename, fields_of_interest):

    error = []

    # Make sure it is a normal file and exists
    if not os.path.exists(filename):
        error = ("Error: The file %s was not found!\n" % args.FILE)
    elif not os.path.isfile(filename):
        error = ("Error: %s is not a file\n" % args.FILE)

    field_values = get_all_fieldvalues(filename, fields_of_interest)

    return field_values, error


def analyze_received_and_date_field(received_field, date_field):

    previous_timestamp = []
    current_timestamp = []

    results = [[] for i in range(1)]
    processed_field_vals = [[] for i in range(1)]
    timestamp_vals = []

    for current_entry in received_field:

        # Split the current entry
        temp = current_entry.split(";")
        temp = temp[-1]
        temp = temp.strip()
        temp = temp.split('(')
        temp = temp[0].strip()

        current_timestamp = datetime.strptime(temp, "%a, %d %b %Y %H:%M:%S %z")
        timestamp_vals.append(current_timestamp)

    timestamp_vals.append(datetime.strptime(date_field[0].strip(), "Date: %a, %d %b %Y %H:%M:%S %z"))

    results[0] = True
    previous_timestamp = []
    for current_timestamp in timestamp_vals:
        if previous_timestamp and current_timestamp:
            # The Received fields are arranged in reverse chronological order
            if (previous_timestamp < current_timestamp):
                results[0] = False
                break
        previous_timestamp = current_timestamp

    processed_field_vals[0] = timestamp_vals[::-1]

    return results, processed_field_vals


def analyze_auth_res_fields(auth_res_fields):
    results = True

    for current_list in auth_res_fields:

        for current_entry in current_list:
            # Split the current entry
            temp = current_entry.split()

            for current_sub_field in temp:

                if "spf" in current_sub_field or "dkim" in current_sub_field:
                    value = current_sub_field.split("=")
                    if value[1] == "fail":
                        results = False
                        break
    return results


# Main entry point function for the email header parser
#  @param filename the filename of an email (with header) saved as plaintext
#  @returns the list of values for all the fields of interest found in the header
#
def level_1_authenticator(filename, field_values, fields_of_interest):

    received_idx = fields_of_interest.index("Received:")
    date_idx = fields_of_interest.index("Date:")
    arc_auth_res_idx = fields_of_interest.index("ARC-Authentication-Results:")
    auth_res_idx = fields_of_interest.index("Authentication-Results:")
    message_id_idx = fields_of_interest.index("Message-ID:")
    from_idx = fields_of_interest.index("From:")
    to_idx = fields_of_interest.index("To:")
    subject_idx = fields_of_interest.index("Subject:")
    mime_ver_idx = fields_of_interest.index("MIME-Version:")
    dkim_sig_idx = fields_of_interest.index("DKIM-Signature:")
    received_by_idx = fields_of_interest.index("Received: by")
    return_path_idx = fields_of_interest.index("Return-Path:")

    results, processed_field_vals = analyze_received_and_date_field(field_values[received_idx], field_values[date_idx])

    results.append(analyze_auth_res_fields([field_values[arc_auth_res_idx], field_values[auth_res_idx]]))

    processed_field_vals.append(field_values[message_id_idx])
    processed_field_vals.append(field_values[from_idx])
    processed_field_vals.append(field_values[to_idx])
    processed_field_vals.append(field_values[subject_idx])
    processed_field_vals.append(field_values[mime_ver_idx])
    processed_field_vals.append(field_values[dkim_sig_idx])
    processed_field_vals.append(field_values[received_by_idx])
    processed_field_vals.append(field_values[return_path_idx])

    return results, processed_field_vals


def generate_report(filename, results, processed_field_vals, fields_of_interest):

    report_file_name = os.path.splitext(os.path.basename(filename))[0]
    report_file_name = report_file_name + "_rep.txt"
    report_file_path = os.path.join("..", "RESULTS", "EMAIL_HEADERS", report_file_name)

    verdict = "Authentic\n"

    final_str = ""

    if(results[0]):
        final_str = final_str + "Email traceback path timestamp: Pass\n"
    else:
        final_str = final_str + "Email traceback path timestamp: FAILED\n"
        verdict = "Tampered\n"

    if(results[1]):
        final_str = final_str + "Email Protocol Verification: Pass\n"
    else:
        final_str = final_str + "Email Protocol Verification: FAILED\n"
        verdict = "Tampered\n"

    for field_name in fields_of_interest:

        flen = len(field_name)

        if field_name in "Received:":
            final_str = final_str + "\n----------------------------------\n"
            final_str = final_str + "Mail Transit Timestamps:\n"
            final_str = final_str + "----------------------------------\n"

            for i in range(len(processed_field_vals[0])):

                if i == 0:
                    final_str = final_str + "Sent timestamp:        "
                elif i == len(processed_field_vals[0])-1:
                    final_str = final_str + "Received timestamp: "
                else:
                    final_str = final_str + "Travel timestamp:      "

                final_str = final_str + str(processed_field_vals[0][i]) + "\n"

        elif field_name in "Message-ID:":
            temp = str(processed_field_vals[1])
            temp = temp[flen+4:-5]
            final_str = final_str + "\n\n-----------------\n"
            final_str = final_str + "Message-ID:\n"
            final_str = final_str + "-----------------\n"
            final_str = final_str + temp

        elif field_name in "From:":
            temp = str(processed_field_vals[2])
            temp = temp[flen+3:-4]
            final_str = final_str + "\n\n----------\n"
            final_str = final_str + "From:\n"
            final_str = final_str + "----------\n"
            final_str = final_str + temp

        elif field_name in "To:":
            temp = str(processed_field_vals[3])
            temp = temp[flen+3:-4]
            final_str = final_str + "\n\n----------\n"
            final_str = final_str + "To:\n"
            final_str = final_str + "----------\n"
            final_str = final_str + temp

        elif field_name in "Subject:":
            temp = str(processed_field_vals[4])
            temp = temp[flen+3:-4]
            final_str = final_str + "\n\n----------\n"
            final_str = final_str + "Subject:\n"
            final_str = final_str + "----------\n"
            final_str = final_str + temp

        elif field_name in "MIME-Version:":
            temp = str(processed_field_vals[5])
            temp = temp[flen+3:-4]
            final_str = final_str + "\n\n--------------------\n"
            final_str = final_str + "MIME-Version:\n"
            final_str = final_str + "--------------------\n"
            final_str = final_str + temp

        elif field_name in "DKIM-Signature:":
            temp = str(processed_field_vals[6])
            temp = temp[flen+3:-4]
            temp = temp.replace(" ", "")
            temp = temp.replace("\\n", "<br>")
            final_str = final_str + "\n\n---------------------\n"
            final_str = final_str + "DKIM-Signature:\n"
            final_str = final_str + "---------------------\n"
            final_str = final_str + temp

        elif field_name in "Received: by":
            temp = str(processed_field_vals[7])
            temp = temp[flen+3:-4]
            temp = temp.replace("\\n", "<br>")
            temp = temp.split(';')
            temp = temp[0]
            final_str = final_str + "\n\n-----------------\n"
            final_str = final_str + "Received by:\n"
            final_str = final_str + "-----------------\n"
            final_str = final_str + temp

        elif field_name in "Return-Path:":
            temp = str(processed_field_vals[8])
            temp = temp[flen+4:-5]
            final_str = final_str + "\n\n-----------------\n"
            final_str = final_str + "Return-Path:\n"
            final_str = final_str + "-----------------\n"
            final_str = final_str + temp

    f = open(report_file_path, "w")
    f.write(final_str)
    f.close()

    return verdict + report_file_name + "\n"
