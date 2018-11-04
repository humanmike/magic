# coding:utf-8
import requests
import json
from libs.share_modules import ParseYamlDataClass
from libs.share_utils import InsertLog
from libs.share_utils import log

swaggeryaml = ParseYamlDataClass()


class BaseHttp(object):

    # 处理响应体
    def __format_response(rep):
        responsebody = rep.json()
        responsecode = rep.status()
        return responsebody, responsecode

    # 根据Swagger接口文档的请求方式及url进行对应请求
    def get_swagger(self, projectname, apiname, pathname, filelistname):
        path = swaggeryaml.get_path(projectname, apiname, pathname, filelistname)
        url, methods = swaggeryaml.get_api(path)
        if 'get' in methods:
            httpreq = self.get_data
        elif 'post' in methods:
            httpreq = self.post_data
        else:
            httpreq = self.get_data
            log('not found methods')
        log('httpreq and url is', httpreq, url)
        return httpreq, url

    # 获取对应Api文档的请求内容数据
    def get_stage(self, projectname, apiname, pathname, filelistname, statuscode):
        path = swaggeryaml.get_path(projectname, apiname, pathname, filelistname)
        body = swaggeryaml.get_api_data(path, statuscode)
        verify = body.get('verify', '')
        body.pop('verify', '')
        return body, verify

    # 发送请求
    def send_http(self):
        httpreq, url = self.get_swagger(filelistname='api', projectname='project',
                                        apiname='auth', pathname='login')
        body, verify = self.get_stage(filelistname='stage', projectname='project', apiname='auth',
                                      pathname='login2', statuscode='200Ok')
        log('body is', body)
        try:
            result = httpreq(url, data=json.dumps(body))
        except BaseException as msg:
            daily = InsertLog()
            daily.error(msg)
        log('result is', result.json())
        return result

    # 执行post请求
    @staticmethod
    def post_data(url, data=None, header=None, icon='2'):
        if icon == '1':
            result = requests.post(url, data=data, headers=header)
        elif icon == '2':
            result = requests.post(url, data=data)
        elif icon == 'upload':
            result = requests.post(url, files=data, headers=header)
        return result

    # 执行get请求
    @staticmethod
    def get_data(url, data=None, header=None, icon='1'):
        if icon == '1':
            result = requests.get(url, data=data, headers=header)
        elif icon == '2':
            result = requests.get(url, data)
        elif icon == '3':
            result = requests.get(url, data, headers=header)
        return result


if __name__ == '__main__':
    run = BaseHttp()
    run.send_http()
    # run.get_swagger(filelistname='api', projectname='project', apiname='auth', pathname='invite_join_team')
    # run.get_stage(filelistname='stage', projectname='project', apiname='auth', pathname='login', statuscode='200Ok')
