class InvalidTestException(Exception):
    """
        2013-08-24:
            Raised for the harness to short-circuit a test
    """
    
    def __init__(self, message, path=None):
        self.message = message
        self.path = path
        Exception.__init__(self, message, path)
        
    def __str__(self):
        path = self.path or "self"
        return " ".join([path, self.message])
