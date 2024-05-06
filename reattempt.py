# reattempt.py
from typing import Callable, Type, Tuple, TypeVar, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')


class ReAttempt(ABC):
	def __init__(
		self,
		max_retries: int = 3,  # positive integer
		acceptable_exception: Tuple[Type[Exception], ...] = Exception,
		on_success: Optional[Callable[[int, int, T], None]] = None,
		on_exception: Optional[Callable[[int, int, Exception], None]] = None
	):
		self._max_retries = max_retries
		self._acceptable_exception = acceptable_exception
		self._on_success = self.default_on_success if on_success is None else on_success
		self._on_exception = self.default_on_exception if on_exception is None else on_exception
	
	@staticmethod
	@abstractmethod
	def default_on_success(retry_index: int, max_retries: int, result: T) -> None:
		pass
	
	@staticmethod
	@abstractmethod
	def default_on_exception(retry_index: int, max_retries: int, exception: Exception) -> None:
		pass
	
	@abstractmethod
	def run(self, func: Callable[..., T], *args, **kwargs) -> tuple[bool, Optional[T]]:
		pass


class StandardReAttempt(ReAttempt):
	@staticmethod
	def default_on_success(retry_index: int, max_retries: int, result: T) -> None:
		print(f'\tAttempt {retry_index + 1}/{max_retries}: Success.')
	
	@staticmethod
	def default_on_exception(retry_index: int, max_retries: int, exception: Exception) -> None:
		print(f'\tAttempt {retry_index + 1}/{max_retries}: {exception}')
	
	def run(self, func: Callable[..., T], *args, **kwargs) -> tuple[bool, Optional[T]]:
		for retry_index in range(self._max_retries):
			try:
				result = func(*args, **kwargs)
				self._on_success(retry_index, self._max_retries, result)
				return True, result
			except Exception as e:
				if isinstance(e, self._acceptable_exception):
					self._on_exception(retry_index, self._max_retries, e)
				else:
					raise
		return False, None
