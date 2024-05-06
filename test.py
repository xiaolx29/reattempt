import pytest
from reattempt import StandardReAttempt

def test_success():
  sra = StandardReAttempt()
  result = sra.run(lambda : return 1)
  assert result == (True, 1)

def test_exception():
  sra = StandardReAttempt()
  result = sra.run(lambda : raise Exception('exception')
  assert result == (False, None)
