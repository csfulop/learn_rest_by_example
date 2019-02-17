"""
Use custom Pecan hook to return JSON error content.
For more details see: https://pecan.readthedocs.io/en/latest/hooks.html
"""

import json

import webob
from pecan.hooks import PecanHook


class JsonErrorHook(PecanHook):
    def on_error(self, state, exc) -> webob.Response:
        response = {'status': state.response.status_int, 'detail': str(exc)}
        return webob.Response(
            body=json.dumps(response),
            status=state.response.status_int,
            content_type='application/json',  # FIXME: use application/problem+json
            charset='UTF-8'
        )
