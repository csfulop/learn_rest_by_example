import json

import webob
from pecan.hooks import PecanHook


class JsonErrorHook(PecanHook):
    def on_error(self, state, exc):
        response = {'status': state.response.status_int, 'detail': str(exc)}
        return webob.Response(
            body=json.dumps(response),
            status=state.response.status_int,
            content_type='application/json',
            charset='UTF-8'
        )
