# mm1/tests/test_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mm1 import views

class TestUrls(SimpleTestCase):
    
    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)
    
    def test_timetable_url_is_resolved(self):
        url = reverse('timetable')
        self.assertEqual(resolve(url).func, views.timetable)

    def test_add_room_url_is_resolved(self):
        url = reverse('addroom')
        self.assertEqual(resolve(url).func, views.add_room)

    def test_add_instructor_url_is_resolved(self):
        url = reverse('addinstructor')
        self.assertEqual(resolve(url).func, views.add_instructor)

    def test_instructor_list_url_is_resolved(self):
        url = reverse('editinstructor')
        self.assertEqual(resolve(url).func, views.inst_list_view)

    def test_add_meetingtime_url_is_resolved(self):
        url = reverse('addmeetingtime')
        self.assertEqual(resolve(url).func, views.add_meeting_time)

    def test_meetingtime_list_url_is_resolved(self):
        url = reverse('editmeetingtime')
        self.assertEqual(resolve(url).func, views.meeting_list_view)

    def test_add_course_url_is_resolved(self):
        url = reverse('addcourse')
        self.assertEqual(resolve(url).func, views.add_course)

    def test_course_list_url_is_resolved(self):
        url = reverse('editcourse')
        self.assertEqual(resolve(url).func, views.course_list_view)

    def test_add_department_url_is_resolved(self):
        url = reverse('adddepartment')
        self.assertEqual(resolve(url).func, views.add_department)

    def test_delete_meetingtime_url_is_resolved(self):
        url = reverse('deletemeetingtime', args=['1'])
        self.assertEqual(resolve(url).func, views.delete_meeting_time)

    def test_delete_course_url_is_resolved(self):
        url = reverse('deletecourse', args=['1'])
        self.assertEqual(resolve(url).func, views.delete_course)

    def test_delete_instructor_url_is_resolved(self):
        url = reverse('deleteinstructor', args=[1])
        self.assertEqual(resolve(url).func, views.delete_instructor)

    def test_room_list_url_is_resolved(self):
        url = reverse('editrooms')
        self.assertEqual(resolve(url).func, views.room_list)

    def test_delete_room_url_is_resolved(self):
        url = reverse('deleteroom', args=[1])
        self.assertEqual(resolve(url).func, views.delete_room)

    def test_department_list_url_is_resolved(self):
        url = reverse('editdepartment')
        self.assertEqual(resolve(url).func, views.department_list)

    def test_delete_department_url_is_resolved(self):
        url = reverse('deletedepartment', args=[1])
        self.assertEqual(resolve(url).func, views.delete_department)

    def test_add_section_url_is_resolved(self):
        url = reverse('addsection')
        self.assertEqual(resolve(url).func, views.add_section)

    def test_section_list_url_is_resolved(self):
        url = reverse('editsection')
        self.assertEqual(resolve(url).func, views.section_list)

    def test_delete_section_url_is_resolved(self):
        url = reverse('deletesection', args=['1'])
        self.assertEqual(resolve(url).func, views.delete_section)
