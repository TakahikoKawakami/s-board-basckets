import base64
import requests
import json
import time
import logging
from urllib.parse import urlencode

from .BaseApi import BaseApi
from .entities import ErrorResponse

class BaseServiceApi(BaseApi):
    def _showAuthorizationString(self):
        return self.config.accessToken

    def _getSmaregiAuth(self):
        string = self._showAuthorizationString()
        return "Bearer " + string
        
    
    def _getHeader(self):
        return {
            'Authorization': self._getSmaregiAuth(),
            'Content-Type':	'application/x-www-form-urlencoded',        
        }
        
        
    def _getQuery(self, field=None, sort=None, whereDict=None):
        body = {
            'limit': 1000,
            'page': 1
        }
        if (field is not None):
            body.update({
                'fields': field
            })
        if (sort is not None):
            body.update({
                'sort': sort
            })
        if (whereDict is not None):
            body.update(whereDict)

        return body
        
        
    def _getQueryForDetail(self, field=None, sort=None, whereDict=None, **kwargs):
        body = {
        }
        if (field is not None):
            body.update({
                'fields': field
            })
        if (sort is not None):
            body.update({
                'sort': sort
            })
        if (whereDict is not None):
            body.update(whereDict)
        body.update(kwargs)

        return body

    
    def _getRequestBody():
        body = {}


        
    def _apiGet(self, uri: str, header: dict, body: dict) -> tuple[int, any]:
        """APIを実施します
        link、pageがある場合、すべて実施してデータを結合します

        Args:
            uri (str): [description]
            header (dict): [description]
            body (dict): [description]

        Returns:
            tuple[int, any]: status, response の tuple statusが200でなければ、responseはエラー内容
        """
        response = requests.get(self.uri, headers=header, params=urlencode(body))
        resultList = response.json()
        if response.status_code != 200:
            errorResponse = ErrorResponse(resultList)
            return (response.status_code, errorResponse)

        while (('link' in response.headers) and ('next' in response.links)):
            print(response.links)
            uriNext = response.links['next']['url']
            response = requests.get(uriNext, headers=header)
            if response.status_code != 200:
                errorResponse = ErrorResponse(resultList)
                return (response.status_code, errorResponse)
            resultList.extend(response.json())

        return (response.status_code, resultList)


    def _apiPost(self, uri: str, header: dict, body: dict) -> tuple[int, any]:
        """POSTのAPIを実施します

        Args:
            uri (str): [description]
            header (dict): [description]
            body (dict): [description]

        Returns:
            tuple[int, any]: status_code, response の tuple
        """
        response = requests.post(self.uri, headers=header, data=json.dumps(body))
        result = response.json()
        if response.status_code != 200:
            errorResponse = ErrorResponse(result)
            return (response.status_code, errorResponse)

        return (response.status_code, result)
