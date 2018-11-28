import inspect
import json

import requests

from wechat.client.api.base import BaseAPICollection
from wechat.storage.memorystorage import MemoryStorage

AccessToken = 'access_token'


def _is_api_endpoint(obj): return isinstance(obj, BaseAPICollection)


class BaseAPIClient:
    POST = 'post'
    GET = 'get'

    API_URL_PREFIX = None

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, app_id, app_secret, storage=None, timeout=3, auto_retry=True):
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.storage = storage or MemoryStorage()
        self._http = requests.Session()
        self.auto_retry = auto_retry
        self.timeout = timeout

    @property
    def access_token(self):
        access_token = self.storage.get(AccessToken)
        if access_token is None:
            access_token = self._get_access_token()
        return access_token

    @property
    def app_id(self):
        return self.__app_id

    def get(self, endpoint, **kwargs):
        return self._request(
            method=self.GET,
            url_or_endpoint=endpoint,
            **kwargs
        )

    def post(self, endpoint, **kwargs):
        return self._request(
            method=self.POST,
            url_or_endpoint=endpoint,
            **kwargs
        )

    def _get_access_token(self):
        """
        Reference:
            https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140183
        """

        rv = self.post(
            endpoint='/token',
            datas={
                "grant_type": "client_credential",
                "appid": self.__app_id,
                "secret": self.__app_secret
            },
            result_processor=lambda result: result['access_token']
        )

        # -60 ensure access_token is valid
        self.storage.set(AccessToken, rv, ttl=7200 - 60)

        return rv

    # TODO: 0.0
    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('API_URL_PREFIX', self.API_URL_PREFIX)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'access_token' not in kwargs['params']:
            kwargs['params']['access_token'] = self.access_token
        if isinstance(kwargs.get('data', ''), dict):
            body = json.dumps(kwargs['data'], ensure_ascii=False)
            body = body.encode('utf-8')
            kwargs['data'] = body

        kwargs['timeout'] = kwargs.get('timeout', self.timeout)
        result_processor = kwargs.pop('result_processor', None)
        res = self._http.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as e:
            raise WechatAPIException(
                errcode=None,
                errmsg=None,
                client=self,
                request=e.request,
                response=e.response
            )

        return self._handle_result(
            res, method, url, result_processor, **kwargs
        )

    def _handle_result(self, res, method=None, url=None,
                       result_processor=None, **kwargs):
        result = res

        if not isinstance(result, dict):
            return result

        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result.get('errmsg', errcode)
            if self.auto_retry and errcode in (
                    WechatAPIStatus.INVALID_CREDENTIAL,
                    WechatAPIStatus.INVALID_ACCESS_TOKEN,
                    WechatAPIStatus.EXPIRED_ACCESS_TOKEN):
                # logger.info('Access token expired, fetch a new one and retry request')
                access_token = self._get_access_token()
                kwargs['params']['access_token'] = access_token
                return self._request(
                    method=method,
                    url_or_endpoint=url,
                    result_processor=result_processor,
                    **kwargs
                )
            elif errcode == WechatAPIStatus.OUT_OF_API_FREQ_LIMIT:
                # api freq out of limit
                raise APILimitedException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise WechatAPIException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )

        return result if not result_processor else result_processor(result)


class WechatAPIStatus:
    OK = 0

    # AppSecret 错误，或是 Access Token 无效
    # 请开发者认真比对AppSecret的正确性，或查看是否正在为恰当的公众号调用接口
    INVALID_CREDENTIAL = 40001

    # 错误的凭证类型
    INVALID_CREDENTIAL_TYPE = 40002

    # 错误的 OpenID
    # 请开发者确认 OpenID 是否已关注公众号，或是否是其他公众号的 OpenID
    INVALID_OPENID = 40003

    # 不合法的 Access Token
    # 请开发者认真比对 Access Token 的有效性（如是否过期），或查看是否正在为恰当的公众号调用接口
    INVALID_ACCESS_TOKEN = 40014

    # Access Token 已失效
    # 请检查 Access Token 的有效期，重新刷新 Access Token
    EXPIRED_ACCESS_TOKEN = 42001

    # 接口调用频率超过限制
    OUT_OF_API_FREQ_LIMIT = 45009


class WechatAPIException(Exception):
    def __init__(self, *args, **kwargs):
        pass


class APILimitedException(WechatAPIException):
    pass
