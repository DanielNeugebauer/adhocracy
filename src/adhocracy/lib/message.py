from pylons.i18n import _
from pylons import config


def render_body(body, recipient, include_footer, is_preview=False):
    from adhocracy.lib import helpers as h
    from adhocracy.lib.templating import render
    from adhocracy.lib.auth.welcome import welcome_url

    if recipient.gender == 'f':
        salutation = _('Dear Ms.')
    elif recipient.gender == 'm':
        salutation = _('Dear Mr.')
    else:
        salutation = _('Dear')

    if is_preview:
        welcome_url = welcome_url(recipient,
                                  (u'X' * len(recipient.welcome_code)
                                   if recipient.welcome_code
                                   else u'NO_WELCOME_CODE_SET'))
    else:
        welcome_url = welcome_url(recipient, recipient.welcome_code)

    rendered_body = body.format(**{
        'uid': u'%d' % recipient.id,
        'name': recipient.name,
        'email': recipient.email,
        'welcome_url': welcome_url,
        'salutation': salutation,
    })

    return render("/massmessage/body.txt", {
        'body': rendered_body,
        'page_url': config.get('adhocracy.domain').strip(),
        'settings_url': h.entity_url(recipient,
                                     member='settings/notifications',
                                     absolute=True),
        'include_footer': include_footer,
    })


def _send(message, force_resend=False):
    for r in message.recipients:
        if (r.recipient.is_email_activated() and
                r.recipient.email_messages):

            from adhocracy.lib import mail

            body = render_body(message.body, r.recipient,
                               message.include_footer)

            mail.to_user(r.recipient,
                         message.subject,
                         body,
                         headers={},
                         decorate_body=False,
                         email_from=message.email_from,
                         name_from=message.name_from)
