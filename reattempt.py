# reattempt.py
from typing import Callable, Type, Tuple, TypeVar, Optional, Union

T = TypeVar('T')  # return value type


class ReAttempt:
	def __init__(
		self,
		max_retries: int = 3,  # positive integer
		acceptable_exception: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
		on_success: Optional[Callable[[int, int, T], None]] = None,
		on_exception: Optional[Callable[[int, int, Exception], None]] = None,
		pass_retry_info: bool = False
	):
		self._max_retries = max_retries
		self._acceptable_exception = acceptable_exception
		self._on_success = self.default_on_success if on_success is None else on_success
		self._on_exception = self.default_on_exception if on_exception is None else on_exception
		self._pass_retry_info = pass_retry_info
	
	def default_on_success(self, retry_index: int, max_retries: int, result: T) -> None:
		print('\tAttempt {}/{}: Result: {}.'.format(retry_index + 1, max_retries, result))

	def default_on_exception(self, retry_index: int, max_retries: int, exception: Exception) -> None:
		print('\tAttempt {}/{}: Exception: {}{}.'.format(retry_index + 1, max_retries, type(exception), exception))
	
	def attempt(self, func: Callable[..., T], retry_index: int, *args, **kwargs) -> T:
		if self._pass_retry_info:
			kwargs.update({'retry_index': retry_index, 'max_retries': self._max_retries})
		result = func(*args, **kwargs)
		return result
	
	def raise_or_continue(self, exception: Exception) -> bool:
		return isinstance(exception, self._acceptable_exception)
	
	def run(self, func: Callable[..., T], *args, **kwargs) -> Tuple[bool, Optional[T]]:
		for retry_index in range(self._max_retries):
			try:
				result = self.attempt(func, retry_index, *args, **kwargs)
				self._on_success(retry_index, self._max_retries, result)
				return True, result
			except Exception as exception:
				self._on_exception(retry_index, self._max_retries, exception)
				if self.raise_or_continue(exception):
					continue
				else:
					raise
		return False, None


class QuietReAttempt(ReAttempt):
	def __init__(
		self,
		max_retries: int = 3,
		acceptable_exception: Union[Type[Exception], Tuple[Type[Exception], ...]] = Exception,
		on_success: Optional[Callable[[int, T], None]] = None,
		on_exception: Optional[Callable[[int, Exception], None]] = None, pass_retry_info: bool = False
	):
		super().__init__(max_retries, acceptable_exception, on_success, on_exception, pass_retry_info)
		
	def default_on_success(self, retry_index: int, max_retries: int, result: T) -> None:
		pass
	
	def default_on_exception(self, retry_index: int, max_retries: int, exception: Exception) -> None:
		pass
