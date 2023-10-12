# prawless/core/paginator.py

class Paginator:
    """A class for managing pagination parameters."""

    def __init__(self):
        self.after = None
        self.before = None
        self.limit = None
        self.count = 0
        self.show = None

    def get_params(self) -> dict:
        """
        Get pagination parameters as a dictionary.

        Returns:
            dict: A dictionary containing pagination parameters.
        """
        params = {
            'after': self.after,
            'before': self.before,
            'limit': self.limit,
            'count': self.count,
            'show': self.show
        }
        return {k: v for k, v in params.items() if v is not None}
