from requests import Session
from html_form_to_dict import html_form_to_dict
from re import search
from json import loads
from random import random
from concurrent.futures import ThreadPoolExecutor

REGEX = r"var FB_PUBLIC_LOAD_DATA_ = (.*);"

def send_form(link: str) -> bool:
	# Set up session
	s = Session()

	# Add a fake browser user agent
	# (Should probably be randomized for each request, will this feature add later)
	s.headers.update({"user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.99.4951.54 Safari/537.36"})

	# Get the form (necessary for cookies & form metadata/hidden fields)
	resp = s.get(link)

	# Get the form metadata
	# This is a neat library which basically just searches for:
	# <input type="hidden" name="key" value="value">
	# And turns it into:
	# {"key": "value"}
	form = html_form_to_dict(resp.text)

	# Extract form questions from HTML
	questions = loads(search(REGEX, resp.text).group(1))[1][1]

	# Get question IDs
	q_ids = [question[4][0][0] for question in questions]

	# Insert random data into form for each question
	form.update({f"entry.{q_id}": str(random()) for q_id in q_ids})

	# Send the form
	status = s.post(link.replace("viewform", "formResponse"), data=form)

	# Return status code (Did the form send successfully?)
	return status.status_code == 200
