import urllib.parse
try:
	from tornado.curl_httpclient import CurlAsyncHTTPClient as AsyncHTTPClient
except:
	from tornado.httpclient import AsyncHTTPClient

class Single():
    ''' 单例模式 '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,"_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

def urlencode(url,query):
    ''' 用来处理url '''
    return url + "?" + urllib.parse.urlencode(query)

class Response():
    def __init__(self,request):
        self._content = None
        self.encoding = None
        self.request = request

    # 生成response对象
    @classmethod
    def _response(cls,response,request):
        resp = cls(request)
        ''' 这个地方可能有些问题，这个request对象应该返回我们封装的request对象，而不是tornado中的request对象
            但由于暂时request对象没有封装好，所以，暂时保留tornado中的request的对象，所以说，现在的request在之后会被替换
        '''
        resp.__dict__.update(response.__dict__)
        return resp

    @property
    def body(self):
        if self.buffer is None:
            return None
        elif self._body is None:
            self._body = self.buffer.getvalue()

        return self._body

    @property
    def content(self):
        if self.buffer is None:
            return None
        elif self._body is None:
            self._body = self.buffer.getvalue()

        return self._body

    @property
    def text(self):
        if not self.encoding:
            self.encoding = "utf-8"
        return self.content.decode(encoding=self.encoding,errors="ignore")

    @property
    def status(self):
        return self.code

class Request(Single):
    def __init__(self):
        if not hasattr(self,"client"):
            self.client = AsyncHTTPClient()

    def prepare(self,
                url=None, headers={}, files=None, data=None,
                params=None, auth=None, cookies=None, hooks=None, json=None,**kwargs):
        ''' 暂时只重写了部分参数，其他暂时空缺 '''
        body = urllib.parse.urlencode(data) if data else ""
        if params:
            url = url + "?" + urllib.parse.urlencode(query=params)
        if cookies:
            headers.update({"Cookie":urllib.parse.urlencode(cookies)})

        return url,{
            "headers":headers,
            "body":body,
        }

    async def requests(self,method,url,**kwargs):
        ''' 相当于一个基本的请求 '''
        url,kwargs = self.prepare(url=url,**kwargs)

        response = await self.client.fetch(url,method=method,**kwargs)
        resp = Response._response(response=response,request=self)
        return resp

    async def get(self,url,**kwargs):
        response = await self.requests(method="GET",url=url,**kwargs)
        return response

    async def post(self,url,**kwargs):
        return await self.requests(method="POST", url=url,**kwargs)


requests = Request()

# 测试代码
# if __name__ == '__main__':
#     import asyncio
#     loop = asyncio.get_event_loop()
#     async def main():
#         response = await requests.post("https://www.baidu.com",cookies={"abc":123})
#         print(response.text)
#     loop.run_until_complete(main())
