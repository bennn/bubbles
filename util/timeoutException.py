class TimeoutException(Exception):
    """
        2013-08-24:
            Raised for the harness when a test case times out
    """
    
    def __init__(self, path=None):
        self.path = path
        Exception.__init__(self, path)
        
    def __str__(self):
        return self.path or "self"
