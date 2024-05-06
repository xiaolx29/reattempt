# reattempt
A simple retry library for python

Example:
```python
import requests
from reattempt import ReAttempt

def get_response_from_github(**kwargs):
  response = requests.get(**kwargs)
  response.raise_for_status()
  return response

retry = ReAttempt(max_retries = 5, acceptable_exception = (requests.exceptions.Timeout, requests.exceptions.RequestException))
print(f'Trying to get response from github.')
success, result = retry.run(get_response_from_github, url = 'https://github.com/xiaolx29/reattempt', timeout = 20)
print(result.text if success else 'Failed after 5 attempts.')
```
