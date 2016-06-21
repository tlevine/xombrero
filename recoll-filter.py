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
        ipath = int(params["ipath:"].decode("utf-8"))
        self.fp.seek(ipath)        
        return self.getnext()

    def getnext(self, *_):
        try:
            uri = nextline(fp)
        except StopIteration:
            ok = True
            docdata = None
            uri = None
            eof = rclexecm.RclExecM.eofnow
        else:
            try:
                title = nextline(fp)
                date = nextline(fp)
            except StopIteration:
                ok = False
                docdata = None
                eof = rclexecm.RclExecM.eofnow
            else:
                ok = True
                docdata = render_docdata(title, date)
                eof = rclexecm.RclExecM.noteof

        return (ok, docdata, uri, eof)

def nextline(fp):
    line = fp.readline()
    if line:
        return line[:-1]
    else:
        raise StopIteration

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
