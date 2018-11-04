# coding:utf-8
import yaml
import os
import re
import json
import requests
from libs.share_utils import InsertLog
from libs.share_utils import log

# from string import digits


daily = InsertLog()


class ParseYamlDataClass(object):

    # 获取文件路径
    @classmethod
    def get_path(cls, projectname, apiname, pathname, filelistname='api'):
        filepath = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '../{}/{}/{}/{}.yaml'. \
                         format(filelistname, projectname, apiname, pathname)))
        return filepath

    # 获取api swagger api文档信息
    def get_api(self):
        filepath = self.get_path(apiname='auth', projectname='project', pathname='index',)
        with open(filepath, encoding='utf-8') as f:
            deatil = yaml.load(f)
        log('swagger deatil is',deatil)
        path = (list(deatil['paths'].keys()))[0]
        host = (deatil['servers'][0]['url'])
        url = '{}{}'.format(host, path)
        methods = list((((deatil['paths'])).get(path, None)).keys())[0]
        if methods is None:
            methods = 'get'
        return url, methods

    # 获取api stage请求内容
    def get_api_data(self, filepath,statusvalue):
        with open(filepath, encoding='utf-8') as f:
            # 以字典格式读取yaml文件
            deatil = yaml.load(f)
        data = list(deatil.keys())
        for i in range(len(data)):
            if statusvalue in data[i]:
                # 获取对应的响应状态
                status = data[i]
                # 拆分获取对应的状态码
                #code = re.sub('\D', '', status)
                # 拆分获取对应的状态描述
                #description = re.sub('\d', '', status)
                break
                # remove_digits = str.maketrans('', '', digits)
                # description = status[i].translate(remove_digits)
            else:
                status = '200Ok'
                code = '200'
                description = 'Ok'
                log('not found requestdata')
        requestbody = deatil[status][0]
        requestbody['verify'] = status
        log('requestbody is', requestbody)
        return requestbody

    ##调试
    def send_request(self):
        url, methods = self.get_api()
        body = self.get_api_data('200Ok')
        verify = body.get('verify', '')
        body.pop('verify', '')
        code = re.sub('\D', '', verify)
        log(code)
        # 拆分获取对应的状态描述
        description = re.sub('\d', '', verify)
        log(description)
        result = requests.post(url=url, data=json.dumps(body), verify=False)
        log(result.status_code)


if __name__ == '__main__':
    run = ParseYamlDataClass()
    run.get_api()