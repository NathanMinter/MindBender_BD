class Calculator:
    """Not a good calculator."""

    def add(self, *a):
        x = sum(a)
        return x

    def subtract(self, a, b):
        x = a - b
        return x

    def product(self, *a):
        result = 1
        for n in a:
            result = result * n
        return result
