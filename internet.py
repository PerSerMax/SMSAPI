from typing import Self


class HTTP:
    def __init__(self, a, b, c):
        self._headers = dict()
        self._body = ""
        self._a = a
        self._b = b
        self._c = c

    def add_header(self, key: str, value: str) -> Self:
        self._headers[key] = value
        return self

    def pop_header(self, key: str) -> str:
        return self._headers.pop(key)

    def add_headers(self, headers: dict):
        for k, v in headers.items():
            self.add_header(k, v)

    def pop_headers(self, headers: dict):
        for k, v in headers.items():
            self.pop_header(k)

    @property
    def body(self) -> str:
        return self._body

    @property
    def headers(self):
        return self._headers

    @body.setter
    def body(self, v: str):
        self._body = v

    def to_bytes(self) -> bytes:
        return str(self).encode()

    def __str__(self):
        res = f"{self._a} {self._b} {self._c}\r\n"
        for k, v in self._headers.items():
            res += f"{k}: {v}\r\n"
        res += "\r\n"
        res += self._body
        return res

    @staticmethod
    def _from_bytes(data: bytes):
        str_num = 0
        headers = []
        try:
            data = data.decode()
            data = data.split("\r\n\r\n")

            a, b, c = data[0].split("\r\n")[0].split(maxsplit=2)
            headers = data[0].split("\r\n")[1:]
            body = data[1]

            tmp = dict()
            for h in headers:
                str_num += 1
                k, v = h.split(":", maxsplit=1)
                v = v.lstrip()
                k = k.lstrip()
                tmp[k] = v
            headers = tmp

            return a, b, c, headers, body
        except Exception as e:
            print(f"На строчке номер {str_num} произошла ошибка: {e}")
            print(data[0].split('\r\n')[str_num])


class HRequest(HTTP):
    def __init__(self, method: str, uri: str, http_version: str):
        super().__init__(method, uri, http_version)

    @property
    def method(self):
        return self._a

    @property
    def uri(self):
        return self._b

    @property
    def http_version(self):
        return self._c

    @method.setter
    def method(self, v: str):
        self._a = v.upper()

    @uri.setter
    def uri(self, v: str):
        self._b = v

    @http_version.setter
    def http_version(self, v: str):
        self._c = v.upper()

    @staticmethod
    def from_bytes(data: bytes) -> 'HRequest' or None:
        tmp = HTTP._from_bytes(data)
        if tmp:
            method, uri, http_version, headers, body = tmp
            req = HRequest(method, uri, http_version)
            req.add_headers(headers)
            req.body = body
            return req


class HResponse(HTTP):
    def __init__(self, http_version: str, status_code: str, status_msg: str):
        super().__init__(http_version, status_code, status_msg)

    @property
    def http_version(self):
        return self._a

    @property
    def status_code(self):
        return self._b

    @property
    def status_msg(self):
        return self._c

    @http_version.setter
    def http_version(self, v):
        self._a = v

    @status_code.setter
    def status_code(self, v):
        self._b = v

    @status_msg.setter
    def status_msg(self, v):
        self._c = v

    @staticmethod
    def from_bytes(data: bytes) -> 'HResponse' or None:
        tmp = HTTP._from_bytes(data)
        if tmp:
            http_version, status_code, status_msg, headers, body = tmp
            resp = HResponse(http_version, status_code, status_msg)
            resp.add_headers(headers)
            resp.body = body
            return resp


#Проверка
if __name__ == "__main__":
    a = HRequest.from_bytes(b"GET / HTTP/1.1\r\nHost: www.example.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\n\r\nHERE IS BODY")
    print(a)
    print(a.method, a.uri, a.http_version)
    print(a.headers)
    print(a.body)
