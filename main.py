import xml.etree.ElementTree as ET
import json
import operator


# Work with json
def read_json_file(file_name):
    str_set = {}
    with open(file_name, 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
        for json_obj in json_dict.get('rss').get('channel').get('items'):
            str_set = parse_json_file_by_name('description', json_obj, str_set)
            str_set = parse_json_file_by_name('title', json_obj, str_set)
    return str_set


def parse_json_file_by_name(name, json_obj, str_set):
    strings = json_obj[name].split(' ')
    return collect_strings_with_count(str_set, strings)


# Work with xml
def read_xml_file(file_name):
    str_set = {}
    tree = ET.parse(file_name)
    root = tree.getroot()
    str_set = parse_xml_file_by_tag('title', root, str_set)
    str_set = parse_xml_file_by_tag('description', root, str_set)
    return str_set


def parse_xml_file_by_tag(tag, root, str_set):
    for child in root.findall(f'.//{tag}'):
        xml_str = ET.tostring(child, encoding='unicode')
        xml_str = xml_str.strip().replace(f'<{tag}>', '').replace(f'</{tag}>', '')
        titles = xml_str.split(' ')
        collect_strings_with_count(str_set, titles)
    return str_set


def collect_strings_with_count(s_set, strings):
    keys = s_set.keys()
    for s in strings:
        if len(s) > 6:
            s.strip()
            if s in keys:
                s_set.update({s: s_set.get(s) + 1})
            else:
                s_set.update({s: 1})
    return s_set


def print_first_max_elements(s_set, count):
    print(sorted(s_set.items(), key=operator.itemgetter(1), reverse=True)[:count])


if __name__ == '__main__':
    strings_set = read_json_file('newsafr.json')
    print_first_max_elements(strings_set, 10)
    strings_set = read_xml_file('newsafr.xml')
    print_first_max_elements(strings_set, 10)
