#coding:utf-8

'''
__author__ = yinzhixin
__version__ = 1.0
'''

import sys
import os
import re
import datetime
from functools import wraps
from collections import namedtuple
import requests
from jinja2 import FileSystemLoader, Template
from jinja2 import Environment
import xlrd
from util import DictObj, formatTime
reload(sys)
sys.setdefaultencoding('utf-8')


TEMPALTE_PATH = os.path.join(os.path.dirname(__file__), 'template/')
STATIC = os.path.join(os.path.dirname(__file__), 'static')
#STATIC = '/static'          #jenkins path
REPORT_PATH = os.path.join(os.path.dirname(__file__), 'testreport/')
template_name = 'index.html.template'
reportname = REPORT_PATH + 'index.html'
Detail = namedtuple('Detail', 'interface_name, url, data, reqtype, expection, actual, status')      


class CaseData(object):
    """测试用例数据"""
    def __init__(self, i, arg):
        super(CaseData, self).__init__()
        self.interface_name = arg.row_values(i)[0]
        self.url = arg.row_values(i)[1]
        self.reqtype = arg.row_values(i)[2]
        self.data = arg.row_values(i)[3]
        self.expection = arg.row_values(i)[4]
        

class Results(dict):
    """结果集"""   
    def __init__(self):
        self.setdefault('success', 0)
        self.setdefault('fail', 0)
        self.setdefault('error', 0)
        self.setdefault('detail', [])
        self.static = STATIC
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError, e:
            raise AttributeError(name)

    def add(self,result):
        if result.status == 'Success':
            self.success += 1
        elif result.status == 'Fail':
            self.fail += 1
        elif result.status == 'Error':
            self.error += 1
        else:
            pass
        self.detail.append(result)


class Async(object):
    """as u see"""
    def __init__(self, func,args):
        super(Async, self).__init__()
        self.func = func
        self.args = args

def async_decorator(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_set = Results()
        result_set.starttime = datetime.datetime.now()
        while True:
            try:
                #a = f.send(None)
                a = f.next()
                apply_async(a.func, a.args, callback=result_set.add)
            except StopIteration, e:
                result_set.endtime = datetime.datetime.now()
                result_set.total = result_set.success+result_set.error+result_set.fail
                break
        return result_set
    return wrapper


def run_case(case):
    status = 'Error'
    final_expect = case.expection.replace(' ', '').replace('\"', '').replace("\'", '')
    expect = re.compile(r'{}'.format(final_expect))
    response = requests.request(case.reqtype, case.url, data=case.data)
    try:
        if response.status_code == requests.codes.ok:
            actual = response.content.replace(' ','').replace('\"', '').replace("\'", '')
            if expect.search(actual):
                status = 'Success'
            else:
                status = 'Fail'
        else:
            actual = response.status_code
    except AssertionError, e:
        pass
    finally:
        detaildata = Detail(case.interface_name, \
                                    case.url, case.data, \
                                    case.reqtype, \
                                    case.expection, \
                                    actual, status)
    return detaildata  


def parse_file(casefile):
    """解析excel文件"""
    source = xlrd.open_workbook(casefile)
    sheet_name_list = source.sheet_names()
    for sheet_name in sheet_name_list:
        case = source.sheet_by_name(sheet_name)
        for i in range(1,case.nrows):
            yield CaseData(i, case)


def apply_async(func, args, callback):
    result = func(args)
    return callback(result)

def render_report(result_set):
    '''用测试数据生成测试报告'''
    env = Environment(loader=FileSystemLoader(TEMPALTE_PATH))
    template = env.get_template(template_name)
    content = template.render(result_set).encode('utf-8')
    with open(reportname, 'wb') as f:
        f.write(content)

@async_decorator
def start(itercase):
    for case in itercase:
        yield Async(run_case, case)



if __name__ == '__main__':
    itercase = parse_file('testcase.xlsx')
    result_set = start(itercase)    
    render_report(result_set)       












