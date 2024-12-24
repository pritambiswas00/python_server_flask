from typing import Generic, TypeVar, Union, Callable

# Define type variables
T = TypeVar("T")  # Success type
E = TypeVar("E")  # Error type

class Result(Generic[T, E]):
    """Monadic Result type to represent success or failure."""
    
    def __init__(self, is_ok: bool, value: Union[T, E]):
        self._is_ok = is_ok
        self._value = value

    @staticmethod
    def Ok(value: T) -> 'Result[T, E]':
        return Result(True, value)

    @staticmethod
    def Err(error: E) -> 'Result[T, E]':
        return Result(False, error)

    def is_ok(self) -> bool:
        return self._is_ok

    def is_err(self) -> bool:
        return not self._is_ok

    def unwrap(self) -> T:
        """Unwraps the result if it's Ok, otherwise raises an exception."""
        if self._is_ok:
            return self._value
        raise ValueError(f"Called unwrap on an Err value: {self._value}")

    def unwrap_err(self) -> E:
        """Unwraps the error if it's Err, otherwise raises an exception."""
        if not self._is_ok:
            return self._value
        raise ValueError(f"Called unwrap_err on an Ok value: {self._value}")

    def map(self, func: Callable[[T], T]) -> 'Result[T, E]':
        """Applies a function to the value if it's Ok."""
        if self._is_ok:
            try:
                return Result.Ok(func(self._value))
            except Exception as e:
                return Result.Err(e)
        return self

    def map_err(self, func: Callable[[E], E]) -> 'Result[T, E]':
        """Applies a function to the error if it's Err."""
        if not self._is_ok:
            return Result.Err(func(self._value))
        return self

    def __repr__(self) -> str:
        if self._is_ok:
            return f"Ok({self._value})"
        return f"Err({self._value})"
