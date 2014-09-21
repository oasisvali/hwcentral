class Link(object):
    """
    Just a container class to hold the label and the id (passed as a url param) for a link in a viewmodel
    """

    def __init__(self, label, id, url_name = None):
        self.label = label
        self.id = id
        self.url_name = url_name