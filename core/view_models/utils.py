class Link(object):
    """
    Just a container class to hold the label and the id (passed as a url param) for a link in a viewmodel
    """

    def __init__(self, label, urlname, id=None, section_id=None):
        self.label = label
        self.id = id
        self.urlname = urlname
        self.section_id = section_id