#prawless/entities/subreddit/rules.py
class SubredditRule:
    """A class representing a single rule in a Reddit subreddit."""
    
    def __init__(self, data):
        self._data = data

    @property
    def short_name(self) -> str:
        return self._data.get('short_name')

    @property
    def description(self) -> str:
        return self._data.get('description')

    @property
    def created_utc(self) -> float:
        return self._data.get('created_utc')
    
    @property
    def violation_reason(self) -> str:
        return self._data.get('violation_reason')
    
    @property
    def priority(self) -> int:
        return self._data.get('priority')

    def __str__(self):
        return self.short_name


class SubredditRules:
    """A class representing all the rules of a Reddit subreddit."""
    
    def __init__(self, data: list):
        self._rules = [SubredditRule(rule_data) for rule_data in data]

    @property
    def rules(self):
        return self._rules

    def __iter__(self):
        return iter(self._rules)

    def __getitem__(self, index):
        return self._rules[index]

    def __len__(self):
        return len(self._rules)

    def __str__(self):
        return ", ".join([rule.short_name for rule in self._rules])

