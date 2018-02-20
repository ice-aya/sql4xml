#!/usr/bin/python3

# sql4xml.py: A Python utility to query XML data with SQL.
#
# Copyright (c) 2018 Andrey Abalyaev <ice-aya@ya.ru>
# 
# License
# 
#     This program is free software: you can redistribute it and/or modify it
#     under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     This program is distributed in the hope that it will be useful, but WITHOUT
#     ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#     FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#     for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with software.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3

def load_config(file_name = ''):

    def load_cfg_file(file_name):
        from json import load

        with open(file_name, 'r', encoding = 'utf8') as f:
            return load(f)

    def load_all_configs():
        return load_cfg_file('desc.json'), load_cfg_file('queries.json'), load_cfg_file('files.json')

    def load_big_config(file_name):
        d = load_cfg_file(file_name)
        return d['desc'], d['queries'], d['files']

    if file_name != '': return load_big_config(file_name)
    return load_all_configs()

def datatables_create(cur, desc):
    for t in desc.keys():
        cur.executescript(' '.join(['create table', t, '(', ', '.join([f for f in desc[t]['fields'].keys()]), ');']))

def datatables_fill(cur, desc, files):

    def xml_processing(xmlfile, desc):
        import xml.etree.ElementTree as ET

        def chain_call(root, l, find_all):
            if len(l) > 1: return chain_call(root.find(l[0]), l[1:], find_all)
            elif find_all: return root.findall(l[0])
            else: return root.find(l[0])

        chain_find = lambda root, l: chain_call(root, l, False)
        chain_findall = lambda root, l: chain_call(root, l, True)

        for r in chain_findall(ET.parse(xmlfile).getroot(), desc['root']):
            yield {k : chain_find(r, v).text for k, v in desc['fields'].items()}

    def datatable_fill(table, data):
        for d in data:
            cur.execute(
                ' '.join([
                    'insert into', table,
                    '(', ', '.join([k for k in d.keys()]), ')',
                    ' values (', ', '.join(['"' + d[k] + '"' if d[k] is not None else '""' for k in d.keys()]), ');'
                ])
            )

    for t in desc.keys():
        for f in files[t]:
            datatable_fill(t, xml_processing(f, desc[t]))

def datatables_query(cur, queries):

    def write_rows(fn):
        with open(fn, 'w+') as f:
            for row in cur.fetchall():
                for fld in row:
                    print(fld if fld is not None else '', end = ';', file = f)
                print(file = f)

    for fn in queries.keys():
        cur.execute(queries[fn])
        write_rows(fn)

def main():
    import sys

    desc, queries, files = load_config(sys.argv[1]) if len(sys.argv) > 1 else load_config()
    cur = sqlite3.connect(':memory:').cursor()

    datatables_create(cur, desc)
    datatables_fill(cur, desc, files)
    datatables_query(cur, queries)

if __name__ == "__main__":
    main()