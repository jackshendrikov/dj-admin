from urllib.parse import urlparse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

import re
import urllib

DOMAIN_FORMAT = re.compile(
    r"(?:^(\w{1,255}):(.{1,255})@|^)"  # http basic authentication [optional]

    r"(?:(?:(?=\S{0,253}(?:$|:))"  # check full domain length to be less than or equal to 253 
    # (starting after http basic auth, stopping before port)

    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"  # check for at least one subdomain 
    # (maximum length per subdomain: 63 characters), dashes in between allowed

    r"(?:[a-z0-9]{1,63})))"  # check for top level domain, no dashes allowed

    r"|localhost)"  # accept also "localhost" only

    r"(:\d{1,5})?",  # port [optional]
    re.IGNORECASE
)

SCHEME_FORMAT = re.compile(
    r"^(http|hxxp)s?$",  # scheme: http(s)
    re.IGNORECASE
)

COUNTRY_FORMAT = re.compile(
    # all countries codes
    r"^(AF|AX|AL|DZ|AS|AD|AO|AI|AQ|AG|AR|AM|AW|AU|AT|AZ|BS|BH|BD|BB|BY|BE|BZ|BJ|BM|BT|BO|"
    r"BQ|BA|BW|BV|BR|IO|BN|BG|BF|BI|KH|CM|CA|CV|KY|CF|TD|CL|CN|CX|CC|CO|KM|CG|CD|CK|CR|CI|"
    r"HR|CU|CW|CY|CZ|DK|DJ|DM|DO|EC|EG|SV|GQ|ER|EE|ET|FK|FO|FJ|FI|FR|GF|PF|TF|GA|GM|GE|DE|"
    r"GH|GI|GR|GL|GD|GP|GU|GT|GG|GN|GW|GY|HT|HM|VA|HN|HK|HU|IS|IN|ID|IR|IQ|IE|IM|IL|IT|JM|"
    r"JP|JE|JO|KZ|KE|KI|KP|KR|KW|KG|LA|LV|LB|LS|LR|LY|LI|LT|LU|MO|MK|MG|MW|MY|MV|ML|MT|MH|"
    r"MQ|MR|MU|YT|MX|FM|MD|MC|MN|ME|MS|MA|MZ|MM|NA|NR|NP|NL|NC|NZ|NI|NE|NG|NU|NF|MP|NO|OM|"
    r"PK|PW|PS|PA|PG|PY|PE|PH|PN|PL|PT|PR|QA|RE|RO|RU|RW|BL|SH|KN|LC|MF|PM|VC|WS|SM|ST|SA|"
    r"SN|RS|SC|SL|SG|SX|SK|SI|SB|SO|ZA|GS|SS|ES|LK|SD|SR|SJ|SZ|SE|CH|SY|TW|TJ|TZ|TH|TL|TG|"
    r"TK|TO|TT|TN|TR|TM|TC|TV|UG|UA|AE|GB|US|UM|UY|UZ|VU|VE|VN|VG|VI|WF|EH|YE|ZM|ZW)$",

    re.IGNORECASE
)


def validate_url(url):
    try:
        url = url.strip()

        if not url:
            raise ValidationError(_('No URL specified'), code='invalid')

        if len(url) > 2048:
            raise ValidationError(_('URL exceeds its maximum length of 2048 characters (given length={%(urlLen)d})'),
                                  params={'urlLen': len(url)}, )

        result = urllib.parse.urlparse(url)
        scheme = result.scheme
        domain = result.netloc

        if not scheme:
            raise ValidationError(_('No URL scheme specified'), code='invalid')

        if not re.fullmatch(SCHEME_FORMAT, scheme):
            raise ValidationError(_('URL scheme must either be http(s) (given scheme={%(scheme)s})'),
                                  params={'scheme': scheme}, )

        if not domain:
            raise ValidationError(_('No URL domain specified'), code='invalid')

        if not re.fullmatch(DOMAIN_FORMAT, domain):
            raise ValidationError(_('URL domain malformed (domain={%(domain)s})'),
                                  params={'domain': domain}, )

    except AttributeError:
        raise ValidationError(_('Invalid URL'), code='invalid')


def validate_country(country):
    if not re.fullmatch(COUNTRY_FORMAT, country):
        raise ValidationError(_('Invalid Country Code'), code='invalid')
