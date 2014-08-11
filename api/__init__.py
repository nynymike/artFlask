__author__ = 'mike'

from datetime import datetime as dtime
from model import Website, Medium, LimitedTime


def date_from_str(s):
    return dtime.strptime(s, '%b %d %Y').date()


def website_list_from_urls(urls):
    return [Website(name="url%d" % n, url=url) for n, url in enumerate(urls)]


def website_list_from_dict(url_dict):
    return [Website(name=k, url=v) for k, v in url_dict.items()]


def mediums_from_names(names):
    return [Medium.query.get(name) or Medium(name=name) for name in names]


def object_from_dict(class_name):
    def wrapper(d):
        return class_name(**d)
    return wrapper


def objects_from_ids(class_name):
    def wrapper(lst):
        return [class_name.query.get(obj_id) for obj_id in lst]
    return wrapper


def times_from_stringlist(stringlist):
    FORMAT = '%b %d %X %Z %Y'
    return [LimitedTime(start=dtime.strptime(start, FORMAT)) for start in stringlist]


def website_from_dict(d):
    return [Website(name=k, url=v) for k, v in d.items()]


