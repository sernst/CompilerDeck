# AndroidLogcatThread.py
# (C)2012-2013
# Scott Ernst

import re
from collections import namedtuple

from pyaid.ArgsUtils import ArgsUtils
from pyaid.system.SystemUtils import SystemUtils

from pyglass.threading.RemoteExecutionThread import RemoteExecutionThread

#___________________________________________________________________________________________________ AndroidLogcatThread
class AndroidLogcatThread(RemoteExecutionThread):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    DUMP_MODE   = 'dump'
    CLEAR_MODE  = 'clear'

    _LOGCAT_ENTRY = namedtuple('LOGCAT_ENTRY', ['id', 'value', 'color', 'backColor', 'ignore'])

    _ENTRY_TYPES = [
        {'values':['myAppAne'], 'reValues':[], 'color':'#997788', 'backColor':'#FFDDEE'},
        {'values':['myapp'], 'reValues':[], 'color':'#667799', 'backColor':'#DDEEFF'},
        {'values':['adobe', 'cordova', 'droidgap', 'phonegap'],
         'reValues':['air'], 'color':'#779977', 'backColor':'#EEFFEE'
        }
    ]

    _LOGCAT_HEADER_RE = re.compile(
        '\[\s+(?P<month>[0-9]+)-(?P<day>[0-9]+)\s+(?P<time>[0-9:\.]+)\s+(?P<pid>[^\s]+)\s+'
        + '(?P<level>[A-Za-z]{1})/(?P<id>[^\]]+)\]'
    )

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of InstallAPKThread."""
        RemoteExecutionThread.__init__(self, parent, **kwargs)
        self._mode = ArgsUtils.get('mode', AndroidLogcatThread.DUMP_MODE, kwargs)

#___________________________________________________________________________________________________ _runImpl
    def _runImpl(self):
        if self._mode == AndroidLogcatThread.CLEAR_MODE:
            result = self._runClear()
            messages = [
                'Android logcat cleared.',
                'Logcat clearing failed. Is your device connected?'
            ]
        else:
            result = self._runDump()
            messages = [
                'Android logcat dump complete.',
                'Android logcat dump failed. Is your device connected?'
            ]

        if result['out']:
            self._log.write(
                '<div style="color:#666666;">'
                + '<div style="font-size:18px">Result:'
                + '</div>' + result['out']
                + ('' if result['code'] else ('<br/>' + result['error']))
                + '</div>'
            )

        if result['code'] and result['error']:
            self._log.write(
                '<div style="color:#993333">'
                + '<div style="font-size:18px">Error:'
                + '</div>' + result['error'] + '</div>'
            )

        self._log.write(
            ('FAILED: [' + str(result['code']) + ']' + messages[1])
             if result['code'] else
            ('SUCCESS: ' + messages[0])
        )
        return result['code']

#___________________________________________________________________________________________________ _runDump
    def _runDump(self):
        self._log.write(
            '<div style="font-size:24px">Retrieving Android Logcat...</div>\n'
        )

        cmd = [
            '"%s"' % self.parent().mainWindow.getAndroidSDKPath('platform-tools', 'adb.exe'),
            'logcat',
            '-d',
            '-v', 'long'
        ]

        result = SystemUtils.executeCommand(cmd)
        if 'out' in result:
            out = result['out']

            res = AndroidLogcatThread._LOGCAT_HEADER_RE.finditer(out)
            if res:
                entries = []
                for r in res:
                    if entries:
                        entries[-1]['value'] = out[entries[-1]['res'].end():r.start()].strip()
                    entries.append({
                        'res':r,
                        'level':r.groupdict()['level'],
                        'pid':r.groupdict()['pid'],
                        'time':r.groupdict()['time'],
                        'id':r.groupdict()['id']
                    })
                entries[-1]['value'] = out[entries[-1]['res'].end():].strip()

                res = ''
                for item in entries:
                    if 'value' not in item:
                        continue

                    item = self._parseLogEntry(item)

                    if item.ignore:
                        res += u'<div style="color:#999999;font-size:10px;">' + item.value + u'</div>'
                        continue

                    res += u'<div style="font-size:5px;">.</div><div style="color:' + item.color \
                        + u';font-size:14px;">' \
                        + u'<span style="background-color:' + item.backColor \
                        + u';font-size:10px;">[' + item.id \
                        + u']</span> ' + item.value + u'</div><div style="font-size:5px;">.</div>'

                if res:
                    result['out'] = res

        return result

#___________________________________________________________________________________________________ _runClear
    def _runClear(self):
        self._log.write(
            '<div style="font-size:24px">Clearing Android Logcat...</div>\n'
        )

        cmd = [
            '"%s"' % self.parent().mainWindow.getAndroidSDKPath('platform-tools', 'adb.exe'),
            'logcat',
            '-c'
        ]

        return SystemUtils.executeCommand(cmd)

#___________________________________________________________________________________________________ _parseLogEntry
    def _parseLogEntry(self, item):
        cls = AndroidLogcatThread
        try:
            vid   = item['id'].decode('utf8', 'ignore')
            value = item['value'].decode('utf8', 'ignore')
        except Exception, err:
            print 'ITEM:', item
            print 'ID:', item['id']
            print 'VALUE:', item['value']
            raise

        for searchType in cls._ENTRY_TYPES:
            result = cls._LOGCAT_ENTRY(
                id=vid,
                value=value,
                ignore=False,
                color=searchType['color'],
                backColor=searchType['backColor'],
            )

            for search in searchType['values']:
                if vid.lower().find(search) != -1:
                    return result

            for search in searchType['reValues']:
                if re.compile('(^|[^A-Za-z]+)%s($|[^A-Za-z]+)' % search).search(vid.lower()):
                    return result

        for searchType in cls._ENTRY_TYPES:
            result = cls._LOGCAT_ENTRY(
                id=vid,
                value=value,
                ignore=False,
                color=searchType['color'],
                backColor=searchType['backColor'],
            )

            for search in searchType['values']:
                if value.lower().find(search) != -1:
                    return result

            for search in searchType['reValues']:
                if re.compile('(^|[^A-Za-z]+)%s($|[^A-Za-z]+)' % search).search(value.lower()):
                    return result

        return cls._LOGCAT_ENTRY(
            id=vid,
            value=value,
            ignore=True,
            color=None,
            backColor=None,
        )
