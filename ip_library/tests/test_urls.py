from django.test import TestCase
from django.urls import reverse, resolve
from ip_library.views import show_ip_tags, show_ip_tags_report

class TestUrls(TestCase):
    
    def test_json_tags_resolved(self):
        url = reverse('json_tags', kwargs={'ip_address': '192.168.0.1'})
        self.assertEqual(resolve(url).func, show_ip_tags)

    def test_report_tags_resolved(self):
        url = reverse('report_tags', kwargs={'ip_address': '192.168.0.1'})
        self.assertEqual(resolve(url).func, show_ip_tags_report)

