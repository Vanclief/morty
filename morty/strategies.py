spec = importlib.util.spec_from_file_location("Delta", "./strategies/delta.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.Delta()

# class Strategies:
    # def __init__(self):
        # self.delta = Delta
