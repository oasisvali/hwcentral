from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe

from core.models import AssignmentQuestionsList
from core.utils.regex import check_substitution_tags, get_substitution_tag_contents, sub_substitution_tags


class AQLMetaDM(object):
    def __init__(self, pk, data):
        self.revision = data['revision']
        self.pk = pk

    def prep_render(self, user):
        """
        substitutes in any secure img urls into the revision string and marks it as safe html
        @param user:
        @return:
        """
        from cabinet.cabinet_api import get_aql_meta_img_url_secure

        assignment_questions_list = AssignmentQuestionsList.objects.get(pk=self.pk)

        # check that revision string has valid substitution tags
        check_substitution_tags(self.revision)

        # first find all img filenames that need to substituted with their secure img urls
        img_filenames = get_substitution_tag_contents(self.revision)

        # now build secure urls for all of them
        secure_img_urls = []
        for img_filename in img_filenames:
            secure_img_urls.append(get_aql_meta_img_url_secure(user, assignment_questions_list, img_filename))

        # now sub them back into the revision string
        self.revision = sub_substitution_tags(self.revision, secure_img_urls)

        # attach the img_reloader for img tags in the revision html
        self.revision = mark_safe(add_img_reloader(self.revision))


def add_img_reloader(html):
    html_soup = BeautifulSoup(html, 'html.parser')
    for img_tag in html_soup.find_all('img'):
        img_tag['onerror'] = 'img_reload(this);'
    return str(html_soup)
