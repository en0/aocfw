# AOC Framework

A framework for writing Advent of code solutions.

## Basic Usage

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

## Create a unittest

```python
from unittest import TestCase, main
from aocfw import TestCaseMixin

# assuming p1.py contains a Solution object that extends SolutionBase
from p1 import Solution


class SolutionTest(TestCase, TestCaseMixin):

    solution = Solution
    source = "sample.txt"
    # or sample = StringIO("1,2,3,4,5")
    given = 7


if __name__ == "__main__":
    main()
```

## Testing Bits

```python
from unittest import TestCase, main
from aocfw import TestCaseMixin
from p1 import Solution


class SolutionTest(TestCase, TestCaseMixin):

    solution = Solution
    source = "sample.txt"
    given = None # None disables the "given" test
    
    def test_some_thing(self):
        data = self.get_parsed_data()
        ans = Solution().some_thing(data)
        self.assertEqual(ans, "foo")

if __name__ == "__main__":
    main()
```
