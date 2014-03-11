import logging

import urlparse
import re

from pylons import request

from adhocracy import config
from adhocracy.lib.base import BaseController
from adhocracy.lib.templating import render_json, ret_abort

log = logging.getLogger(__name__)


class OembedController(BaseController):
    """ see http://www.oembed.com/ """

    identifier = 'oembed'

    def oembed(self, format=u'json'):
        if not 'url' in request.params:
            return ret_abort(u"Required parameter 'url' is missing", code=400)

        u = urlparse.urlparse(request.params.get('url'))

        # validate input url
        if (u.scheme != config.get('adhocracy.protocol')
                or u.netloc != config.get('adhocracy.domain')):
            return ret_abort(u"URL not supported", code=404)

        # set format to overlay
        path = re.sub('(\.[^./]*)?$', '.overlay', u.path)
        new_url = urlparse.ParseResult(u.scheme, u.netloc, path,
                                       u.params, u.query, u.fragment)
        new_url = urlparse.urlunparse(new_url)

        data = {
            'type': 'rich',
            'version': '1.0',
            'width': min(640, int(request.params.get('maxwidth', 640))),
            'height': int(request.params.get('maxheight', 750)),
            'provider_name': config.get('adhocracy.site.name')
        }

        data['html'] = '<iframe src="%s" frameborder="0"></iframe>' % new_url

        if format == u'json':
            return render_json(data)
        else:
            ret_abort(u"The format parameter must be one of: {json}.",
                      code=501)
