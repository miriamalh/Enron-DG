 -*- coding: utf-8 -*-

import pandas as pd
from email.parser import Parser


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


def conversation(row):
    """To mark conversation instances"""
    if row['Recipients'] is None:
        return None
    elif row['Subject2'] == '' or row['Subject2'] == '(no subject)':
        return None
    elif row['count'] == 1:
        return 'single conversation'
    else:
        return 'Undefined'


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

# ------------------------------------------ Extract Conversations -------------------------------------
emails['count'] = emails.groupby('Subject2')['Subject2'].transform('count')
pd.isnull(emails['Recipients'])

# Mark None and 'single conversations'
emails['Conversation'] = emails.apply(conversation, axis=1)

#                           ====== Mark conversations between single addresses =======
sub_df = emails[['Sender', 'Recipients', 'Datetime', 'Subject', 'Subject2', 'Content', 'count', 'Conversation']].\
    dropna()
# drop emails sending to multiple addresses
sub_df = sub_df.loc[(sub_df['Recipients'].map(len) == 1) & (sub_df['Conversation'] != 'single conversation')]
