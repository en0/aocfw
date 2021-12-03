# AOC Framework

A framework for writing Advent of code solutions.

```python
from aocfw import SolutionBase


class Solution(SolutionBase[int, int]):
    def solve(self, data) -> int:
        return sum(data)


if __name__ == "__main__":
    Solution.run(source="./input.txt")
```

## Customize
```python
from aocfw import SolutionBase
from aocfw.typing import IParser, ILoader


class CustomParser(IParser):
    def parse(self, data):
        for d in data:
            yield str(d)
            
            
class CustomLoader(ILoader):
    def read(self, callback, **kwargs):
        kwargs.setdefault("foo", "bar")
        return callback(kwargs["foo"])

            
class Solution(SolutionBase):
    bindings = {
        IParser: CustomParser,
        ILoader: ILoader,
    }
    
    def solve(self, data) -> int:
        ...


if __name__ == "__main__":
    Solution.run(source="./input.txt")
```
