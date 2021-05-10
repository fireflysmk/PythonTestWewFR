class GetRequests:

    @staticmethod
    def parse_input_data(data: str):
        result = {}
        if data:
            data_lst = data.split('&')
            for i in data_lst:
                k, v = i.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(env):
        query = env['QUERY_STRING']
        req_dict = GetRequests.parse_input_data(query)
        return req_dict


class PostRequests:

    @staticmethod
    def parse_input_data(data: str):
        res = {}
        if data:
            data_lst = data.split('&')
            for i in data_lst:
                k, v = i.split('=')
                res[k] = v
        return res

    @staticmethod
    def get_wsgi_input_data(env) -> bytes:

        length_data = env.get('CONTENT_LENGTH')
        try:
            content_len = int (length_data)
        except ValueError:
            content_len = 0

        if content_len > 0:
            data = env['wsgi.input'].read(content_len)
        else:
            data = b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        res = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            res = self.parse_input_data(data_str)
        return res

    def get_request_params(self, env):
        data = self.get_wsgi_input_data(env)
        data = self.parse_wsgi_input_data(data)
        return data
