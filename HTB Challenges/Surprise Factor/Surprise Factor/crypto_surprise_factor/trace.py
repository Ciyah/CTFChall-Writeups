import json
from dataclasses import dataclass, field

@dataclass
class TraceCollector:
    tracked_functions: set = field(default_factory=set)
    trace: list = field(default_factory=list)
    legend: dict = field(default_factory=dict)

    def register(self, name, symbol):
        self.legend[name] = symbol

    def configure(self, tracked_functions):
        self.tracked_functions = set(tracked_functions or set())

    def reset(self):
        self.trace.clear()

    def record(self, name):
        if name in self.tracked_functions:
            self.trace.append(self.legend[name])

    def get_trace(self):
        return list(self.trace)

    def export_json(self, path, metadata):
        payload = dict(metadata)
        payload["legend"] = {
            name: symbol
            for name, symbol in self.legend.items()
            if name in self.tracked_functions
        }
        payload["trace"] = self.get_trace()
        with open(path, "w", encoding="ascii") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)


TRACE = TraceCollector()

def traceable(name, symbol):
    TRACE.register(name, symbol)

    def decorator(func):
        def wrapper(*args, **kwargs):
            TRACE.record(name)
            return func(*args, **kwargs)

        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        return wrapper

    return decorator
