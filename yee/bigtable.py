#!/usr/bin/env python

import csv
import collections
import cPickle

from .utils import read_csv, read_csv_field


class BigTable(object):
    def __init__(self, init_file_name=None):
        self.header = {}
        self.rows = []

        if init_file_name is not None:
            self.init_from_file(init_file_name)

    def init_from_file(self, file_name, delimiter=','):
        data = read_csv(file_name, delimiter)
        self.rows = data['data']
        self.header = data['keys']

    def merge_from_file(self, file_name, left, right=None, delimiter=','):
        if right is None:
            right = left
        right_data = read_csv(file_name, delimiter)
        right_index = right_data['keys'][right]
        quick_lookup = collections.defaultdict(lambda: [])
        for i in right_data['data']:
            quick_lookup[i[right_index]].append(i)

        left_index = self.header[left]
        origin_length = len(self.rows[0])
        new_rows = []
        for row in self.rows:
            column = row[left_index]
            for i in quick_lookup[column]:
                new_rows.append(row + i[:right_index] + i[right_index + 1:])

        for i in right_data['keys']:
            if i == right:
                continue
            if right_data['keys'][i] > right_index:
                offset = origin_length - 1
            else:
                offset = origin_length
            self.header[i] = right_data['keys'][i] + offset
        self.rows = new_rows

    def show(self):
        print(self.header)
        print(self.rows)

    def dumps(self, name):
        data = {
            'rows': self.rows,
            'header': self.header
        }
        with open(name, 'w') as ftr:
            cPickle.dump(data, ftr)

    def get_rows(self, key, value):
        index = self.header[key]
        ret = []
        for i in self.rows:
            if i[index] == value:
                ret.append(i)
        return ret

    def get_values(self, key, value, output_key):
        index = self.header[key]
        output_index = self.header[output_key]
        ret = []
        for i in self.rows:
            if i[index] == value:
                ret.append(i[output_index])
        return ret


if __name__ == '__main__':
    a = BigTable()
    a.init_from_file('./products.csv', ',')
    a.merge_from_file('./train.csv', 'product_id')
    a.merge_from_file('./aisles.csv', 'aisle_id')
    print(a.get_rows('product_id', '49683'))
    print(a.get_values('product_id', '49683', 'product_name'))
