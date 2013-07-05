# FlashUtils.py
# (C)2012-2013
# Scott Ernst

#___________________________________________________________________________________________________ FlashUtils
class FlashUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ convertFlashToSwfVersion
    @classmethod
    def convertFlashToSwfVersion(cls, flashVersion):
        """Creates a new instance of FlashUtils."""
        out = 0
        v   = str(flashVersion).split('.')

        if v[0] == '10':
            out = 10 + max(0, int(v[-1]) - 1)
        elif v[0] == '11':
            out = 13 + int(v[-1])

        return out


