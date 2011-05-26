
class DummyResponseHandler(object):
    """
    A sample ResponseHandler which does nothing
    but shows how the response handling can be 
    extended.
    """

    def __init__(self, test, response):
        self.test = test
        self.response = response
