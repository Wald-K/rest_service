from django.test import TestCase
from ip_library.libs.extras import (ip_to_binary_list, network_to_binary_list,
                                    split_network_cidr_addr, NodeLibrary,
                                    TagsProvider)


class TestIpOperations(TestCase):

    def test_ip_to_binary_list(self):
        ip_binary_list = ip_to_binary_list('192.168.0.1')
        self.assertEqual(ip_binary_list, 
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])

    def test_network_to_binary_list(self):
        ip_binary_list = network_to_binary_list('10.20.0.0', 16)
        self.assertEqual(ip_binary_list,
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0])

    def test_split_network_cidr_addr(self):
        ip_addr, net_size = split_network_cidr_addr('203.0.113.0/24')
        self.assertEqual((ip_addr, net_size), ('203.0.113.0', 24))


class TestNodeLibraryOperations(TestCase):

    def setUp(self):
        self.node_library = NodeLibrary()

    def test_putting_one_tag_on_second_level(self):
        bit_00 = [0, 0]
        tags_00 = 'tag_00'

        self.node_library.set_bits(bit_00)
        self.node_library.insert(tags_00)

        self.assertEqual(self.node_library.left.left.tags, {'tag_00'})
        self.assertIsInstance(self.node_library.left, NodeLibrary)
        self.assertIsInstance(self.node_library.left.left, NodeLibrary)
        self.assertEqual(self.node_library.right, None)

    def test_putting_one_tag_on_third_level(self):
        bit_010 = [0, 1, 0]
        tags_010 = 'tag_010'

        self.node_library.set_bits(bit_010)
        self.node_library.insert(tags_010)
        
        self.assertEqual(self.node_library.left.right.left.tags, {'tag_010'})
        self.assertIsInstance(self.node_library.left, NodeLibrary)
        self.assertIsInstance(self.node_library.left.right, NodeLibrary)
        self.assertIsInstance(self.node_library.left.right.left, NodeLibrary)
        self.assertEqual(self.node_library.right, None)


class TestTagsProviderOperations(TestCase):

    def setUp(self):
        self.node_library = NodeLibrary()
        self.tags_provider = TagsProvider(self.node_library)
    
    def test_getting_tags_for_ip(self):
        bit_010 = [0, 1]
        tags_010 = 'tag_01'
        self.node_library.set_bits(bit_010)
        self.node_library.insert(tags_010)
        
        bit_010 = [0, 1, 0]
        tags_010 = 'tag_010'
        self.node_library.set_bits(bit_010)
        self.node_library.insert(tags_010)

        found_tags = self.tags_provider.get_tags_for_ip([0, 1, 0])
        self.assertEqual(found_tags, ['tag_01', 'tag_010'])

        found_tags = self.tags_provider.get_tags_for_ip([0, 1, 1])
        self.assertEqual(found_tags, ['tag_01'])

        found_tags = self.tags_provider.get_tags_for_ip([0, 1])
        self.assertEqual(found_tags, ['tag_01'])

        found_tags = self.tags_provider.get_tags_for_ip([0, 0])
        self.assertEqual(found_tags, [])
