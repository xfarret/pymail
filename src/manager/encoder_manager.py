import base64
from email.header import decode_header


class EncoderManager:

    @staticmethod
    def __b64padanddecode__(b):
        """Decode unpadded base64 data"""
        b += (-len(b) % 4) * '='  # base64 padding (if adds '===', no valid padding anyway)
        return base64.b64decode(b, altchars='+,', validate=True).decode('utf-16-be')

    @staticmethod
    def imaputf7decode(s):
        """Decode a string encoded according to RFC2060 aka IMAP UTF7.
        Minimal validation of input, only works with trusted data"""
        lst = s.split('&')
        out = lst[0]
        for e in lst[1:]:
            u, a = e.split('-', 1)  # u: utf16 between & and 1st -, a: ASCII chars folowing it
            if u == '':
                out += '&'
            else:
                out += EncoderManager.__b64padanddecode__(u)
            out += a
        return out

    @staticmethod
    def imaputf7encode(s):
        """"Encode a string into RFC2060 aka IMAP UTF7"""
        s = s.replace('&', '&-')
        iters = iter(s)
        unipart = out = ''
        for c in s:
            if 0x20 <= ord(c) <= 0x7f:
                if unipart != '':
                    out += '&' + base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=') + '-'
                    unipart = ''
                out += c
            else:
                unipart += c
        if unipart != '':
            out += '&' + base64.b64encode(unipart.encode('utf-16-be')).decode('ascii').rstrip('=') + '-'
        return out

    @staticmethod
    def imap8859decode(s):
        if s is None:
            return None

        list_encoded = decode_header(s)

        result = list()
        for elem_list in list_encoded:
            try:
                if elem_list[1] is None:
                    result.append(elem_list[0].decode())
                else:
                    result.append(elem_list[0].decode(elem_list[1]))
            except AttributeError:
                result.append(elem_list[0])

        str = ' '.join(result)
        return str
