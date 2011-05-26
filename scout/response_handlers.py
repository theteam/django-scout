
class BaseResponseHandler(object):
    """
    The base response handler class, all new response handlers
    should subclass from this one.
    """

    def __init__(self, test, response):
        self.test = test
        self.response = response

    def handle_response(self):
        """
        This is the method called from the PingRunner,
        and is therefore the main control method. It
        does not need to return anything.
        """
        pass


class DummyResponseHandler(BaseResponseHandler):
    """
    A sample ResponseHandler which does nothing except 
    show an example of a ResponseHandler.
    """
    pass
