class NoAPIResultFetchedError(Exception):
    def __init__(self):
        super().__init__("API result data is empty. Did you forget to first fetch the data?")