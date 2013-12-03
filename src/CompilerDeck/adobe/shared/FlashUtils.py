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
        v     = str(flashVersion).split('.')
        major = int(v[0])

        if major == 10:
            out = 10 + max(0, int(v[-1]) - 1)
        elif major == 11:
            out = 13 + int(v[-1])
        else:
            # Starting with flash player 12, consecutive releases are produced at the major level,
            # i.e. 13 follows 12 instead of 12.1.
            out = 23 + (major - 12)

        return out


