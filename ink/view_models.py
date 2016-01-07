from core.utils.labels import get_user_label, get_classroom_label
from core.view_models.base import FormViewModel, AuthenticatedVM, FormBody
from ink.urlnames import InkUrlNames


class IndexBody(FormBody):
    """
    Used to store the viewmodels that define the Index view
    """

    def __init__(self, main_form, password_form):
        super(IndexBody, self).__init__(main_form, InkUrlNames.INDEX.name)
        self.password_form = password_form

class ParentIdBody(FormBody):
    def __init__(self, student, parent_form):
        self.student_name = get_user_label(student)
        self.student_class = get_classroom_label(student.classrooms_enrolled_set.get())
        self.flagged = student.dossier.flagged
        self.email = student.email
        self.phone = student.dossier.phone
        self.secondary_email = student.dossier.secondaryEmail
        self.secondary_phone = student.dossier.secondaryPhone

        self.parent_form = parent_form

