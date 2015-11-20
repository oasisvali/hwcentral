import re


def merge_dicts(dict_list):
    """
    dict with higher index overwrites dict with lower index in case of matching key
    """
    merged_dict = {}
    for dictionary in dict_list:
        merged_dict.update(dictionary)
    return merged_dict

def make_string_lean(string):
    """
    collapses all whitespace in string and strips whitespace from ends
    """

    whitespace = re.compile(r'\s+')
    string = whitespace.sub(' ', string)
    return string.strip()