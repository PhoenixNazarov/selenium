
import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')

mail.login('nikitakrol86@gmail.com', '2587Sdr545')

mail.select("inbox")

result, data = mail.search(None, "ALL")
ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-2]
result, data = mail.fetch(latest_email_id, "(RFC822)")

raw_email = data[0][1]

import email
email_message = email.message_from_string(raw_email.decode('utf-8'))

for part in email_message.walk():
    # each part is a either non-multipart, or another multipart message
    # that contains further parts... Message is organized like a tree
    if part.get_content_type() == 'text/plain':
        code = (part.get_payload(None, True)) # prints the raw text

# code = get_first_text_block(email_message)
code = (code.decode(errors = 'ignore')).split()
d_code = 0
for i in code:
    if i.isdigit():
        if len(i) ==
        print(i)
print(code)
import base64
# code = base64.b64decode(a)
import re
nums ='qweqwe 123'
nums = re.findall(r'\d+', code)
nums = [int(i) for i in nums]
print(nums)