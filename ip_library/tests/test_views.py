from django.test import TestCase, Client
from django.urls import reverse
from ip_library.libs.heavy_load import node_library

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

    def test_view_show_ip_tags(self):
        response = self.client.get(reverse('json_tags',
                                   kwargs={'ip_address': '192.168.0.1'}))
        if node_library != None:
            self.assertEqual(response.status_code, 200)

    def test_view_show_ip_tags_bad_ip_address(self):
        response = self.client.get(reverse('json_tags', 
                                   kwargs={'ip_address': '192.168.256.1'}))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {"message": "Invalid IP address in request"})

    def test_view_show_ip_tags_report(self):
        response = self.client.get(reverse('report_tags',
                                   kwargs={'ip_address': '192.168.0.1'}))
        if node_library is not None:
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'ip_library/report.html')

    def test_view_show_ip_tags_report_bad_ip_address(self):
        response = self.client.get(reverse('report_tags',
                                   kwargs={'ip_address': '192.168.256.1'}))
        if node_library is not None:
            self.assertEqual(response.status_code, 400)
            self.assertTemplateUsed(response, 'ip_library/error_info.html')

    def test_using_error_template_when_library_not_loaded(self):
        response = self.client.get(reverse('report_tags', 
                                   kwargs={'ip_address': '192.168.256.1'}))
        self.assertTemplateUsed(response, 'ip_library/error_info.html')
