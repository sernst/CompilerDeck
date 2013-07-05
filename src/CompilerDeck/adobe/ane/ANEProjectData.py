# ANEProjectData.py
# (C)2012-2013
# Scott Ernst

from CompilerDeck.adobe.shared.ProjectData import ProjectData

#___________________________________________________________________________________________________ ANEProjectData
class ANEProjectData(ProjectData):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, projectPath, **kwargs):
        """Creates a new instance of ClassTemplate."""
        ProjectData.__init__(self, projectPath=projectPath, **kwargs)

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: sharedClasses
    @property
    def sharedClasses(self):
        return self.getSetting('SHARED_CLASSES', [])

#___________________________________________________________________________________________________ GS: androidLibIncludes
    @property
    def androidLibIncludes(self):
        return self.getSetting(['ANDROID', 'LIB_INCLUDES'], [], error=False)
