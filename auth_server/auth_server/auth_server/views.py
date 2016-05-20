import logging, jwt, json, datetime, uuid, re
from django.http.response import HttpResponse
from django.conf import settings

from .utils import get_private_key, get_certificate


logger = logging.getLogger('django.request')


SCOPE_RE = re.compile(r'^(?P<type>repository):(?P<name>[^:]+)(?::(?P<tag>[^:]))?:(?P<actions>.*)$')
class Scope(object):
    def __init__(self, scope_type, name, tag, actions):
        self.type = scope_type
        self.name = name
        self.tag = tag
        self.actions = actions

    def __repr__(self):
        return 'Scope(%r, %r, %r, %r)' % (self.type,
                                          self.name,
                                          self.tag,
                                          self.actions)

    @classmethod
    def parse(cls, scope_str):
        if isinstance(scope_str, unicode):
            scope_str = scope_str.encode('utf8')
        parsed = SCOPE_RE.match(scope_str.strip().lower())
        return Scope(parsed.group('type'),
                     parsed.group('name'),
                     parsed.group('tag'),
                     parsed.group('actions').split(','))


def get_token(request):
    now = datetime.datetime.utcnow()
    token_payload = {
                     'iss' : 'auth_server',
                     'sub' : 'test',
                     'aud' : 'test-registry',
                     'exp' : now + datetime.timedelta(seconds = settings.TOKEN_VALID_FOR_SECONDS),
                     'nbf' : now,
                     'iat' : now,
                     'jti' : uuid.uuid4().get_hex(),
                     'access' : [
                                {
                                 'type' : scope.type,
                                 'name' : scope.name,
                                 'actions' : scope.actions
                                 }
                                for scope in (Scope.parse(s) for s
                                              in request.GET.getlist('scope'))
                                 ]
                     }
    logger.debug(('token', token_payload))
    response_payload = {
                        'token' : jwt.encode(token_payload,
                                             get_private_key(),
                                             headers = {
                                                        'x5c' : [ get_certificate() ]
                                                        },
                                             algorithm = settings.JWT_SIGNATURE_ALGO),
                        'expires_in' : '3600',
                        'issued_at' : datetime.datetime.utcnow().isoformat() + 'Z'
                        }
    logger.debug(('response', json.dumps(response_payload)))
    return HttpResponse(json.dumps(response_payload),
                        content_type = 'application/json')
