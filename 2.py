import requests
from pprint import pprint



class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }
        return headers

    def get_file_list(self):
        url_to_upload = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        resp = requests.get(url_to_upload, headers=self.get_headers())
        resp_json = resp.json()
        return resp_json

    def get_upload_link(self, file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {
            'path': file_path,
            'overwrite': 'true'
        }
        response = requests.get(upload_url, headers=headers, params=params)
        data = response.json()
        href = data.get('href')
        print(href)
        return href

    def upload(self, file_path, file_name):
        href = self.get_upload_link(file_path=file_path)
        resp = requests.put(href, data=open(file_name, 'rb'))
        if resp.status_code == 201:
            print('Success')
        print(resp.json())
        return resp.json()


if __name__ == '__main__':
    path_to_file = 'file.txt'

    token = "y0_AgAAAAACQgvtAADLWwAAAADeux0_w1bvFpzaTNu8qus6x1PNTR4Z-QI"
    to = YaUploader(token)
    res = to.upload('file1.txt', path_to_file)
    print(res)
