#!/usr/bin/env python2.7
import rclexecm

class XombreroHistoryExtractor:
    def __init__(self, em):
        self.em = em

    def openfile(self, params):
        try:
            self.fp = open(params["filename:"], "rb")
        except Exception as err:
            self.em.rclog("openfile: failed: [%s]" % err)
            return False
        else:
            return True

    def getipath(self, params):
        raise NotImplementedError('aaaaa')
        ipath = params["ipath:"][:-4]

        docdata = ""
        eof = rclexecm.RclExecM.noteof

        try:
            docdata = self._docdata(int(ipath.decode('utf-8')))
        except Exception as err:
            ok = False
        else:
            ok = True
            docdata = self._data(ipath)
            eof = rclexecm.RclExecM.eofnext

        return (ok, docdata, ipath, eof)

    def getnext(self, *_):
        try:
            uri = next(self.fp)[:-1]
        except StopIteration:
            ok = True
            docdata = None
            uri = None
            eof = rclexecm.RclExecM.eofnow
        else:
            try:
                title = next(self.fp)[:-1]
                date = next(self.fp)[:-1]
            except StopIteration:
                ok = False
                docdata = None
                eof = rclexecm.RclExecM.eofnow
            else:
                ok = True
                docdata = render_docdata(title, date)
                eof = rclexecm.RclExecM.noteof

        return (ok, docdata, uri, eof)

def render_docdata(date, title):
    clean_title = title.replace(b'&', b'&amp;') \
        .replace(b'<', b'&lt;').replace(b'>', b'&gt;')
    return b'''\
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="date" content="%(date)s">
  </head>
  <body>%(title)s</body>
</html>
''' % {'date': date, 'title': clean_title}


proto = rclexecm.RclExecM()
extract = XombreroHistoryExtractor(proto)
rclexecm.main(proto, extract)
