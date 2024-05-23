from functools import partial
from typing import List
from reattempt import ReAttempt

raise_lists = [
    [False, False, False],
    [True, True, True],
    [True, True, False],
    [True, False, False]
]

def function(raise_list: List[bool], retry_index: int, max_retries: int):
    if raise_list[retry_index]:
        raise Exception('Exception')
    else:
        return 'no exception'


if __name__ == '__main__':
    re_attempt = ReAttempt(pass_retry_info = True)
    for raise_list in raise_lists:
        print('Running test of ReAttempt:')
        print('Raise List: {}'.format(raise_list))
        result = re_attempt.run(partial(function, raise_list = raise_list))
        print('Return: {}'.format(result))