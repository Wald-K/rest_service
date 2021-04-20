import json
import logging


library_logger = logging.getLogger('library_logger')

def ip_to_binary_list(ip):
    octet_list = ip.split(".")
    octet_list_bin = [format(int(oct), '08b') for oct in octet_list]
    binary_addr_str = ("").join(octet_list_bin)
    binary_addr_str_int = list(map(int, binary_addr_str))
    return binary_addr_str_int


def network_to_binary_list(address, net_size):
    ip_bin = ip_to_binary_list(address)
    network = ip_bin[0:net_size]
    return network


def split_network_cidr_addr(ip_cidr):
    [ip_addr, net_size] = ip_cidr.split('/')
    return ip_addr, int(net_size)


class NodeLibrary:
    def __init__(self):
        self.left = None
        self.right = None
        self.tags = set()
        self.bits = None

    def set_bits(self, bits):
        self.bits = bits

    def insert(self, data):
        if len(self.bits) == 0:
            self.tags.add(data)
        else:
            if self.bits[0] == 0: # go to left
                if self.left is None:
                    self.left = NodeLibrary()
                new_bits = self.bits[1:]
                self.left.set_bits(new_bits)
                self.left.insert(data)
            elif self.bits[0] == 1:
                if self.right is None:
                    self.right = NodeLibrary()
                new_bits = self.bits[1:]
                self.right.set_bits(new_bits)
                self.right.insert(data)
            else:
                library_logger.error('Invalid sign in network ip address')


    def get_left(self):
        return self.left

    def get_right(self):
        return self.right


class LibraryLoader:
    def __init__(self, json_file):
        self.library_nodes = None
        self.json_file = json_file

    def load_library_nodes(self):
        with open(self.json_file) as json_file:
            tag_network_list = json.load(json_file)
            node_library = NodeLibrary()
            for tag_network in tag_network_list:
                ip_addr, net_size = split_network_cidr_addr(
                    tag_network.get("ip_network"))
                network_ip_binary = network_to_binary_list(ip_addr, net_size)
                tag = tag_network.get("tag")
                node_library.set_bits(network_ip_binary)
                node_library.insert(tag)

        return node_library


class TagsProvider:
    def __init__(self, node_library: NodeLibrary):
        self.node_library = node_library

    def get_tags_for_ip(self, ip_addr: list):
        tags = set()
        tags_list = []
        current_node = self.node_library
        for bit in ip_addr:
            if bit == 0:
                current_node = current_node.left
            else:
                current_node = current_node.right
            if current_node is None:
                break
            else:
                tags_for_node = current_node.tags
                if tags_for_node != set():
                    tags.update(tags_for_node)
        tags_list = sorted(tags)
        return tags_list
