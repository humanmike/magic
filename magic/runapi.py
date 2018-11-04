# coding:utf-8
import requests
import json
from libs.share_utils import log


def send_request():
    url = 'https://api.ones.team/project/master/auth/login'
    data = dict(
        password='12345678',
        email='linhong+do@ones.ai',
    )
    result = requests.post(url=url, data=json.dumps(data))
    log(result.text)




if __name__ == '__main__':
    send_request()

    # getYaml = ParseYamlDataClass()
    # url, methods = getYaml.get_api()
    # body, status, code = getYaml.get_api_data('630')
    # result = requests.post(url=url, data=body, verify=False)
    # log(result.json())