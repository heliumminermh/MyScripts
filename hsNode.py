from maya.mel import *
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.mel as mel
import math, re, inspect
from pymel.core import *

mayaVer = int(str(cmds.about(v=1))[0:4])
if mayaVer < 2024:
    from maya.OpenMaya import *
    import maya.OpenMaya as om
    import maya.api.OpenMaya as om2
else:
    from maya.api.OpenMaya import *
    import maya.api.OpenMaya as om

class myNode(type):

    def __repr__(self):
        return 'hsNode'

class hsNode(str, metaclass=myNode):
    _cNum = None
    _cType = None
    _uvNums = None
    _attrSup = None

    def __new__(cls, *args, **kwargs):
        hsN = (super(hsNode, cls).__new__)(cls, *args, **kwargs)
        return hsN

    def __repr__(self):
        frame = inspect.currentframe().f_back
        dictN = dict(list(frame.f_globals.items()) + list(frame.f_locals.items()))
        fGlobals = frame.f_globals
        for (k, var) in list(dictN.items()):
            if isinstance(var, self.__class__):
                if hash(self) == hash(var):
                    if self._cNum >= 0 or self._uvNums:
                        fGlobals[k] = hsNode(self.name())
                    else:
                        fGlobals[k] = self.asObj()
                    break
        return self.name()

    def __str__(self):
        frame = inspect.currentframe().f_back
        dictN = dict(list(frame.f_globals.items()) + list(frame.f_locals.items()))
        fGlobals = frame.f_globals
        for (k, var) in list(dictN.items()):
            if isinstance(var, self.__class__):
                if hash(self) == hash(var):
                    if self._cNum > 0 or self._uvNums:
                        fGlobals[k] = hsNode(self.name())
                    else:
                        fGlobals[k] = self.asObj()
                    break
        return self.name()

    def __call__(self, getInfo=0):
        if getInfo:
            argList = [arg for arg in dir(self) if not arg.startswith('_')]
            uArgList = [arg for arg in dir(str) if not arg.startswith('_')]
            for arg in uArgList:
                argList.remove(arg)
            for item in argList:
                try:
                    exec('print(item); print(inspect.getargspec(self.' + item + '));')
                except:
                    pass
                exec('print(self.' + item + '.__doc__')
                print('\n')
            print('Total Methods (Rigging Pipeline): ', len(argList) + len(uArgList))
        numParents = self._MDagPath().length() - 1
        numSibs = self.selectSiblings()[-1] - 1
        numChd = self.numChildren()
        self.select()
        return [self.name(), numParents, numSibs, numChd]

    def __del__(self):
        pass

    def __init__(self, obj, attrSup=0):
        """
        To Support main auto rig scripts via hsNode

        Module Name :
        -------------
        **hsNode_v2.0**

        About :
        -------
        Author: Yogesh Nichal
        Rigging Artist & Programmer
        """
        self._attrSup = attrSup
        self.isComp = False
        _hsNode__mayaVer = int(str(cmds.about(v=1))[0:4])
        if not objExists(str(obj)):
            self._confirmAction('Maya Node "%s" Doesn\'t Exist' % str(obj), True)
        if '.' in str(obj):
            self.isComp = True
            if '.vtx[' in str(obj):
                self._cType = 'vtx'
            elif '.e[' in str(obj):
                self._cType = 'e'
            elif re.match('^.*\\.cv\\[(?P<uVal>\\d+)\\]\\[(?P<vVal>\\d+)\\]$', str(obj)):
                self._cType = 'uv'
            elif re.match('^.*\\.cv\\[(?P<uVal>\\d+)\\]$', str(obj)):
                self._cType = 'cv'
            elif '.f[' in str(obj):
                self._cType = 'f'
            self._cNum = 0
            if re.match('^.*\\.(cv|vtx|f|e)\\[(?P<uVal>\\d+)\\]$', str(obj)):
                reObj = re.search('(?<=\\[)(?P<vtxNum>[\\d]+)(?=\\])', str(obj))
                self._cNum = int(reObj.group())
            elif re.match('^.*\\.cv\\[(?P<uVal>\\d+)\\]\\[(?P<vVal>\\d+)\\]$', str(obj)):
                reObj = re.match('^.*\\.cv\\[(?P<uVal>\\d+)\\]\\[(?P<vVal>\\d+)\\]$', str(obj))
                self._uvNums = [int(reObj.group('uVal')), int(reObj.group('vVal'))]
            else:
                self._confirmAction('Need to provide vtx, edge, face or cv', raiseErr=True)
            objName = str(obj).split('.', 1)[0]
            activList = om.MSelectionList()
            activList.add(objName)
            pathDg = om.MDagPath()
            if _hsNode__mayaVer < 2025:
                activList.getDagPath(0, pathDg)
            else:
                pathDg = activList.getDagPath(0)
            if self._cType == 'vtx':
                compIt = om.MItMeshVertex(pathDg)
            elif self._cType == 'e':
                compIt = om.MItMeshEdge(pathDg)
            elif self._cType == 'f':
                compIt = om.MItMeshPolygon(pathDg)
            elif self._cType == 'cv':
                compIt = om.MItCurveCV(pathDg)
            elif self._cType == 'uv':
                compIt = om.MItSurfaceCV(pathDg)
            if self._cType != 'uv':
                while not compIt.isDone():
                    if compIt.index() == self._cNum:
                        cName = compIt.currentItem()
                        break
                    else:
                        next(compIt)
            else:
                while not compIt.isDone():
                    while not compIt.isRowDone():
                        utilU = om.MScriptUtil()
                        utilU.createFromInt(0)
                        uInt = utilU.asIntPtr()
                        utilV = om.MScriptUtil()
                        utilV.createFromInt(0)
                        vInt = utilV.asIntPtr()
                        compIt.getIndex(uInt, vInt)
                        uvList = [om.MScriptUtil.getInt(uInt), om.MScriptUtil.getInt(vInt)]
                        if uvList == self._uvNums:
                            cName = compIt.currentItem()
                            break
                        else:
                            next(compIt)
                    if uvList == self._uvNums:
                        break
                    else:
                        compIt.nextRow()
        self.obj = str(obj)
        self.obj = self._MDagPath()
        self.setCtrlColor = self.applyCtrlColor
        if '.' not in self.name():
            if attrSup:
                attrList = self.listAttr(True, k=1)
                if attrList:
                    for attr in attrList:
                        if '.' not in attr:
                            attr2 = type(attr, (), {'set': (self._asset)(attr), 'get': (self._asget)(attr)})
                            exec('self.' + attr + '=attr2()')

    def _asset(self, attr, attrVal=0):
        def asset(attr, attrVal):
            self.setAttr(attr.__class__.__name__, attrVal)
        return asset

    def _asget(self, attr):
        def asget(attr):
            print(self.getAttr(attr.__class__.__name__))
        return asget

    def _MDagPath(self, mObj=None):
        activList = om.MSelectionList()
        pathDg = om.MDagPath()
        if self._mayaVer() < 2025:
            if mObj:
                om.MDagPath.getAPathTo(mObj, pathDg)
            else:
                activList.add(self.obj)
                activList.getDagPath(0, pathDg)
        elif mObj:
            pathDg = pathDg.getAPathTo(mObj)
        else:
            activList.add(self.obj)
            pathDg = activList.getDagPath(0)
        return pathDg

    def _MDagPath2(self, mObj=None):
        activList = om2.MSelectionList()
        pathDg = om2.MDagPath()
        if mObj:
            pathDg = pathDg.getAPathTo(mObj)
        else:
            activList.add(self.name())
            pathDg = activList.getDagPath(0)
        return pathDg

    def _confirmAction(self, action, raiseErr=False):
        if raiseErr:
            if not cmds.confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message=action, button=['Yes', 'No'], defaultButton='Yes'):
                raise RuntimeError(action)
        confirm = cmds.confirmDialog(title='Confirm Action?', message=action, button=['Yes', 'No'], defaultButton='Yes')
        if confirm == 'Yes':
            if cmds.objExists('skinMesh'):
                cmds.select('skinMesh')
            else:
                cmds.polySphere(name='skinMesh')
                cmds.select('skinMesh')
        elif confirm == 'No':
            return False
        return None

    def asObj(self):
        if self._cNum > 0:
            return hsNode(self.name().split('.', 1)[0])
        return hsNode(self.name())

    def name(self):
        dgPath = self._MDagPath()
        shapes = self.getShape(1)
        nodeName = ''  # Initialize with an empty string
        if not self._cNum:
            self._cNum = 0
        if self._cNum > 0 or self.isComp or self._cType == 'uv':
            if shapes:
                if len(shapes) == 1:
                    dgPath.pop()
            dgNodeFn = om.MFnDagNode()
            dgNodeFn.setObject(dgPath)
            nodeName = dgNodeFn.partialPathName()
        if not (self._cNum > 0 and self._cType):
            if not self.isComp or self._cType != 'uv':
                if nodeName:
                    nodeName += '.' + self._cType + '[' + str(self._cNum) + ']'
            elif self._cType == 'uv':
                if self._uvNums:
                    nodeName += '.cv[' + str(self._uvNums[0]) + ']' + '[' + str(self._uvNums[1]) + ']'
        return nodeName

    def _fullName(self):
        dgPath = self._MDagPath()
        if self._cNum > 0:
            dgPath.pop()
        dgNodeFn = om.MFnDagNode()
        dgNodeFn.setObject(dgPath)
        if self._cNum > 0:
            return dgNodeFn.fullPathName() + '.' + self._cType + '[' + str(self._cNum) + ']'
        return dgNodeFn.fullPathName()

    def fullName(self):
        """
                Objective:
                ----------
                It is useful whenever world space calculations are made.
                
                Returns
                -------
                MFnDagNode.fullPathName()               #_ Complete path name from root to hsNode
                """
        dgPath = self._MDagPath()
        shapes = self.getShape(1)
        if self._cNum > 0:
            if len(shapes) == 1:
                dgPath.pop()
            dgNodeFn = om.MFnDagNode()
            dgNodeFn.setObject(dgPath)
            if self._cNum > 0:
                return dgNodeFn.fullPathName() + '.' + self._cType + '[' + str(self._cNum) + ']'
            return dgNodeFn.fullPathName()

    def hasShape(self):
        """
                Returns True is hsNode has shape
                """
        if self._cNum > 0:
            shapes = cmds.listRelatives((self.name().split('.', 1)[0]), shapes=1)
        else:
            shapes = cmds.listRelatives((self.name()), shapes=1)
        if shapes:
            return True
        return False

    def getShape(self, multiShapes=False):
        """
                Returns:
                --------
                return u'shapeName'  #_ hsNode
                """
        try:
            if not multiShapes:
                if self._cNum > 0:
                    return hsNode(cmds.listRelatives((self._fullName().split('.', 1)[0]), shapes=1, f=1)[0])
                return hsNode(cmds.listRelatives((self._fullName()), shapes=1, f=1)[0])
            else:
                if self._cNum > 0:
                    return list(map(hsNode, cmds.listRelatives((self._fullName().split('.', 1)[0]), shapes=1, f=1)))
                return list(map(hsNode, cmds.listRelatives((self._fullName()), shapes=1, f=1)))
        except:
            return

    def nodeType(self, transformCheck=False):
        if not transformCheck:
            if self.hasShape():
                return cmds.nodeType(self.getShape())
            return cmds.nodeType(self.name())
        else:
            return cmds.nodeType(self.name())

    def _mayaVer(self):
        mayaStr = str(cmds.about(v=1))
        first4 = mayaStr[0:4]
        if first4.isalnum():
            if first4.startswith('20'):
                return int(first4)
            return 2014

    def _MObject(self):
        """
                Returns the Instance of Maya API node : MObject
                """
        dgPath = self._MDagPath()
        if self._cNum > 0:
            dgPath.pop()
        return dgPath.node()

    def _MBoundingBox(self):
        """
                Returns the Instance of Maya API node : MBoundixBox
                """
        mBB = self._MFnDagNode()
        if self._mayaVer() < 2025:
            return mBB.boundingBox()
        return mBB.boundingBox

    def _MFnDagNode(self, mObj=None, toShapeNode=False):
        """
                Returns the Instance of Maya API node : MFnDagNode
                """
        dgPath = self._MDagPath(mObj)
        if not toShapeNode:
            if self._cNum > 0 or self._cType == 'uv':
                dgPath.pop()
            return om.MFnDagNode(dgPath)

    def _MFnDependencyNode(self, mObj=None):
        """
                Returns the Instance of Maya API node : MFnDependencyNode
                """
        depFn = om.MFnDependencyNode()
        if mObj:
            depFn.setObject(mObj)
            return depFn
        dgPath = self._MDagPath()
        if self._cNum > 0:
            dgPath.pop()
        depFn.setObject(dgPath.node())
        return depFn

    def _nextVar(self, givenName, fromEnd=True, skipCount=0, versionUpAll=False):
        hsN = givenName
        if not versionUpAll:
            numList = re.findall('\\d+', hsN)
            numRange = list(range(len(numList)))
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                lenStr = len(numStr)
                nextNum = int(numStr) + 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

                reObj = re.search(patternStr, self.shortName())
                spanRange = reObj.span(len(numList) - 1 * skipCount)
                nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
                if objExists(nextName):
                    nextName = hsNode(nextName)
                return [nextName, nextNum]
            numStr = numList[skipCount]
            lenStr = len(numStr)
            nextNum = int(numStr) + 1
            nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
            patternStr = '[^\\d+]*'
            for num in numRange:
                patternStr += '(\\d+)'
                patternStr += '[^\\d+]*'

            reObj = re.search(patternStr, self.shortName())
            spanRange = reObj.span(skipCount + 1)
            nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
            if objExists(nextName):
                nextName = hsNode(nextName)
            return [nextName, nextNum]
        else:

            def repMGrp(mObj):
                numVal = int(mObj.group())
                formNum = len(mObj.group())
                formVar = '%0.' + str(formNum) + 'd'
                return str(formVar % (numVal + 1))

            nextName = re.sub('\\d+', repMGrp, self.shortName())
            if objExists(nextName):
                return hsNode(nextName)
            return nextName

    def _preVar(self, givenName, fromEnd=True, skipCount=0, versionUpAll=False):
        hsN = givenName
        if not versionUpAll:
            numList = re.findall('\\d+', hsN)
            numRange = list(range(len(numList)))
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                lenStr = len(numStr)
                nextNum = int(numStr) - 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

                reObj = re.search(patternStr, self.shortName())
                spanRange = reObj.span(len(numList) - 1 * skipCount)
                nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
                if cmds.objExists(nextName):
                    nextName = hsNode(nextName)
                return [nextName, nextNum]
            numStr = numList[skipCount]
            lenStr = len(numStr)
            nextNum = int(numStr) - 1
            nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
            patternStr = '[^\\d+]*'
            for num in numRange:
                patternStr += '(\\d+)'
                patternStr += '[^\\d+]*'

            reObj = re.search(patternStr, self.shortName())
            spanRange = reObj.span(skipCount + 1)
            nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
            if cmds.objExists(nextName):
                nextName = hsNode(nextName)
            return [nextName, nextNum]
        else:

            def repMGrp(mObj):
                numVal = int(mObj.group())
                formNum = len(mObj.group())
                formVar = '%0.' + str(formNum) + 'd'
                return str(formVar % (numVal - 1))

            nextName = re.sub('\\d+', repMGrp, self.shortName())
            if cmds.objExists(nextName):
                return hsNode(nextName)
            return nextName

    def _refreshView(self, num=1):
        """
                Usage:
                ------
                It refreshes current view of maya scene
                """
        if num:
            mEval = mel.eval
            for a in range(num):
                mEval('refresh -cv')

        else:
            pass

    def _startTime(self):
        """
                This function needs to be initiated to use 'hsN.computeTime()'
                """
        global _hsNode__start_Time
        _hsNode__start_Time = timerX()
        om.MGlobal.displayInfo('Started the time for "Total time calculation ..!!"')

    def _computeTime(self, killTime=False):
        """
                Returns:
                --------
                [[progressHour, progressMinute, progressSecond], '%dHr %dMin %dSec' % (progressHour, progressMinute, progressSecond)]
                
                For Ex, Returns:
                [[0, 10, 25], '0Hr 10Min 25Sec']
                """
        global _hsNode__start_Time
        _progHour = 0
        _progMinute = 0
        _progSecond = 0
        try:
            _progHour = int(cmds.timerX(startTime=_hsNode__start_Time) / 3600)
            _progMinute = int(cmds.timerX(startTime=_hsNode__start_Time) / 60 % 60)
            _progSecond = int(cmds.timerX(startTime=_hsNode__start_Time) % 60)
            if killTime:
                cmds.warning('Time is stopped.. Need to initiate time again ..!')
                del _hsNode__start_Time
        except NameError:
            cmds.warning('Time is not initiated.. First you need to start time ..!')

        if not _progHour:
            if not _progMinute:
                if not _progSecond:
                    return
            return [[_progHour, _progMinute, _progSecond], '%dHr %dMin %dSec' % (_progHour, _progMinute, _progSecond)]

    def _selected(self, getIter=False, listStr=False):
        """
                Returns:
                --------
                Returns [list of hsNodes] #_ if possible else normal strings
                Returns None                      #_ if nothing is selected ..          
                """
        selList = cmds.ls(sl=1, fl=1)
        if not selList:
            return
        if listStr:
            if getIter:
                return (obj for obj in selList)
            return selList
        elif getIter:
            try:
                sList = (hsNode(obj) for obj in selList)
                return sList
            except:
                return (obj for obj in selList)

        else:
            try:
                sList = list(map(hsNode, selList))
                return sList
            except:
                hsNodes = []
                append = hsNodes.append
                for obj in selList:
                    try:
                        append(hsNode(obj))
                    except:
                        append(obj)

                return hsNodes

    def _getFilePath(self, fileName=None):
        if not fileName:
            scnName = cmds.file(q=1, sn=1)
        else:
            scnName = fileName
        if scnName:
            (filePath, fileNameFull) = scnName.rsplit('/', 1)
            (fileName, fileExtn) = fileNameFull.rsplit('.')
            return [filePath, fileName, fileExtn]
        return

    def _message(self, messageTxt):
        """
                Sends a given message through confirmDialog window
                """
        cmds.confirmDialog(title='Message ..!', message=messageTxt, button=['Yes'], defaultButton='Yes')

    def _error(self, errorMsg):
        """
                Sends a given error message through confirmDialog window.
                After closing the window, RuntimeError will be raised
                """
        cmds.confirmDialog(title='Error..', bgc=(1, 0.5, 0), message=errorMsg, button=['Yes'], defaultButton='Yes')
        raise RuntimeError(errorMsg)

    def shortName(self):
        """
                Returns
                -------
                MFnDependencyNode.name()                #_ shortName | Exact Name | Only Name of the hsNode
                """
        depNodeFn = self._MFnDependencyNode()
        if self._cNum > 0:
            dgPath = self._MDagPath()
            dgPath.pop()
            dgNodeFn = om.MFnDagNode()
            dgNodeFn.setObject(dgPath)
            parentName = dgNodeFn.partialPathName()
            return parentName + '.' + self._cType + '[' + str(self._cNum) + ']'
        return depNodeFn.name()

    def longName(self):
        """
                Objective:
                ----------
                It is useful whenever world space calculations are made.
                
                Returns
                -------
                MFnDagNode.fullPathName()               #_ Complete path name from root to hsNode
                """
        dgNodeFn = self._MFnDagNode()
        if self._cNum > 0:
            return dgNodeFn.fullPathName() + '.' + self._cType + '[' + str(self._cNum) + ']'
        return dgNodeFn.fullPathName()

    def rename(self, newName):
        """Rename the object to given newName. And updates the name of instance.."""
        depFn = om.MFnDependencyNode()
        depFn.setObject(self._MObject())
        if self.isShape():
            if self._cNum > 0:
                rename(self.parent().split('.', 1)[0], newName)
            else:
                rename(self.parent(), newName)
        elif self._cNum > 0:
            rename(self.name().split('.', 1)[0], newName)
        else:
            rename(self.name(), newName)
        frame = inspect.currentframe().f_back
        dictN = dict(list(frame.f_globals.items()) + list(frame.f_locals.items()))
        for (k, var) in list(dictN.items()):
            if isinstance(var, self.__class__):
                if hash(self) == hash(var):
                    if self._cNum > 0:
                        frame.f_globals[k] = hsNode(self.name())
                    else:
                        frame.f_globals[k] = self.asObj()
                    break

        return hsNode(self.name())

    def select(self, *args, **kwargs):
        """
                Objective:
                ----------
                hsNode will be selected with below available flags
                
                Flags:
                ------
                Available flags : 'r', 'relative', 'add', 'af', 'addFirst', 'd', 'deselect', 'tgl', 'toggle'
                
                Returns:
                --------
                Nothing
                """
        if not kwargs:
            kwargs = {'r': 1}
        try:
            (cmds.select)(self.name(), *args, **kwargs)
        except TypeError as msg:
            try:
                if args == ([],):
                    for modeFlag in ('add', 'af', 'addFirst', 'd', 'deselect', 'tgl','toggle'):
                        if kwargs.get(modeFlag, False):
                            return

                    cmds.select(cl=True)
                else:
                    raise TypeError(msg)
            finally:
                msg = None
                del msg

    def extractNum(self, fromEnd=True, skipCount=0):
        """
                Returns: 
                -------
                return [num, numStr]    #_ the extracted number from end of the object name
                
                Usage:
                ------
                obj.vtx[105]  # Returns 105 
                obj.e[206]      # Returns 206 
                """
        numList = re.findall('\\d+', self.shortName())
        if numList:
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                num = int(numStr)
                return [num, numStr]
            else:
                numStr = numList[skipCount]
                num = int(numStr)
                return [num, numStr]

        else:
            return

    def isMesh(self):
        shpNode = self.getShape()
        if shpNode:
            if shpNode.nodeType() == 'mesh':
                return True
            return False
        else:
            if self.nodeType() == 'mesh':
                return True
            return False

    def isSkinMesh(self):
        if not self.isMesh():
            return False
        skinClust = self.listHistory(type='skinCluster')
        if not skinClust:
            return False
        return True

    def old_isShape(self):
        pNode = self.parent()
        if pNode:
            if not self.hasShape():
                if pNode.isTrans():
                    pass
            return False
        pShapes = pNode.listRelatives(shapes=1)
        if pShapes:
            if self.name() in pShapes or self.fullName() in pShapes:
                return True
        else:
            return False

    def isShape(self):
        dgPath = self._MDagPath()
        dgPath.pop(1)
        if self._cNum > 0:
            dgPath.pop()
        dgNodeFn = om.MFnDagNode()
        dgNodeFn.setObject(dgPath)
        parentName = dgNodeFn.partialPathName()
        if cmds.objExists(parentName):
            pNode = hsNode(parentName)
        else:
            pNode = None
        if pNode:
            if not self.hasShape():
                if pNode.isTrans():
                    pass
            return False
        pShapes = pNode.listRelatives(shapes=1)
        if pShapes:
            if self.name() in pShapes or self.fullName() in pShapes:
                return True
        else:
            return False

    def isComponent(self):
        if '.' in self.shortName():
            return True
        return False

    def isParentOf(self, trgtObj, prntImplied=True):
        asTrgt = hsNode(trgtObj)
        if prntImplied:
            if asTrgt.attributeQuery('mPrnt', n=(asTrgt.name()), ex=1):
                if asTrgt.attributeQuery('mPrnt', n=(asTrgt.name()), at=1) == 'message':
                    if asTrgt.isChildOf(self.name()):
                        return True
            nodeDg = self._MFnDagNode()
            mObj = asTrgt._MObject()
            return nodeDg.isParentOf(mObj)

    def isCurv(self):
        if self.getShape():
            if self.getShape().nodeType() == 'nurbsCurve':
                return True
            return False
        else:
            if self.nodeType() == 'nurbsCurve':
                return True
            return False

    def isEdge(self):
        if '.e[' in self.name():
            return True
        return False

    def isVertex(self):
        if '.vtx[' in self.name():
            return True
        return False

    def isFace(self):
        if '.f[' in self.name():
            return True
        return False

    def isJnt(self):
        if cmds.nodeType(self.name()) == 'joint':
            return True
        return False

    def isLoc(self):
        if self.getShape():
            if self.getShape().nodeType() == 'locator':
                return True
            return False
        else:
            if self.nodeType() == 'locator':
                return True
            return False

    def hasAttrLocked(self, attr):
        if self.hasAttr(attr):
            attrType = self.attributeQuery(attr, at=1)
            if attrType == 'double3':
                boolAttr = False
                subAttrs = self.attributeQuery(attr, listChildren=1)
                if subAttrs:
                    for subAttr in subAttrs:
                        if self.getAttr(subAttr, l=1):
                            boolAttr = True
                            break

                return boolAttr
            if self.getAttr(attr, l=1):
                return True
            return False

    def isTrans(self):
        if self.nodeType(True) == 'transform':
            return True
        return False

    def isNodeType(self, objType):
        if self.getShape():
            if self.getShape().nodeType() == objType:
                return True
            return False
        else:
            if self.nodeType() == objType:
                return True
            return False

    def isLastJnt(self, numFromEnd=0, childImplied=True):
        jnt = self.asObj()
        if cmds.nodeType(jnt.name()) == 'joint':
            pass
        else:
            self._confirmAction('"%s" is Not Joint..' % self.name(), True)
        if numFromEnd == 0:
            chdList = jnt.getChildren()
            if not chdList:
                return True
            if self.selectHI('jnt', topSelect=False):
                jnt.select()
                return False
            jnt.select()
            return True
        if len(self.selectHI('jnt', topSelect=False)) == numFromEnd:
            jnt.select()
            return True
        jnt.select()
        return False

    def isLeftSide(self, offset=0.05, dirAxis='x'):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|shp|^comp|comp'
        posList = self.getPos()
        if posList[0] >= offset:
            return True
        return False

    def isRightSide(self, offset=0.05, dirAxis='x'):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|shp|^comp|comp'
        posList = self.getPos()
        if posList[0] <= -1 * offset:
            return True
        return False

    def isMiddleSide(self, offset=0.05, dirAxis='x'):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|shp|^comp|comp'
        posList = self.getPos()
        if posList[0] <= offset:
            if posList[0] >= -1 * offset:
                return True
            return False

    def startswith(self, *args, **kwargs):
        return (self.__str__().startswith)(*args, **kwargs)

    def listHistory(self, **kwargs):
        """
                Usage:
                ------
                hsN.listHistory()               
                #_ type & type='constraint' are supported
                hsN.listHistory(type='pointConstraint')                 
                hsN.listHistory(type='skinCluster')
                
                Returns:
                --------
                return histNodes
                """
        self.select()
        histNodes = []
        try:
            histNodes = (cmds.listHistory)(**kwargs)
        except:
            if kwargs:
                if 'type' in list(kwargs.keys()):
                    nodeList = listHistory()
                    if nodeList:
                        for node in nodeList:
                            if kwargs['type'] == 'constraint':
                                try:
                                    node = hsNode(node)
                                except:
                                    continue

                                if not not (nodeType(node) == 'pointConstraint' or nodeType(node) == 'orientConstraint' or nodeType(node) == 'parentConstraint' or nodeType(node) == 'scaleConstraint' or nodeType(node) == 'aimConstraint' or nodeType(node) == 'tangentConstraint' or nodeType(node) == 'normalConstraint'):
                                    if not not nodeType(node) == 'geometryConstraint':
                                        if nodeType(node) == 'poleVectorConstraint':
                                            if self.isParentOf(node):
                                                histNodes.append(node)
                                        else:
                                            if 'Constraint' in kwargs['type'] and nodeType(node) == kwargs['type']:
                                                try:
                                                    node = hsNode(node)
                                                except:
                                                    continue

                                                if self.isParentOf(node):
                                                    histNodes.append(node)
                                            else:
                                                if nodeType(node) == kwargs['type']:
                                                    histNodes.append(node)

            else:
                return

        if histNodes:
            return histNodes
        return

    def getPosLoc(self, makeChild=True, snapRot=False, hideLoc=True, locName=None, oppAxis=None, grpLevel=0, offsetDist=None, getSpot=False):
        """
                Purpose:
                --------
                Returns number of locaters as per the given list of locNames at the same position of hsNode
                
                Args:
                -----
                makeChild : True | False (Makes newly created locator as child to hsN)
                snapRot : True | False (Snaps rotation of newly created locator to hsN)
                hideLoc : True | False (Hides locator on its creation)
                locName : It can be a single name (string) | List of names (strings)
                oppAxis : None | 'x' or 'X' | 'y' or 'Y' | 'z' or 'Z'
                          [Places the locator on opposite side of the axis (With snapRot as it is given)]
                grpLevel : 0 | 1-10 [posLoc will be grouped with same pivot]
                offsetDist =['x', 1] | [['x', '-y', 'z'], 1] #_ A list contains direction and distance
                
                Returns:
                --------
                return locList          #_ hsNodes              
                """
        if locName:
            locNames = [locName] if type(locName) != list else locName
            locList = []
            for locName in locNames:
                nextUniqName = None
                if objExists(locName):
                    nextUniqName = hsNode(locName).nextUniqueName()
                else:
                    if getSpot:
                        locName_ = hsNode(curve(n=locName, p=[(-1.0, 0.0, 0.0),(-0.70711, 0.0, -0.70711),(0.0, 0.0, -1.0),(0.0, -0.70711, -0.70711),(0.0, -1.0, 0.0),(0.0, -0.70711, 0.70711),(0.0, 0.0, 1.0),(0.0, 0.70711, 0.70711),(0.0, 1.0, 0.0),(0.0, 0.70711, -0.70711),(0.0, 0.0, -1.0),(0.0, 0.0, 0.0),(0.0, -1.0, 0.0),(-0.70711, -0.70711, 0.0),(-1.0, 0.0, 0.0),(1.0, 0.0, 0.0),(0.0, 0.0, 0.0),(0.0, 0.0, 1.0),(0.0, 0.0, -1.0),(0.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, -1.0, 0.0),(0.70711, -0.70711, 0.0),(1.0, 0.0, 0.0),(0.70711, 0.70711, 0.0),(0.0, 1.0, 0.0),(-0.70711, 0.70711, 0.0),(-1.0, 0.0, 0.0),(-0.70711, 0.0, 0.70711),(0.0, 0.0, 1.0),(0.70711, 0.0, 0.70711),(1.0, 0.0, 0.0),(0.70711, 0.0, -0.70711),(0.0, 0.0, -1.0)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33], d=1))
                        locName_.applyCtrlColor(17)
                    else:
                        cmds.spaceLocator(n=locName)
                        locName_ = hsN._selected()[0]
                    if nextUniqName:
                        locName_ = locName_.rename(nextUniqName)
                    locList.append(locName_)

        else:
            if getSpot:
                locName_ = hsNode(curve(n=(self.shortName() + '_PosLoc'), p=[(-1.0, 0.0, 0.0),(-0.70711, 0.0, -0.70711),(0.0, 0.0, -1.0),(0.0, -0.70711, -0.70711),(0.0, -1.0, 0.0),(0.0, -0.70711, 0.70711),(0.0, 0.0, 1.0),(0.0, 0.70711, 0.70711),(0.0, 1.0, 0.0),(0.0, 0.70711, -0.70711),(0.0, 0.0, -1.0),(0.0, 0.0, 0.0),(0.0, -1.0, 0.0),(-0.70711, -0.70711, 0.0),(-1.0, 0.0, 0.0),(1.0, 0.0, 0.0),(0.0, 0.0, 0.0),(0.0, 0.0, 1.0),(0.0, 0.0, -1.0),(0.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, -1.0, 0.0),(0.70711, -0.70711, 0.0),(1.0, 0.0, 0.0),(0.70711, 0.70711, 0.0),(0.0, 1.0, 0.0),(-0.70711, 0.70711, 0.0),(-1.0, 0.0, 0.0),(-0.70711, 0.0, 0.70711),(0.0, 0.0, 1.0),(0.70711, 0.0, 0.70711),(1.0, 0.0, 0.0),(0.70711, 0.0, -0.70711),(0.0, 0.0, -1.0)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33], d=1))
                locName_.applyCtrlColor(17)
            else:
                cmds.spaceLocator(n=(self.shortName() + '_PosLoc'))
            locList = hsN._selected()
        for asLoc in locList:
            asLoc.snapPosTo(self.name())
            if snapRot:
                asLoc.snapRotTo(self.name())
            if hideLoc:
                asLoc.hide()
            if makeChild:
                if not self.isComponent():
                    cmds.parent(asLoc, self.name())

        if oppAxis:
            transAxis = 't' + oppAxis.lower()
            if oppAxis.lower() == 'x':
                r1Axis = 'ry'
                r2Axis = 'rz'
                r3Axis = 'rx'
            elif oppAxis.lower() == 'y':
                r1Axis = 'rz'
                r2Axis = 'rx'
                r3Axis = 'ry'
            elif oppAxis.lower() == 'z':
                r1Axis = 'rx'
                r2Axis = 'ry'
                r3Axis = 'rz'
            for pLoc in locList:
                pLoc.setAttr(transAxis, pLoc.getAttr(transAxis) * -1)
                pLoc.setAttr(r1Axis, pLoc.getAttr(r1Axis) * -1 + 180)
                pLoc.setAttr(r2Axis, pLoc.getAttr(r2Axis) * -1)
                pLoc.setAttr(r3Axis, pLoc.getAttr(r3Axis) * -1)
                if grpLevel:
                    pLoc.grpIt(grpLevel, True, None, True)

        if offsetDist:
            axisDirList = [offsetDist[0]] if type(offsetDist[0]) != list else offsetDist[0]
            moveVal = offsetDist[1]
            for axisDir in axisDirList:
                if axisDir == 'x':
                    x = moveVal
                    y = 0
                    z = 0
                else:
                    if axisDir == '-x':
                        x = -moveVal
                        y = 0
                        z = 0
                    elif axisDir == 'y':
                        x = 0
                        y = moveVal
                        z = 0
                    elif axisDir == '-y':
                        x = 0
                        y = -moveVal
                        z = 0
                    elif axisDir == 'z':
                        x = 0
                        y = 0
                        z = moveVal
                    elif axisDir == '-z':
                        x = 0
                        y = 0
                        z = -moveVal
                    select(locList, r=1)
                    cmds.move(x, y, z, r=1)

        return locList

    def getPosJnt(self, makeChild=True, jntNames=None, snapOrient=False):
        """
                Args:
                -----
                locName : it can be a single name (string) or list of names (strings)
                
                Returns:
                --------
                Returns number of locaters as per the given list of locNames at the same position of hsNode
                """
        if jntNames:
            jntNames = [jntNames] if type(jntNames) != list else jntNames
            jntList = []
            for jntName in jntNames:
                cmds.select(cl=1)
                jntList.append(hsNode(joint(p=(0, 0, 0), n=jntName)))

        else:
            jntList = [hsNode(joint(p=(0, 0, 0), n=(self.shortName() + '_01_Skn_Jnt')))]
        for asJnt in jntList:
            asJnt.snapPosTo(self.name())
            if snapOrient:
                asJnt.jntOrientTo(self.name())
            if makeChild:
                if not asJnt.isChildOf(self.name()):
                    cmds.parent(asJnt, self.name())
                else:
                    cmds.warning('"{0}" is already child of "{1}"\nSkipping !!'.format(asJnt.Name(), self.name()))

        if len(jntList) == 1:
            return jntList[0]
        else:
            return jntList

    def pickWalkUp(self, pickCount=1, nodeType=None, selectAll=True, includeSrc=False, parentImplied=False):
        """
                if pickList:            
                        if len(pickList) == 1:
                                return pickList[0]              #_ hsNode
                        else:
                                return pickList                 #_ hsNode(s)
                else:
                        return None
                """
        if pickCount == 1:
            if nodeType == 'joint':
                if parentImplied:
                    if self.attributeQuery('mPrnt', n=(self.name()), ex=1):
                        if self.attributeQuery('mPrnt', n=(self.name()), at=1) == 'message':
                            return self.parent()
        else:
            self.select()
            pickList = []
            skipList = []
            for num in range(pickCount):

                def getPickList(pickList, skipList, nodeType):
                    currentJnt = self._selected()[0]
                    if currentJnt.attributeQuery('mPrnt', n=(currentJnt.name()), ex=1):
                        if currentJnt.attributeQuery('mPrnt', n=(currentJnt.name()), at=1) == 'message':
                            prntJnt = currentJnt.parent()
                            prntJnt.select()
                        else:
                            cmds.pickWalk(d='up')
                    else:
                        cmds.pickWalk(d='up')
                    currentItem = self._selected()[0]
                    if currentItem != self.asObj():
                        if nodeType:
                            if currentItem.nodeType() != nodeType:
                                if skipList:
                                    if currentItem != skipList[(-1)]:
                                        skipList.append(currentItem)
                                        getPickList(pickList, skipList, nodeType)
                                else:
                                    skipList.append(currentItem)
                                    getPickList(pickList, skipList, nodeType)
                        elif pickList:
                            if currentItem != pickList[(-1)]:
                                if currentItem not in skipList:
                                    pickList.append(currentItem)
                                else:
                                    pickList.append(currentItem)
                            elif pickList:
                                if currentItem != pickList[(-1)] and currentItem not in skipList:
                                    pickList.append(currentItem)
                        else:
                            pickList.append(currentItem)
                    return [pickList, skipList]

                pickList, skipList = getPickList(pickList, skipList, nodeType)

            if pickList:
                if includeSrc:
                    pickList.insert(0, self.asObj())
                if selectAll:
                    cmds.select(pickList, r=1)
                if len(pickList) == 1:
                    return pickList[0]
                return pickList
            else:
                cmds.select(cl=1)
                return

    def pickWalkDown(self, pickCount=1, nodeType=None, selectAll=True, includeSrc=False, childImplied=True):
        """
                if pickList:            
                        if len(pickList) == 1:
                                return pickList[0]              #_ hsNode
                        else:
                                return pickList                 #_ hsNode(s)
                else:
                        return None
                """
        if pickCount == 1:
            if nodeType == 'joint':
                if childImplied:
                    if self.attributeQuery('mChd', n=(self.name()), ex=1):
                        if self.attributeQuery('mChd', n=(self.name()), at=1) == 'message':
                            return self.child()
        else:
            self.select(r=1)
            pickList = []
            skipList = []
            for num in range(pickCount):

                def getPickList(pickList, skipList, nodeType):
                    currentJnt = self._selected()[0]
                    if currentJnt.attributeQuery('mChd', n=(currentJnt.name()), ex=1):
                        if currentJnt.attributeQuery('mChd', n=(currentJnt.name()), at=1) == 'message':
                            chdJnt = currentJnt.child()
                            chdJnt.select()
                        else:
                            cmds.pickWalk(d='down')
                    else:
                        cmds.pickWalk(d='down')
                    currentItem = self._selected()[0]
                    if currentItem != self.asObj():
                        if nodeType:
                            if currentItem.nodeType() != nodeType:
                                if skipList:
                                    if currentItem != skipList[(-1)]:
                                        skipList.append(currentItem)
                                        getPickList(pickList, skipList, nodeType)
                                else:
                                    skipList.append(currentItem)
                                    getPickList(pickList, skipList, nodeType)
                        elif pickList:
                            if currentItem != pickList[(-1)]:
                                if currentItem not in skipList:
                                    pickList.append(currentItem)
                                else:
                                    pickList.append(currentItem)
                            elif pickList:
                                if currentItem != pickList[(-1)] and currentItem not in skipList:
                                    pickList.append(currentItem)
                        else:
                            pickList.append(currentItem)
                    return [pickList, skipList]

                pickList, skipList = getPickList(pickList, skipList, nodeType)

            if pickList:
                if includeSrc:
                    pickList.insert(0, self.asObj())
                if selectAll:
                    cmds.select(pickList, r=1)
                if len(pickList) == 1:
                    return pickList[0]
                return pickList
            else:
                cmds.select(cl=1)
                return

    def pickWalkLeft(self, pickCount=1, nodeType=None, selectAll=True, includeSrc=False):
        """
                if pickList:            
                        if len(pickList) == 1:
                                return pickList[0]              #_ hsNode
                        else:
                                return pickList                 #_ hsNode(s)
                else:
                        return None
                """
        self.select(r=1)
        pickList = []
        skipList = []
        for num in range(pickCount):

            def getPickList(pickList, skipList, nodeType):
                cmds.pickWalk(d='left')
                currentItem = self._selected()[0]
                if currentItem != self.asObj():
                    if nodeType:
                        if currentItem.nodeType() != nodeType:
                            if skipList:
                                if currentItem != skipList[(-1)]:
                                    skipList.append(currentItem)
                                    getPickList(pickList, skipList, nodeType)
                            else:
                                skipList.append(currentItem)
                                getPickList(pickList, skipList, nodeType)
                    elif pickList:
                        if currentItem != pickList[(-1)]:
                            if currentItem not in skipList:
                                pickList.append(currentItem)
                            else:
                                pickList.append(currentItem)
                        elif pickList:
                            if currentItem != pickList[(-1)] and currentItem not in skipList:
                                pickList.append(currentItem)
                    else:
                        pickList.append(currentItem)
                return [
                 pickList, skipList]

            pickList, skipList = getPickList(pickList, skipList, nodeType)

        if pickList:
            if includeSrc:
                pickList.insert(0, self.asObj())
            if selectAll:
                cmds.select(pickList, r=1)
            if len(pickList) == 1:
                return pickList[0]
            return pickList
        else:
            cmds.select(cl=1)
            return

    def pickWalkRight(self, pickCount=1, nodeType=None, selectAll=True, includeSrc=False):
        """
                if pickList:            
                        if len(pickList) == 1:
                                return pickList[0]              #_ hsNode
                        else:
                                return pickList                 #_ hsNode(s)
                else:
                        return None
                """
        self.select(r=1)
        pickList = []
        skipList = []
        for num in range(pickCount):

            def getPickList(pickList, skipList, nodeType):
                cmds.pickWalk(d='right')
                currentItem = self._selected()[0]
                if currentItem != self.asObj():
                    if nodeType:
                        if currentItem.nodeType() != nodeType:
                            if skipList:
                                if currentItem != skipList[(-1)]:
                                    skipList.append(currentItem)
                                    getPickList(pickList, skipList, nodeType)
                            else:
                                skipList.append(currentItem)
                                getPickList(pickList, skipList, nodeType)
                    elif pickList:
                        if currentItem != pickList[(-1)]:
                            if currentItem not in skipList:
                                pickList.append(currentItem)
                            else:
                                pickList.append(currentItem)
                        elif pickList:
                            if currentItem != pickList[(-1)] and currentItem not in skipList:
                                pickList.append(currentItem)
                    else:
                        pickList.append(currentItem)
                return [pickList, skipList]

            pickList, skipList = getPickList(pickList, skipList, nodeType)

        if pickList:
            if includeSrc:
                pickList.append(self.asObj())
            if selectAll:
                cmds.select(pickList, r=1)
            if len(pickList) == 1:
                return pickList[0]
            return pickList
        else:
            cmds.select(cl=1)
            return

    def getPos(self, shapePos=False):
        """
                Objective:
                ----------
                To return the world position of an object, meshVtx, meshEdg or curveCV

                Returns: List of 3 values
                --------
                [x,y,z]  #_ for types: 'obj' or 'cv' or 'vtx' or 'edg' or 'f'           
                """
        if '.' not in self.name():
            if not shapePos:
                transFn = om.MFnTransform()
                pathDg = self._MDagPath()
                transFn.setObject(pathDg)
                point = om.MPoint()
                point = transFn.rotatePivot(MSpace.kWorld)
                objPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                return objPos
            if self.isNodeType('nurbsCurve'):
                (cvList, numCVs) = self.getVtxList()
                cmds.select(cvList, r=1)
                cmds.setToolTo('Move')
                cPos = cmds.manipMoveContext('Move', q=1, p=1)
                return cPos
        elif self._cNum > 0:
            if '.vtx[' in self.name():
                mDgPath = self._MDagPath()
                mItVtx = om.MItMeshVertex(mDgPath)
                vtxPos = []
                while not mItVtx.isDone():
                    if mItVtx.index() == self._cNum:
                        point = om.MPoint()
                        point = mItVtx.position(MSpace.kWorld)
                        vtxPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                        break
                    else:
                        next(mItVtx)

                return vtxPos
            if self._cNum >= 0:
                if re.match('^.*\\.cv\\[(?P<uVal>\\d+)\\]$', self.name()):
                    mDgPath = self._MDagPath()
                    mItCV = om.MItCurveCV(mDgPath)
                    cvPos = []
                    while not mItCV.isDone():
                        if mItCV.index() == self._cNum:
                            point = om.MPoint()
                            point = mItCV.position(MSpace.kWorld)
                            cvPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                            break
                        else:
                            next(mItCV)

                    return cvPos
                if self._uvNums:
                    mDgPath = self._MDagPath()
                    mItCV = om.MItSurfaceCV(mDgPath)
                    cvPos = []
                    while not mItCV.isDone():
                        while not mItCV.isRowDone():
                            utilU = MScriptUtil()
                            utilU.createFromInt(0)
                            uInt = utilU.asIntPtr()
                            utilV = MScriptUtil()
                            utilV.createFromInt(0)
                            vInt = utilV.asIntPtr()
                            mItCV.getIndex(uInt, vInt)
                            uvList = [MScriptUtil.getInt(uInt), MScriptUtil.getInt(vInt)]
                            if uvList == self._uvNums:
                                break
                            else:
                                next(mItCV)

                        if uvList == self._uvNums:
                            break
                        else:
                            mItCV.nextRow()

                    point = om.MPoint()
                    point = mItCV.position(MSpace.kWorld)
                    cvPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                    return cvPos
                if self._cNum > 0:
                    if '.f[' in self.name():
                        mItPoly = self._MItMeshPolygon()
                        polyPos = []
                        while not mItPoly.isDone():
                            if mItPoly.index() == self._cNum:
                                point = om.MPoint()
                                point = mItPoly.center(MSpace.kWorld)
                                polyPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                                break
                            else:
                                next(mItPoly)

                        return polyPos
                if self._cNum > 0:
                    if '.e[' in self.name():
                        mDgPath = self._MDagPath()
                        mItEdg = om.MItMeshEdge(mDgPath)
                        ePos = []
                        while not mItEdg.isDone():
                            if mItEdg.index() == self._cNum:
                                point = om.MPoint()
                                point = mItEdg.center(MSpace.kWorld)
                                ePos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                                break
                            else:
                                next(mItEdg)

                        return ePos

    def setPos(self, posList=[0, 0, 0]):
        self.select(r=1)
        cmds.move((posList[0]), (posList[1]), (posList[2]), rpr=1)

    def nearestObj(self, objListOrIter, nearIndex=0):
        """
                List is faster than iterator by 1 min for 5411 vertices
                """
        distanceDict = {}
        for destObj in objListOrIter:
            dist = self.distanceTo(destObj)[0]
            distanceDict[dist] = destObj

        shortDist = min(distanceDict.keys())
        return hsNode(distanceDict[shortDist])

    def longestObj(self, objList):
        """
                Returns : obj | vtx [hsNode]
                """
        distanceDict = {}
        for destObj in objList:
            dist = self.distanceTo(destObj)[0]
            distanceDict[dist] = destObj

        longDist = max(distanceDict.keys())
        return hsNode(distanceDict[longDist])

    def getDirVect(self, dirObjOrPos):
        if type(dirObjOrPos) != list:
            dirObj = hsNode(dirObjOrPos)
            destPos = dirObj.getPos()
        else:
            destPos = dirObjOrPos
        srcPos = self.getPos()
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        return om.MVector(distX, distY, distZ)

    def getClosestDist_Msh(self, meshObj):
        """
                Returns:
                --------
                return mDist
                """
        ncTypes = 'mesh|curv|jnt|trans|comp'
        nameCPOM = str(createNode('closestPointOnMesh', n='closestPoint'))
        locPos = self.getPos()
        setAttr((nameCPOM + '.inPosition'), (locPos[0]), (locPos[1]), (locPos[2]), type='double3')
        setAttr(nameCPOM + '.isHistoricallyInteresting', 1)
        connectAttr(meshObj + '.worldMatrix[0]', nameCPOM + '.inputMatrix')
        connectAttr(meshObj + '.worldMesh', nameCPOM + '.inMesh')
        endPos = getAttr(nameCPOM + '.position')[0]
        distX = endPos[0] - locPos[0]
        distY = endPos[1] - locPos[1]
        distZ = endPos[2] - locPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        delete(nameCPOM)
        return mDist

    def getClosestPos_Crv(self, curvName, getLoc=True, getNPOC=False):
        """
                Returns
                -------
                if getLoc:
                        if getNPOC:
                                return [destLoc, nameNPOC]
                        else:
                                return [destLoc]                                
                else: #_ Returns closest pos
                        if getNPOC:                     
                                return [closestPos, nameNPOC]
                        else:
                                return [closestPos]                     
                """
        nameNPOC = str(createNode('nearestPointOnCurve', n=('NearestPoint_' + curvName)))
        fromPos = self.getPos()
        setAttr((nameNPOC + '.inPosition'), (fromPos[0]), (fromPos[1]), (fromPos[2]), type='double3')
        setAttr(nameNPOC + '.ihi', 1)
        connectAttr(curvName + '.ws', nameNPOC + '.inputCurve')
        curvPosX = getAttr(nameNPOC + '.positionX')
        curvPosY = getAttr(nameNPOC + '.positionY')
        curvPosZ = getAttr(nameNPOC + '.positionZ')
        closestPos = [curvPosX, curvPosY, curvPosZ]
        if not getNPOC:
            delete(nameNPOC)
        if getLoc:
            destLoc = spaceLocator(p=(0, 0, 0))
            cmds.move(curvPosX, curvPosY, curvPosZ, r=1)
            if getNPOC:
                return [destLoc, nameNPOC]
            return [destLoc]
        else:
            if getNPOC:
                return [closestPos, nameNPOC]
            else:
                return [closestPos]

    def getClosestParam_Crv(self, curvName, getLoc=True):
        asCurv = hsNode(curvName)
        fnCurv = asCurv._MFnNurbsCurve()
        nPos = self.nearestPointOn(curvName, 'crv', 0)
        mPnt = MPoint(nPos[0], nPos[1], nPos[2])
        util = MScriptUtil()
        util.createFromDouble(0.0)
        ptr = util.asDoublePtr()
        fnCurv.getParamAtPoint(mPnt, ptr, MSpace.kWorld)
        return MScriptUtil.getDouble(ptr)

    def getDirPos(self, dirObj, extnRatio, locName='Extn_Loc', giveLoc=True):
        srcObj = self.asObj()
        dirVect = self.getDirVect(dirObj)
        extnPos = [num * (extnRatio + 1) for num in dirVect]
        extnLoc = hsNode(cmds.spaceLocator(n=locName, p=[extnPos[0], extnPos[1], extnPos[2]])[0])
        extnLoc.snapPosTo(srcObj)
        extnLoc.centerPivot()
        extnLoc.unfreezeTrans()
        if giveLoc == True:
            return extnLoc
        extnPos = cmds.xform(extnLoc, q=1, ws=1, t=1)
        delete(extnLoc)
        return extnPos

    def snapPosTo(self, destPosOrObj=[0, 0, 0], snapRot=False, shapePos=False):
        """
                destObjOrPos = strObj | hsNode | objPos[0,0,0]
                if snapRot : snaps hsNode's rotation to destObj
                if shapePos : snaps hsNode's position to destObj's shapePos
                """
        destObj = None
        if type(destPosOrObj) != list:
            destObj = hsNode(destPosOrObj)
            destPos = destObj.getPos(shapePos)
        else:
            destPos = destPosOrObj
        self.select(r=1)
        cmds.move((destPos[0]), (destPos[1]), (destPos[2]), rpr=1)
        if snapRot:
            if destObj:
                self.snapRotTo(destObj)

    def nearestPointOn(self, curvName, trgtType='crv', getLoc=True, attachToPath=False):
        asCurv = hsNode(curvName)
        nameNPOC = str(cmds.createNode('nearestPointOnCurve', n=(asCurv.name() + '_NPOC')))
        srcPos = self.getPos()
        cmds.setAttr((nameNPOC + '.inPosition'), (srcPos[0]), (srcPos[1]), (srcPos[2]), type='double3')
        cmds.setAttr(nameNPOC + '.ihi', 1)
        cmds.connectAttr(curvName + '.ws', nameNPOC + '.inputCurve')
        curvPosX = cmds.getAttr(nameNPOC + '.positionX')
        curvPosY = cmds.getAttr(nameNPOC + '.positionY')
        curvPosZ = cmds.getAttr(nameNPOC + '.positionZ')
        delete(nameNPOC)
        if getLoc:
            destLoc = cmds.spaceLocator(p=(0, 0, 0))
            cmds.move(curvPosX, curvPosY, curvPosZ, r=1)
            if attachToPath:
                mPos = om.MPoint(curvPosX, curvPosY, curvPosZ)
                sUtil = om.MScriptUtil()
                val = sUtil.asDoublePtr()
                curvFn = asCurv._MFnNurbsCurve()
                curvFn.getParamAtPoint(mPos, val, MSpace.kWorld)
                sUtil = om.MScriptUtil(val)
                uVal = sUtil.asDouble()
                pAnim = cmds.pathAnimation(destLoc, asCurv, upAxis='y', fractionMode=True, endTimeU=playbackOptions(query=1, maxTime=1), startTimeU=playbackOptions(minTime=1, query=1), worldUpType='vector', inverseUp=False, inverseFront=False, follow=True, bank=False, followAxis='x', worldUpVector=(0,1,0))
                cmds.cutKey(pAnim + '.uValue')
                cmds.setAttr(pAnim + '.uValue', uVal)
            return destLoc
        return [curvPosX, curvPosY, curvPosZ]

    def distanceTo(self, destObjOrPos, getNode=False):
        """
                Objective:
                ----------
                To measure the distance between (two objects) or (two positions) or (one obj and one position or veceversa)
                                
                Returns:
                --------
                [mDist, distNode, locList, distShape, distAttr] #_ If getNode is True
                [mDist]                                                                                 #_ If getNode is False  
                """
        srcObj = self.name()
        srcPos = self.getPos()
        destNode = None
        if type(destObjOrPos) != list:
            destNode = hsNode(destObjOrPos)
            destPos = destNode.getPos()
        else:
            destPos = destObjOrPos
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        if getNode:
            distShape = hsNode(distanceDimension(sp=(-100, -100, -100), ep=(100, 100,
                                                                            100)))
            distNode = hsNode(distShape.parent())
            distNode = distNode.rename(destNode.shortName() + '_Dist')
            distAttr = distShape.name() + '.distance'
            srcLoc = hsNode(cmds.listConnections(distShape.name() + '.startPoint')[0])
            destLoc = hsNode(cmds.listConnections(distShape.name() + '.endPoint')[0])
            srcLoc.snapPosTo(srcObj)
            destLoc.snapPosTo(destNode.name())
            if objExists(srcObj):
                if type(srcObj) != list:
                    srcLoc.rename(srcObj + '_SrcLoc')
                    srcLoc.parentTo(self.asObj())
                if objExists(destNode.name()):
                    if type(destNode.name()) != list:
                        destLoc.rename(destNode.shortName() + '_EndLoc')
                        destLoc.parentTo(destNode.asObj())
                        distNode.parentTo(destNode.asObj())
                    locList = [srcLoc.name(), destLoc.name()]
                    return [mDist, locList, distNode, distShape.name(), distAttr]
            return [mDist]

    def delete(self, **kwargs):
        (cmds.delete)((self.name()), **kwargs)

    def deleteNode(self):
        cmds.delete(self._MDagPath().fullPathName())

    def deleteHistory(self):
        self.select(r=1)
        mel.eval('DeleteHistory')
        self.select(cl=1)

    def deleteKey(self, attrList):
        attrList = [attrList] if not isinstance(attrList, list) else attrList
        for attr in attrList:
            fullAttrName = self.name() + '.' + attr
            cutKey(fullAttrName)
        return True

    def deselect(self):
        self.select(d=1)

    def getNearestVtx_OnMesh(self, trgtMesh, skipDir=None, excludeList=None):
        hsN = hsNode(trgtMesh)
        vIt = MItMeshVertex(hsN._MDagPath())
        srcPos = self.getPos()

        for _ in range(vIt.isDone()):
            pnt = vIt.position(MSpace.kWorld)
            nDist = self.distanceTo((pnt.x, pnt.y, pnt.z))[0]
            if vIt.index() == 0:
                break
            next(vIt)
        for _ in range(vIt.isDone()):
            if excludeList and vIt.index() in excludeList:
                next(vIt)
                continue
            pnt = vIt.position(MSpace.kWorld)
            if skipDir:
                if (skipDir == "+x" and pnt.x > 0.0) or \
                   (skipDir == "-x" and pnt.x < 0.0) or \
                   (skipDir == "+y" and pnt.y > 0.0) or \
                   (skipDir == "-y" and pnt.y < 0.0) or \
                   (skipDir == "+z" and pnt.z > 0.0) or \
                   (skipDir == "-z" and pnt.z < 0.0):
                    next(vIt)
                    continue

            dist = self.distanceTo((pnt.x, pnt.y, pnt.z))[0]

            if dist < nDist:
                nDist = dist
                nVtx = str(trgtMesh) + ".vtx[" + str(vIt.index()) + "]"
                nNum = vIt.index()

            next(vIt)

        cmds.select(nVtx, r=1)
        return [nVtx, nNum]
    def getNearestVtx_OnMesh(self, trgtMesh, skipDir=None, excludeList=None):
        hsN = hsNode(trgtMesh)
        vIt = MItMeshVertex(hsN._MDagPath())
        srcPos = self.getPos()
        
        for _ in range(vIt.isDone()):
            pnt = vIt.position(MSpace.kWorld)
            nDist = self.distanceTo((pnt.x, pnt.y, pnt.z))[0]
            
            if vIt.index() == 0:
                break
            
            next(vIt)
        
        for _ in range(vIt.isDone()):
            if excludeList and vIt.index() in excludeList:
                next(vIt)
                continue
            
            pnt = vIt.position(MSpace.kWorld)
            
            if skipDir:
                if (skipDir == "+x" and pnt.x > 0.0) or \
                   (skipDir == "-x" and pnt.x < 0.0) or \
                   (skipDir == "+y" and pnt.y > 0.0) or \
                   (skipDir == "-y" and pnt.y < 0.0) or \
                   (skipDir == "+z" and pnt.z > 0.0) or \
                   (skipDir == "-z" and pnt.z < 0.0):
                    next(vIt)
                    continue
            
            dist = self.distanceTo((pnt.x, pnt.y, pnt.z))[0]
            
            if dist < nDist:
                nDist = dist
                nVtx = str(trgtMesh) + ".vtx[" + str(vIt.index()) + "]"
                nNum = vIt.index()
            next(vIt)
        
        cmds.select(nVtx, r=1)
        return [nVtx, nNum]

    def _appendTo(self, listVar):
        """
                appends hsNode to any Python List Variable
                """
        if type(listVar) != list:
            self._error('listVar should be of type "list[]"')
        try:
            listVar.append(self.asObj())
        except:
            listVar.append(self.name())

    def applyCtrlColor(self, colorNum=None):
        """
                if colorNum is given:
                        colorNum =6             #_ is for Blue color
                        colorNum =13            #_ is for Red color
                        colorNum =17            #_ is for Yellow color
                else:
                        'L' Prefixed Ctrls                              : Blue Color
                        'R' Prefixed Ctrls                              : Red Color
                        Ctrls Other than ['L' and 'R']  : Yellow Color          
                """
        ncTypes = 'curv|^comp'
        self.setAttr('overrideEnabled', 1)
        if not colorNum:
            if self.__str__().startswith('L'):
                self.setAttr('overrideColor', 6)
            elif self.__str__().startswith('R'):
                self.setAttr('overrideColor', 13)
            else:
                self.setAttr('overrideColor', 17)
        else:
            self.setAttr('overrideColor', colorNum)

    def _MFnMesh(self):
        """
                Returns the Instance of Maya API node : MFnMesh
                """
        ncTypes = 'mesh'
        return om.MFnMesh(self._MDagPath())

    def _MFnMesh2(self):
        """
                Returns the Instance of Maya API node : MFnMesh
                """
        ncTypes = 'mesh'
        return om2.MFnMesh(self._MDagPath2())

    def _MFnNurbsCurve(self):
        """
                Returns the Instance of Maya API node : MFnNurbsCurve
                """
        ncTypes = 'curv'
        curvFn = om.MFnNurbsCurve()
        curvFn.setObject(self._MDagPath())
        return curvFn

    def _MItMeshPolygon(self):
        """
                Returns the Instance of Maya API node : MItMeshPolygon
                """
        ncTypes = 'mesh'
        dgPath = self._MDagPath()
        mItPoly = om.MItMeshPolygon(dgPath)
        return mItPoly

    def _MItMeshVertex(self):
        """
                Returns the Instance of Maya API node : MItMeshVertex
                """
        ncTypes = 'mesh'
        dgPath = self._MDagPath()
        mItVtx = om.MItMeshVertex(dgPath)
        return mItVtx

    def reorderDeformers(self, deformTypes=None):
        """
                deformTypes =['sculpt', 'skinCluster', 'cMuscleRelative', 'nonLinear', 'cluster', 'blendShape', 'ffd', 'wrap', 'tweak']                 
                """
        ncTypes = 'mesh|curv'
        if not deformTypes:
            deformTypes = ['sculpt', 'skinCluster', 'cMuscleRelative', 'nonLinear', 'cluster', 'blendShape', 'ffd', 'wrap', 'tweak']
        deformList = []
        for deformType in deformTypes:
            deforms = self.listHistory(type=deformType)
            if deforms:
                deformList.extend(deforms)

        if deformList:
            if len(deformList) > 1:
                for num in range(0, len(deformList) - 1):
                    for deformNode in deformList[num + 1]:
                        try:
                            cmds.reorderDeformers(deformList[num][0], deformNode, self.name())
                        except:
                            pass

            if len(deformList[0]) > 1:
                for deformNode in deformList[0][1:]:
                    try:
                        cmds.reorderDeformers(str(deformList[0][0]), str(deformNode), self.name())
                    except:
                        pass

        print(deformTypes)

    def extendToShape(self):
        """doc"""
        ncTypes = 'mesh|curv'
        try:
            self.obj.extendToShape()
            shapeName = self.name()
            return hsNode(shapeName)
        except:
            return

    def extendToParent(self, numParent=1):
        """doc"""
        ncTypes = 'mesh|curv|jnt'
        try:
            if self.parent(numParent):
                self.obj.pop(numParent)
                prntName = self.name()
                return hsNode(prntName)
            return
        except:
            return

    def extendToChild(self, numChild=1):
        """doc"""
        ncTypes = 'mesh|curv|jnt'
        try:
            if self.child(numChild):
                return hsNode(self.child(numChild))
            return
        except:
            return

    def getSibIndex(self, prntImplied=True):
        """doc"""
        ncTypes = '^comp'
        if prntImplied:
            if self.attributeQuery('mPrnt', n=(self.name()), ex=1):
                if self.attributeQuery('mPrnt', n=(self.name()), at=1) == 'message':
                    if self.parent(prntImplied=1) == self.parent(prntImplied=0):
                        return self.getSibIndex(0)
                    return 0
                sibIndex = 0
                myParent = self.parent(prntImplied=prntImplied)
                if myParent:
                    sibParent = myParent
                    chdCount = sibParent.numChildren()
                    for num in range(chdCount):
                        if sibParent.child(num, 0) == self.asObj():
                            sibIndex = num
                            break

                    return sibIndex
            return

    def getSkinCluster(self, additionalCheck=1):
        ncTypes = 'mesh'
        conNode = self.connectionInfo('inMesh', sfd=1)
        if conNode:
            skinClust = conNode.split('.')[0]
            if cmds.nodeType(skinClust) == 'skinCluster':
                return skinClust
        skinClust = self.listHistory(type='skinCluster')
        if not skinClust:
            return
        if additionalCheck:
            if self.isMesh():
                skinClust = mel.eval('findRelatedSkinCluster ' + self.name())
                if skinClust:
                    return skinClust
                inMeshObj = self.shape().listConnections('inMesh')
                if inMeshObj[0].nodeType() != 'skinCluster':
                    conNodeAttr = self.shape().connectionInfo('instObjGroups[0].objectGroups[0].objectGrpColor', sfd=1)
                    if conNodeAttr:
                        skinClustList = cmds.listConnections((conNodeAttr.split('.')[0]), type='skinCluster')
                        if skinClustList:
                            skinClust = skinClustList
                            if skinClust:
                                return skinClust[0]
            if skinClust:
                return skinClust[0]
        return

    def getSkinJnts(self):
        """                
                return [infList, len(infList)]
                """
        ncTypes = 'mesh | curv'
        if not self.isMesh():
            if not self.isCurv():
                return
            skinClust = self.getSkinCluster()
            if not skinClust:
                return
            infList = cmds.skinCluster(skinClust, q=1, inf=1)
            infList = list(map(hsNode, infList))
            return [infList, len(infList)]

    def setSibIndex(self, indexNum=0, prntImplied=True):
        """doc"""
        ncTypes = '^comp'
        if prntImplied:
            if self.attributeQuery('mPrnt', n=(self.name()), ex=1):
                if self.attributeQuery('mPrnt', n=(self.name()), at=1) == 'message':
                    if self.parent(prntImplied=1) == self.parent(prntImplied=0):
                        return self.setSibIndex(indexNum, 0)
                    return True
                sibParent = self.parent(prntImplied=prntImplied)
                if sibParent:
                    sibCount = sibParent.numChildren()
                    if indexNum >= sibCount:
                        indexNum = sibCount - 1
                    while 1:
                        if self.getSibIndex(prntImplied) == indexNum:
                            break
                        else:
                            reorder((self.name()), relative=1)

                    return True
            return False

    def shape(self):
        """
                Returns: u'shapeName' of hsNode
                """
        ncTypes = 'mesh|curv|shp'
        return self.getShape()

    def addPrefix(self, prfxName, reName=True):
        """
                Objective:
                ----------
                if reName:  Renames the hsNode with the given prfxName and returns the node
                else:           Retuns name only 'prfxName + hsNode.shortName'
                
                Returns:
                --------
                u'prfxName + hsNode.shortName()'
                """
        ncTypes = 'mesh|curv|^comp'
        if reName:
            self.rename(prfxName + self.shortName())
            return hsNode(self.name())
        else:
            return prfxName + self.shortName()

    def addSuffix(self, sufxName, reName=True):
        """
                Objective:
                ----------
                if reName:  Renames the hsNode with the given sufxName and returns the node
                else:           Retuns name only 'hsNode.shortName + sufxName'
                
                Returns:
                --------
                u'hsNode.shortName() + sufxName'
                """
        ncTypes = 'mesh|curv|^comp'
        if reName:
            self.rename(self.shortName() + sufxName)
            return hsNode(self.name())
        else:
            return self.shortName() + sufxName

    def old_nodeType(self, objType=None):
        """doc"""
        ncTypes = 'mesh|curv|^comp'
        if objType:
            if self.getShape():
                if self.getShape().nodeType() == objType:
                    return True
                else:
                    return False
            else:
                if self.nodeType() == objType:
                    return True
                else:
                    return False
        else:
            if self.hasShape():
                return cmds.nodeType(self.getShape())
            else:
                return cmds.nodeType(self.name())

    def stripNum(self):
        """doc"""
        ncTypes = 'mesh|curv|^comp'
        objName = self.shortName()
        numPartReg = re.compile('([0-9]+)$')
        baseName = numPartReg.split(str(objName))[0]
        return baseName

    def addChild(self, chdNode, chdIndex=None):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        asChd = hsNode(chdNode)
        if asChd.parent() == self.name():
            if chdIndex:
                asChd.setSibIndex(chdIndex)
            warning('"{0:s}" is already child of "{1:s}"'.format(chdNode, self.shortName()))
            return
        asChd.parentTo(self.name())
        if chdIndex:
            return asChd.setSibIndex(chdIndex)

    def addExtnEndJnt(self, jntName=None, atDist=1):
        prntJnt = self.parent()
        extnPos = prntJnt.getDirPos(self.name(), atDist, None, False)
        if not jntName:
            jntName = self.name() + '_Extn'
        exJnt = hsNode(cmds.joint(p=[extnPos[0], extnPos[1], extnPos[2]], n=jntName))
        if self.isJnt():
            exJnt.setAttr('radius', self.getAttr('radius'))
        exJnt.parentTo(self.name())
        return exJnt

    def parent(self, numParent=1, allParents=False, nType=None, prntImplied=True):
        """
        nType = nodeType         #_ It is used when allParents is True

        allParents & numParent:
        -----------------------
        if allParents == True and numParent == 0:
            #_ returns all parents
        elif allParents == True and numParent >= 1:
            #_ returns all parents up to numParent
        elif allParents == False and numParent >= 1:
            #_ returns particular parent at numParent
        """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if prntImplied:
            if not allParents or numParent == 1:
                prntList = []
                if self.attributeQuery('mPrnt', n=self.name(), ex=1):
                    if self.attributeQuery('mPrnt', n=self.name(), at=1) == 'message':
                        prntList = cmds.listConnections(self.name() + '.mPrnt')
                        if prntList:
                            prntStr = prntList[0]
                            if cmds.objExists(prntStr):
                                return hsNode(prntStr)
            elif allParents:
                if numParent > 1:
                    a = 1
                    pCount = True
                    prntList = []
                    while pCount:
                        try:
                            if not prntList:
                                asParent = self.parent()
                            else:
                                asParent = prntList[-1].parent()
                            if asParent:
                                if nType:
                                    if asParent.nodeType() == nType:
                                        prntList.append(asParent)
                                    else:
                                        numParent += 1
                                else:
                                    prntList.append(asParent)
                        except:
                            pCount = False

                        if numParent:
                            if a >= numParent:
                                break
                            a += 1

                    if prntList:
                        return prntList
        if not allParents:
            dgPath = self._MDagPath()
            dgPath.pop(numParent)
            if self._cNum > 0:
                dgPath.pop()
            dgNodeFn = om.MFnDagNode()
            dgNodeFn.setObject(dgPath)
            parentName = dgNodeFn.partialPathName()
            if cmds.objExists(parentName):
                return hsNode(parentName)

        else:
            a = 1
            pCount = True
            prntList = []
            while pCount:
                try:
                    asParent = self.parent(a)
                    if asParent:
                        if nType:
                            if asParent.nodeType() == nType:
                                prntList.append(asParent)
                            else:
                                numParent += 1
                        else:
                            prntList.append(asParent)
                except:
                    pCount = False

                if numParent:
                    if a >= numParent:
                        break
                    a += 1

            if prntList:
                return prntList
        return

    def getParent(self, numParent=1, allParents=False, nType=None, prntImplied=True):
        """
                nType =nodeType         #_ It is used when allParents is True
                
                allParents & numParent:
                -----------------------
                if allParents == True and numParent=0:
                        #_ returns all parents
                elif allParents == True and numParent=> 1:
                        #_ returns all parents upto numParent
                elif allParents == False and numParent=> 1:
                        #_ returns perticular parent at numParent                                               
                """
        return self.parent(numParent=1, allParents=False, nType=None, prntImplied=True)

    def root(self):
        """doc"""
        ncTypes = 'mesh|curv|trans|shp|^comp'
        dgPath = self._MDagPath()
        if self.parent():
            rootName = self.parent(dgPath.length() - 1)
            return hsNode(rootName)
        return hsNode(self.name())

    def attributeQuery(self, *args, **kwargs):
        if 'n' not in kwargs:
            if 'node' not in kwargs:
                kwargs['node'] = self.name()
            return (cmds.attributeQuery)(*args, **kwargs)

    def child(self, indexNum=0, childImplied=True):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|^comp'
        if childImplied:
            chdList = []
            if self.attributeQuery('mChd', n=(self.name()), ex=1):
                if self.attributeQuery('mChd', n=(self.name()), at=1) == 'message':
                    chdList = listConnections(self.name() + '.mChd')
                    if chdList:
                        chdStr = chdList[0]
                        if cmds.objExists(chdStr):
                            return hsNode(chdStr)
                    numChildren = self.numChildren()
                    if indexNum >= numChildren:
                        return
                dgPath = self._MDagPath()
                chdObj = dgPath.child(indexNum)
                if chdObj:
                    dagNodeFn = self._MFnDagNode(chdObj)
                    chdName = dagNodeFn.partialPathName()
                    return hsNode(chdName)
            return

    def getChildren(self, type=None, childImplied=True, **kwargs):
        """
                custom types: 'constrain' or 'constraint'
                        conList =['point', 'orient', 'parent', 'scale', 'aim', 'geometry', 'normal', 'tangent']
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        allChildren = (cmds.listRelatives)(self.name(), c=1, pa=1, **kwargs)
        if childImplied:
            impliedChild = self.child(0, True)
            if impliedChild:
                if not allChildren:
                    allChildren = []
                if impliedChild not in allChildren:
                    allChildren.append(impliedChild)
                asChildren = []
                if allChildren:
                    for child in allChildren:
                        try:
                            asChildren.append(hsNode(child))
                        except:
                            asChildren.append(child)

                else:
                    return
                if not type:
                    return asChildren
            typeChildren = []
            if type == 'constrain' or type == 'constraint':
                conList = [conType + 'Constraint' for conType in ['point', 'orient', 'parent', 'scale', 'aim', 'geometry', 'normal', 'tangent']]
                for child in asChildren:
                    if str(cmds.nodeType(child)) in conList:
                        typeChildren.append(child)

            else:
                for child in asChildren:
                    if cmds.nodeType(child) == type:
                        typeChildren.append(child)

            return typeChildren

    def numChildren(self, type=None, **kwargs):
        """
                Returns:
                --------
                Number of all children or number of typed children
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        allChildren = (cmds.listRelatives)(self.name(), c=1, **kwargs)
        if not allChildren:
            return 0
        if not type:
            if allChildren:
                return len(allChildren)
            return 0
        else:
            typeChildren = []
            for child in allChildren:
                if cmds.nodeType(child) == type:
                    typeChildren.append(child)

            if typeChildren:
                return len(typeChildren)
            return 0

    def parentTo(self, parentNode=None):
        """
                if parentNode:
                        parent(hsNode, parentNode)
                else:
                        parent(hsNode, w=1)  #_ Parents to world if parentNode is not given
                """
        ncTypes = 'mesh|curv|loc|jnt|trans|shp|^comp'
        if parentNode:
            if not self.isChildOf(parentNode):
                cmds.parent(self.name(), str(parentNode))
            else:
                om.MGlobal.displayWarning('{0} is already child of {1}'.format(self.shortName(), parentNode))
        else:
            cmds.parent((self.name()), w=1)

    def unparent(self):
        """
                Purpose:
                --------
                Parents hsNode to world
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if self.parent():
            cmds.parent((self.name()), w=1)
        else:
            self._message('%s is already parented to world' % self.shortName())

    def getInputs(self, nType=None):
        """
                if histNodes:
                        if len(histNodes) == 1:
                                return histNodes[0]
                        elif len(histNodes) > 1:
                                return histNodes
                else:
                        return None
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        if nType:
            histNodes = cmds.listHistory((self.name()), pdo=1, il=1, type=nType)
        else:
            histNodes = cmds.listHistory((self.name()), pdo=1, il=1)
        if histNodes:
            if len(histNodes) == 1:
                return histNodes[0]
            if len(histNodes) > 1:
                return histNodes
        else:
            return

    def getOutputs(self, nType=None):
        """
                if outNodes:                            
                        if len(outNodes) == 1:
                                return outNodes[0]
                        elif len(outNodes) > 1:
                                return outNodes
                else:
                        return None             
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        if nType:
            outNodes = []
            allNodes = cmds.listHistory((self.name()), future=1)
            for outNode in allNodes:
                if nodeType(outNode) == nType:
                    outNodes.append(outNode)

        else:
            outNodes = cmds.listHistory((self.name()), future=1)
        if outNodes:
            if len(outNodes) == 1:
                return outNodes[0]
            if len(outNodes) > 1:
                return outNodes
        else:
            return

    def grpIt(self, grpLevel=1, snapPiv=True, grpSufxList=None, snapRot=False):
        """
                Returns:(hsNodes)
                -----------------
                return grpList [lsitOfGrps(hsNodes)]
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        lockAgain = False
        if self.hasAttrLocked('t'):
            lockedAttrs = self.listLockedAttrs('t')
            if lockedAttrs:
                lockAgain = True
            if grpSufxList:
                grpSufxList = [grpSufxList] if type(grpSufxList) != list else grpSufxList
            objName = self.shortName()
            objGrp = objName
            self.select(r=1)
            if not grpLevel:
                return self.asObj()
            num = 0
            grpList = []

            def groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList):
                if not grpSufxList:
                    grpSufxList = ['_Grp','_GrpTp','_GrpEx','_TopGp','_TopEx','_RootGp','_RootEx']
                else:
                    grpTempList = ['_Grp','_GrpTp','_GrpEx','_TopGp','_TopEx','_RootGp','_RootEx']
                    grpTempSufxList = [grpSufxList] if type(grpSufxList) != list else grpSufxList
                    if len(grpList) > len(grpSufxList):
                        grpSufxList.extend(grpTempList[len(grpSufxList):])
                if num < grpLevel:
                    select(objGrp, r=1)
                    sufxName = '_' + grpSufxList[num] if (not grpSufxList[num].startswith('_')) else (grpSufxList[num])
                    objGrp = hsNode(cmds.group(n=(objName + sufxName)))
                    grpList.append(objGrp)
                    if snapPiv:
                        objGrp.snapPivTo(self.name())
                    if snapRot:
                        if self.parent(2):
                            self.parentTo(self.parent(2))
                        else:
                            self.parentTo()
                        objGrp.snapRotTo(self.name())
                        self.parentTo(objGrp)
                    num = num + 1
                    groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList)
                return grpList

            grpList = groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList)
            if lockAgain:
                self.lockAttrs(lockedAttrs)
            return grpList

    def old_grpIt(self, grpLevel=1, snapPiv=True):
        objName = self.shortName()
        self.select(r=1)
        if not grpLevel:
            return self.asObj()
        if grpLevel == 1 or grpLevel == 2 or grpLevel == 3 or grpLevel == 4:
            objGrp = hsNode(group(n=(objName + '_Grp')))
            if snapPiv:
                objGrp.snapPivTo(objName)
        if grpLevel == 2 or grpLevel == 3 or grpLevel == 4:
            select(objGrp, r=1)
            objGrp = hsNode(group(n=(objName + '_GrpTp')))
            if snapPiv:
                objGrp.snapPivTo(objName)
        if grpLevel == 3 or grpLevel == 4:
            select(objGrp, r=1)
            objGrp = hsNode(group(n=(objName + '_GrpEx')))
            if snapPiv:
                objGrp.snapPivTo(objName)
            if grpLevel == 4:
                select(objGrp, r=1)
                objGrp = hsNode(group(n=(objName + '_Top')))
                if snapPiv:
                    objGrp.snapPivTo(objName)
        return objGrp

    def listConstraints(self, conTypes=None):
        """
                Usage:
                ------
                conTypes =['point', 'orient', 'parent', 'scale', 'aim', 'geometry', 'normal', 'tangent']
                #_ if type is not given, it lists all constraints..             
                        hsN.listConstraints()
                #_ Else it list only requested type             
                        hsN.listConstraints(conType='point')            
                        hsN.listConstraints(conType='parent')
                
                Returns:
                --------
                if conNodes:
                        return conNodes  #_ List of nodes
                else:
                        return None     
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        conNodes = []
        conList = ['point', 'orient', 'parent', 'scale', 'aim', 'geometry', 'normal', 'tangent']
        if conTypes:
            conTypes = [conTypes] if type(conTypes) != list else conTypes
            for conType in conTypes:
                if conType not in conList:
                    self._error("conType should be one of the list['point', 'orient', 'parent', 'scale', 'aim', 'geometry', 'normal', 'poleVector']")
                else:
                    conNode = None
                    exec('conNode = ' + conType + 'Constraint("' + self.name() + '", q=1)')
                if conNode:
                    conNodes.append(hsNode(conNode))

        else:
            for conName in conList:
                conNode = None
                exec('conNode = ' + conName + 'Constraint("' + self.name() + '", q=1)')
                if conNode:
                    conNodes.append(hsNode(conNode))

        if conNodes:
            return conNodes
        else:
            return

    def listRelatives(self, *args, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        if kwargs:
            if 'fullPath' not in kwargs or 'f' not in kwargs:
                kwargs['fullPath'] = 1
        else:
            kwargs['fullPath'] = 1
        relativeList = (cmds.listRelatives)(self.name(), *args, **kwargs)
        if relativeList:
            return [hsNode(obj) for obj in relativeList]
        else:
            return

    def length(self, nameLength=False):
        if nameLength:
            return len(self.shortName())
        else:
            return self._MDagPath().length()

    def listAttr(self, shortForm=True, **kwargs):
        attrList = (cmds.listAttr)((self.name()), **kwargs)
        if attrList:
            attrList = [str(attr) for attr in attrList]
            if not shortForm:
                return attrList
            attrList = [attributeName((self.name() + '.' + attr), s=1) for attr in attrList]
            return [str(attr) for attr in attrList]
        else:
            return

    def lockAttrs(self, attrList=None, keyable=False):
        """
                Args:
                -----
                attrList = 't' | 'tx' | 'v' | ['t', 'r'] | ['translateX', 'r'] etc 
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attrList] if type(attrList) != list else attrList
        for attr in attrList:
            attrType = cmds.attributeQuery(attr, n=(self.name()), at=1)
            if attrType == 'double3':
                subAttrs = cmds.attributeQuery(attr, n=(self.name()), listChildren=1)
                if subAttrs:
                    for subAttr in subAttrs:
                        cmds.setAttr((self.name() + '.' + subAttr), l=1, k=keyable)

            else:
                cmds.setAttr((self.name() + '.' + attr), l=1, k=keyable)

    def openAttrs(self, attrList=None, keyable=True):
        """
                Args:
                -----
                attrList = 't' | 'tx' | 'v' | ['t', 'r'] | ['translateX', 'r'] etc 
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attrList] if type(attrList) != list else attrList
        for attr in attrList:
            attrType = cmds.attributeQuery(attr, n=(self.name()), at=1)
            if attrType == 'double3':
                subAttrs = cmds.attributeQuery(attr, n=(self.name()), listChildren=1)
                if subAttrs:
                    for subAttr in subAttrs:
                        cmds.setAttr((self.name() + '.' + subAttr), l=0, k=keyable)

            else:
                cmds.setAttr((self.name() + '.' + attr), l=0, k=keyable)

    def hasAttr(self, attrList):
        """ 
                Check for whether attr or attrList exists with hsNode
                For Ex: depFn.hasAttribute(attr)
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attrList] if type(attrList) != list else attrList
        for attrName in attrList:
            depFn = self._MFnDependencyNode()
            if not depFn.hasAttribute(str(attrName)):
                return False

        return True

    def hasAttrLocked(self, attr):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrType = attributeQuery(attr, n=(self.name()), at=1)
        if attrType == 'double3':
            boolType = False
            subAttrs = attributeQuery(attr, n=(self.name()), listChildren=1)
            if subAttrs:
                for subAttr in subAttrs:
                    if getAttr((self.attr(subAttr)), l=1):
                        boolType = True
                        break

            return boolType
        if getAttr((str(node) + '.' + attr), l=1):
            return True
        return False

    def listLockedAttrs(self, compoundAttr):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        lockedAttrs = []
        if self.hasAttr(compoundAttr):
            if cmds.attributeQuery(compoundAttr, n=(self.name()), at=1) == 'double3':
                chdAttrs = cmds.attributeQuery(compoundAttr, n=(self.name()), lc=1)
                if chdAttrs:
                    for attr in chdAttrs:
                        if getAttr((self.name() + '.' + attr), l=1):
                            lockedAttrs.append(attr)

        return lockedAttrs

    def hasUniqueName(self):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        depN = self._MFnDependencyNode()
        return depN.hasUniqueName()

    def hasParent(self, trgtObj, numParent=None):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        asTrgt = hsNode(trgtObj)
        if numParent:
            prntNode = self.parent()
            if prntNode:
                if self.parent(numParent).shortName() == prntNode.shortName():
                    return True
                return False
            else:
                return False
        else:
            nodeDg = self._MFnDagNode()
            mObj = asTrgt._MObject()
            return nodeDg.isChildOf(mObj)

    def isAnimated(self, attr=None):
        """
                Args:
                -----
                attr = 'tx' | 'rx' etc
                                
                Returns: True | False
                """
        if attr:
            if cmds.findKeyframe((self.name()), at=attr, c=1):
                return True
            return False
        else:
            if cmds.findKeyframe((self.name()), c=1):
                return True
            return False

    def isChildOf(self, trgtObj, checkAllParents=0, childImplied=True):
        """
                Args:
                -----
                If checkAllParents : trgtObj can be any of its parent
                else                       : trgtObj will be checked only for firstParent
                """
        ncTypes = 'mesh|curv|loc|jnt|trans|shp|^comp'
        asTrgt = hsNode(trgtObj)
        if checkAllParents:
            return self.hasParent(trgtObj)
        prntNode = self.parent()
        if prntNode:
            if prntNode.shortName() == asTrgt.shortName():
                return True
            return False
        else:
            return False

    def hasChild(self, trgtObj):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        nodeDg = self._MFnDagNode()
        asTrgt = hsNode(trgtObj)
        mObj = asTrgt._MObject()
        return nodeDg.isParentOf(mObj)

    def hide(self):
        """
                Args:
                ----
                objList = objStr | objList
                
                Usage:
                ------
                If any node's visibility is locked, it will unlock, hide and lock the visibility again..
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        conAttr = None
        if not self.getAttr('v'):
            return
        try:
            cmds.setAttr(self.name() + '.v', 0)
        except:
            try:
                toLockAgain = False
                if cmds.getAttr((self.attr('v')), l=True):
                    toLockAgain = True
                    self.setAttr('v', l=False)
                cmds.setAttr(self.name() + '.v', 0)
                if toLockAgain:
                    self.setAttr('v', l=True)
            except:
                conAttr = self.connectionInfo('v', sfd=1)
                if conAttr:
                    try:
                        cmds.setAttr(conAttr, 0)
                    except:
                        self._error("'%s' is locked | connected..\nThis '%s' Attr Couldn't be set" % [str(self.attr('v')), str(conAttr)])

        if conAttr:
            return conAttr
        return

    def isVisible(self, checkParents=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        if not self.getAttr('v'):
            return False
        if checkParents:
            prntList = self.parent(0, True)
            if prntList:
                return all([obj.getAttr('v') for obj in prntList])
            return True
        else:
            return True

    def isHidden(self, checkParents=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        if not self.isVisible(checkParents):
            return True
        return False

    def show(self, useParents=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        conAttr = None
        if self.isVisible(1):
            return True

        def showObj(asObj, inAttr='v'):
            try:
                conAttr = asObj.connectionInfo(inAttr, sfd=1)
            except:
                conAttr = cmds.connectionInfo((asObj + '.' + inAttr), sfd=1)

            if conAttr:
                if cmds.nodeType(conAttr) == 'animCurveUU':
                    return showObj(conAttr.split('.')[0], 'input')
                try:
                    cmds.setAttr(conAttr, 1)
                    return conAttr
                except:
                    return False

            else:
                try:
                    asObj.setAttr('v', 1)
                    return True
                except:
                    try:
                        toLockAgain = False
                        if asObj.getAttr('v', l=True):
                            toLockAgain = True
                            asObj.setAttr('v', l=False)
                        asObj.setAttr('v', 1)
                        if toLockAgain:
                            asObj.setAttr('v', l=True)
                        return True
                    except:
                        return False

        if not useParents:
            return showObj(self.asObj())
        trueNFalseList = []
        trueNFalseAppend = trueNFalseList.append
        trueNFalseAppend(showObj(self.asObj()))
        prntList = self.parent(0, True)
        if prntList:
            for prnt in prntList:
                trueNFalseAppend(showObj(prnt))
                if self.isVisible(1):
                    break

        return all(trueNFalseList)

    def nextUniqueName(self, reName=False, fromEnd=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        hsN = self.asObj()
        origName = self.shortName()

        def getUniqueName(nextName, origName):
            nextName = self._nextVar(nextName, fromEnd)[0]
            try:
                cmds.select(('*' + nextName), r=1)
                cmds.select(cl=1)
                return getUniqueName(nextName, origName)
            except:
                pass

            if not cmds.objExists(nextName):
                self.rename(nextName)
                if self.hasUniqueName():
                    if not reName:
                        self.rename(origName)
                    return nextName
            else:
                return getUniqueName(nextName, origName)

        if self.extractNum():
            return getUniqueName(hsN.shortName(), origName)
        if '_' not in self.shortName():
            nextName = self.shortName() + '_01'
        else:
            endSufx = self.shortName().split('_')[-1]
            nextName = self.shortName().replace(endSufx, '01_' + endSufx)
        hsN.rename(nextName)
        if hsN.hasUniqueName():
            if not reName:
                hsN.rename(origName)
            return nextName
        return getUniqueName(hsN, origName)

    def attr(self, attrList):
        """
                Objective:
                ----------
                To get the attr like : hsNode + '.' + attrName
                
                Returns:
                --------
                attributeList           #_ if len(attrList) > 1  
                attributeList[0]        #_ if len(attrList) == 1                
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attrList] if type(attrList) != list else attrList
        attributeList = []
        for attrName in attrList:
            if cmds.objExists(self.name() + '.' + str(attrName)):
                attributeList.append(self.name() + '.' + str(attrName))
            else:
                self._confirmAction('Attribute "%s" Not Exists' % (self.name() + '.' + str(attrName)))

        if attributeList:
            if len(attributeList) > 1:
                return attributeList
            return attributeList[0]
        else:
            return

    def addAttr(self, attr, addDivider=0, *args, **kwargs):
        """
        Examples:
        ---------
        Enum Attr:
        ---------
        >>> addAttr("parentTo", en="Wrist:Root:", at="enum", k=1)

        Others:
        -------
        >>> addAttr('persp', ln='test', at='double', k=1)
        >>> addAttr('persp.test', query=1, hasMaxValue=True)
        False

        >>> addAttr('persp.test', edit=1, hasMaxValue=False)
        >>> addAttr('persp.test', query=1, hasMaxValue=True)
        False

        >>> addAttr('persp.test', edit=1, hasMaxValue=True)
        >>> addAttr('persp.test', query=1, hasMaxValue=True)
        True
        """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attr] if isinstance(attr, str) else attr
        resList = []

        if not addDivider or isinstance(addDivider, str):
            self.addAttrDivider(addDivider)
        else:
            self.addAttrDivider()
        for attr in attrList:
            at = kwargs.pop('attributeType', kwargs.pop('at', None))
            if at is not None:
                try:
                    kwargs['at'] = {float: 'double', int: 'long', bool: 'bool', str: 'string'}[at]
                except KeyError:
                    kwargs['at'] = at

            if kwargs.get('e', kwargs.get('edit', False)):
                for (editArg, value) in kwargs.items():
                    if editArg not in ('e', 'edit') and value:
                        break
                else:
                    if any(editArg in ('hasMinValue', 'hnv', 'hasMaxValue', 'hxv', 'hasSoftMinValue', 'hsn', 'hasSoftMaxValue', 'hsx') for
                           editArg in kwargs):
                        if bool(value) != bool(cmds.addAttr(self.name(), ln=attr, **{'query': True, editArg: True})):
                            return cmds.addAttr(self.name(), ln=attr, **kwargs)
                        else:
                            return

            if not 'enumName' in kwargs or 'e' in kwargs or 'edit' in kwargs:
                res = cmds.addAttr(self.attr(attr), **kwargs)
            else:
                res = cmds.addAttr(self.name(), ln=attr, **kwargs)

            if kwargs.get('q', kwargs.get('query', False)):
                for (queriedArg, value) in kwargs.items():
                    if queriedArg not in ('q', 'query') and value:
                        break
                else:
                    if queriedArg in ('dt', 'dataType'):
                        if res is not None:
                            res = res[0]
                    else:
                        if queriedArg in ('p', 'parent'):
                            node = None
                            if args:
                                node = hsNode(args[0])
                            else:
                                node = ls(sl=1)[0]
                            if isinstance(node, Attribute):
                                node = node.node()
                            res = node.attr(res)
                        resList.append(res)

        if addDivider == 2:
            self.addAttrDivider(None)
        if len(resList) == 1:
            return resList[0]
        return resList

    def setAttr(self, attr, *args, **kwargs):
        """
                List of attrs can be provided at a time.
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        attrList = [attr] if type(attr) != list else attr
        for attr in attrList:
            attr = str(self.name() + '.' + attr)
            try:
                (cmds.setAttr)(attr, *args, **kwargs)
            except TypeError as msg:
                try:
                    val = kwargs.pop('type', kwargs.pop('typ', False))
                    typ = cmds.addAttr(attr, q=1, at=1)
                    if val == 'string' and typ == 'enum':
                        enums = cmds.addAttr(attr, q=1, en=1).split(':')
                        index = enums.index(args[0])
                        args = (index,)
                        (cmds.setAttr)(attr, *args, **kwargs)
                    else:
                        raise TypeError(msg)
                finally:
                    msg = None
                    del msg

            except RuntimeError as msg:
                try:
                    if 'No object matches name: ' in str(msg):
                        raise _objectError(attr)
                    else:
                        raise
                finally:
                    msg = None
                    del msg

    def addAttrDivider(self, dividerName=None):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        hsName = self.name()
        if not dividerName:
            Done = False
            for num in range(5, 16):
                if not cmds.attributeQuery(('_' * num), node=hsName, ex=1):
                    self.addAttr(('_' * num), at='enum', en=' ')
                    self.setAttr(('_' * num), e=1, k=0, channelBox=1)
                    Done = True
                    break

            if not Done:
                self._message('Oops.. Maximum "_*num" count exceeded ..!\nUse Any Divider Name')
        else:
            if isinstance(dividerName, str) or isinstance(dividerName, str):
                if not cmds.attributeQuery((dividerName.upper()), node=hsName, ex=1):
                    self.addAttr((dividerName.upper()), at='enum', en=' ', k=1)
                    self.setAttr((dividerName.upper()), e=1, k=0, channelBox=1)
                else:
                    warning('Attribute "%s" Already Exists ..!' % dividerName)

    def old_getPos(self, objType='obj', vtxOrNum=None):
        """
                Objective:
                ----------
                To return the world position of an object, meshVtx or curveCV

                Returns:
                --------
                [objPos]  if objType=='obj', [vtxPos] if objType=='vtx', [cvPos] if objType=='cv'                               
                """
        if objType.lower() == 'obj':
            transFn = MFnTransform()
            pathDg = self._MDagPath()
            transFn.setObject(pathDg)
            point = om.MPoint()
            point = transFn.rotatePivot(MSpace.kWorld)
            objPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
            return [objPos]
        if objType.lower() == 'vtx':
            if vtxOrNum:
                if type(vtxOrNum) != int:
                    testObj = re.search('(?<=\\[)(?P<vtxNum>[\\d]+)(?=\\])', str(vtxOrNum))
                    if testObj:
                        vtxNum = int(testObj.group('vtxNum'))
                    else:
                        self._confirmAction('vtxNum is not found', raiseErr=True)
                else:
                    vtxNum = vtxOrNum
                mDgPath = self._MDagPath()
                mItVtx = MItMeshVertex(mDgPath)
                vtxPos = []
                while not mItVtx.isDone():
                    if mItVtx.index() == vtxNum:
                        point = om.MPoint()
                        point = mItVtx.position(MSpace.kWorld)
                        vtxPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                        break
                    else:
                        next(mItVtx)

                return [vtxPos]
            if objType.lower() == 'cv':
                if vtxOrNum:
                    cvOrNum = vtxOrNum
                    if type(cvOrNum) != int:
                        testObj = re.search('(?<=\\[)(?P<cvNum>[\\d]+)(?=\\])', str(cvOrNum))
                        if testObj:
                            cvNum = int(testObj.group('cvNum'))
                        else:
                            self._confirmAction('cvNum is not found', raiseErr=True)
                    else:
                        cvNum = cvOrNum
                    mDgPath = self._MDagPath()
                    mItCV = MItCurveCV(mDgPath)
                    cvPos = []
                    while not mItCV.isDone():
                        if mItCV.index() == cvNum:
                            point = om.MPoint()
                            point = mItCV.position(MSpace.kWorld)
                            cvPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                            break
                        else:
                            next(mItCV)

                    return [cvPos]
            if objType.lower() == 'edg':
                if vtxOrNum:
                    edgOrNum = vtxOrNum
                    if type(edgOrNum) != int:
                        testObj = re.search('(?<=\\[)(?P<edgNum>[\\d]+)(?=\\])', str(edgOrNum))
                        if testObj:
                            edgNum = int(testObj.group('edgNum'))
                        else:
                            self._confirmAction('edgNum is not found', raiseErr=True)
                    else:
                        edgNum = edgOrNum
                    mDgPath = self._MDagPath()
                    mItEdg = MItMeshEdge(mDgPath)
                    cvPos = []
                    while not mItEdg.isDone():
                        if mItEdg.index() == edgNum:
                            point = om.MPoint()
                            point = mItEdg.center(MSpace.kWorld)
                            cvPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                            break
                        else:
                            next(mItEdg)

                    return [cvPos]

    def get_2PosVect(self, destObjOrPos):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|^comp'
        if type(destObjOrPos) != list:
            destObjOrPos = hsNode(destObjOrPos)
            destPos = destObjOrPos.getPos()
        else:
            destPos = destObjOrPos
        srcPos = self.getPos()
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        return om.MVector(distX, distY, distZ)

    def get_2PosExtn(self, destObjOrPos, extnRatio, locName='as_Extn_Loc', getLoc=True, getSpot=False):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|^comp'
        if getSpot:
            getLoc = False
        dirVect = self.get_2PosVect(destObjOrPos)
        extnPos = [num * (extnRatio + 1) for num in dirVect]
        extnLoc = hsNode(spaceLocator(n=locName, p=[extnPos[0], extnPos[1], extnPos[2]])[0])
        extnLoc.snapPosTo(self.name())
        extnLoc.centerPivot()
        extnLoc.unfreezeTrans()
        if getLoc == True:
            return extnLoc
        if getSpot:
            extLoc = extnLoc.getPosLoc(0, 0, 0, locName, getSpot=True)[0]
            extnLoc.delete()
            return extLoc
        extnPos = xform(extnLoc, q=1, ws=1, t=1)
        delete(extnLoc)
        return extnPos

    def getPos_Vtx(self, vtxOrNum):
        """doc"""
        ncTypes = 'mesh|comp'
        if type(vtxOrNum) != int:
            testObj = re.search('(?<=\\[)(?P<vtxNum>[\\d]+)(?=\\])', str(vtxOrNum))
            if testObj:
                vtxNum = int(testObj.group('vtxNum'))
            else:
                self._confirmAction('vtxNum is not found', raiseErr=True)
        mDgPath = self._MDagPath()
        mItVtx = MItMeshVertex(mDgPath)
        vtxPos = []
        while not mItVtx.isDone():
            vtxId = mItVtx.index()
            if vtxId == vtxNum:
                mObj = mItVtx.currentItem()
                pathDg = om.MDagPath()
                om.MGlobal.setSelectionMode(om.MGlobal.kSelectComponentMode)
                om.MGlobal.select(mDgPath, mObj, om.MGlobal.kReplaceList)
                point = om.MPoint()
                point = mItVtx.position(MSpace.kWorld)
                vtxPos = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                break
            else:
                next(mItVtx)

        return vtxPos

    def setName(self, newName):
        """Rename the object to given name"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        return self.rename(newName)

    def getRot(self, worldSpace=False):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if worldSpace:
            pLoc = self.getPosLoc(False, True)[0]
            locRot = pLoc.getRot()
            pLoc.delete()
            return locRot
        return list(self.getAttr('r'))

    def setRot(self, rotList=[0, 0, 0]):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        cmds.setAttr((self.fullName() + '.rotate'), (rotList[0]), (rotList[1]), (rotList[2]), type='double3')

    def getFaceList(self):
        """
                Returns:(hsNodes)
                -----------------
                Returns allFaceList
                """
        ncTypes = 'mesh|^comp'
        polyIt = self._MItMeshPolygon()
        allFaceList = []
        for num in range(polyIt.count()):
            allFaceList.append(hsNode(self.name() + '.f[' + str(num) + ']'))

        return allFaceList

    def getVtxList(self, get_hsNodes=True):
        """
                Returns(hsNodes):
                -----------------
                if self.isNodeType('nurbsCurve'):
                        return [cvList, numCVs]
                elif self.isNodeType('mesh'):                   
                        return [vtxList, numVtx]
                elif self.isNodeType('nurbsSurface'):
                        return [cvList, numCVs]
                """
        ncTypes = 'mesh|curv|^comp'
        if self.isNodeType('nurbsCurve'):
            shapeList = self.getShape(1)
            if len(shapeList) == 1:
                curvFn = MFnNurbsCurve(self._MDagPath())
                numCVs = curvFn.numCVs()
                if curvFn.form() == 3:
                    numCVs = numCVs - curvFn.degree()
                cvList = [hsNode(self.name() + '.cv[' + str(num) + ']') for num in range(numCVs)]
                cmds.select(cvList, r=1)
                return [cvList, numCVs]
            cv_List = []
            for shape in shapeList:
                curvFn = MFnNurbsCurve(shape._MDagPath())
                numCVs = curvFn.numCVs()
                if curvFn.form() == 3:
                    numCVs = numCVs - curvFn.degree()
                else:
                    cvList = [hsNode(shape.name() + '.cv[' + str(num) + ']') for num in range(numCVs)]
                    cv_List.extend(cvList)

            cmds.select(cv_List, r=1)
            return [cv_List, len(cv_List)]
        else:
            if self.isNodeType('mesh'):
                polyIt = self._MItMeshVertex()
                numVtx = polyIt.count()
                vtxList = [self.name() + '.vtx[' + str(num) + ']' for num in range(numVtx)]
                if get_hsNodes:
                    vtxList = list(map(hsNode, vtxList))
                return [vtxList, numVtx]
            if self.isNodeType('nurbsSurface'):
                cvIter = MItSurfaceCV(self.shape()._MDagPath())
                cvList = []
                while not cvIter.isDone():
                    while not cvIter.isRowDone():
                        utilU = om.MScriptUtil()
                        utilU.createFromInt(0)
                        ptrU = utilU.asIntPtr()
                        utilV = om.MScriptUtil()
                        utilV.createFromInt(0)
                        ptrV = utilV.asIntPtr()
                        cvIter.getIndex(ptrU, ptrV)
                        cvList.append(self.name() + '.cv[' + str(utilU.getInt(ptrU)) + '][' + str(utilV.getInt(ptrV)) + ']')
                        next(cvIter)

                    cvIter.nextRow()

                cmds.select(cvList, r=1)
                cvList = filterExpand(sm=28)
                numCVs = len(cvList)
                return [cvList, numCVs]

    def getAttr(self, attr, *args, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        datatype = kwargs.get('type', kwargs.get('typ', None))
        attr = str(self.name() + '.' + attr)
        try:
            attrVal = (cmds.getAttr)(attr, *args, **kwargs)
            if type(attrVal) != list:
                return attrVal
            if type(attrVal) == list:
                if len(attrVal) == 1:
                    if type(attrVal[0]) == tuple:
                        return list(attrVal[0])
                if type(attrVal) == list:
                    if len(attrVal) == 3:
                        return attrVal
        except TypeError as msg:
            try:
                val = kwargs.pop('type', kwargs.pop('typ', False))
                typ = cmds.addAttr(attr, q=1, at=1)
                if val == 'string':
                    if typ == 'enum':
                        enums = cmds.addAttr(attr, q=1, en=1).split(':')
                        index = enums.index(args[0])
                        args = (index,)
                        return (cmds.getAttr)(attr, *args, **kwargs)
                raise TypeError(msg)
            finally:
                msg = None
                del msg

        except RuntimeError as msg:
            try:
                if 'No object matches name: ' in str(msg):
                    raise _objectError(attr)
                else:
                    raise
            finally:
                msg = None
                del msg

    def snapRotTo(self, destObj, dirUpObj=None, aimAxis=None, upAxis=None):
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        src = self.asObj()
        if not (dirUpObj or aimAxis or upAxis):
            oriConst = cmds.orientConstraint(str(destObj), src, weight=1)
            rVal = self.getRot()
            cmds.delete(oriConst)
            cmds.setAttr(src + '.r', rVal[0], rVal[1], rVal[2], type='double3')
            return
        if dirUpObj and aimAxis and upAxis:
            oriConst = cmds.orientConstraint(str(destObj), src, weight=1)
            rVal = self.getRot()
            cmds.delete(oriConst)
            cmds.setAttr(src + '.r', rVal[0], rVal[1], rVal[2], type='double3')
            return
        if dirUpObj or aimAxis or upAxis:
            aimCon = cmds.aimConstraint(destObj, src, 1, upAxis, str(dirUpObj), 'object', (0, 0, 0), aimAxis, ('weight', 'upVector', 'worldUpObject', 'worldUpType', 'offset', 'aimVector'))
            rVal = self.getRot()
            cmds.delete(aimCon)
            cmds.setAttr(src + '.r', rVal[0], rVal[1], rVal[2], type='double3')
            return
        if not (dirUpObj and aimAxis and upAxis):
            aimCon = cmds.aimConstraint(destObj, src, 1, upAxis, 'scene', (0, 0, 0), aimAxis, ('weight', 'upVector', 'worldUpType', 'offset', 'aimVector'))
            rVal = self.getRot()
            cmds.delete(aimCon)
            cmds.setAttr(src + '.r', rVal[0], rVal[1], rVal[2], type='double3')
            return

    def snapShpTo(self, destPosOrObj=[0, 0, 0], shapePos=False):
        """doc"""
        ncTypes = 'mesh|curv|^comp'
        if type(destPosOrObj) != list:
            if '.' not in destPosOrObj:
                destObj = hsNode(destPosOrObj)
                destPos = destObj.getPos(shapePos)
            elif '.vtx[' in destPosOrObj or '.cv[' in destPosOrObj or '.e[' in destPosOrObj:
                destVtx = destPosOrObj
                vtxObjNode = hsNode(destVtx.split('.')[0])
                destPos = vtxObjNode.getPos(shapePos)
        else:
            destPos = destPosOrObj
        shpPos = self.getPos(True)
        select((self.getVtxList()[0]), r=1)
        cmds.move((-shpPos[0]), (-shpPos[1]), (-shpPos[2]), r=1)
        cmds.move((destPos[0]), (destPos[1]), (destPos[2]), r=1)

    def snapPivTo(self, destObj=[0, 0, 0]):
        """
                Args:
                -----
                destObj = destObj | destPos[0, 1, 0]
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        srcObj = self.name()
        if type(destObj) != list:
            if cmds.objExists(destObj):
                destObj = hsNode(destObj)
                destPos = destObj.getPos()
            else:
                self._error('%s -- Object Not Exists' % str(destObj))
        elif len(destObj) == 3:
            destPos = destObj
        cmds.move(destPos[0], destPos[1], destPos[2], srcObj + '.scalePivot', srcObj + '.rotatePivot')

    def transferAnimToGrp(self, attr='r'):
        """Moves animation from ctrls to grp"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if attr == 't':
            attrX = '.tx'
            attrY = '.ty'
            attrZ = '.tz'
        elif attr == 'r':
            attrX = '.rx'
            attrY = '.ry'
            attrZ = '.rz'
        ctrlList = hsN._selected()
        for ctrl in ctrlList:
            ctrlGrp = ctrl.firstParent()
            grp_X = cmds.getAttr(ctrlGrp + attrX)
            grp_Y = cmds.getAttr(ctrlGrp + attrY)
            grp_Z = cmds.getAttr(ctrlGrp + attrZ)
            ctrl_X = cmds.getAttr(ctrl + attrX)
            ctrl_Y = cmds.getAttr(ctrl + attrY)
            ctrl_Z = cmds.getAttr(ctrl + attrZ)
            cmds.setAttr(ctrlGrp + attrX, grp_X + ctrl_X)
            cmds.setAttr(ctrlGrp + attrY, grp_Y + ctrl_Y)
            cmds.setAttr(ctrlGrp + attrZ, grp_Z + ctrl_Z)
            cmds.setAttr(ctrl + attrX, 0)
            cmds.setAttr(ctrl + attrY, 0)
            cmds.setAttr(ctrl + attrZ, 0)

        cmds.select(ctrlList, r=1)

    def rotateBy(self, valList=[0, 90, 0], rAttr=None, mSpace=1):
        """
                rAttr =['ry', val], if rAttr is given, valList will be neglected ..
                mSpace ==0 : 'Object Space'
                mSpace ==1 : 'World Space'
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if rAttr:
            currentRot = self.getAttr(rAttr[0])
            valIncrement = currentRot + rAttr[1]
            self.setAttr(rAttr[0], valIncrement)
            self.select()
            self._refreshView(1)
            return
        if mSpace == 0:
            space = MSpace.kObject
        elif mSpace == 1:
            space = MSpace.kWorld
        rad = math.radians
        dgN = self._MDagPath()
        euT = MEulerRotation(rad(valList[0]), rad(valList[1]), rad(valList[2]), MEulerRotation.kXYZ)
        fnT = MFnTransform(dgN)
        fnT.rotateBy(euT, space)
        self.select()
        self._refreshView(1)

    def scaleBy(self, valList=[1, 1, 1], freezeIt=False, asIncrement=False, refreshView=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if type(valList) != list:
            if isinstance(valList, int) or isinstance(valList, float):
                if asIncrement:
                    currentScale = self.getAttr('s')
                    valList = [x + valList for x in currentScale]
                    self.setAttr('s', (valList[0]), (valList[1]), (valList[2]), type='double3')
                    if refreshView:
                        self.select()
                        self._refreshView(1)
                    return
                valList = [valList, valList, valList]
            dgN = self._MDagPath()
            fnT = MFnTransform()
            sUtil = MScriptUtil()
            sUtil.createFromDouble(valList[0], valList[1], valList[2])
            sPtr = sUtil.asDoublePtr()
            fnT.setObject(dgN)
            fnT.scaleBy(sPtr)
            if freezeIt:
                self.freeze()
        self.select()
        self._refreshView(1)

    def translateBy(self, valList=[0, 0, 0], freezeIt=False, mSpace=1):
        """
                Args:
                -----
                valList =[x, y, z]
                freezeIt =self will be freezed after translated
                mSpace =0: Local, 1 =World
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if mSpace == 1:
            currentTrans = self.getPos()
            valList[0] = currentTrans[0] + valList[0]
            valList[1] = currentTrans[1] + valList[1]
            valList[2] = currentTrans[2] + valList[2]
            self.setPos(valList)
            self.select()
            self._refreshView(1)
        elif mSpace == 0:
            dgN = self._MDagPath()
            fnT = MFnTransform()
            sUtil = MScriptUtil()
            sUtil.createFromDouble(valList[0], valList[1], valList[2])
            sPtr = sUtil.asDoublePtr()
            fnT.setObject(dgN)
            mVec = om.MVector(valList[0], valList[1], valList[2])
            fnT.translateBy(mVec, om.MSpace.kObject)
        if freezeIt:
            self.freeze()
        self.select()
        self._refreshView(1)

    def template(self, refreshView=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        self.select()
        cmds.TemplateObject()
        if refreshView:
            self.select()
            self._refreshView()

    def untemplate(self, refreshView=True):
        """Use hsN.setDisplayType"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        self.select()
        cmds.UntemplateObject()
        if refreshView:
            self.select()
            self._refreshView()

    def setDisplayType(self, valOrAttr=0, addAttrDivider=0, refreshView=True):
        """
                Args:
                -----
                valOrAttr               : 0 (Normal) | 1 (Template) | 2 (Reference) | srcAttr | srcObj 
                addAttrDivider  : Adds attrDivider to driver object if valOrAttr is object
                """
        ncTypes = 'mesh|curv|shp|trans'
        if self.hasShape():
            shpNode = self.getShape()
            conSrc = shpNode.connectionInfo('drawOverride', sfd=1)
            if conSrc:
                cmds.disconnectAttr(conSrc, shpNode.attr('drawOverride'))
            conSrc = shpNode.connectionInfo('overrideDisplayType', sfd=1)
            if conSrc:
                cmds.disconnectAttr(conSrc, shpNode.attr('overrideDisplayType'))
            shpNode.setAttr('overrideEnabled', 0)
        conSrc = self.connectionInfo('drawOverride', sfd=1)
        if conSrc:
            cmds.disconnectAttr(conSrc, self.attr('drawOverride'))
        conSrc = self.connectionInfo('overrideDisplayType', sfd=1)
        if conSrc:
            cmds.disconnectAttr(conSrc, self.attr('overrideDisplayType'))
        self.setAttr('overrideEnabled', 1)
        if isinstance(valOrAttr, int):
            if valOrAttr >= 2:
                valOrAttr = 2
            self.setAttr('overrideDisplayType', valOrAttr)
        else:
            if isinstance(valOrAttr, str) or isinstance(valOrAttr, str):
                if cmds.objExists(valOrAttr):
                    if '.' in valOrAttr:
                        if cmds.attributeQuery((valOrAttr.split('.')[-1]), n=(valOrAttr.split('.')[0]), ex=1):
                            cmds.connectAttr(valOrAttr, self.attr('overrideDisplayType'))
                        else:
                            cmds.warning("{0} -> Object Or Attr doesn't exist".format(valOrAttr))
                    elif cmds.objExists(valOrAttr):
                        asObj = hsNode(valOrAttr)
                        if not cmds.attributeQuery('displayType', n=asObj, ex=1):
                            asObj.addAttr('displayType', addAttrDivider, en='Normal:Template:Reference:', at='enum', k=1, dv=1)
                        asObj.setAttr('displayType', 0)
                        asObj.connectAttr('displayType', self.name(), 'overrideDisplayType')
                    else:
                        cmds.warning("{0} -> Object doesn't exist".format(valOrAttr))
        if refreshView:
            self.select()
            self._refreshView()

    def transferAnimTo(self, dest, attr='r', move=False):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        src = self.fullName()
        attrList = [attr] if type(attr) != list else attr
        self.select()
        for attr in attrList:
            if attr == 't':
                if self.isAnimated('t'):
                    lockAgain = False
                    if self.hasAttrLocked('t'):
                        self.openAttrs('t')
                        lockAgain = True
                    if move == True:
                        cmds.cutKey(src, at=['tx', 'ty', 'tz'], option='keys')
                        cmds.setAttr((src + '.translate'), 0, 0, 0, type='double3')
                    else:
                        cmds.copyKey(src, attribute=['tx', 'ty', 'tz'], option='keys')
                    pasteKey(dest, attribute=['tx', 'ty', 'tz'], option='replaceCompletely')
                    if lockAgain:
                        self.lockAttrs('t')
            elif attr == 'r':
                if self.isAnimated('r'):
                    lockAgain = False
                    if self.hasAttrLocked('r'):
                        self.openAttrs('r')
                        lockAgain = True
                    if move == True:
                        cmds.cutKey(src, at=['rx', 'ry', 'rz'], option='keys')
                        cmds.setAttr((src + '.rotate'), 0, 0, 0, type='double3')
                    else:
                        cmds.copyKey(src, attribute=['rx', 'ry', 'rz'], option='keys')
                    try:
                        cmds.pasteKey(dest, attribute=['rx', 'ry', 'rz'], option='replaceCompletely')
                    except:
                        pass

                    if lockAgain:
                        self.lockAttrs('r')
            else:
                om.MGlobal.displayInfo("This attribute's Animation Cann't Be Transfered")

    def moveValuesToGrp(self, srcList, attrList=['r'], grpLevel=2):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        for src in srcList:
            for attr in attrList:
                if attr == 't':
                    select(src, r=1)
                    for num in range(grpLevel):
                        pickWalk(d='up')

                    grpName = selected()[0]
                    baseVal = getAttr(src + '.translate')
                    setAttr((src + '.translate'), 0, 0, 0, type='double3')
                    grpVal = getAttr(grpName + '.translate')
                    grpVal[0] += baseVal[0]
                    grpVal[1] += baseVal[1]
                    grpVal[2] += baseVal[2]
                    setAttr((grpName + '.translate'), (grpVal[0]), (grpVal[1]), (grpVal[2]), type='double3')
                if attr == 'r':
                    select(src, r=1)
                    for num in range(grpLevel):
                        pickWalk(d='up')

                    grpName = selected()[0]
                    baseVal = getAttr(src + '.rotate')
                    setAttr((src + '.rotate'), 0, 0, 0, type='double3')
                    grpVal = getAttr(grpName + '.rotate')
                    grpVal[0] += baseVal[0]
                    grpVal[1] += baseVal[1]
                    grpVal[2] += baseVal[2]
                    setAttr((grpName + '.rotate'), (grpVal[0]), (grpVal[1]), (grpVal[2]), type='double3')

    def movePoseToGrp(self, attrList=['r'], grpLevel=1, unlockAttrs=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        attrList = [attrList] if type(attrList) != list else attrList
        if grpLevel > 1:
            grpNode = self.pickWalkUp(grpLevel)[-1]
        else:
            grpNode = self.pickWalkUp(grpLevel)
        posLoc = self.getPosLoc(0, True, 0)[0]
        for attr in attrList:
            if attr == 't':
                lockAgain = False
                if self.hasAttrLocked('t'):
                    self.openAttrs('t')
                    lockAgain = True
                else:
                    self.setAttr('t', 0, 0, 0, type='double3')
                    grpNode.snapPosTo(posLoc)
                    if lockAgain:
                        self.lockAttrs('t')
            if attr == 'r':
                lockAgain = False
                if self.hasAttrLocked('r'):
                    self.openAttrs('r')
                    lockAgain = True
                initRot = self.getRot()
                self.setAttr('r', 0, 0, 0, type='double3')
                grpNode.snapRotTo(posLoc)
                if lockAgain:
                    self.lockAttrs('r')

        posLoc.delete()
        grpNode.select()

    def moveValuesFromGrps(self, srcList, attrList=['r'], grpLevel=2):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        for src in srcList:
            for attr in attrList:
                if attr == 't':
                    asSrc = hsNode(src)
                    asLoc = asSrc.getPosLoc(False, False)[0]
                    topNextGrp = asSrc.parent(grpLevel + 1)
                    asLoc.parentTo(topNextGrp)
                    asSrc.select()
                    baseVal = asLoc.getAttr('t')
                    for num in range(grpLevel)[0:]:
                        pickWalk(d='up')
                        grpName = selected()[0]
                        try:
                            setAttr((grpName + '.translate'), 0, 0, 0, type='double3')
                        except:
                            pass

                    setAttr((src + '.translate'), (baseVal[0]), (baseVal[1]), (baseVal[2]), type='double3')
                    asLoc.deleteNode()
                if attr == 'r':
                    asSrc = hsNode(src)
                    asLoc = asSrc.getPosLoc(False, True)[0]
                    topNextGrp = asSrc.parent(grpLevel + 1)
                    asLoc.parentTo(topNextGrp)
                    asSrc.select()
                    baseVal = asLoc.getAttr('r')
                    for num in range(grpLevel)[0:]:
                        pickWalk(d='up')
                        grpName = selected()[0]
                        try:
                            setAttr((grpName + '.rotate'), 0, 0, 0, type='double3')
                        except:
                            pass

                    setAttr((src + '.rotate'), (baseVal[0]), (baseVal[1]), (baseVal[2]), type='double3')
                    asLoc.deleteNode()

        select(srcList, r=1)

    def moveAnimToGrp(self, attr='r'):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if not ctrlList:
            ctrlList = selected()
            if not ctrlList:
                self._error('You need to either select the objects or provide the args..')
        attrList = [attrList] if (not type(attrList) == list) else attrList
        for attr in attrList:
            cmds.select(ctrl, r=1)
            self._refreshView(1)
            ctrlGrp = self.pickWalkUp()
            self.transferAnimTo(ctrlGrp, attr, True)

    def moveAnimTo(self, dest, attr='r', remove=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        self.transferAnimTo(self.name(), dest, attr, remove)

    def centerPivot(self):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        self.select()
        mel.eval('CenterPivot')

    def connectionInfo(self, attrName, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        return (cmds.connectionInfo)((self.attr(attrName)), **kwargs)

    def contains(self, objOrPos):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if type(objOrPos) != list and cmds.objExists(objOrPos):
            hsN = hsNode(objOrPos)
            trgtPos = hsN.getPos()
        elif type(objOrPos) == list and len(objOrPos) == 3:
            trgtPos = objOrPos
        else:
            self._error('Object : %s Not Exists' % str(objOrPos))
        bBox = self._MBoundingBox()
        mPnt = om.MPoint(trgtPos[0], trgtPos[1], trgtPos[2])
        return bBox.contains(mPnt)

    def intersects(self, trgtObj):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        bBox = self._MBoundingBox()
        asTrgt = hsNode(trgtObj)
        trgtBox = asTrgt._MBoundingBox()
        return bBox.intersects(trgtBox)

    def connections(self, attrName=None, **kwargs):
        """
                kwargs: connections:c, plug:p, src:s, dest:d [returns]
                -------------------------------------------------------
                plug(p=1)   : ['curve1.translate', 'curve2.rotate', etc]
                no args         : ['curve1', 'curve2', etc]
                attrName        : [related to attr only ..]
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if attrName:
            return (cmds.listConnections)((self.attr(attrName)), **kwargs)
        return (cmds.listConnections)((self.name()), **kwargs)

    def connectAttr(self, srcAttr, trgtObj, trgtAttr=None, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        trgtList = [trgtObj] if type(trgtObj) != list else trgtObj
        for trgtObj in trgtList:
            if '.' in str(trgtObj):
                try:
                    cmds.connectAttr((self.attr(srcAttr)), trgtObj, f=1)
                except:
                    self._confirmAction('Connection can not be made ..!', raiseErr=True)

            elif trgtAttr:
                trgtAttrList = [trgtAttr] if type(trgtAttr) != list else trgtAttr
                for trgtAttr in trgtAttrList:
                    cmds.connectAttr((self.attr(srcAttr)), (trgtObj + '.' + trgtAttr), f=1)

            else:
                self._confirmAction("trgtAttr needs to be provided ..\nin case trgtObj doesn't has attr", raiseErr=True)

    def reverseConnect(self, srcAttr, trgtObj, trgtAttr=None, zeroToOne=False, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if not zeroToOne:
            if '.' in str(trgtObj):
                destAttr = trgtObj
                mdNode = cmds.shadingNode('multiplyDivide', asUtility=1, n='_RevMD')
            else:
                destAttr = trgtObj + '.' + trgtAttr
                mdNode = cmds.shadingNode('multiplyDivide', asUtility=1, n=(str(trgtObj) + '_RevMD'))
            cmds.setAttr(mdNode + '.operation', 1)
            if attributeQuery(srcAttr, n=(self.name()), at=1) == 'double3':
                cmds.setAttr((mdNode + '.input2'), (-1), (-1), (-1), type='double3')
                (self.connectAttr)(srcAttr, mdNode, 'input1', **kwargs)
                cmds.connectAttr((mdNode + '.output'), destAttr, f=1)
            else:
                cmds.setAttr(mdNode + '.input2X', -1)
                (self.connectAttr)(srcAttr, mdNode, 'input1X', **kwargs)
                cmds.connectAttr((mdNode + '.outputX'), destAttr, f=1)
        else:
            if '.' in str(trgtObj):
                drivenAttr = trgtObj
                revNodeName = trgtObj.split('.')[0] + '_RevRN'
            else:
                drivenAttr = trgtObj + '.' + trgtAttr
                revNodeName = str(trgtObj) + '_RevRN'
            revNode = shadingNode('reverse', asUtility=1, n=revNodeName)
            if attributeQuery(srcAttr, n=(self.name()), at=1) == 'double3':
                (self.connectAttr)(srcAttr, revNode, 'input', **kwargs)
                cmds.connectAttr((revNode + '.output'), drivenAttr, f=1)
            else:
                (self.connectAttr)(srcAttr, revNode, 'inputX', **kwargs)
                cmds.connectAttr((revNode + '.outputX'), drivenAttr, f=1)

    def disconnectAttr(self, srcAttr, trgtObj=None, trgtAttr=None):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if '.' in str(trgtObj):
            cmds.disconnectAttr(self.attr(srcAttr), trgtObj)
        elif trgtAttr:
            cmds.disconnectAttr(self.attr(srcAttr), trgtObj + '.' + trgtAttr)
        else:
            self._confirmAction("trgtAttr needs to be provided ..\nincase trgtObj doesn't has attr", raiseErr=True)

    def freeze(self, **kwargs):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp'
        if not kwargs:
            kwargs = {'t':1, 'r':1,  's':1}
        self.select(r=1)
        (cmds.makeIdentity)(apply=True, **kwargs)

    def jntOrient(self, jntAxis='x', secAxisList=['y', 'y'], selectHI=True, endJnt=True, freezeIt=False):
        """doc"""
        ncTypes = 'jnt'
        if freezeIt:
            self.freeze(t=1, r=1, s=1, jo=1)
        if jntAxis.startswith('-'):
            jntAxis = jntAxis.split('-')[-1]
        if secAxisList[0].split('-')[-1] == jntAxis.split('-')[-1]:
            self._confirmAction("jntAxis(Primary Axis) and Secondary Axis(secAxisList[0]) cann't be same", True)
        if secAxisList[0].startswith('-') and not secAxisList[1].startswith('-'):
            secAxisList[0] = secAxisList[0].split('-')[-1]
            secAxisList[1] = '-' + secAxisList[1]
        else:
            if secAxisList[0].startswith('-'):
                if secAxisList[1].startswith('-'):
                    secAxisList[0] = secAxisList[0].split('-')[-1]
                    secAxisList[1] = secAxisList[1].split('-')[-1]
                tempJnts = []
                if selectHI:
                    hiJntList = self.selectHI('jnt')
                else:
                    hiJntList = [self.name()]
                if endJnt:
                    for jnt in hiJntList:
                        if jnt.isLastJnt():
                            prevJnt = jnt.parent()
                            destLoc = prevJnt.get_2PosExtn(jnt, 1)
                            cmds.select(cl=1)
                            tempJnt = hsNode(cmds.joint(p=(0, 0, 0)))
                            tempJnt.snapPosTo(destLoc)
                            cmds.select(cl=1)
                            cmds.delete(destLoc)
                            cmds.parent(tempJnt, jnt)
                            tempJnts.append(tempJnt)

                self.freeze()
                axisList = ['x', 'y', 'z']
                axisList.remove(jntAxis)
                axisList.remove(secAxisList[0])
                jntDirAxis = jntAxis + secAxisList[0] + axisList[0]
                if secAxisList[1].startswith('-'):
                    secAxisUp = secAxisList[1].split('-')[1] + 'down'
                else:
                    secAxisUp = secAxisList[1] + 'up'
                self.select(r=1)
                if selectHI:
                    joint(ch=1, e=1, oj=jntDirAxis, secondaryAxisOrient=secAxisUp)
                else:
                    joint(ch=0, e=1, oj=jntDirAxis, secondaryAxisOrient=secAxisUp)
                if tempJnts:
                    cmds.delete(tempJnts)
            cmds.select(cl=1)

    def jntOrientTo(self, trgtJnt, axisList=['x', 'y', 'z']):
        """doc"""
        ncTypes = 'jnt'
        axisList = [axisList] if type(axisList) != list else axisList
        asTrgt = hsNode(trgtJnt)
        if asTrgt.nodeType() != 'joint':
            self._error('%s is not a "joint"' % asTrgt.shortName())
        if len(axisList) == 3:
            rAxis = asTrgt.getAttr('rotateAxis')
            jntOrient = asTrgt.getAttr('jointOrient')
            self.setAttr('rotateAxis', rAxis[0], rAxis[1], rAxis[2])
            self.setAttr('jointOrient', jntOrient[0], jntOrient[1], jntOrient[2])
        else:
            for axisName in axisList:
                rAxis = asTrgt.getAttr('rotateAxis' + axisName.upper())
                jntOrient = asTrgt.getAttr('jointOrient' + axisName.upper())
                self.setAttr('rotateAxis' + axisName.upper(), rAxis)
                self.setAttr('jointOrient' + axisName.upper(), jntOrient)

    def jntRadius(self, val=None):
        """doc"""
        ncTypes = 'jnt'
        if not val:
            return self.getAttr('radius')
        self.setAttr('radius', val)

    def jntSplit(self, splitCount=1, makeCopy=False, namePrfx=None, nameSufx='_Skn_Jnt', matchOrient=False, getPos=0, getLoc=0, getEnds=0):
        """
                Args:
                -----
                baseJnt  : baseJnt should have at least one child jnt
                namePrfx : if not given, splitJnt new name is : 
                        >> baseJnt.shortName().replace('_Jnt', '') + '%0.2d' %num + nameSufx
                makeCopy : if True
                        >> Copy baseJnt and parents all split jnts under baseJnt
                
                Returns: (hsNodes)
                --------
                ['Split_01_Skn_Jnt', 'Split_02_Skn_Jnt', ..]  #_ hsNodes
                """
        ncTypes = 'jnt'
        base_Jnt = self.asObj()
        chd_Jnt = base_Jnt.child()
        if not chd_Jnt:
            return []
        jnt_Axis = base_Jnt.jntAxis()
        if jnt_Axis:
            jntAxis = jnt_Axis[-1]
        elif base_Jnt.startswith('R_'):
            jntAxis = '-x'
        else:
            jntAxis = 'x'
        jntRadius = base_Jnt.jntRadius()
        splitJnts = []
        if makeCopy:
            if not jntAxis.startswith('-'):
                baseJnt = base_Jnt.getPosJnt(makeChild=True, jntNames=None, snapOrient=False)
                baseJnt.parentTo(base_Jnt.parent())
                chdJnt = chd_Jnt.getPosJnt(makeChild=True, jntNames='as_Split_EndJnt', snapOrient=False)
                chdJnt.parentTo(baseJnt)
                allAxis = ['x', 'y', 'z']
                allAxis.remove(jntAxis)
                eRig.mJntOrient(baseJnt, jntAxis, allAxis)
            else:
                baseJnt = base_Jnt.duplicate()[0]
                allChildren = [str(obj) for obj in listRelatives(baseJnt, c=1)]
                if len(allChildren) > 1:
                    delete(list(set(allChildren) ^ set([baseJnt.child()])))
                chdJnt = baseJnt.child()
                if chdJnt.child():
                    delete(chdJnt.child())
                jntAxis = jntAxis.strip('-')
            baseJnt.setAttr('radius', jntRadius)
            if matchOrient:
                baseJnt.jntOrientTo(base_Jnt)
                chdJnt.jntOrientTo(base_Jnt)
            chdJnt.setAttr('radius', jntRadius)
            if namePrfx:
                namePrfx = namePrfx + '_' if (not namePrfx.endswith('_')) else namePrfx
                nameSufx = '_' + nameSufx if (not nameSufx.startswith('_')) else nameSufx
                baseJnt = baseJnt.rename(namePrfx + '01' + nameSufx)
                splitJnts.append(hsNode(baseJnt))
                if splitCount:
                    chdJnt = chdJnt.rename(namePrfx + '%0.2d' % splitCount + '_End_Jnt')
                else:
                    chdJnt = chdJnt.rename(namePrfx + '02_End_jnt')
                    splitJnts.append(hsNode(chdJnt))
                    return splitJnts
            else:
                baseJnt = baseJnt.rename(base_Jnt.shortName().replace('_Skn_Jnt', '') + '_01' + nameSufx)
                splitJnts.append(hsNode(baseJnt))
                chdJnt = chdJnt.rename(chd_Jnt.shortName().replace('_Skn_Jnt', '') + '%0.2d' % splitCount + nameSufx)
                if not splitCount:
                    splitJnts.append(hsNode(chdJnt))
                    return splitJnts
        else:
            if jntAxis.startswith('-'):
                jntAxis = jntAxis.strip('-')
            baseJnt = hsNode(base_Jnt)
            chdJnt = hsNode(chd_Jnt)
        numPlus = 1.0 / (splitCount + 1)
        splitVal = 0
        posList = []
        for num in range(splitCount):
            splitVal += numPlus
            posList.append(self.get_2PosExtn(chdJnt, -splitVal, None, None))

        posList.reverse()
        if getEnds:
            posList.insert(0, baseJnt.getPos())
            posList.append(chdJnt.getPos())
        if getPos:
            return posList
        print(posList)
        for num in range(len(posList)):
            if getLoc:
                gLoc = hsNode(cmds.spaceLocator()[0])
            elif num == 0:
                insertJoint(baseJnt)
            else:
                insertJoint(newJnt)
            if namePrfx:
                if makeCopy:
                    newName = namePrfx + '%0.2d' % (num + 2) + nameSufx
                else:
                    newName = namePrfx + '%0.2d' % (num + 1) + nameSufx
            elif makeCopy:
                if num == 0:
                    newName = baseJnt.nextUniqueName()
                else:
                    newName = newJnt.nextUniqueName()
            else:
                newName = baseJnt.shortName().replace('_Skn_Jnt', '') + '_%0.2d' % (num + 1) + nameSufx
            if getLoc:
                gLoc = gLoc.rename(newName)
                gLoc.snapPosTo([posList[num][0], posList[num][1], posList[num][2]])
                if matchOrient:
                    gLoc.snapRotTo(base_Jnt)
                else:
                    splitJnts.append(gLoc)
            else:
                newJnt = hsN._selected()[0]
                joint(newJnt, co=1, e=1, p=(posList[num][0], posList[num][1], posList[num][2]))
                newJnt = newJnt.rename(newName)
                if matchOrient:
                    newJnt.jntOrientTo(base_Jnt, jntAxis)
                newJnt.setAttr('radius', jntRadius)
                splitJnts.append(hsNode(newJnt))

        if makeCopy:
            chdJnt = chdJnt.rename(newJnt.nextUniqueName().replace(nameSufx, '_End_Jnt'))
            splitJnts.append(hsNode(chdJnt))
        return splitJnts

    def jntAxis(self):
        """
                Returns:
                -------
                return [[0, 1, 0], 'y'] or [[-1, 0, 0], '-x'] etc
                """
        ncTypes = 'jnt'
        jntName = self.name()
        switch = 1
        relative_c = 1
        relative_p = 1
        pos_neg = 1
        if nodeType(jntName) != 'joint':
            raise RuntimeError('%s is not Joint, but %s\n' % (jntName, nodeType(jntName)))
        chdList = listRelatives(jntName, c=1, typ='joint', fullPath=1)
        if chdList:
            chdList = list(map(hsNode, chdList))
            chdJnt = chdList[0]
        else:
            print("Child Joint Doesn't Exist!")
            switch = -1
            relative_c = 0
            parentList = cmds.listRelatives(jntName, p=1, typ='joint')
            if parentList:
                parentList = list(map(hsNode, parentList))
                chdJnt = parentList[0]
            else:
                relative_p = 0
                print("Parent Joint Doesn't Exist!")
                chdJnt = jntName
        jntPos = cmds.joint(jntName, q=1, a=1, p=1)
        jntVect = MVector(jntPos[0], jntPos[1], jntPos[2])
        chdPos = cmds.joint(chdJnt, q=1, a=1, p=1)
        chdVect = MVector(chdPos[0], chdPos[1], chdPos[2])
        if switch == 1:
            aimVect = chdVect - jntVect
        else:
            aimVect = -(chdVect - jntVect)
        aimVect.normalize()
        normVect = aimVect
        baseLoc = cmds.spaceLocator(p=(jntVect.x, jntVect.y, jntVect.z))
        cmds.parent(baseLoc, jntName)
        cmds.makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        cmds.CenterPivot()
        basePos = cmds.pointPosition(baseLoc, w=1)
        baseVect = MVector(basePos[0], basePos[1], basePos[2])
        cmds.move(1, 0, 0, r=1, ls=1, wd=1)
        locPos = cmds.pointPosition(baseLoc, w=1)
        tempPosX = MVector(locPos[0], locPos[1], locPos[2])
        normVectX = tempPosX - baseVect
        normVectX.normalize()
        cmds.move((-1), 1, 0, r=1, ls=1, wd=1)
        locPos = cmds.pointPosition(baseLoc, w=1)
        tempPosY = MVector(locPos[0], locPos[1], locPos[2])
        normVectY = tempPosY - baseVect
        normVectY.normalize()
        cmds.move(0, (-1), 1, r=1, ls=1, wd=1)
        locPos = cmds.pointPosition(baseLoc, w=1)
        tempPosZ = MVector(locPos[0], locPos[1], locPos[2])
        normVectZ = tempPosZ - baseVect
        normVectZ.normalize()
        cmds.move(0, 0, (-1), r=1, ls=1, wd=1)
        vectList = [
         normVectX.x, normVectX.y, normVectX.z, normVectY.x, normVectY.y, normVectY.z, normVectZ.x, normVectZ.y, normVectZ.z, normVect.x, normVect.y, normVect.z]
        tempArray = []
        for i in range(0, 12):
            tempArray.append(float(round(vectList[i], 3)))

        normVectX = MVector(tempArray[0], tempArray[1], tempArray[2])
        normVectY = MVector(tempArray[3], tempArray[4], tempArray[5])
        normVectZ = MVector(tempArray[6], tempArray[7], tempArray[8])
        normVect = MVector(tempArray[9], tempArray[10], tempArray[11])
        aimVal = ''
        if normVectY == normVect:
            aimVal = 'y'
            dirVect = MVector(0, 1, 0)
        elif normVectY == -normVect:
            aimVal = '-y'
            dirVect = MVector(0, -1, 0)
        elif normVectZ == normVect:
            aimVal = 'z'
            dirVect = MVector(0, 0, 1)
        elif normVectZ == -normVect:
            aimVal = '-z'
            dirVect = MVector(0, 0, -1)
        elif normVectX == normVect:
            aimVal = 'x'
            dirVect = MVector(1, 0, 0)
        elif normVectX == -normVect:
            aimVal = '-x'
            dirVect = MVector(-1, 0, 0)
        elif relative_p == 1 and relative_c == 1:
            dirVect = None
        elif relative_p == 1:
            dirVect = None
        elif relative_p == 0:
            aimVal = 'w'
            cmds.warning('Joint has no child or Joint has no parent\n')
            dirVect = MVector(0, 1, 0)
        if len(aimVal) == 2:
            pos_neg = -1
            normVect = -normVect
        cmds.delete(baseLoc)
        if dirVect:
            toPrint = "Aim vector is '" + aimVal + "' -> [%.1f, %.1f, %.1f]  \n" % (dirVect.x, dirVect.y, dirVect.z)
            return [[dirVect.x, dirVect.y, dirVect.z], aimVal]
        return

    def jntDisconnect(self, disconnectHI=False):
        """doc"""
        ncTypes = 'jnt'
        self.select()
        DisconnectJoint()

    def jntDist(self, includeHI=False, impliedParent=True):
        """doc"""
        ncTypes = 'jnt'
        if includeHI:
            chdList = self.selectHI('jnt', True)
            if chdList:
                return sum((chdJnt.jntDist() for chdJnt in chdList))
            return 0
        else:
            prntJnt = self.parent()
            if prntJnt:
                if prntJnt.isJnt():
                    jntAxis = prntJnt.jntAxis()[1]
                    jntAxis = jntAxis.strip('-')
                    return self.getAttr('t' + jntAxis)
                return 0
            else:
                return 0

    def jntLength(self, includeHI=False, impliedParent=True):
        """doc"""
        ncTypes = 'jnt'
        if includeHI:
            chdList = self.selectHI('jnt', False)
            if chdList:
                return sum((chdJnt.jntDist() for chdJnt in chdList))
            return 0
        else:
            chdJnt = self.child()
            if chdJnt:
                return chdJnt.jntDist()
            return 0

    def mConstrain(self, objList=None, conList=None, extras=None, **kwargs):
        """
                Args:
                -----
                conList = 'point' | 'orient' | 'parent' | 'scale' | 'geometry' | 'normal | 'tangent' | 'aim' | 'poleVector' | 'pointOnPoly'
                extras = None | 'mirror' | 'copy' | 'move' [objList should be provided]
                **kwargs : weight(w=1), maintainOffset(mo=1), remove(rm=1), targetList(tl=1), weightAliasList(wal=1), name(n='_PointCon'), e=1, q=1
                
                Examples:
                ---------                       
                hsNode.mConstrain('object02', 'orient')         #_ If no kwargs, kwargs ={'mo'=1, 'w':1}
                        # Result: [u'object02_OrientCon']
                hsNode.mConstrain(['object02', 'object03'], ['orient', 'point'])  
                        # Result: [u'object02_OrientCon', u'object02_OrientCon', u'object03_PointCon', u'object03_PointCon']

                Query Mode:
                -----------
                hsNode.mConstrain(q=1, wal=1) #hsNode ='object03'
                        # Result: [u'object01W0', u'object02W0'] # 
                hsNode.mConstrain(q=1)  #_ Return all constraints list                           
                        # Result: ['object02_OrientCon', 'object02_PointCon'] # 
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp|^shp'
        if not kwargs:
            kwargs = {'mo':1, 'w':1}
        if 'q' in kwargs:
            pass
        else:
            objList = [objList] if type(objList) != list else objList
        srcName = self.name()
        if conList:
            conList = [conList] if type(conList) != list else conList
            select(cl=1)
            if set(['point', 'parent']).issubset(conList):
                self._confirmAction("You cann't apply \n'point' and 'parent' constraints at a time", raiseErr=True)
            if set(['orient', 'parent']).issubset(conList):
                self._confirmAction("You cann't apply \n'orient' and 'parent' constraints at a time", raiseErr=True)
            if set(['point', 'orient', 'parent']).issubset(conList):
                self._confirmAction("You cann't apply \n'point', 'orient' and 'parent' constraints at a time", raiseErr=True)
            conNodeList = []
            queryList = []
            constrainList = ['point','orient','parent','scale','normal','aim','geometry','tangent','pointOnPoly']
            if conList:
                for conName in conList:
                    if objList and 'q' not in kwargs:
                        objConList = []
                        for obj in objList:
                            if conName != 'poleVector':
                                exec('conNode = cmds.' + conName + 'Constraint("' + srcName + '", "' + str(obj) + '", n="' + str(obj) + '_' + conName.title() + 'Con", **kwargs)[0]')
                            else:
                                exec('conNode = cmds.' + conName + 'Constraint("' + srcName + '", "' + str(obj) + '", n="' + str(obj) + '_' + conName.title() + 'Con", w=' + str(kwargs['w']) + ')[0]')
                            asConNode = hsNode(conNode)
                            if conName == 'parent' or conName == 'orient':
                                asConNode.setAttr('interpType', 2)
                            if conNode not in conNodeList:
                                objConList.append(asConNode)

                        conNodeList.extend(objConList)
                    else:
                        if 'q' in kwargs:
                            qList = None
                            conName = str(conName)
                            if nodeType(conName) == 'parentConstraint':
                                exec('qList = cmds.parentConstraint("' + str(conName) + '", **kwargs)')
                            elif nodeType(conName) == 'pointConstraint':
                                exec('qList = cmds.pointConstraint("' + str(conName) + '", **kwargs)')
                            elif nodeType(conName) == 'orientConstraint':
                                exec('qList = cmds.orientConstraint("' + str(conName) + '", **kwargs)')
                            elif nodeType(conName) == 'scaleConstraint':
                                exec('qList = cmds.scaleConstraint("' + str(conName) + '", **kwargs)')
                            elif nodeType(conName) == 'aimConstraint':
                                exec('qList = cmds.aimConstraint("' + str(conName) + '", **kwargs)')
                            if qList:
                                qList = [qList] if type(qList) != list else qList
                                qList = list(map(hsNode, qList))
                                queryList.extend(qList)

            elif objList:
                conList = objList
                conList = [conList] if type(conList) != list else conList
                if 'q' in kwargs:
                    for conName in conList:
                        qList = None
                        if len(list(kwargs.keys())) > 1 or cmds.objExists(conName):
                            exec('qList = cmds.' + nodeType(conName) + '("' + conName + '", **kwargs)')
                        else:
                            exec('qList = cmds.' + conName + 'Constraint("' + self.name() + '", **kwargs)')
                        if qList:
                            qList = [qList] if type(qList) != list else qList
                            qList = list(map(hsNode, qList))
                            queryList.extend(qList)

            else:
                qList = None
                try:
                    exec('qList = cmds.' + nodeType(self.name()) + '("' + self.name() + '", **kwargs)')
                    if qList:
                        qList = [qList] if type(qList) != list else qList
                        qList = list(map(hsNode, qList))
                        queryList.extend(qList)
                except:
                    for conName in constrainList:
                        exec('qList = cmds.' + conName + 'Constraint("' + self.name() + '", **kwargs)')
                        if qList:
                            qList = [qList] if type(qList) != list else qList
                            qList = list(map(hsNode, qList))
                            queryList.extend(qList)

            if 'q' in kwargs:
                return list(set(queryList))
            return conNodeList

    def constrainTo(self, objList, conList='parent', **kwargs):
        """
                Args:
                -----
                conList         : 'parent' or ['point'] or ['point', 'orient', 'scale'] etc             
                **kwargs        : weight(w=1), maintainOffset(mo=1), remove(rm=1), targetList(tl=1), weightAliasList(wal=1), name(n='_PointCon'), e=1, q=1
                if kwargs not given:
                        kwargs ={'mo': 1, 'w':1}
                        
                Usage:
                ------
                Ex1: >>> conList =hsN.constrainTo('object02', 'orient')         #_ If no kwargs, kwargs ={'mo'=1, 'w':1}
                                 # Result: [u'object02_OrientCon']
                Ex2: >>> conList =hsN.constrainTo(['object02', 'object03'], ['orient', 'point'])  
                                 # Result: [u'object02_OrientCon', u'object02_OrientCon', u'object03_PointCon', u'object03_PointCon']
                                 
                Returns:
                --------
                if len(conList) > 1:                                    
                        return conNodeList      
                else:
                        return conNodeList[0]
                """
        ncTypes = 'mesh|curv|jnt|trans|^comp|^shp'
        if not kwargs:
            kwargs = {'mo':1, 'w':1}
        srcName = self.name()
        objList = [objList] if type(objList) != list else objList
        conList = [conList] if type(conList) != list else conList
        cmds.select(cl=1)
        if set(['point', 'parent']).issubset(conList):
            self._confirmAction("You cann't apply \n'point' and 'parent' constraints at a time", raiseErr=True)
        if set(['orient', 'parent']).issubset(conList):
            self._confirmAction("You cann't apply \n'orient' and 'parent' constraints at a time", raiseErr=True)
        if set(['point', 'orient', 'parent']).issubset(conList):
            self._confirmAction("You cann't apply \n'point', 'orient' and 'parent' constraints at a time", raiseErr=True)
        conNodeList = []
        queryList = []
        objList = [str(obj) for obj in objList]
        for conType in conList:
            for obj in objList:
                if conType == 'parent':
                    conNode = (cmds.parentConstraint)(obj, (self.name()), **kwargs)[0]
                else:
                    if conType == 'orient':
                        conNode = (cmds.orientConstraint)(obj, (self.name()), **kwargs)[0]
                    elif conType == 'point':
                        conNode = (cmds.pointConstraint)(obj, (self.name()), **kwargs)[0]
                    elif conType == 'scale':
                        conNode = (cmds.scaleConstraint)(obj, (self.name()), **kwargs)[0]
                    elif conType == 'aim':
                        conNode = (cmds.aimConstraint)(obj, (self.name()), **kwargs)[0]
                    elif conType == 'poleVector':
                        conNode = (cmds.poleVectorConstraint)(obj, (self.name()), **kwargs)[0]
                    else:
                        if conType == 'poleVector' or conType == 'orient':
                            conNode.setAttr('interpType', 2)
                    asConNode = hsNode(conNode)
                    if conType == 'parent' or conType == 'orient':
                        asConNode.setAttr('interpType', 2)
                if asConNode not in conNodeList:
                    conNodeList.append(asConNode)

        return conNodeList

    def isConnected(self, attrName):
        conList = self.connectionInfo(attrName, sfd=1)
        if conList:
            return True
        return False

    def isConstrained(self, byTrgtList=None, constrainList=None):
        trgtList = []
        if byTrgtList:
            trgtList = [byTrgtList] if type(byTrgtList) != list else byTrgtList
        testList = []
        if not constrainList:
            constrainList = self.mConstrain(q=1)
        else:
            conList = [constrainList] if type(constrainList) != list else constrainList
            constrainList = []
            for conName in conList:
                conList = self.mConstrain(conName, q=1)
                if conList:
                    constrainList.extend(conList)

        if constrainList:
            for conName in constrainList:
                if not trgtList:
                    if self.mConstrain(conName, q=1):
                        testList.append(True)
                    else:
                        testList.append(False)
                else:
                    for trgt in trgtList:
                        tList = self.mConstrain(conName, q=1, tl=1)
                        if tList:
                            if trgt in tList:
                                testList.append(True)
                            else:
                                testList.append(False)

        else:
            testList.append(False)
        return all(testList)

    def mDistance_Vtx(self, src, dest):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp|^shp'
        srcPos = cmds.xform(src, q=1, ws=1, t=1)
        destPos = cmds.xform(dest, q=1, ws=1, t=1)
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        return mDist

    def distanceTo_BB(self, sel02):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp|^shp'
        posA = cmds.xform((self.name()), q=1, ws=1, bb=1)
        posB = cmds.xform(sel02, q=1, ws=1, bb=1)
        xVal_A = (posA[0] + posA[3]) / 2.0
        yVal_A = (posA[1] + posA[4]) / 2.0
        zVal_A = (posA[2] + posA[5]) / 2.0
        xVal_B = (posB[0] + posB[3]) / 2.0
        yVal_B = (posB[1] + posB[4]) / 2.0
        zVal_B = (posB[2] + posB[5]) / 2.0
        arg01 = xVal_A - xVal_B
        arg02 = yVal_A - yVal_B
        arg03 = zVal_A - zVal_B
        distBB = math.sqrt(arg01 * arg01 + arg02 * arg02 + arg03 * arg03)
        return distBB

    def unfreezeTrans(self):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^comp|^shp'
        init_Pos = self.getPos()
        self.setPos([0, 0, 0])
        self.freeze(t=1, r=1, s=1)
        self.setPos(init_Pos)
        self.select()

    def selectSiblings(self, srRange=None, fromEnd=True, skipCount=0, selectNodes=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        sibList = self.parent().getChildren(type='transform')
        nodesList = []
        if srRange:
            if not self.extractNum():
                return
            (slNum, slNumStr) = self.extractNum(fromEnd, skipCount)[0:2]
            fillStr = '%0.' + str(len(slNumStr)) + 'd'
            nextName = self.asObj()
            nodesList.append(nextName)
            if not nextName.hasUniqueName():
                self._confirmAction('"%s" Is Not Unique Name ..!' % nextName.name())

    def getAllNodes(srRange, slNum, selectNodes=True):
        nodesList = []
        if srRange > slNum:
            nextName, nextNum = _nextVar(nextName, fromEnd, skipCount)
            if cmds.objExists(nextName) and nextNum <= srRange and nextName in sibList:
                nextName = hsNode(nextName)
                nodesList.append(nextName)
                nodesList.extend(getAllNodes(nextName, fromEnd, skipCount, nodesList))
        elif srRange < slNum:
            nextName, nextNum = _preVar(nextName, fromEnd, skipCount)
            if cmds.objExists(nextName) and nextNum >= srRange and nextName in sibList:
                nextName = hsNode(nextName)
                nodesList.append(nextName)
                nodesList.extend(getAllNodes(nextName, fromEnd, skipCount, nodesList))
        else:
            nodesList = [hsNode(obj) for obj in sibList]
        if selectNodes:
            cmds.select(nodesList, r=1)
        return [nodesList, len(nodesList)]

    def selectSeries(self, srRange=None, fromEnd=True, skipCount=0, selectNodes=True):
        """
                if fromEnd == True, search from end else search from start
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        extractedNum = self.extractNum(fromEnd, skipCount)
        if extractedNum:
            (slNum, slNumStr) = extractedNum[0:2]
        else:
            self._confirmAction("%s doesn't have 'Series Number'" % self.name())
            self.select(r=1)
            return
        fillStr = '%0.' + str(len(slNumStr)) + 'd'
        if not self.extractNum():
            return
        nodesList = []
        if srRange:
            nextName = self.asObj()
            nodesList.append(nextName)
            if not nextName.hasUniqueName():
                self._confirmAction('"%s" Is Not Unique Name ..!' % nextName.name())

    def getAllNodes(srRange, slNum, selectNodes=True):
        nodesList = []
        if srRange > slNum:
            nextName, nextNum = _nextVar(nextName, fromEnd, skipCount)
            if cmds.objExists(nextName) and nextNum <= srRange and nextName in sibList:
                nextName = hsNode(nextName)
                nodesList.append(nextName)
                nodesList.extend(getAllNodes(nextName, fromEnd, skipCount, nodesList))
        elif srRange < slNum:
            nextName, nextNum = _preVar(nextName, fromEnd, skipCount)
            if cmds.objExists(nextName) and nextNum >= srRange and nextName in sibList:
                nextName = hsNode(nextName)
                nodesList.append(nextName)
                nodesList.extend(getAllNodes(nextName, fromEnd, skipCount, nodesList))
        else:
            hsN = self.shortName()
            numList = re.findall(r'\d+', hsN)
            numRange = list(range(len(numList)))
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                patternStr = r'[^0-9]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += r'[^0-9]*'
                reObj = re.search(patternStr, hsN)
                spanRange = reObj.span(len(numList) - 1 * skipCount)
                cmds.select((hsN[0:spanRange[0]] + '*' + hsN[spanRange[1]:]), r=1)
                nodesList = [hsNode(obj) for obj in cmds.ls(sl=1) if re.search(patternStr, obj)]
            else:
                numStr = numList[skipCount]
                patternStr = r'[^0-9]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += r'[^0-9]*'
                reObj = re.search(patternStr, hsN)
                spanRange = reObj.span(skipCount + 1)
                cmds.select((hsN[0:spanRange[0]] + '*' + hsN[spanRange[1]:]), r=1)
                nodesList = [hsNode(obj) for obj in cmds.ls(sl=1) if re.search(patternStr, obj)]
        if selectNodes:
            cmds.select(nodesList, r=1)
        return [nodesList, len(nodesList)]

    def prefixHI(self, prefix, topSelect=True, selectHI=True):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^shp|^comp'
        finalList = []
        self.select(r=1)
        if selectHI:
            cmds.select(hi=1)
        if not topSelect:
            self.select(d=1)
        if self._selected():
            allNodes = self._selected()
            allNodes.reverse()
            for node in allNodes:
                node.rename(prefix + hsNode.name(node))

            allNodes.reverse()
            finalList.append(allNodes)
        select(finalList, r=1)
        return finalList

    def unfreezeRotation(self, grpLevel, vtxNumOrObj, trgtType='vtx'):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|^shp|^comp'
        obj = self.name()
        self.select()
        self._refreshView(1)
        if grpLevel == 0:
            extGrp = self.asObj()
            objGrp = self.pickWalkUp()
        elif grpLevel == 1:
            (extGrp, objGrp) = self.pickWalkUp(2)
        elif grpLevel == 2:
            (topGrp, extGrp, objGrp) = self.pickWalkUp(3)
        extGrpPos = self.getPos(extGrp)
        dirLoc = om.spaceLocator(p=(0, 0, 0), n='dir_Loc')
        vtxLoc = om.spaceLocator(p=(0, 0, 0), n='vtx_Loc')
        destPos = self.getPos(obj)
        if trgtType == 'obj':
            self.snapTo_Obj(vtxLoc, vtxNumOrObj)
            om.parent(vtxLoc, obj)
        om.select(extGrp, r=1)
        cmds.move(0, 0, 0, rpr=1)
        self.mFreeze(extGrp)
        if trgtType == 'vtx':
            try:
                self.snapTo_Vtx(vtxLoc, obj + '.vtx[' + str(vtxNumOrObj) + ']')
            except:
                self.snapTo_Vtx(vtxLoc, obj + '.cv[' + str(vtxNumOrObj) + ']')

            aimCon = om.aimConstraint(vtxLoc, dirLoc, weight=1, upVector=(0, 1, 0), worldUpType='vector', offset=(0,0,0), aimVector=(0,0,-1), worldUpVector=(0,1,0))
            finalRot = om.xform(dirLoc, q=1, ws=1, ro=1)
            if trgtType == 'obj':
                om.parent(vtxLoc, w=1)
        om.parent(extGrp, dirLoc)
        dirLoc.setAttr('rotate', 0, 0, 0, type='double3')
        om.parent(extGrp, w=1)
        extGrp.select()
        self.mFreeze(extGrp)
        extGrp.setAttr('rotate', (finalRot[0]), (finalRot[1]), (finalRot[2]), type='double3')
        cmds.select(extGrp, r=1)
        cmds.move((destPos[0]), (destPos[1]), (destPos[2]), rpr=1)
        cmds.parent(extGrp, objGrp)
        cmds.delete(dirLoc)
        cmds.delete(vtxLoc)

    def selectHI(self, objType='jnt', topSelect=True, includeShapes=False, childImplied=1):
        """
                Objective:
                ----------
                Selects all objects of given type or other than given type under the given object
                
                Return Statement:
                ----------------
                return hsN._selected()          
                """
        ncTypes = 'mesh|curv|jnt|trans|^shp|^comp'
        if objType == 'jnt' or objType == 'joint' or objType == '^jnt' or objType == '^joint':
            nType = 'joint'
        elif objType == 'crv' or objType == 'curv' or objType == 'nurbsCurve' or objType == '^crv' or objType == '^curv' or objType == '^nurbsCurve':
            nType = 'nurbsCurve'
        elif objType == 'mesh' or objType == 'obj' or objType == '^mesh' or objType == '^obj':
            nType = 'mesh'
        else:
            nType = objType
        self.select(r=1)
        cmds.select(hi=1)
        selList = self._selected()
        if childImplied:
            asObj = self.asObj()
            if asObj.attributeQuery('mChd', n=(asObj.name()), ex=1):
                if asObj.attributeQuery('mChd', n=(asObj.name()), at=1) == 'message':
                    impliedList = asObj.child().selectHI()
                    select(selList, impliedList, r=1)
                if objType.startswith('^'):
                    for node in ls(sl=1):
                        if nodeType(node) == nType:
                            if nodeType(node) == 'joint':
                                cmds.select(node, tgl=1)
                            if nodeType(node) == nType:
                                if not not nodeType(node) == 'nurbsCurve':
                                    if nodeType(node) == 'mesh':
                                        pass
                                    cmds.select(node, tgl=1)
                                    node = hsNode(node)
                                    cmds.select((node.parent()), tgl=1)

                else:
                    for node in ls(sl=1):
                        if nodeType(node) != nType:
                            cmds.select(node, tgl=1)

                if not topSelect:
                    self.select(d=1)
            if nType == 'joint':
                return list(map(hsNode, cmds.ls(sl=1)))
        if not objType.startswith('^'):
            if nType == 'nurbsCurve' or nType == 'mesh':
                if not includeShapes:
                    pickWalk(d='up')
                else:
                    for obj in ls(sl=1):
                        obj = hsNode(obj)
                        select((obj.parent()), add=1)

                return list(map(hsNode, cmds.ls(sl=1)))
            return list(map(hsNode, cmds.ls(sl=1)))

    def searchReplaceHI(self, searchWord, replaceWord, topSelect=True, selectHI=True):
        """
                Objective:
                ----------
                Search and replaces the words under the given object
                
                Return Stmnt:
                -------------
                return allNodes  #_ All nodes with replaced / renamed words under given obj.    
                """
        ncTypes = 'mesh|curv|jnt|trans'
        finalList = []
        self.select(r=1)
        if selectHI:
            select(hi=1)
        if not topSelect:
            self.select(d=1)
        allNodes = hsN.selected()
        allNodes.reverse()
        for node in allNodes:
            renameWord = node.name().replace(searchWord, replaceWord)
            try:
                node.rename(renameWord)
            except:
                pass

        allNodes.reverse()
        finalList.extend(allNodes)
        select(finalList, r=1)
        return finalList

    def shapeCtrl(self, trgt):
        """ 
                Args:
                -----
                shapeObj or hsNode : nurbs ctrl
                trgt : cluster or joint
                """
        ncTypes = 'mesh|curv|jnt|trans|shp|^comp'
        shapeObj = self.name()
        ctrlName = PyNode(shapeObj).name()
        shapeNode = PyNode(shapeObj).getShape()
        if PyNode(trgt).getShape():
            shapeType == 1
            select(shapeObj, r=1)
            makeIdentity(apply=True, s=1, r=1, t=1, n=0)
        else:
            shapeType = 0
        parent(shapeNode, trgt, r=1, shape=1)
        trgtShape = PyNode(trgt).getShape()
        if shapeType == 1:
            trgtShape.setAttr('lodVisibility', 0)
        else:
            trgtShape.setAttr('lodVisibility', 1)
        delete(shapeObj)
        rename(trgt, ctrlName)

    def nextVar(self, fromEnd=True, skipCount=0, versionUpAll=False):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp'
        hsN = self.shortName()
        if not versionUpAll:
            numList = re.findall('\\d+', self.shortName())
            numRange = list(range(len(numList)))
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                lenStr = len(numStr)
                nextNum = int(numStr) + 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

                reObj = re.search(patternStr, self.shortName())
                spanRange = reObj.span(len(numList) - 1 * skipCount)
                nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
                if objExists(nextName):
                    try:
                        nextName = hsNode(nextName)
                    except:
                        pass

                    return [nextName, nextNum]
                numStr = numList[skipCount]
                lenStr = len(numStr)
                nextNum = int(numStr) + 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

            reObj = re.search(patternStr, self.shortName())
            spanRange = reObj.span(skipCount + 1)
            nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
            if objExists(nextName):
                try:
                    nextName = hsNode(nextName)
                except:
                    pass

                return [nextName, nextNum]
        else:

            def repMGrp(mObj):
                numVal = int(mObj.group())
                formNum = len(mObj.group())
                formVar = '%0.' + str(formNum) + 'd'
                return str(formVar % (numVal + 1))

            nextName = re.sub('\\d+', repMGrp, self.shortName())
            if objExists(nextName):
                return hsNode(nextName)
            return nextName

    def nextSeriesNode(self, fromEnd=True, skipCount=0, versionUpAll=False):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp'
        hsN = self.shortName()
        if not self.extractNum():
            return
        if not versionUpAll:
            numList = re.findall('\\d+', hsN)
            numRange = list(range(len(numList)))
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                lenStr = len(numStr)
                nextNum = int(numStr) + 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

                reObj = re.search(patternStr, hsN)
                spanRange = reObj.span(len(numList) - 1 * skipCount)
                nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
                if objExists(nextName):
                    try:
                        nextName = hsNode(nextName)
                    except:
                        pass

                    return nextName
                return
            else:
                numStr = numList[skipCount]
                lenStr = len(numStr)
                nextNum = int(numStr) + 1
                nextNumStr = ('%0.' + str(lenStr) + 'd') % nextNum
                patternStr = '[^\\d+]*'
                for num in numRange:
                    patternStr += '(\\d+)'
                    patternStr += '[^\\d+]*'

                reObj = re.search(patternStr, self.shortName())
                spanRange = reObj.span(skipCount + 1)
                nextName = hsN[0:spanRange[0]] + nextNumStr + hsN[spanRange[1]:]
                if objExists(nextName):
                    try:
                        nextName = hsNode(nextName)
                    except:
                        pass

                    return nextName
                return
        else:

            def repMGrp(mObj):
                numVal = int(mObj.group())
                formNum = len(mObj.group())
                formVar = '%0.' + str(formNum) + 'd'
                return str(formVar % (numVal + 1))

            nextName = re.sub('\\d+', repMGrp, self.shortName())
            if objExists(nextName):
                try:
                    nextName = hsNode(nextName)
                except:
                    pass

                return nextName
            return

    def dupeNVersionUp(self):
        """doc"""
        ncTypes = 'mesh|curv|jnt|trans|shp'
        topGrp = self.name()
        select(topGrp, r=1)
        duplicate(rr=1)
        dupGrp = selected()[0]
        select(hi=1)
        allNodes = selected()
        allNodes.reverse()
        for node in allNodes:
            node = hsNode(node)
            splitList = str.split(str(node), '|')
            nextName = node.nextVar()[0]
            try:
                node.rename(nextName)
            except:
                continue

        dupGrp.rename(hsNode.stripNum(dupGrp))

    def deleteAttr(self, attrList):
        """
                attrList =[attrList] if type(attrList) != list else attrList
                """
        ncTypes = 'mesh|curv|jnt|trans'
        attrList = [attrList] if type(attrList) != list else attrList
        for attrName in attrList:
            self.setAttr(attrName, e=1, l=0)
            deleteAttr((self.name()), attribute=attrName)

    def duplicate(self, centerPiv=False, grpLevel=0, **kwargs):
        """
                Returns:
                --------
                if grpLevel:
                        dupGrp =dupNode.grpIt(dupNode, grpLevel)[-1]
                        return [dupNode, dupGrp]
                else:
                        return [hsNode(dupNode)]                
                """
        ncTypes = 'mesh|curv|jnt|trans|shp'
        if 'n' not in kwargs:
            kwargs['n'] = self.nextUniqueName()
        if 'rr' not in kwargs:
            kwargs['rr'] = True
        srcNode = self.name()
        cmds.select(srcNode, r=1)
        dupNode = hsNode((cmds.duplicate)(**kwargs)[0])
        if centerPiv:
            self.centerPivot(dupNode)
        if grpLevel:
            dupGrp = dupNode.grpIt(grpLevel)[-1]
            return [dupNode, dupGrp]
        return [dupNode]

    def _about_hsNode(self):
        if window('hsNodeCreditsWin', ex=1):
            cmds.deleteUI('hsNodeCreditsWin')
        window('hsNodeCreditsWin', s=False, rtf=1, t='as_hsNode_v1.5 Credits..', wh=(320,500), mxb=0, mnb=0)
        frameLayout(l='', bs='in')
        columnLayout(adj=5)
        text('\n**hsNode_v1.5**\n', fn='boldLabelFont')
        text('About :', fn='boldLabelFont', align='left')
        separator(st='single', h=10, w=25)
        text('Author: Yogesh Nichal')
        text('Rigging Artist & Programmer')
        text(l='')
        text('Visit :', fn='boldLabelFont', align='left')
        separator(st='single', h=10)
        text('http://www.yogeshnichal.com')
        text(l='')
        text('Contact :', fn='boldLabelFont', align='left')
        separator(st='single', h=10)
        text('Mail Id: yogeshnichal@gmail.com')
        text(l='')
        text('Copyright (c) as_hsNode :', fn='boldLabelFont', align='left')
        separator(st='single', h=10)
        text('** Yogesh Nichal. All Rights Reserved. **')
        text(l='')
        text('Validity', fn='boldLabelFont', align='left')
        separator(st='single', h=10)
        text('** Life Time **')
        text(l='')
        button(l='<< Close >>', c="cmds.deleteUI('hsNodeCreditsWin')")
        separator(st='single', h=10, w=25)
        window('hsNodeCreditsWin', e=1, wh=(320, 375))
        showWindow('hsNodeCreditsWin')
        self._refreshView(5)
        pause(sec=5)
        cmds.deleteUI('hsNodeCreditsWin')

loc = cmds.spaceLocator()[0]
hsN = hsNode(loc)
hsN.deleteNode()
om.MGlobal.displayInfo('hsNode activated...!')