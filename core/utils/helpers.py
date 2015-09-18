import re


def merge_dicts(dict_list):
    """
    dict with higher index overwrites dict with lower index in case of matching key
    """
    merged_dict = {}
    for dictionary in dict_list:
        merged_dict.update(dictionary)
    return merged_dict

def collapse_whitespace(str):
    whitespace = re.compile(r'\s+')
    return whitespace.sub(' ', str)