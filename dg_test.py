# -*- coding: utf-8 -*-

import pandas as pd
from email.parser import Parser
from jwzthreading import make_message, thread


def parse_email(row, attribute):
    email = Parser().parsestr(row['message'])
    if attribute == 'content':
        return email.get_payload()
    else:
        return email[attribute]


def split_email_addresses(line):
    """To separate multiple email addresses"""
    if line:
        addrs = line.split(',')
        addrs = map(lambda x: x.strip(), addrs)
    else:
        addrs = None
    return addrs


file_path = raw_input('CSV file pathname: ')

# -------------------------------------------- Process File -------------------------------------------

# Extract required fields from messages
emails = pd.read_csv(file_path)
emails['Datetime'] = emails.apply(parse_email, axis=1, args=('date',))
emails['Sender'] = emails.apply(parse_email, axis=1, args=('from',))
emails['Recipients'] = emails.apply(parse_email, axis=1, args=('to',))
emails['Subject'] = emails.apply(parse_email, axis=1, args=('subject',))
emails['Content'] = emails.apply(parse_email, axis=1, args=('content',))
# Drop duplicate emails
emails = emails.drop_duplicates(subset=['Datetime', 'Sender', 'Recipients', 'Subject', 'Content'])
# Sort by Datetime
emails['Datetime'] = pd.to_datetime(emails['Datetime'])
emails['Time sent'], emails['Date sent'] = emails['Datetime'].apply(lambda x: x.time()), \
                                            emails['Datetime'].apply(lambda x: x.date())
emails = emails.sort_values(by='Datetime', ascending=True)
# Clean Recipients (split) and Subject columns
emails['Subject2'] = \
    emails['Subject'].apply(lambda x: x.replace('RE:', '').replace('Re:', '').replace('FW:', '').strip())
emails['Recipients'] = emails['Recipients'].map(split_email_addresses)
#Save file
emails.to_csv('output.csv')

# ------------------------------------------ Extract Conversations -------------------------------------
'''
Here I'll be using A.M. Kuchling's implementation of of an algorithm for threading mail
messages, as described at http://www.jwz.org/doc/threading.html.
'''


# Make a list of messages and convert to Message objects
## message_list = emails['message'].values.tolist() # error here, need to fix
## message_objects = map(make_message, message_list)



# Return a dictionary mapping subjects to Containers. Each container may
# have a .children attribute giving descendants of each message
## mapped_dict = thread(message_objects)
