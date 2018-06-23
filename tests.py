from diskspace import diskspace

import unittest
import StringIO
import sys

import argparse
import os
import subprocess
import re

class TestSubprocessCheckOutput(unittest.TestCase):

    def test_return(self):
        command = 'du'
        output = subprocess.check_output(command)
        self.assertEqual(diskspace.subprocess_check_output(command), output)


class TestBytesToReadable(unittest.TestCase):

    def test_return(self):
        blocks = 1
        self.assertEqual(diskspace.bytes_to_readable(blocks), '512.00B')
        blocks = 100
        self.assertEqual(diskspace.bytes_to_readable(blocks), '50.00Kb')
        blocks = 100000
        self.assertEqual(diskspace.bytes_to_readable(blocks), '48.83Mb')
        blocks = 10000000
        self.assertEqual(diskspace.bytes_to_readable(blocks), '4.77Gb')
        blocks = 10000000000
        self.assertEqual(diskspace.bytes_to_readable(blocks), '4.66Tb')



class TestPrintTree(unittest.TestCase):

    def setUp(self):
        self.file_tree = {'/home': {'print_size': '6.00Kb',
                                    'children': [], 'size': 12}}
        self.file_tree_node = {'print_size': '6.00Kb',
                               'children': [], 'size': 12}
        self.path = '/home'
        self.largest_size = 8
        self.total_size = 340

    def test_output(self):
        system_output = StringIO.StringIO()
        sys.stdout = system_output

        diskspace.print_tree(self.file_tree, self.file_tree_node, self.path,
                             self.largest_size, self.total_size)
        sys.stdout = sys.__stdout__
        self.assertEqual(system_output.getvalue(), '  6.00Kb    3%  /home\n')

    def test_invalid_percentage(self):
        file_tree_node = {'print_size': '6.00Kb',
                               'children': [], 'size': -10}
        system_output = StringIO.StringIO()
        sys.stdout = system_output

        diskspace.print_tree(self.file_tree, file_tree_node, self.path,
                             self.largest_size, 1)
        sys.stdout = sys.__stdout__
        self.assertEqual(system_output.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
