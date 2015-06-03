__author__ = 'hrishikesh'


class Parent_trend_graph(object):
    """

    for the graph in the parent view to get info on the student's subject and avg and class teacher etc
    """

    def __init__(self, user, sub_listings, average, sub_ticker=None):
        self.user_subjects = user.userinfo.school.name
        self.sub_ticker = sub_ticker
        self.listings = sub_listings
        self.average = average
