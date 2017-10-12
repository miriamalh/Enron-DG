# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 20:19:46 2017
@author: miriam
"""

import pandas as pd
from email.parser import Parser


def parse_email(row, attribute):
    email = Parser().parsestr(row['message'])
    if attribute == 'content':
        return email.get_payload()
    else:
        return email[attribute]


file_path = '/Users/Miriam/Desktop/DG_test/emails.csv'
emails = pd.read_csv(file_path)

emails['Datetime'] = emails.apply(parse_email, axis=1, args=('date',))
emails['Sender'] = emails.apply(parse_email, axis=1, args=('from',))
emails['Recipients'] = emails.apply(parse_email, axis=1, args=('to',))
emails['Subject'] = emails.apply(parse_email, axis=1, args=('subject',))
emails['Content'] = emails.apply(parse_email, axis=1, args=('content',))

emails['Datetime'] = pd.to_datetime(emails['Datetime'])
emails['Time sent'], emails['Date sent'] = emails['Datetime'].apply(lambda x: x.time()), \
                                          emails['Datetime'].apply(lambda x: x.date())

emails = emails.sort_values(by='Datetime',ascending=True)

