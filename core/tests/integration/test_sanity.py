# These tests use the django dummy client to check the following:
#
# if all the basic views are functioning
# authentication/permission checks
# correct template use
# correct response codes
import getpass

from django.test import TestCase
from sh import git

from cabinet.cabinet_maintenance import delete_submission
from core.utils.constants import HWCentralEnv
from hwcentral import settings
from scripts.setup.full_school import DEBUG_SETUP_PASSWORD


class BasicSanityTest(TestCase):
    fixtures = ['skeleton', 'qa_school', 'sanity_test']

    @classmethod
    def setUpClass(cls):
        super(BasicSanityTest, cls).setUpClass()
        # ONLY FOR LOCAL
        if settings.ENVIRON == HWCentralEnv.LOCAL:
            # switch the cabinet to the sanity test branch
            user = getpass.getuser()
            git_cabinet = git.bake(_cwd='/home/%s/hwcentral-cabinet' % user)
            git_cabinet.stash('save', '-u')  # stash changes, including untracked files
            git_cabinet.fetch()
            git_cabinet.checkout('sanity_test')
            # no need to restart nginx at this point, sanity_test branch should only differ in terms of data not conf

    @classmethod
    def tearDownClass(cls):
        super(BasicSanityTest, cls).setUpClass()
        # ONLY FOR LOCAL
        if settings.ENVIRON == HWCentralEnv.LOCAL:
            # switch the cabinet back to the master branch
            user = getpass.getuser()
            git_cabinet = git.bake(_cwd='/home/%s/hwcentral-cabinet' % user)
            # cleaning up any changes made
            git_cabinet.clean('-df')
            git_cabinet.reset('--hard', 'HEAD')
            git_cabinet.checkout('master')
            git_cabinet.stash('apply')
            # no need to restart nginx at this point, sanity_test branch should only differ in terms of data not conf

    def check_response_code(self, path, expected_response_code):
        response = self.client.get(path)
        self.assertEqual(expected_response_code, response.status_code)
        return response

    def check_template_response_code(self, path, expected_template, expected_response_code):
        response = self.check_response_code(path, expected_response_code)
        self.assertEqual(expected_template, response.templates[0].name)
        return response

    def check_json_response_code(self, path, expected_response_code):
        response = self.check_response_code(path, expected_response_code)
        self.assertEqual('application/json', response['Content-Type'])
        return  response

    def check_login_redirect(self, path):
        response = self.client.get(path)
        self.assertRedirects(response, '/login/?next=' + path)
        return response

    def check_sleep_login_redirect(self, path):
        response = self.client.get(path)
        self.assertRedirects(response, '/login/?next=' + path, target_status_code=503)
        return response

    def check_admin_login_redirect(self, path):
        response = self.client.get(path)
        self.assertRedirects(response, '/admin/login/?next=' + path)

    def check_home_redirect(self, path):
        response = self.client.get(path)
        self.assertRedirects(response, '/home/')

    def test_sleep(self):
        with self.settings(ROOT_URLCONF = 'hwcentral.urls.sleep_mode'):
            self.check_template_response_code('/', 'index.html', 200)  # index does not have a sleep mode
            self.check_template_response_code('/login/', '503.html', 503)
            self.check_template_response_code('/home/', '503.html', 503)
            self.check_template_response_code('/admin/', '503.html', 503)
            self.check_template_response_code('/some/invalid/url/', '503.html', 503)
            self.check_sleep_login_redirect('/secure-static/someid/')

    def test_sphinx(self):
        self.check_template_response_code('/sphinx/', 'sphinx/index.html', 200)
        with self.settings(ROOT_URLCONF='hwcentral.urls.prod'):
            self.check_template_response_code('/sphinx/', '404.html', 404)

    def test_ink(self):
        self.check_login_redirect('/ink/')
        self.check_login_redirect('/ink/parent/3/')

        self.assertTrue(self.client.login(username='oasis_vali', password=DEBUG_SETUP_PASSWORD))
        self.check_template_response_code('/ink/', '404.html', 404)
        self.check_template_response_code('/ink/parent/3/', '404.html', 404)
        self.client.logout()

        self.assertTrue(self.client.login(username='seema_swami', password=DEBUG_SETUP_PASSWORD))
        self.check_template_response_code('/ink/', '404.html', 404)
        self.check_template_response_code('/ink/parent/3/', '404.html', 404)
        self.client.logout()

        self.assertTrue(self.client.login(username='neelam_chakraborty', password=DEBUG_SETUP_PASSWORD))
        self.check_template_response_code('/ink/', '404.html', 404)
        self.check_template_response_code('/ink/parent/3/', '404.html', 404)
        self.client.logout()

        self.assertTrue(self.client.login(username='sharmila_vali', password=DEBUG_SETUP_PASSWORD))
        self.check_template_response_code('/ink/', '404.html', 404)
        self.check_template_response_code('/ink/parent/3/', '404.html', 404)
        self.client.logout()

        self.assertTrue(self.client.login(username='hwcadmin_school_1', password=DEBUG_SETUP_PASSWORD))
        self.check_template_response_code('/ink/', 'ink/index.html', 200)
        self.check_template_response_code('/ink/parent/3/', 'ink/parent_id.html', 200)


    def test_unauthenticated(self):
        self.check_template_response_code('/', 'index.html', 200)
        self.check_template_response_code('/login/', 'login.html', 200)
        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_login_redirect('/home/')
        self.check_login_redirect('/settings/')
        self.check_login_redirect('/subject/1/')
        self.check_login_redirect('/classroom/1/')
        self.check_login_redirect('/subject/1/1/')
        self.check_login_redirect('/assignment/1/')
        self.check_login_redirect('/assignment/preview/1/')
        self.check_login_redirect('/assignment/1/')
        self.check_login_redirect('/submission/1/')
        self.check_login_redirect('/announcement/')
        self.check_login_redirect('/password/')
        self.check_login_redirect('/assignment/')
        self.check_login_redirect('/assignment/override/')
        self.check_login_redirect('/secure-static/someid/')

        self.check_login_redirect('/ajax/announcements/')
        self.check_login_redirect('/ajax/question-set-choice-widget/')
        self.check_login_redirect('/ajax/question-set-choice-widget/override/')

        self.check_login_redirect('/chart/student/1/')
        self.check_login_redirect('/chart/student/1/1/')
        self.check_login_redirect('/chart/subjectroom/1/')
        self.check_login_redirect('/chart/subjectteacher/1/')
        self.check_login_redirect('/chart/classteacher/1/1/')
        self.check_login_redirect('/chart/assignment/1/')
        self.check_login_redirect('/chart/completion/1/')
        self.check_login_redirect('/chart/standard-assignment/1/')

        self.assertRedirects(self.client.get('/logout/'), '/')


    def test_admin(self):
        self.check_admin_login_redirect('/admin/')
        self.check_admin_login_redirect('/admin/doc/')

        with self.settings(ROOT_URLCONF='hwcentral.urls.prod'):
            self.check_template_response_code('/admin/', '404.html', 404)
            self.check_template_response_code('/admin/doc/', '404.html',  404)

    def test_500(self):
        with self.settings(ROOT_URLCONF='hwcentral.urls.prod'):
            with self.assertRaises(Exception):
                self.client.get('/tTrNJnEzCxJfqtDBtWO2cOo6dsA/')
            #TODO: some way of verifying the right template (500.html) and response code (500) were returned

    def test_404(self):
        self.check_template_response_code('/invalid-url/', '404.html', 404)
        self.check_template_response_code('/some/invalid/url/', '404.html', 404)

    def test_authenticated_student(self):
        self.assertTrue(self.client.login(username='oasis_vali', password=DEBUG_SETUP_PASSWORD))
        self.check_home_redirect('/')
        self.check_home_redirect('/login/')

        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_template_response_code('/home/', 'authenticated/home/student.html', 200)
        self.check_template_response_code('/settings/', 'authenticated/settings/student.html', 200)
        self.check_template_response_code('/subject/1/', 'authenticated/subject_id/student.html', 200)
        self.check_template_response_code('/classroom/1/', '404.html', 404)
        self.check_template_response_code('/subject/1/1/', '404.html', 404)
        self.check_template_response_code('/assignment/1/', '404.html', 404)        #inactive
        self.assertRedirects(self.client.get('/assignment/2/'), '/submission/4/')   #uncorrected - new submission
        self.check_template_response_code('/assignment/3/', '404.html', 404)        #corrected
        self.check_template_response_code('/assignment/preview/1/', '404.html', 404)
        self.check_template_response_code('/submission/4/', 'authenticated/submission_id/uncorrected.html', 200)
        self.check_template_response_code('/submission/1/', 'authenticated/submission_id/corrected.html', 200)
        self.check_template_response_code('/announcement/', '404.html', 404)
        self.check_template_response_code('/password/', 'authenticated/password.html', 200)
        self.check_template_response_code('/assignment/', '404.html', 404)
        self.check_template_response_code('/assignment/override/', '404.html', 404)
        self.check_response_code('/secure-static/b2FzaXNfdmFsaTpodHRwOi8vbG9jYWxob3N0Ojk4NzgvcXVlc3Rpb25zL2NvbnRhaW5lcnMvMS8xLzgvMS8xL2ltZy8xLnBuZzpUV1dqeVl2ejR3MC0yQzNueWpkcWltZHFBams/', 200)

        self.check_json_response_code('/ajax/announcements/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/', 404)
        self.check_json_response_code('/ajax/question-set-choice-widget/override/', 404)

        self.check_json_response_code('/chart/student/3/', 200)
        self.check_json_response_code('/chart/student/3/1/', 200)
        self.check_json_response_code('/chart/subjectroom/1/', 404)
        self.check_json_response_code('/chart/subjectteacher/4/', 404)
        self.check_json_response_code('/chart/classteacher/7/1/', 404)

        self.check_json_response_code('/chart/assignment/3/', 200)  # corrected
        self.check_json_response_code('/chart/assignment/2/', 404)  # uncorrected
        self.check_json_response_code('/chart/assignment/1/', 404)  # inactive

        self.check_json_response_code('/chart/completion/3/', 404)
        self.check_json_response_code('/chart/completion/2/', 404)
        self.check_json_response_code('/chart/completion/1/', 404)

        self.check_json_response_code('/chart/standard-assignment/3/', 404)
        self.check_json_response_code('/chart/standard-assignment/2/', 404)
        self.check_json_response_code('/chart/standard-assignment/1/', 404)

        self.client.logout()

        # now login as another student to check some edge cases
        self.assertTrue(self.client.login(username='sidhant_pai', password=DEBUG_SETUP_PASSWORD))
        self.assertRedirects(self.client.get('/assignment/2/'), '/submission/3/')   #uncorrected - existing submission

        self.client.logout()
        delete_submission(4)    # cleanup newly created files from cabinet


    def test_authenticated_parent(self):
        self.assertTrue(self.client.login(username='sharmila_vali', password=DEBUG_SETUP_PASSWORD))
        self.check_home_redirect('/')
        self.check_home_redirect('/login/')

        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_template_response_code('/home/', 'authenticated/home/parent.html', 200)
        self.check_template_response_code('/settings/', 'authenticated/settings/parent.html', 200)
        self.check_template_response_code('/subject/1/', '404.html', 404)
        self.check_template_response_code('/classroom/1/', '404.html', 404)
        self.check_template_response_code('/subject/1/3/', 'authenticated/subject_id/parent.html', 200)
        self.check_template_response_code('/assignment/1/', '404.html', 404)                            #inactive
        self.check_template_response_code('/assignment/2/', 'authenticated/assignment_id.html', 200)    #uncorrected
        self.check_template_response_code('/assignment/3/', '404.html', 404)                            #corrected
        self.check_template_response_code('/assignment/preview/1/', '404.html', 404)
        self.check_template_response_code('/submission/1/', 'authenticated/submission_id/corrected.html', 200)
        self.check_template_response_code('/announcement/', '404.html', 404)
        self.check_template_response_code('/password/', 'authenticated/password.html', 200)
        self.check_template_response_code('/assignment/', '404.html', 404)
        self.check_template_response_code('/assignment/override/', '404.html', 404)
        self.check_response_code('/secure-static/c2hhcm1pbGFfdmFsaTpodHRwOi8vbG9jYWxob3N0Ojk4NzgvcXVlc3Rpb25zL2NvbnRhaW5lcnMvMS8xLzgvMS8xL2ltZy8xLnBuZzpkeEFJMDh6MFlXR1dBNzRxbUFBYWk3YVVMYXc/', 200)

        self.check_json_response_code('/ajax/announcements/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/', 404)
        self.check_json_response_code('/ajax/question-set-choice-widget/override/', 404)

        self.check_json_response_code('/chart/student/3/', 200)
        self.check_json_response_code('/chart/student/3/1/', 200)
        self.check_json_response_code('/chart/subjectroom/1/', 404)
        self.check_json_response_code('/chart/subjectteacher/4/', 404)
        self.check_json_response_code('/chart/classteacher/7/1/', 404)

        self.check_json_response_code('/chart/assignment/3/', 200)  # corrected
        self.check_json_response_code('/chart/assignment/2/', 404)  # uncorrected
        self.check_json_response_code('/chart/assignment/1/', 404)  # inactive

        self.check_json_response_code('/chart/completion/3/', 404)
        self.check_json_response_code('/chart/completion/2/', 404)
        self.check_json_response_code('/chart/completion/1/', 404)

        self.check_json_response_code('/chart/standard-assignment/3/', 404)
        self.check_json_response_code('/chart/standard-assignment/2/', 404)
        self.check_json_response_code('/chart/standard-assignment/1/', 404)

        self.client.logout()

    def test_authenticated_subjectteacher(self):
        self.assertTrue(self.client.login(username='seema_swami', password=DEBUG_SETUP_PASSWORD))
        self.check_home_redirect('/')
        self.check_home_redirect('/login/')

        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_template_response_code('/home/', 'authenticated/home/teacher.html', 200)
        self.check_template_response_code('/settings/', 'authenticated/settings/teacher.html', 200)
        self.check_template_response_code('/subject/1/', 'authenticated/subject_id/teacher.html', 200)
        self.check_template_response_code('/classroom/1/', '404.html', 404)
        self.check_template_response_code('/subject/1/3/', '404.html', 404)
        self.check_template_response_code('/assignment/1/', 'authenticated/assignment_id.html', 200)    #inactive
        self.check_template_response_code('/assignment/2/', 'authenticated/assignment_id.html', 200)    #uncorrected
        self.check_template_response_code('/assignment/3/', '404.html', 404)                            #corrected
        self.check_template_response_code('/assignment/preview/1/', 'authenticated/assignment_id.html', 200)
        self.check_template_response_code('/submission/1/', 'authenticated/submission_id/corrected.html', 200)
        self.check_template_response_code('/announcement/', 'authenticated/announcement.html', 200)
        self.check_template_response_code('/password/', 'authenticated/password.html', 200)
        self.check_template_response_code('/assignment/', 'authenticated/assignment.html', 200)
        self.check_template_response_code('/assignment/override/', 'authenticated/assignment.html', 200)
        self.check_response_code('/secure-static/c2VlbWFfc3dhbWk6aHR0cDovL2xvY2FsaG9zdDo5ODc4L3F1ZXN0aW9ucy9yYXcvMS8xLzgvMS8xL2ltZy8xLnBuZzpNdElHUno4UVBMajEtR0xERVNta2NjVzVIUEU/', 200)

        self.check_json_response_code('/ajax/announcements/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/override/', 200)

        self.check_json_response_code('/chart/student/3/', 404)
        self.check_json_response_code('/chart/student/3/1/', 200)
        self.check_json_response_code('/chart/subjectroom/1/', 200)
        self.check_json_response_code('/chart/subjectteacher/4/', 200)
        self.check_json_response_code('/chart/classteacher/7/1/', 404)

        self.check_json_response_code('/chart/assignment/3/', 200)  # corrected
        self.check_json_response_code('/chart/assignment/2/', 404)  # uncorrected
        self.check_json_response_code('/chart/assignment/1/', 404)  # inactive

        self.check_json_response_code('/chart/completion/3/', 200)
        self.check_json_response_code('/chart/completion/2/', 200)
        self.check_json_response_code('/chart/completion/1/', 200)

        self.check_json_response_code('/chart/standard-assignment/3/', 200)
        self.check_json_response_code('/chart/standard-assignment/2/', 404)
        self.check_json_response_code('/chart/standard-assignment/1/', 404)

        self.client.logout()

    def test_authenticated_classteacher(self):
        self.assertTrue(self.client.login(username='amita_singh', password=DEBUG_SETUP_PASSWORD))
        self.check_home_redirect('/')
        self.check_home_redirect('/login/')

        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_template_response_code('/home/', 'authenticated/home/teacher.html', 200)
        self.check_template_response_code('/settings/', 'authenticated/settings/teacher.html', 200)
        self.check_template_response_code('/subject/1/', 'authenticated/subject_id/teacher.html', 200)
        self.check_template_response_code('/classroom/1/', 'authenticated/classroom_id.html', 200)
        self.check_template_response_code('/subject/1/3/', '404.html', 404)
        self.check_template_response_code('/assignment/1/', 'authenticated/assignment_id.html', 200)    #inactive
        self.check_template_response_code('/assignment/2/', 'authenticated/assignment_id.html', 200)    #uncorrected
        self.check_template_response_code('/assignment/3/', '404.html', 404)                            #corrected
        self.check_template_response_code('/assignment/preview/1/', '404.html', 404)
        self.check_template_response_code('/submission/1/', 'authenticated/submission_id/corrected.html', 200)
        self.check_template_response_code('/announcement/', 'authenticated/announcement.html', 200)
        self.check_template_response_code('/password/', 'authenticated/password.html', 200)
        self.check_template_response_code('/assignment/', 'authenticated/assignment.html', 200)
        self.check_template_response_code('/assignment/override/', 'authenticated/assignment.html', 200)
        self.check_response_code('/secure-static/YW1pdGFfc2luZ2g6aHR0cDovL2xvY2FsaG9zdDo5ODc4L3F1ZXN0aW9ucy9yYXcvMS8xLzgvMS8xL2ltZy8xLnBuZzphTXFYamdScS1RVWtKdU44bFZHUk5WMlVFUk0/', 200)

        self.check_json_response_code('/ajax/announcements/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/override/', 200)

        self.check_json_response_code('/chart/student/3/', 200)
        self.check_json_response_code('/chart/student/3/1/', 200)
        self.check_json_response_code('/chart/subjectroom/1/', 200)
        self.check_json_response_code('/chart/subjectteacher/4/', 404)
        self.check_json_response_code('/chart/classteacher/7/1/', 200)

        self.check_json_response_code('/chart/assignment/3/', 200)  # corrected
        self.check_json_response_code('/chart/assignment/2/', 404)  # uncorrected
        self.check_json_response_code('/chart/assignment/1/', 404)  # inactive

        self.check_json_response_code('/chart/completion/3/', 200)
        self.check_json_response_code('/chart/completion/2/', 200)
        self.check_json_response_code('/chart/completion/1/', 200)

        self.check_json_response_code('/chart/standard-assignment/3/', 200)
        self.check_json_response_code('/chart/standard-assignment/2/', 404)
        self.check_json_response_code('/chart/standard-assignment/1/', 404)

        self.client.logout()

    def test_authenticated_admin(self):
        self.assertTrue(self.client.login(username='neelam_chakraborty', password=DEBUG_SETUP_PASSWORD))
        self.check_home_redirect('/')
        self.check_home_redirect('/login/')

        self.check_template_response_code('/forgot-password/', 'forgot_password/form.html', 200)
        self.check_template_response_code('/forgot-password/mailed/', 'forgot_password/mailed.html', 200)
        self.check_template_response_code('/password-reset/someuidb-sometoken/', 'password_reset/form.html', 200)
        self.check_template_response_code('/password-reset/complete/', 'password_reset/complete.html', 200)

        self.check_template_response_code('/home/', 'authenticated/home/admin.html', 200)
        self.check_template_response_code('/settings/', 'authenticated/settings/admin.html', 200)
        self.check_template_response_code('/subject/1/', 'authenticated/subject_id/admin.html', 200)
        self.check_template_response_code('/classroom/1/', 'authenticated/classroom_id.html', 200)
        self.check_template_response_code('/subject/1/3/', '404.html', 404)
        self.check_template_response_code('/assignment/1/', 'authenticated/assignment_id.html', 200)    #inactive
        self.check_template_response_code('/assignment/2/', 'authenticated/assignment_id.html', 200)    #uncorrected
        self.check_template_response_code('/assignment/3/', '404.html', 404)                            #corrected
        self.check_template_response_code('/assignment/preview/1/', '404.html', 404)
        self.check_template_response_code('/submission/1/', 'authenticated/submission_id/corrected.html', 200)
        self.check_template_response_code('/announcement/', 'authenticated/announcement.html', 200)
        self.check_template_response_code('/password/', 'authenticated/password.html', 200)
        self.check_template_response_code('/assignment/', '404.html', 404)
        self.check_template_response_code('/assignment/override/', '404.html', 404)
        self.check_response_code('/secure-static/bmVlbGFtX2NoYWtyYWJvcnR5Omh0dHA6Ly9sb2NhbGhvc3Q6OTg3OC9xdWVzdGlvbnMvcmF3LzEvMS84LzEvMS9pbWcvMS5wbmc6VzlkR0RXUWJpRjExMkUyNVZ6ODFVejdSNnlN/', 200)

        self.check_json_response_code('/ajax/announcements/', 200)
        self.check_json_response_code('/ajax/question-set-choice-widget/', 404)
        self.check_json_response_code('/ajax/question-set-choice-widget/override/', 404)

        self.check_json_response_code('/chart/student/3/', 200)
        self.check_json_response_code('/chart/student/3/1/', 200)
        self.check_json_response_code('/chart/subjectroom/1/', 200)
        self.check_json_response_code('/chart/subjectteacher/4/', 200)
        self.check_json_response_code('/chart/classteacher/7/1/', 200)

        self.check_json_response_code('/chart/assignment/3/', 200)  # corrected
        self.check_json_response_code('/chart/assignment/2/', 404)  # uncorrected
        self.check_json_response_code('/chart/assignment/1/', 404)  # inactive

        self.check_json_response_code('/chart/completion/3/', 200)
        self.check_json_response_code('/chart/completion/2/', 200)
        self.check_json_response_code('/chart/completion/1/', 200)

        self.check_json_response_code('/chart/standard-assignment/3/', 200)
        self.check_json_response_code('/chart/standard-assignment/2/', 404)
        self.check_json_response_code('/chart/standard-assignment/1/', 404)

        self.client.logout()
