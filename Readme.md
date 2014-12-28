GAE Plivo utilty
---

Adapted from [plivo/plivo-python](https://github.com/plivo/plivo-python)

Features
---

- [x] send sms
- [ ] get sms
...

Install
---

    $ pip install gae-plivio

Use
---

```python

from gae_plivio import plivo

# Your PLIVO_AUTH_ID and PLIVO_AUTH_TOKEN can be found
# on your Plivo Dashboard https://manage.plivo.com/dashboard
PLIVO_AUTH_ID = "Enter your Plivo AUTH ID here"
PLIVO_AUTH_TOKEN = "Enter your Plivo AUTH TOKEN here"

# Enter your Plivo phone number. This will show up on your caller ID
plivo_number = "14153337777"

# Enter the phone number that you would like to receive your SMS
destination_number = "14153338888"

# Enter the SMS that you want to send
text = "Welcome to Plivo!"

message_params = {
  'src':plivo_number,
  'dst':destination_number,
  'text':text,
}
p = plivo.RestAPI(PLIVO_AUTH_ID, PLIVO_AUTH_TOKEN)
print p.send_message(message_params)

```

Example
---

```bash

  echo "PLIVO_NUMBER: ''" > test/secrets.yml
  echo "PLIVO_AUTH_ID: ''" >> test/secrets.yml
  echo "PLIVO_AUTH_TOKEN: ''" >> test/secrets.yml"
  make deps example

```

Test
---

    $ make deps test