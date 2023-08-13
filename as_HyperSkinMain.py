import subprocess, xml.etree.ElementTree, time
import maya.cmds as cmds
import maya.mel as mel
import webbrowser as web, gc, hsNode, importlib
importlib.reload(hsNode)
import hsNode as hsN
from hsNode import *
import pymel.core as pm
from pymel.all import *
from pymel.core import *
try:
    import as_eSkinMain as eSkin
except:
    pass

from uuid import getnode
import shutil
if int(str(cmds.about(v=1))[0:4]) < 2025:
    from maya.OpenMaya import *
    import maya.OpenMaya as om
    import maya.api.OpenMaya as om2
    import maya.OpenMayaAnim as oma
else:
    import maya.OpenMaya as om
import sys, os, math, re, pprint, socket
from hsNode import hsNode  # Import the hsNode function from the hsNode module
import as_HyperSkinMain as hsN
from maya.cmds import *
from maya.mel import *
import datetime as dt
import maya.cmds as mc
import random as rand, json
import pymel.core as pm
from pymel.all import *
from pymel.core import *

class as_HyperSkinMain(object):
    __slots__ = ['_limit2Ver', 'path', 'skinShapes', 'fileName']

    def __init__(self, filePath=None):
        """
                " Hyper Speed Skinning" based on "Art & Technology" Combination
                                                
                **as_HyperSkinMain_v4.2**
                
                About :         
                --------------------------------        
                Author: Yogesh Nichal
                Character Rigging Artist & Programmer

                """
        cmds.softSelect(e=1, softSelectEnabled=0)
        if cmds.currentUnit(q=1, linear=1) != 'centimeter':
            cmds.currentUnit(linear='centimeter')
        else:
            self.path = filePath
            self.skinShapes = {}
            self.fileName = None
            if self.path:
                self.updateSkinWeights(self.path)
            _limit2Ver = [2018, 2019, 2020, 2022, 2024]
            _checkMayaVersion = 1
            if _checkMayaVersion:
                if self._mayaVer() in _limit2Ver:
                    pass
                else:
                    self._as_HyperSkinMain__confirmAction('This tool is compiled only for Maya {0}!!'.format(str(_limit2Ver)))
                    raise RuntimeError('This tool is compiled only for Maya {0}!!'.format(str(_limit2Ver)))

    def checkInAHSSUsers(self):
        pass

    def changeOptions_AdvancedGCMs(self):
        advanceCheck = True
        if advanceCheck:
            radioButton('as_SnapType01_RB', e=1, l='Internal')
            radioButton('as_SnapType02_RB', e=1, l='External')
        else:
            radioButton('as_SnapType01_RB', e=1, l='Radial')
            radioButton('as_SnapType02_RB', e=1, l='Nearest')

    def as_PruneOppJntWeights(self):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 1
        _as_HyperSkinMain__displayTotalTime = 0
        _as_HyperSkinMain__freeVersion = 0
        if _as_HyperSkinMain__freeVersion:
            HyperSkin.restrictedZone_FreeTool()
        HyperSkin.startTime(_as_HyperSkinMain__displayTotalTime)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
        if not ls(sl=1):
            (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        else:
            selList = selected()
            if selList:
                skinMesh = selList[0]
            if HyperSkin.isSkinned(skinMesh):
                skinClust = listHistory(skinMesh, type='skinCluster')[0]
            else:
                HyperSkin.error('Selected Mesh Is Not Skinned !!')
        all_InfList = [jnt for jnt in skinCluster(skinClust, inf=1, q=1) if nodeType(jnt) == 'joint']
        skinJntList = list(map(hsNode, all_InfList))
        vtxList_R = HyperSkin.getMeshVtx(skinMesh, 'R_', 'x', False)
        vtxList_L = HyperSkin.getMeshVtx(skinMesh, 'L_', 'x', True)
        [cmds.setAttr(jnt + '.liw', 0) for jnt in skinJntList]
        if prefixOrSuffix == 'Prefix':
            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList if jnt.startswith(R_Prfx)]
        else:
            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList if jnt.endsswith(R_Prfx)]
        HyperSkin.startProgressWin(vtxList_L, 'Pruning Opp. Weights (LH)', rv=1)
        for vtx in vtxList_L:
            HyperSkin.progressWin(vtx)
            valList = skinPercent(skinClust, vtx, q=1, v=1)
            for num in range(len(valList)):
                if prefixOrSuffix == 'Prefix':
                    if valList[num] > 0.0 and skinJntList[num].startswith(R_Prfx):
                        skinPercent(skinClust, vtx, tv=(skinJntList[num], 0.0))
                    else:
                        if valList[num] > 0.0:
                            if skinJntList[num].endswith(R_Prfx):
                                skinPercent(skinClust, vtx, tv=(skinJntList[num], 0.0))

        HyperSkin.endProgressWin(vtxList_L, 1)
        [cmds.setAttr(jnt + '.liw', 0) for jnt in skinJntList]
        if prefixOrSuffix == 'Prefix':
            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList if jnt.startswith(L_Prfx)]
        else:
            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList if jnt.endsswith(L_Prfx)]
        HyperSkin.startProgressWin(vtxList_R, 'Pruning Opp. Weights (RH)', rv=1)
        for vtx in vtxList_R:
            HyperSkin.progressWin(vtx)
            valList = skinPercent(skinClust, vtx, q=1, v=1)
            for num in range(len(valList)):
                if prefixOrSuffix == 'Prefix':
                    if valList[num] > 0.0 and skinJntList[num].startswith(L_Prfx):
                        skinPercent(skinClust, vtx, tv=(skinJntList[num], 0.0))
                    else:
                        if valList[num] > 0.0:
                            if skinJntList[num].endswith(L_Prfx):
                                skinPercent(skinClust, vtx, tv=(skinJntList[num], 0.0))

        HyperSkin.endProgressWin(vtxList_R, 1)
        [cmds.setAttr(jnt + '.liw', 0) for jnt in skinJntList]

    def as_HyperSkin(self):
        skinMesh = None
        try:
            skinMesh = textField('as_SkinMesh_TF', q=1, tx=1)
        except:
            pass

        selList = hsN.selected()
        self.as_AboutHyperSkin()
        try:
            deleteUI('as_HyperSkinWin')
        except:
            pass

        try:
            uiName = loadUI(v=0, uiFile='D:/My_Scripts/as_Scripts/as_QtPS/as_HyperSkinMain.ui')
        except:
            try:
                uiName = loadUI(v=0, uiFile=(internalVar(usd=1) + 'as_QtPS/as_HyperSkinMain.ui'))
            except:
                uiName = loadUI(v=0, uiFile=(internalVar(uad=1) + 'scripts/as_QtPS/as_HyperSkinMain.ui'))

        showWindow(uiName)
        checkBox('as_ExtractGCMs_CB', e=1, onCommand="button('as_ExtractGCMs_PB', e=1, l='Extract Proxy');button('as_HyperSmooth_PB', e=1, l='Finalize Proxy')", offCommand="button('as_ExtractGCMs_PB', e=1, l='Hyper Skin');button('as_HyperSmooth_PB', e=1, l='Hyper Smooth')")
        HyperSkin.refreshView(1)
        HyperSkin.updateUI_Options()
        cmds.popupMenu('as_TransferSkinHSS_PM', p='as_TransferSkinHSS_BTN')
        cmds.menuItem('as_TransferSkinHSS_MI', l='Transfer >> Skin', c='HyperSkin.transferSkinning()', image='circlePoly.png', en=1)
        cmds.menuItem('as_TransferSkinHSS2_MI', l='Copy >> Skin (Nearest Point & Joints)', c='HyperSkin.transferSkinning(tt=1)', image='circlePoly.png', en=1)
        cmds.popupMenu('as_EasySmooth_PM', p='as_EasySmooth_BTN')
        cmds.menuItem('as_EasySmooth_MI', l='Smooth >> Edge Loops', c='HyperSkin.smoothEdgeLoops()', image='circlePoly.png', en=1)
        cmds.popupMenu('as_SelectVerticesHSS_PM', p='as_MirrorGCMs_PB_3')
        cmds.menuItem('as_SelectVerticesHSS1_MI', l='Select >> Side Vertices', c='HyperSkin.selectSkinVertices("L_")', image='circlePoly.png', en=1)
        cmds.menuItem('as_SelectVerticesHSS2_MI', l='Delete >> Edge Loops', c='HyperSkin.deleteEdgeLoops()', image='circlePoly.png', en=1)
        cmds.menuItem('as_SelectVerticesHSS3_MI', l='Insert >> Edge Loops', c='cmds.SplitEdgeRingToolOptions()', image='circlePoly.png', en=1)
        cmds.menuItem('as_SelectVerticesHSS4_MI', l='Get >> Visualize Volume', c='HyperSkin.getVisVolume()', image='circlePoly.png', en=1)
        cmds.popupMenu('as_SelectSkinJntsHSS_PM', p='as_GetSkinJnts_PB')
        cmds.menuItem('as_SelectSkinJntsHSS1_MI', l='Select >> Weighted Influences', c='HyperSkin.selectSkinJnts(1)', image='circlePoly.png', en=1)
        if selList:
            if selList[0].isSkinMesh():
                selList[0].select()
                HyperSkin.add_SkinMesh('as_SkinMesh_TF')
        elif skinMesh:
            if objExists(skinMesh):
                skinMesh = hsNode(skinMesh)
                if skinMesh.isSkinMesh():
                    skinMesh.select()
                    HyperSkin.add_SkinMesh('as_SkinMesh_TF')

    def getNearestObj(self, srcObj, destList, srcType='obj', destType='obj', nearCount=1):
        distanceDict = {}
        for destObj in destList:
            dist = HyperSkin.mDistance(srcObj, destObj, srcType, destType)[0]
            distanceDict[destObj] = dist

        distObjList = HyperSkin.sortByDict(distanceDict)
        select((distObjList[0:nearCount]), r=1)
        if nearCount == 1:
            return distObjList[0]
        return distObjList[0:nearCount]

    def getRootJnt_FromJntsList(self, jntList=None):
        if not jntList:
            jntList = hsN.selected()
        jntList = list(map(hsNode, jntList))
        rootJnt = jntList[0]
        a = 1
        for jnt in jntList[:-1]:
            if jnt.isParentOf(jntList[a]):
                rootJnt = jnt
            else:
                if jntList[a].isParentOf(rootJnt):
                    rootJnt = jntList[a]
                a += 1

        jntList.remove(rootJnt)
        noRoot = False
        for jnt in jntList:
            if not rootJnt.isParentOf(jnt):
                noRoot = True

        if noRoot:
            return
        return rootJnt

    def nearestVtx_OnMesh(self, srcObjOrPos='srcObjOrPos', trgtMesh='trgtMesh', excludeList=None, skipDir=None, precision=1):
        """
                Returns:
                --------
                return [hsNode(nVtx), int(nNum)]
                """
        hsN = hsNode(trgtMesh)
        srcPos = hsNode(srcObjOrPos).getPos() if type(srcObjOrPos) != list else srcObjOrPos
        fnMesh = MFnMesh(hsN._MDagPath())
        refPnt = MPoint(srcPos[0], srcPos[1], srcPos[2])
        nPnt = MPoint(0.0, 0.0, 0.0)
        sUtil = MScriptUtil()
        polyNum = sUtil.asIntPtr()
        try:
            fnMesh.getClosestPoint(refPnt, nPnt, MSpace.kWorld, polyNum)
        except:
            mVec = om.MVector()
            fnMesh.getClosestPointAndNormal(refPnt, nPnt, mVec, MSpace.kWorld, polyNum)
            del mVec

        faceNum = sUtil.getInt(polyNum)
        select(trgtMesh + '.f[' + str(faceNum) + ']')
        mel.ConvertSelectionToVertices()
        if precision >= 10:
            precision = 10
        else:
            precision = abs(precision)
        if precision:
            for num in range(precision):
                GrowPolygonSelectionRegion()

        vtxList = [str(vtx) for vtx in filterExpand(sm=31)]
        remList = []
        if excludeList:
            excludeList = [excludeList] if type(excludeList) != list else excludeList
            for vtx in vtxList:
                asVtx = hsNode(vtx)
                if asVtx.extractNum()[0] in excludeList:
                    remList.append(vtx)
                    if asVtx.extractNum()[0] == 1993:
                        probVtx = asVtx

        if remList:
            for remVtx in remList:
                vtxList.remove(remVtx)

        if vtxList:
            nVtx = hsNode(HyperSkin.getNearestObj(srcObjOrPos, vtxList, 'vtx', 'vtx'))
        else:
            return
        reObj = re.search('\\[(\\d+)\\]', nVtx)
        if reObj:
            vtxNum = int(reObj.group(1))
        else:
            vtxNum = 0
        return [nVtx, vtxNum]

    def getNearestGeoList02(self, vtx, geoList, numGeos=1):
        """
            To Get Nearest Geos from given geometries From Vtx Using om2
        
            Args:
                vtx (str): The vertex (in the format 'pCube1.vtx[0]') from which to find the nearest geometries.
                geoList (list): List of geometries as strings or MObjects.
                numGeos (int): Number of nearest geometries to return in order [nearestOne, next1, next2, etc].
        
            Returns:
                tuple: Tuple containing two lists:
                    1) List of nearest geometry names.
                    2) List of nearest geometry MObjects.
            """
        vtx_selectionList = om2.MSelectionList()
        vtx_selectionList.add(vtx)
        (vtx_dagPath, vtx_component) = vtx_selectionList.getComponent(0)
        vtx_iter = om2.MItMeshVertex(vtx_dagPath)
        vtx_index = om2.MFnSingleIndexedComponent(vtx_component).element(0)
        vtx_iter.setIndex(vtx_index)
        vtx_point = vtx_iter.position(space=(om2.MSpace.kWorld))
        distances = []
        for geo in geoList:
            pivot_point = om2.MPoint(cmds.xform(geo, query=True, worldSpace=True, rotatePivot=True))
            distance = vtx_point.distanceTo(pivot_point)
            distances.append((geo, distance))

        distances.sort(key=(lambda x: x[1]))
        nearest_geos = [geo[0] for geo in distances[:numGeos]]
        nearest_mobjs = []
        for geo in nearest_geos:
            selectionList = om2.MSelectionList()
            selectionList.add(geo)
            nearest_mobjs.append(selectionList.getDependNode(0))

        cmds.select(nearest_geos, replace=True)
        return [
         nearest_geos, nearest_mobjs]

    def nearestVtxOnMesh_vtxList(self, srcObjOrPos='srcObjOrPos', trgtMesh='trgtMesh', excludeList=None, skipDir=None, precision=1, vtxList=None):
        """
                Returns:
                --------
                return [hsNode(nVtx), int(nNum)]
                """
        trgtMesh = hsNode(trgtMesh)
        srcPos = hsNode(srcObjOrPos).getPos() if type(srcObjOrPos) != list else srcObjOrPos
        fnMesh = MFnMesh(trgtMesh._MDagPath())
        refPnt = MPoint(srcPos[0], srcPos[1], srcPos[2])
        nPnt = MPoint(0.0, 0.0, 0.0)
        sUtil = MScriptUtil()
        polyNum = sUtil.asIntPtr()
        try:
            fnMesh.getClosestPoint(refPnt, nPnt, MSpace.kWorld, polyNum)
            faceNum = sUtil.getInt(polyNum)
            select(trgtMesh + '.f[' + str(faceNum) + ']')
        except:
            if vtxList:
                nVtx = HyperSkin.getNearestObj(srcObjOrPos, vtxList, 'obj', 'vtx')
                cmds.select(nVtx, r=1)
                return [nVtx]
            else:
                HyperSkin.confirmAction('First Method Failed !!\nUse Lip Vertices Method !!', True)

        mel.ConvertSelectionToVertices()
        if precision >= 10:
            precision = 10
        else:
            precision = abs(precision)
        if precision:
            for num in range(precision):
                GrowPolygonSelectionRegion()

        vtxList = [str(vtx) for vtx in filterExpand(sm=31)]
        remList = []
        if excludeList:
            excludeList = [excludeList] if type(excludeList) != list else excludeList
            for vtx in vtxList:
                asVtx = hsNode(vtx)
                if asVtx.extractNum()[0] in excludeList:
                    remList.append(vtx)
                    if asVtx.extractNum()[0] == 1993:
                        probVtx = asVtx

        if remList:
            for remVtx in remList:
                vtxList.remove(remVtx)

        if vtxList:
            nVtx = hsNode(HyperSkin.getNearestObj(srcObjOrPos, vtxList, 'vtx', 'vtx'))
        else:
            return
        reObj = re.search('\\[(\\d+)\\]', nVtx)
        if reObj:
            vtxNum = int(reObj.group(1))
        else:
            vtxNum = 0
        return [nVtx, vtxNum]

    def move2ClosestPoint(self, loc, mesh):
        """Note: Mesh should be freezed for correct snapping"""
        softSelect(softSelectEnabled=False, e=1)
        nameCPOM = str(createNode('closestPointOnMesh', n='closestPoint'))
        locPos = xform(loc, q=1, ws=1, t=1)
        setAttr((nameCPOM + '.inPosition'), (locPos[0]), (locPos[1]), (locPos[2]), type='double3')
        setAttr(nameCPOM + '.isHistoricallyInteresting', 1)
        connectAttr(mesh + '.worldMatrix[0]', nameCPOM + '.inputMatrix')
        connectAttr(mesh + '.worldMesh', nameCPOM + '.inMesh')
        meshPosX = getAttr(nameCPOM + '.positionX')
        meshPosY = getAttr(nameCPOM + '.positionY')
        meshPosZ = getAttr(nameCPOM + '.positionZ')
        select(loc, r=1)
        cmds.move(meshPosX, meshPosY, meshPosZ, rpr=1)
        delete(nameCPOM)

    def getSkinJnts(self, skinMesh, allInfs=False):
        skinClust = listHistory(skinMesh, type='skinCluster')
        if skinClust:
            skinClust = skinClust[0]
        else:
            HyperSkin.confirmAction('Skin Cluster Not Found On %s' % str(skinMesh), True)
        if allInfs:
            jntList = list(map(hsNode, skinCluster(skinClust, q=1, inf=1)))
            return jntList
        return skinCluster(skinClust, q=1, wi=1)

    def getCVList(self, curv, get_asNodes=0, getEditPoints=0, **shArgs):
        """
                Returns(asNodes):
                -----------------
                if self.isNodeType('nurbsCurve'):
                        return [cvList, numCVs]
                elif self.isNodeType('mesh'):                   
                        return [vtxList, numVtx]
                elif self.isNodeType('nurbsSurface'):
                        return [cvList, numCVs]                                                         
                """
        ncTypes = 'mesh|curv|^comp'
        if shArgs:
            get_asNodes = shArgs['gan'] if 'gan' in shArgs else get_asNodes
            getEditPoints = shArgs['gep'] if 'gep' in shArgs else getEditPoints
        curv = hsNode(curv)
        if getEditPoints:
            curvShp = curv.shape()
            numSpans = int(curvShp.getAttr('spans'))
            numEPs = numSpans + 1
            vtxList = [curv.name() + '.ep[' + str(num) + ']' for num in range(numEPs)]
            if get_asNodes:
                vtxList = list(map(hsNode, vtxList))
            return [vtxList, numEPs]
        curvFn = MFnNurbsCurve(curv._MDagPath())
        numCVs = curvFn.numCVs()
        if curvFn.form() == 3:
            numCVs = numCVs - curvFn.degree()
        cvList = [curv.name() + '.cv[' + str(num) + ']' for num in range(numCVs)]
        if get_asNodes:
            cvList = list(map(hsNode, cvList))
        cmds.select(cvList, r=1)
        return [cvList, numCVs]

    def getMeshVtx(self, meshObj, sidePos=None, mirrAxis='x', includeMidVtx=True):
        if type(meshObj) != list:
            select(meshObj, r=1)
            try:
                select((MeshVertex(meshObj)), r=1)
                allVtx = filterExpand(sm=31)
            except:
                allVtx = HyperSkin.getCVList(meshObj)[0]

            mel.eval('changeSelectMode -object')
            select(meshObj, r=1)
            SelectVertexMask()
            select(allVtx, r=1)
        elif type(meshObj) == list:
            if '.vtx[' in meshObj[0]:
                allVtx = meshObj
                meshShape = hsNode(cmds.ls((meshObj[0]), o=1)[0])
                meshObj = meshShape.parent()
            else:
                return meshObj
        else:
            return meshObj
        if not sidePos:
            return allVtx
        sideVtxList = []
        for vtx in allVtx:
            posList = HyperSkin.getPos(vtx, 'vtx')[0]
            if mirrAxis == 'x':
                axisVal = posList[0]
            if mirrAxis == 'y':
                axisVal = posList[1]
            if mirrAxis == 'z':
                axisVal = posList[2]
            if includeMidVtx:
                if axisVal >= -0.001:
                    if sidePos == 'L_':
                        sideVtxList.append(vtx)
                if axisVal <= 0.001 and sidePos == 'R_':
                    sideVtxList.append(vtx)
                else:
                    if axisVal >= 0.001:
                        if sidePos == 'L_':
                            sideVtxList.append(vtx)
                        if axisVal <= -0.001:
                            if sidePos == 'R_':
                                sideVtxList.append(vtx)

        if type(meshObj) != list:
            mel.eval('changeSelectMode -object')
        select(meshObj, r=1)
        SelectVertexMask()
        cmds.select(cl=1)
        select(sideVtxList, r=1)
        return filterExpand(sm=31)

    def hasMeshContainsPos(self, checkMesh, checkPointOrObj):
        mesh = om2.MGlobal.getSelectionListByName(checkMesh).getDagPath(0)
        vtxPos = om2.MPoint()
        if type(checkPointOrObj) == list:
            checkPoint = checkPointOrObj
        elif cmds.objExists(checkPointOrObj):
            checkPointOrObj = hsNode(checkPointOrObj)
            checkPoint = checkPointOrObj.getPos()
        checkPoint = om2.MPoint(checkPoint[0], checkPoint[1], checkPoint[2])
        closest_point = om2.MPointOnMesh()
        mesh_fn = om2.MFnMesh(mesh)
        (closest_vec, _) = mesh_fn.getClosestNormal(checkPoint, om2.MSpace.kWorld)
        (closest_point, _) = mesh_fn.getClosestPoint(checkPoint, om2.MSpace.kWorld)
        if closest_vec * (checkPoint - closest_point) >= 0:
            return False
        return True

    def hasMeshContainsPoint(self, checkMesh, checkPointOrObj, precision=5):
        checkMesh = hsNode(checkMesh)
        checkPoint = [0, 0, 0]
        if type(checkPointOrObj) == list:
            checkPoint = checkPointOrObj
        elif cmds.objExists(checkPointOrObj):
            checkPointOrObj = hsNode(checkPointOrObj)
            checkPoint = checkPointOrObj.getPos()
        checkPoint = [round(checkPoint[0], precision), round(checkPoint[1], precision), round(checkPoint[2], precision)]
        if not pluginInfo('nearestPointOnMesh', q=1, l=1):
            if catch((lambda: loadPlugin('nearestPointOnMesh'))):
                mel.error('Plugin "nearestPointOnMesh.mll" could not be found')
            else:
                loadPlugin('nearestPointOnMesh')
        validPoly = 0
        if checkMesh.isMesh():
            if checkMesh.isShape():
                checkMeshShapes = [checkMesh]
                validPoly = 1
            elif checkMesh.hasShape():
                checkMeshShapes = [checkMesh.shape()]
                validPoly = 1
            if not validPoly:
                mel.error('Mel procedure "pointIsInsideMesh": The input object is not, or does not have exactly one child which is a polygon mesh')
            fnMesh = om.MFnMesh(checkMesh._MDagPath())
            refPnt = MPoint(checkPoint[0], checkPoint[1], checkPoint[2])
            vClosestPoint = MPoint(0.0, 0.0, 0.0)
            sUtil = MScriptUtil()
            polyNum = sUtil.asIntPtr()
            vClosestNormal = om.MVector()
            fnMesh.getClosestPointAndNormal(refPnt, vClosestPoint, vClosestNormal, MSpace.kWorld, polyNum)
            vCheckPoint = om.MVector(checkPoint[0], checkPoint[1], checkPoint[2])
            vClosestPoint = om.MVector(vClosestPoint[0], vClosestPoint[1], vClosestPoint[2])
            vPointsRay = vClosestPoint - vCheckPoint
            projMag = vPointsRay * vClosestNormal
            if projMag >= 0:
                return True
            return False

    def getMeshVtx_Overlap(self, outerMesh, innerMesh, checkType='in', inMeshDir='L_', outMeshDir='L_', outTolerance=None):
        """
                Args:
                outerMesh = mesh placed outer side with respect to innerMesh [For Ex: part of pant on top of shoe]
                innerMesh = mesh placed inside with respect to outerMesh [For Ex: part of shoe inside the pant]
                checkType = 'in' or 'In' | 'out' or 'Out'       
                                        ['in' --> innerMesh vertices (overlapped) will be returned]
                                        ['out' --> outerMesh vertices (overlapped) will be returned]
                innerMeshDir = 'L_' | 'R_' | None
                outerMeshDir = 'L_' | 'R_' | None
                outTolerance = None | any number        
                """
        if checkType.lower() == 'in':
            innerVtxList = HyperSkin.getMeshVtx(innerMesh, inMeshDir)
            innerVtxList = list(map(hsNode, innerVtxList))
            overlapList = []
            HyperSkin.startProgressWin(len(innerVtxList))
            for vtx in innerVtxList:
                HyperSkin.progressWin('Getting Inner Overlapped Vtx !!')
                if HyperSkin.hasMeshContainsPoint(outerMesh, vtx):
                    overlapList.append(vtx)

            HyperSkin.endProgressWin(len(innerVtxList), 1)
            if overlapList:
                cmds.select(overlapList, r=1)
                return overlapList
            return
        elif checkType.lower() == 'out':
            outerVtxList = HyperSkin.getMeshVtx(outerMesh, outMeshDir)
            outerVtxList = list(map(hsNode, outerVtxList))
            overlapList = []
            HyperSkin.startProgressWin(len(outerVtxList))
            for vtx in outerVtxList:
                HyperSkin.progressWin('Getting Outer Overlapped Vtx !!')
                loc = vtx.getPosLoc()[0]
                outerMesh.mConstrain(loc, 'normal', aimVector=[0, 1, 0])[0].delete()
                locPos = loc.getPos()
                loc.translateBy([0, -0.001, 0])
                closestPos = HyperSkin.getClosestPos_Dir(vtx.getPos(), loc, innerMesh, False)
                if closestPos:
                    if outTolerance:
                        mDist = HyperSkin.mDistance(locPos, closestPos)
                        if mDist <= outTolerance:
                            overlapList.append(vtx)
                    else:
                        overlapList.append(vtx)
                loc.delete()

            HyperSkin.endProgressWin(len(outerVtxList), 1)
            if overlapList:
                cmds.select(overlapList, r=1)
                return overlapList
            return

    def getMeshFn(self, obj):
        pathDg = HyperSkin.getMPathDg(obj)
        meshFn = MFnMesh()
        meshFn.setObject(pathDg)
        return meshFn

    def old_getMPoint(self, obj):
        pathDg = HyperSkin.getMPathDg(obj)
        transFn = MFnTransform()
        transFn.setObject(pathDg)
        objPos = transFn.rotatePivot(MSpace.kWorld)
        return MPoint(objPos[0], objPos[1], objPos[2])

    def getMPoint(self, objOrPos):
        if type(objOrPos) != list:
            pathDg = HyperSkin.getMPathDg(objOrPos)
            transFn = MFnTransform()
            transFn.setObject(pathDg)
            objPos = transFn.rotatePivot(MSpace.kWorld)
        else:
            objPos = objOrPos
        return MPoint(objPos[0], objPos[1], objPos[2])

    def getClosestPos_Dir(self, posLoc, dirLoc, meshObj, giveLoc=True):
        posPnt = HyperSkin.getMPoint(posLoc)
        try:
            dirPnt = HyperSkin.getMPoint(dirLoc)
            dirPos = [round(dirPnt.x, 3), round(dirPnt.y, 3), round(dirPnt.z, 3)]
        except:
            dirLoc = hsNode(dirLoc)
            dirPos = dirLoc.getPos()

        pX, pY, pZ = round(posPnt.x, 3), round(posPnt.y, 3), round(posPnt.z, 3)
        (dX, dY, dZ) = dirPos
        dirVec = MVector(dX - pX, dY - pY, dZ - pZ)
        pArray = MPointArray()
        meshFn = HyperSkin.getMeshFn(meshObj)
        posExists = meshFn.intersect(posPnt, dirVec, pArray, 0.0, MSpace.kWorld)
        select(cl=1)
        if posExists:
            if giveLoc:
                destPos = pArray[0]
                destLoc = spaceLocator(p=(0, 0, 0))
                cmds.move((destPos.x), (destPos.y), (destPos.z), rpr=1)
                return destLoc
            destPos = pArray[0]
            return [destPos.x, destPos.y, destPos.z]
        else:
            return

    def getClosestDist_Obj(self, vtxName, meshObj):
        nameCPOM = str(createNode('closestPointOnMesh', n='closestPoint'))
        locPos = xform(vtxName, q=1, ws=1, t=1)
        setAttr((nameCPOM + '.inPosition'), (locPos[0]), (locPos[1]), (locPos[2]), type='double3')
        setAttr(nameCPOM + '.isHistoricallyInteresting', 1)
        connectAttr(meshObj + '.worldMatrix[0]', nameCPOM + '.inputMatrix')
        connectAttr(meshObj + '.worldMesh', nameCPOM + '.inMesh')
        endPos = getAttr(nameCPOM + '.position')
        srcPos = xform(vtxName, q=1, ws=1, t=1)
        distX = endPos[0] - srcPos[0]
        distY = endPos[1] - srcPos[1]
        distZ = endPos[2] - srcPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        delete(nameCPOM)
        return mDist

    def getMPathDg(self, obj):
        select(obj, r=1)
        pathDg = om.MDagPath()
        activList = om.MSelectionList()
        if HyperSkin._mayaVer() < 2025:
            om.MGlobal.getActiveSelectionList(activList)
            activList.getDagPath(0, pathDg)
        else:
            activList = om.MGlobal.getActiveSelectionList()
            pathDg = activList.getDagPath(0)
        return pathDg

    def getMBBox(self, bbObj):
        pathDg = HyperSkin.getMPathDg(bbObj)
        dagNodeFn = MFnDagNode()
        dagNodeFn.setObject(pathDg)
        nodeBB = dagNodeFn.boundingBox()
        return nodeBB

    def checkPosIn_BB(self, pos, bbObj):
        bbNode = HyperSkin.getMBBox(bbObj)
        mPnt = MPoint(pos[0], pos[1], pos[2])
        return bbNode.contains(mPnt)

    def message(self, messageTxt):
        """
                Sends a given message through confirmDialog window
                """
        confirmDialog(title='Message ..!', message=messageTxt, button=['Yes'], defaultButton='Yes')

    def mapRange(self, inputVal, minIN, maxIN, minOUT, maxOUT):
        """
                Now Supports inverted / reverse out put range where maxOUT is less than minOUT
                
                Examples:
                Normal Range:
                =============
                HyperSkin.mapRange(0.95,  0.90, 1.65,  0.50, 0.99)  #_ [0.95, [0.90 -> 1.65], [0.50 -> 0.99]]
                HyperSkin.mapRange(0.95,  0.90, 1.65,  0.50, 0.99)  # 0.5326
                HyperSkin.mapRange(1.60,  0.90, 1.65,  0.50, 0.99)  # 0.9573    
                HyperSkin.mapRange(inputVal=1.60,  minIN=0.9, maxIN=1.65,  minOUT=0.5, maxOUT=0.99)
                
                Inverse In Range:
                =================
                HyperSkin.mapRange(0.95,  1.65, 0.90,  0.50, 0.99)  # 0.9573
                HyperSkin.mapRange(1.60,  1.65, 0.90,  0.50, 0.99)  # 0.5326                            
                HyperSkin.mapRange(inputVal=1.60,  minIN=1.65, maxIN=0.90,  minOUT=0.50, maxOUT=0.99)
                                
                Inverse Out Range:
                ==================
                HyperSkin.mapRange(0.95,  0.90, 1.65,  0.99, 0.50)  # 0.9573
                HyperSkin.mapRange(1.60,  0.90, 1.65,  0.99, 0.50)  # 0.5326
                HyperSkin.mapRange(inputVal=0.95,  minIN=0.90, maxIN=1.65,  minOUT=0.99, maxOUT=0.5)
                HyperSkin.mapRange(inputVal=1.60,  minIN=0.90, maxIN=1.65,  minOUT=0.99, maxOUT=0.5)
                
                Inverse In & Out Ranges:
                ========================
                HyperSkin.mapRange(0.95,  1.65, 0.90,  0.99, 0.50)  #_ 0.5326
                HyperSkin.mapRange(1.60,  1.65, 0.90,  0.99, 0.50)  #_ 0.9573
                
                """
        if maxOUT > minOUT:
            outRange = maxOUT - minOUT
        elif minOUT > maxOUT:
            outRange = minOUT - maxOUT
        else:
            outRange = 0.0
        if maxIN > minIN:
            inRange = maxIN - minIN
        elif minIN > maxIN:
            inRange = minIN - maxIN
        else:
            inRange = 0.0
        if inRange:
            if maxIN > minIN:
                valScaled = float(inputVal - minIN) / float(inRange)
            else:
                valScaled = float(inputVal - maxIN) / float(inRange)
        else:
            valScaled = float(inputVal - minIN) / 0.0001
        if maxIN > minIN:
            if maxOUT > minOUT:
                outVal = minOUT + valScaled * outRange
            else:
                outVal = minOUT - valScaled * outRange
        elif minIN > maxIN:
            if maxOUT > minOUT:
                outVal = maxOUT - valScaled * outRange
            else:
                outVal = maxOUT + valScaled * outRange
        else:
            outVal = minOUT
        if maxOUT > minOUT:
            if outVal > maxOUT:
                outVal = maxOUT
            elif outVal < minOUT:
                outVal = minOUT
        elif outVal < maxOUT:
            outVal = maxOUT
        elif outVal > minOUT:
            outVal = minOUT
        return outVal

    def get_NormLoc(self, obj_Piv, obj_Vec1, obj_Vec2, locName='Norm_Loc', giveLoc=True):
        vec01 = HyperSkin.get_2PosVect(obj_Piv, obj_Vec1)
        vec02 = HyperSkin.get_2PosVect(obj_Piv, obj_Vec2)
        normVect = vec01 ^ vec02
        normLoc = spaceLocator(n=locName)
        cmds.move((normVect.x), (normVect.y), (normVect.z), rpr=1)
        select(cl=1)
        stJnt = joint(p=(0, 0, 0), n='Start_Jnt')
        endJnt = joint(p=(0, 0, 0), n='End_Jnt')
        HyperSkin.snapTo_Obj(endJnt, normLoc)
        HyperSkin.snapTo_Obj(stJnt, obj_Piv)
        HyperSkin.snapTo_Obj(normLoc, endJnt)
        delete(stJnt)
        if giveLoc == True:
            return normLoc
        extnPos = xform(normLoc, q=1, ws=1, t=1)
        delete(normLoc)
        return extnPos

    def get_ClosestGeoLoc(self, loc, mesh, locName='Geo_Loc', giveLoc=True):
        """Note: Mesh should be freezed for correct snapping"""
        nameCPOM = str(createNode('closestPointOnMesh', n='closestPoint'))
        locPos = xform(loc, q=1, ws=1, t=1)
        setAttr((nameCPOM + '.inPosition'), (locPos[0]), (locPos[1]), (locPos[2]), type='double3')
        setAttr(nameCPOM + '.isHistoricallyInteresting', 1)
        connectAttr(mesh + '.outMesh', nameCPOM + '.inMesh')
        meshPosX = getAttr(nameCPOM + '.positionX')
        meshPosY = getAttr(nameCPOM + '.positionY')
        meshPosZ = getAttr(nameCPOM + '.positionZ')
        geoLoc = spaceLocator(p=(0, 0, 0), n=locName)
        cmds.move(meshPosX, meshPosY, meshPosZ, rpr=1)
        delete(nameCPOM)
        if giveLoc == True:
            return geoLoc
        locPos = xform(geoLoc, q=1, ws=1, t=1)
        delete(geoLoc)
        return locPos

    def get_2PosVect(self, srcObj, destObj):
        activeList = MSelectionList()
        transFn = MFnTransform()
        pathDg = MDagPath()
        obj = MObject()
        select(srcObj, r=1)
        select(destObj, add=1)
        MGlobal.getActiveSelectionList(activeList)
        activeList.getDependNode(1, obj)
        pathDg.getAPathTo(obj, pathDg)
        transFn.setObject(pathDg)
        destPos = transFn.rotatePivot(MSpace.kWorld)
        activeList.getDependNode(0, obj)
        pathDg.getAPathTo(obj, pathDg)
        transFn.setObject(pathDg)
        srcPos = transFn.rotatePivot(MSpace.kWorld)
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        return MVector(distX, distY, distZ)

    def get_2PosExtn(self, sel01, sel02, ratioAmount, locName='Extn_Loc', getLoc=True):
        select(cl=1)
        stJnt = joint(p=(0, 0, 0), n='Start_Jnt')
        endJnt = joint(p=(0, 0, 0), n='End_Jnt')
        HyperSkin.snapTo_Obj(stJnt, sel01)
        HyperSkin.snapTo_Obj(endJnt, sel02)
        select(stJnt, r=1)
        cmds.move(0, 0, 0, rpr=1)
        dirVect = HyperSkin.get_2PosVect(stJnt, endJnt)
        initLoc = spaceLocator(n='Init_Pos')
        HyperSkin.snapTo_Obj(initLoc, endJnt)
        endLoc = spaceLocator()
        endPos = [num * (ratioAmount + 1) for num in dirVect]
        select(endLoc, r=1)
        cmds.move((endPos[0]), (endPos[1]), (endPos[2]), rpr=1)
        HyperSkin.snapTo_Obj(stJnt, initLoc)
        HyperSkin.snapTo_Obj(endJnt, endLoc)
        HyperSkin.snapTo_Obj(stJnt, sel02)
        HyperSkin.snapTo_Obj(endLoc, endJnt)
        delete(initLoc)
        delete(stJnt)
        if getLoc == True:
            rename(endLoc, locName)
            return endLoc
        extnPos = xform(endLoc, q=1, ws=1, t=1)
        delete(endLoc)
        return extnPos

    def isMesh(self, obj):
        boolMesh = False
        obj = PyNode(obj)
        if obj.getShape():
            objShape = obj.getShape()
            if nodeType(objShape) == 'mesh':
                boolMesh = True
            return boolMesh

    def isSkinned(self, obj):
        asObj = hsNode(obj)
        if not asObj.isMesh():
            return False
        skinClust = asObj.listHistory(type='skinCluster')
        if not skinClust:
            return False
        return True

    def isJnt(self, obj):
        obj = PyNode(obj)
        if nodeType(obj) == 'joint':
            return True
        return False

    def snapTo_Vtx(self, srcList, vtx=[0, 0, 0]):
        """
                Args:
                -----
                srcList  = srcObj | srcObjList (list of srcObjs)
                """
        srcList = [srcList] if type(srcList) != list else srcList
        for srcObj in srcList:
            if type(vtx) != list:
                posB = xform(vtx, q=1, ws=1, t=1)
                rpB = xform(vtx, q=1, rp=1)
                rpA = xform(srcObj, q=1, rp=1)
                snapX = posB[0] + rpB[0] - rpA[0]
                snapY = posB[1] + rpB[1] - rpA[1]
                snapZ = posB[2] + rpB[2] - rpA[2]
                select(srcObj, r=1)
                cmds.move(snapX, snapY, snapZ, rpr=1)
            else:
                select(srcObj, r=1)
                cmds.move((vtx[0]), (vtx[1]), (vtx[2]), rpr=1)

    def unfreezeRotation(self, objList, grpLevel, vtxNumOrObj, trgtType='vtx'):
        objList = [objList] if type(objList) != list else objList
        for obj in objList:
            select(obj, r=1)
            HyperSkin.refreshView(2)
            if grpLevel == 0:
                extGrp = selected()[0]
                pickWalk(d='up')
                objGrp = selected()[0]
            elif grpLevel == 1:
                pickWalk(d='up')
                extGrp = selected()[0]
                pickWalk(d='up')
                objGrp = selected()[0]
            elif grpLevel == 2:
                pickWalk(d='up')
                topGrp = selected()[0]
                pickWalk(d='up')
                extGrp = selected()[0]
                pickWalk(d='up')
                objGrp = selected()[0]
            extGrpPos = HyperSkin.getPos(extGrp)[0]
            dirLoc = spaceLocator(p=(0, 0, 0), n='dir_Loc')
            vtxLoc = spaceLocator(p=(0, 0, 0), n='vtx_Loc')
            destPos = HyperSkin.getPos(obj)[0]
            if trgtType == 'obj':
                HyperSkin.snapTo_Obj(vtxLoc, vtxNumOrObj)
                parent(vtxLoc, obj)
            select(extGrp, r=1)
            cmds.move(0, 0, 0, rpr=1)
            HyperSkin.mFreeze(extGrp)
            if trgtType == 'vtx':
                try:
                    HyperSkin.snapTo_Vtx(vtxLoc, obj + '.vtx[' + str(vtxNumOrObj) + ']')
                except:
                    HyperSkin.snapTo_Vtx(vtxLoc, obj + '.cv[' + str(vtxNumOrObj) + ']')

                aimCon = aimConstraint(vtxLoc, dirLoc, weight=1, upVector=(0, 1,0), worldUpType='vector', offset=(0,0,0), aimVector=(0,0,-1), worldUpVector=(0,1,0))
                finalRot = xform(dirLoc, q=1, ws=1, ro=1)
                if trgtType == 'obj':
                    parent(vtxLoc, w=1)
                else:
                    parent(extGrp, dirLoc)
                    dirLoc.setAttr('rotate', 0, 0, 0, type='double3')
                    parent(extGrp, w=1)
                    extGrp.select(r=1)
                    HyperSkin.mFreeze(extGrp)
                    extGrp.setAttr('rotate', (finalRot[0]), (finalRot[1]), (finalRot[2]), type='double3')
                    select(extGrp, r=1)
                    cmds.move((destPos[0]), (destPos[1]), (destPos[2]), rpr=1)
                    parent(extGrp, objGrp)
                    delete(dirLoc)
                    delete(vtxLoc)

    def startTime(self, runCompute=True):
        """
                This function needs to be initiated to use 'HyperSkin.computeTime()'
                """
        global _as_HyperSkinMain__start_Time
        if not runCompute:
            return
        _as_HyperSkinMain__start_Time = timerX()
        om.MGlobal.displayInfo('Started the time for "Total time calculation ..!!"')
        HyperSkin.refreshView(1)

    def old_startProgressWin(self, numObjs, winTitle='Please Wait ..!', progressNote='Progress : 0%', doInterrupt=True, useProgress=1, **shArgs):
        global myProgressBar
        global progressAddValue
        global progressHour
        global progressListSize
        global progressMinute
        global progressSecond
        global progressValue
        global startTm
        if shArgs:
            numObjs = shArgs['no'] if 'no' in shArgs else numObjs
            winTitle = shArgs['wt'] if 'wt' in shArgs else winTitle
            progressNote = shArgs['pn'] if 'pn' in shArgs else progressNote
            doInterrupt = shArgs['di'] if 'di' in shArgs else doInterrupt
            useProgress = shArgs['up'] if 'up' in shArgs else useProgress
        if not useProgress:
            return
        if type(numObjs) == list:
            numObjs = len(numObjs)
        startTm = timerX()
        progressListSize = numObjs
        progressAddValue = 100.0 / progressListSize
        progressValue = 0.0
        progressHour = 0
        progressMinute = 0
        progressSecond = 0
        if window('as_myProgressWin', exists=1):
            deleteUI('as_myProgressWin', window=1)
        with window('as_myProgressWin', sizeable=1, ip=1, mnb=1, mxb=0, wh=(330, 90), t=winTitle) as progressWin:
            with columnLayout(co=('left', 10), rs=10):
                with frameLayout('as_myProgressFL', collapsable=1, borderVisible=1, labelVisible=1, li=0, h=75, w=310, label='Total No Of Items : %d' % numObjs, marginWidth=5, marginHeight=5):
                    with columnLayout(rs=5):
                        with rowColumnLayout(nc=1, cw=[(1, 295)]):
                            cmds.text('as_myProgressTxt', l=progressNote, align='left')
                            myProgressBar = cmds.progressBar('as_myProgressBar', maxValue=100, width=295, h=25, pr=0, ii=doInterrupt, imp=True)
        window('as_myProgressWin', e=1, wh=(330, 90))

    def startProgressWin(self, numObjs=0, winTitle=None, progressNote=None, doInterrupt=True, innerObjs=None, innerList=None, refreshView=0, useProgress=1, innerNote='Inner Progress', **shArgs):
        """
                Usage (If inner loop exist):
                HyperSkin.startProgressWin(jntList_outer, 'Solving Joints !!', 'Please Wait', innerObjs=vtxList_someList)
                        HyperSkin.startProgressWin(innerList=vtxList_inner)
                                HyperSkin.progressWin(ci=vtx, innerList=vtxList_inner, ep=0, spt=__showProgressTime)
                        HyperSkin.progressWin(ci=jnt)
                HyperSkin.endProgressWin(jntList, 1)    
                """
        global myProgressBar
        global progressAddValue
        global progressHour
        global progressListSize
        global progressMinute
        global progressSecond
        global progressValue
        global startTm
        global topProgressAddValue
        global topProgressBar
        global topProgressHour
        global topProgressListSize
        global topProgressMinute
        global topProgressSecond
        global topProgressValue
        global topStartTm
        if shArgs:
            numObjs = shArgs['no'] if 'no' in shArgs else numObjs
            winTitle = shArgs['wt'] if 'wt' in shArgs else winTitle
            progressNote = shArgs['pn'] if 'pn' in shArgs else progressNote
            doInterrupt = shArgs['di'] if 'di' in shArgs else doInterrupt
            innerObjs = shArgs['io'] if 'io' in shArgs else innerObjs
            innerList = shArgs['il'] if 'il' in shArgs else innerList
            refreshView = shArgs['rv'] if 'rv' in shArgs else refreshView
            useProgress = shArgs['up'] if 'up' in shArgs else useProgress
        if not useProgress:
            return
        if innerList:
            cmds.text('as_topProgressTxt', e=1, l=('Progress : %0.1f' % 0.0))
            cmds.progressBar(topProgressBar, edit=1, progress=0)
            topStartTm = timerX()
            if type(innerList) == list:
                innerList = len(innerList)
            topProgressListSize = innerList
            topProgressAddValue = 100.0 / topProgressListSize
            topProgressValue = 0.0
            topProgressHour = 0
            topProgressMinute = 0
            topProgressSecond = 0
            return
        if type(numObjs) == list:
            numObjs = len(numObjs)
        if not winTitle:
            winTitle = 'Please Wait ..!'
        if not progressNote:
            progressNote = 'Progress : 0%'
        startTm = timerX()
        progressListSize = numObjs
        progressAddValue = 100.0 / progressListSize
        progressValue = 0.0
        progressHour = 0
        progressMinute = 0
        progressSecond = 0
        if innerObjs:
            if type(innerObjs) == list:
                innerObjs = len(innerObjs)
            topStartTm = timerX()
            topProgressListSize = innerObjs
            topProgressAddValue = 100.0 / topProgressListSize
            topProgressValue = 0.0
            topProgressHour = 0
            topProgressMinute = 0
            topProgressSecond = 0
        if window('as_myProgressWin', exists=1):
            deleteUI('as_myProgressWin', window=1)
        if innerObjs:
            winH = 170
            winW = 330
            frameH = 150
            frameW = 310
        else:
            frameH = 150
            frameW = 310
            winH = 90
            winW = 330
        with window('as_myProgressWin', sizeable=1, ip=1, mnb=1, mxb=0, wh=(winW, winH), t=winTitle) as progressWin:
            with columnLayout(co=('left', 10), rs=10):
                with frameLayout('as_myProgressFL', collapsable=1, borderVisible=1, labelVisible=1, li=0, h=frameH / 2.0, w=frameW, label='Total No Of Items : %d' % numObjs, marginWidth=5, marginHeight=5):
                    with columnLayout(rs=5):
                        with rowColumnLayout(nc=1, cw=[(1, 295)]):
                            cmds.text('as_myProgressTxt', l=progressNote, align='left')
                            myProgressBar = cmds.progressBar('as_myProgressBar', maxValue=100, width=295, h=25, pr=0, ii=doInterrupt, imp=True)
            if innerObjs:
                with frameLayout('as_topProgressFL', collapsable=1, borderVisible=1, labelVisible=1, li=0, h=frameH / 2.0, w=frameW, label='Total No Of Items : %d' % innerObjs, marginWidth=5, marginHeight=5):
                    with columnLayout(rs=5):
                        with rowColumnLayout(nc=1, cw=[(1, 295)]):
                            cmds.text('as_topProgressTxt', l=innerNote, align='left')
                            topProgressBar = cmds.progressBar('as_topProgressBar', maxValue=100, width=295, h=25, pr=0, ii=doInterrupt, imp=True)
        window('as_myProgressWin', e=1, wh=(winW, winH))
        if refreshView:
            HyperSkin.refreshView(1)

    def sortByDict(self, dictName, sortType='up', returnType='keys'):
        """
                HyperSkin.sortedByDict({'j1':10, 'j2':2, 'j3':-1.0, 'j4':50.0, 'j5':0, 'j6':10}, 'up')
                
                """
        if type(dictName) != dict:
            raise RuntimeError('"%s" is not dictionary ..!' % str(dictName))
        valList = list(dictName.values())
        shiftToKeys = False
        for val in valList:
            if not type(val) == int:
                if type(val) == float:
                    continue
                else:
                    shiftToKeys = True
                    break

        if shiftToKeys:
            valList = list(dictName.keys())
            for val in valList:
                if not type(val) == int:
                    if type(val) == float:
                        continue
                    else:
                        raise RuntimeError('"%s" is neither "int" nor "float" value ..!' % str(val))

        for testNum in range(len(valList)):
            nextNum = testNum
            for val in valList[testNum:]:
                if sortType == 'up':
                    if valList[testNum] > val:
                        tempNum = valList[testNum]
                        valList[testNum] = val
                        valList[nextNum] = tempNum
                elif sortType == 'down' or sortType == 'dn':
                    if valList[testNum] < val:
                        tempNum = valList[testNum]
                        valList[testNum] = val
                        valList[nextNum] = tempNum
                    nextNum += 1

        if returnType == 'keys':
            keyList = []
            for val in valList:
                for keyName in list(dictName.keys()):
                    if val == dictName[keyName]:
                        if keyName not in keyList:
                            keyList.append(keyName)
                            break

            return keyList
        if returnType == 'values':
            return valList

    def snapTo_Obj(self, srcObjList, destObj=[0, 0, 0], snapRot=False):
        """
                Args:
                -----
                srcObjList  = srcObj | srcObjList (list of srcObjs)
                destObj = destObj | destPos[0, 1, 0]
                
                if snapRot : Snaps srcObj's rotation to destObj  #_ destObj needs to be given
                """
        srcList = [srcObjList] if type(srcObjList) != list else srcObjList
        if type(destObj) != list:
            destObj = hsNode(destObj)
            destPos = destObj.getPos()
        elif len(destObj) == 3:
            destPos = destObj
        for srcObj in srcList:
            select(srcObj, r=1)
            cmds.move((destPos[0]), (destPos[1]), (destPos[2]), rpr=1)

        if snapRot:
            if type(destObj) != list:
                asObj = hsNode(srcObj)
                asObj.snapRotTo(destObj)

    def snapRot(self, src, destObj, dirUpObj=None, aimAxis=[1, 0, 0], upAxis=[0, 1, 0]):
        """
                src  = src or srcList | obj or objList
                
                More features:
                --------------
                Aim Constraint can be used while snapping rotaion of src
                """
        srcList = [src] if type(src) != list else src
        if not dirUpObj:
            for src in srcList:
                oriCon = orientConstraint(destObj, src, weight=1)
                rVal = list(getAttr(src + '.r'))
                delete(oriCon)
                setAttr((src + '.r'), (rVal[0]), (rVal[1]), (rVal[2]), type='double3')

        else:
            for src in srcList:
                aimCon = aimConstraint(destObj, src, weight=1, upVector=upAxis, worldUpObject=str(dirUpObj), worldUpType='object', offset=(0,0,0), aimVector=aimAxis)
                rVal = list(getAttr(src + '.r'))
                delete(aimCon)
                setAttr((src + '.r'), (rVal[0]), (rVal[1]), (rVal[2]), type='double3')

    def snapPiv_Obj(self, srcObj, destObj=[0, 0, 0]):
        if type(destObj) != list:
            destPos = HyperSkin.getPos(destObj)[0]
        else:
            destPos = destObj
        cmds.move(destPos[0], destPos[1], destPos[2], srcObj + '.scalePivot', srcObj + '.rotatePivot')

    def scaleTillInsideMesh(self, srcObj, cvList, trgtMesh, stepVal=0.01, scaleDir='y'):
        """
                HP.adjustTillInsideMesh('L_Palm_HndCtrl', 'L_Palm_Curve_5_HndCtrl', 'body', stepVal=-0.001, action='scale')
                """
        srcObj = hsNode(srcObj)
        if scaleDir == 'x':
            srcObj.scaleBy([1 + stepVal, 1, 1], False, True)
        elif scaleDir == 'y':
            srcObj.scaleBy([1, 1 + stepVal, 1], False, True)
        elif scaleDir == 'z':
            srcObj.scaleBy([1, 1, 1 + stepVal], False, True)
        else:
            srcObj.scaleBy([1 + stepVal, 1 + stepVal, 1 + stepVal], False, True)
        allTests = []
        for cv in cvList:
            allTests.append(HyperSkin.hasMeshContainsPoint(trgtMesh, cv))

        scaleNext = False
        if not all(allTests):
            if scaleDir == 'x':
                srcObj.scaleBy([1 - stepVal, 1, 1], False, True)
            elif scaleDir == 'y':
                srcObj.scaleBy([1, 1 - stepVal, 1], False, True)
            elif scaleDir == 'z':
                srcObj.scaleBy([1, 1, 1 - stepVal], False, True)
            else:
                srcObj.scaleBy([1 - stepVal, 1 - stepVal, 1 - stepVal], False, True)
            return True
        scaleNext = True
        HyperSkin.startProgressWin(10000, 'Please Wait')
        a = 0
        while scaleNext:
            if scaleDir == 'x':
                srcObj.scaleBy([1 + stepVal, 1, 1], False, True, False)
            elif scaleDir == 'y':
                srcObj.scaleBy([1, 1 + stepVal, 1], False, True, False)
            elif scaleDir == 'z':
                srcObj.scaleBy([1, 1, 1 + stepVal], False, True, False)
            else:
                srcObj.scaleBy([1 + stepVal, 1 + stepVal, 1 + stepVal], False, True, False)
            HyperSkin.progressWin('Adjusting Scale !!', 0, 1)
            if a % 100 == 0:
                if stepVal == 0.001:
                    srcObj.select()
                    HyperSkin.refreshView(1)
                    if a % 10 == 0:
                        if stepVal == 0.01:
                            srcObj.select()
                            HyperSkin.refreshView(1)
                        if stepVal == 1:
                            srcObj.select()
                            HyperSkin.refreshView(1)
                        allTests = []
                        for cv in cvList:
                            allTests.append(HyperSkin.hasMeshContainsPoint(trgtMesh, cv))

                        if not all(allTests):
                            break
                        else:
                            scaleNext = True
                        a += 1

        HyperSkin.endProgressWin(100, True)

    def scaleDisc_AfterImportAttrs(self, trgtMesh='body'):
        def unhideNodes(nodeList):
            nodeList = [nodeList] if type(nodeList) != list else nodeList
            for node in [hsNode(obj) for obj in nodeList]:
                node.setAttr('v', lock=0, channelBox=1, keyable=1)
                if node.isMesh():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 0)
                    nodeShape.setAttr('lodVisibility', 1)
                    nodeShape.setAttr('visibility', 1)
                    nodeShape.setAttr('template', 0)
                    nodeShape.setAttr('displayVertices', 0)
                    nodeShape.setAttr('displayUVs', 0)
                if node.isCurv():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 0)
                    nodeShape.setAttr('lodVisibility', 1)
                    nodeShape.setAttr('visibility', 1)
                    nodeShape.setAttr('template', 0)
                    nodeShape.setAttr('overrideEnabled', 0)
                    nodeShape.setAttr('overrideDisplayType', 0)
                    nodeShape.setAttr('overrideLevelOfDetail', 0)
                    nodeShape.setAttr('overrideVisibility', 1)
                if HyperSkin.isMesh(node) or HyperSkin.isJnt(node) or node.isCurv():
                    node.setAttr('lodVisibility', 1)
                    node.setAttr('visibility', 1)
                    node.setAttr('template', 0)
                    node.setAttr('overrideEnabled', 0)
                    node.setAttr('overrideDisplayType', 0)
                    node.setAttr('overrideLevelOfDetail', 0)
                    node.setAttr('overrideVisibility', 1)
                if HyperSkin.isJnt(node):
                    node.setAttr('drawStyle', 2)
                    node.setAttr('radius', 0)
                if HyperSkin.isMesh(node):
                    if not objExists('my_Shader'):
                        myShdr = shadingNode('lambert', asShader=1, n='my_Shader')
                        myShdr.setAttr('color', 0, 0, 0, type='double3')
                    else:
                        myShdr = PyNode('my_Shader')
                    select(node, r=1)
                    hyperShade('my_Shader', assign='my_Shader')
                    myShdr.setAttr('transparency', 1, 1, 1, type='double3')

        def hideNodes(nodeList):
            nodeList = [nodeList] if type(nodeList) != list else nodeList
            for node in [hsNode(obj) for obj in nodeList]:
                if node.isMesh():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 1)
                    nodeShape.setAttr('lodVisibility', 0)
                    nodeShape.setAttr('visibility', 0)
                    nodeShape.setAttr('template', 1)
                    nodeShape.setAttr('overrideEnabled', 1)
                    nodeShape.setAttr('overrideDisplayType', 1)
                    nodeShape.setAttr('overrideLevelOfDetail', 1)
                    nodeShape.setAttr('overrideVisibility', 0)
                    nodeShape.setAttr('displayVertices', 1)
                    nodeShape.setAttr('vertexSize', 10000000)
                    nodeShape.setAttr('displayUVs', 1)
                    nodeShape.setAttr('uvSize', 10000000)
                elif node.isCurv():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 1)
                    nodeShape.setAttr('lodVisibility', 0)
                    nodeShape.setAttr('visibility', 0)
                    nodeShape.setAttr('template', 1)
                    nodeShape.setAttr('overrideEnabled', 1)
                    nodeShape.setAttr('overrideDisplayType', 1)
                    nodeShape.setAttr('overrideLevelOfDetail', 1)
                    nodeShape.setAttr('overrideVisibility', 0)
                if not HyperSkin.isMesh(node):
                    if HyperSkin.isJnt(node) or node.isCurv():
                        node.setAttr('lodVisibility', 0)
                        node.setAttr('visibility', 0)
                        node.setAttr('template', 1)
                        node.setAttr('overrideEnabled', 1)
                        node.setAttr('overrideDisplayType', 1)
                        node.setAttr('overrideLevelOfDetail', 1)
                        node.setAttr('overrideVisibility', 0)
                    if HyperSkin.isJnt(node):
                        node.setAttr('drawStyle', 2)
                        node.setAttr('radius', 0)
                    else:
                        if HyperSkin.isMesh(node):
                            if not objExists('my_Shader'):
                                myShdr = shadingNode('lambert', asShader=1, n='my_Shader')
                                myShdr.setAttr('color', 0, 0, 0, type='double3')
                            else:
                                myShdr = PyNode('my_Shader')
                            select(node, r=1)
                            hyperShade('my_Shader', assign='my_Shader')
                            myShdr.setAttr('transparency', 1, 1, 1, type='double3')
                        node.setAttr('v', lock=True, channelBox=False, keyable=False)

        cmds.select('*DSC', r=1)
        initList = [nd.name() for nd in hsN.selected()]
        dscList = []
        dscDict = {}
        allDiscs = hsN.selected()
        for dsc in allDiscs:
            if dsc.getAttr('copyDisc'):
                if dsc not in dscList:
                    dscList.append(dsc)
                else:
                    if dsc not in dscDict:
                        dscDict[dsc] = {}
                    dscDict[dsc]['copyDisc'] = dsc.getAttr('copyDisc')
            else:
                if dsc.getAttr('discShape'):
                    if dsc not in dscList:
                        dscList.append(dsc)
                    if dsc not in dscDict:
                        dscDict[dsc] = {}
                    dscDict[dsc]['discShape'] = dsc.getAttr('discShape')
                if dsc.getAttr('scale_X'):
                    if dsc not in dscList:
                        dscList.append(dsc)
                    if dsc not in dscDict:
                        dscDict[dsc] = {}
                    dscDict[dsc]['scale_X'] = dsc.getAttr('scale_X')
                if dsc.getAttr('scale_Y'):
                    if dsc not in dscList:
                        dscList.append(dsc)
                    if dsc not in dscDict:
                        dscDict[dsc] = {}
                    dscDict[dsc]['scale_Y'] = dsc.getAttr('scale_Y')
                if dsc.getAttr('scale_Z'):
                    if dsc not in dscList:
                        dscList.append(dsc)
                    if dsc not in dscDict:
                        dscDict[dsc] = {}
                    dscDict[dsc]['scale_Z'] = dsc.getAttr('scale_Z')
                if dsc not in dscDict:
                    dscDict[dsc] = {}
                dscDict[dsc]['snapRotTo'] = dsc.getAttr('snapRotTo')

        adjustedDiscs = []
        for dsc in dscList:
            if 'copyDisc' in dscDict[dsc]:
                splitList = dsc.rsplit('_', 1)
                dsc.select()
                if dscDict[dsc]['copyDisc'] == 1:
                    jntName = hsNode(splitList[0])
                    prntDsc = hsNode(jntName.parent() + '_' + splitList[1])
                    select(dsc, prntDsc)
                    if prntDsc.getAttr('copyDisc') == 1:
                        splitList = prntDsc.rsplit('_', 1)
                        prntDsc.select()
                        jntName2 = hsNode(splitList[0])
                        prntDsc2 = hsNode(jntName2.parent() + '_' + splitList[1])
                        select(prntDsc, prntDsc2)
                        HyperSkin.as_ReplaceGCMs(dscDict[prntDsc]['snapRotTo'])
                        prntDsc = hsNode(jntName2.parent() + '_' + splitList[1])
                    select(dsc, prntDsc)
                    HyperSkin.as_ReplaceGCMs(dscDict[dsc]['snapRotTo'])
                elif dscDict[dsc]['copyDisc'] == 2:
                    jntName = hsNode(splitList[0])
                    chdDsc = hsNode(jntName.child() + '_' + splitList[1])
                    if chdDsc.getAttr('copyDisc') == 2:
                        splitList = chdDsc.rsplit('_', 1)
                        chdDsc.select()
                        jntName2 = hsNode(splitList[0])
                        chdDsc2 = hsNode(jntName2.child() + '_' + splitList[1])
                        select(chdDsc, chdDsc2)
                        HyperSkin.as_ReplaceGCMs(dscDict[chdDsc]['snapRotTo'])
                        chdDsc = hsNode(jntName2.child() + '_' + splitList[1])
                    select(dsc, chdDsc)
                    HyperSkin.as_ReplaceGCMs(dscDict[dsc]['snapRotTo'])
            elif 'discShape' in dscDict[dsc]:
                splitList = dsc.rsplit('_', 1)
                dsc.select()
                if dscDict[dsc]['discShape'] == 1:
                    HyperSkin.as_ReplaceGCMs(dscDict[dsc]['snapRotTo'], dscDict[dsc]['discShape'])
            scaleDir = None
            if 'scale_X' in dscDict[dsc]:
                scaleDir = 'x'
            elif 'scale_Y' in dscDict[dsc]:
                scaleDir = 'y'
            elif 'scale_Z' in dscDict[dsc]:
                scaleDir = 'Z'
            if scaleDir:
                curv = hsNode(dsc.name() + '_Outer')
                unhideNodes(curv)
                curv.hide()
                cvList = curv.getVtxList()[0]
                dscGrp = dsc.pickWalkUp()
                HyperSkin.scaleTillInsideMesh(dscGrp, cvList, trgtMesh, 0.1, scaleDir)
                adjustedDiscs.append(dsc)
                hideNodes(curv)

        select(adjustedDiscs, r=1)
        FrameSelected()
        HyperSkin.message('Adjusted Discs Sucessfully & Automatically !!')

    def searchReplaceAll(self, objList, searchWord, replaceWord, topSelect=True, selectHI=True):
        """
                Objective:
                ----------
                Search and replaces the words under the given object
                
                Return Stmnt:
                -------------
                return allNodes  #_ All nodes with replaced / renamed words under given obj.    
                """
        objList = [objList] if type(objList) != list else objList
        finalList = []
        for topGrp in objList:
            select(topGrp, r=1)
            if selectHI:
                select(hi=1)
            else:
                if not topSelect:
                    select(topGrp, d=1)
                allNodes = selected()
                allNodes.reverse()
                for node in allNodes:
                    renameWord = HyperSkin.name(node).replace(searchWord, replaceWord)
                    try:
                        node.rename(renameWord)
                    except:
                        pass

                allNodes.reverse()
                finalList.append(allNodes)

        select(finalList, r=1)
        return finalList

    def refreshView(self, num):
        if num:
            for a in range(num):
                mel.eval('refresh -cv')
        else:
            pass

    def parentChild_ByImplied(self, chd=None, prnt=None, removeAttrs=False, dscChd=False, **shArgs):
        """
                Usage:
                ------
                #_ Select child joint(implied) first and then parent joint (implied)
                HyperSkin.parentChild_ByImplied(hsN.selected()[0], hsN.selected()[1])         
                """
        if shArgs:
            chd = shArgs['c'] if 'c' in shArgs else chd
            prnt = shArgs['p'] if 'p' in shArgs else prnt
            removeAttrs = shArgs['ra'] if 'ra' in shArgs else removeAttrs
            dscChd = shArgs['dc'] if 'dc' in shArgs else dscChd
        jntList = (chd or prnt or hsN._selected)()
        if len(jntList) == 2:
            (chd, prnt) = jntList
        else:
            if len(jntList) > 2:
                for num in range(len(jntList) - 1):
                    HyperSkin.parentChild_ByImplied(jntList[num], jntList[num + 1])

                return
            if len(jntList) < 2:
                HyperSkin.error('Need Minimum 2 Joints To Be Selected !!')
        if removeAttrs:
            nJnts = hsN.selected()
            for jnt in nJnts:
                if attributeQuery('mChd', n=jnt, ex=1):
                    cmds.deleteAttr(jnt, at='mChd')
                if attributeQuery('mPrnt', n=jnt, ex=1):
                    cmds.deleteAttr(jnt, at='mPrnt')

            HyperSkin.message('Removed Attrs Sucessfully !!')
            return
        if attributeQuery('mPrnt', n=chd, ex=1):
            cmds.deleteAttr(chd, at='mPrnt')
        cmds.addAttr(chd, ln='mPrnt', k=1, at='message')
        cmds.connectAttr(prnt + '.message', chd + '.mPrnt')
        if dscChd:
            if attributeQuery('dscChd', n=prnt, ex=1):
                cmds.deleteAttr(prnt, at='dscChd')
            cmds.addAttr(prnt, ln='dscChd', k=1, at='message')
            cmds.connectAttr(chd + '.message', prnt + '.dscChd')
        elif not attributeQuery('mChd', n=prnt, ex=1):
            cmds.addAttr(prnt, ln='mChd', k=1, at='message')
            cmds.connectAttr(chd + '.message', prnt + '.mChd')
        om.MGlobal.displayInfo('Added impliedChild & impliedParent sucessfully ..!')

    def removeParentChild_ImpliedInfo(self, jntList=None):
        if not jntList:
            jntList = hsN.selected()
        else:
            jntList = [jntList] if type(jntList) != list else jntList
            jntList = list(map(hsNode, jntList))
        for jnt in jntList:
            HyperSkin.removeImpliedChild(jnt)
            HyperSkin.removeImpliedParent(jnt)

    def removeImpliedParent(self, jnt):
        if attributeQuery('mPrnt', n=jnt, ex=1):
            cmds.deleteAttr(jnt, at='mPrnt')
        om.MGlobal.displayInfo('Removed implied parent sucessfully ..!')

    def reorderDeformers(self, meshList=None, deformTypes=None):
        """
                deformTypes =['sculpt', 'skinCluster', 'cMuscleRelative', 'nonLinear', 'cluster', 'blendShape', 'ffd', 'wrap', 'tweak']
                nonLinearOrder =['wave', 'twist', 'squash', 'sine', 'flare', 'bend']
                deformerOrder =['blendShape', 'cluster', 'skinCluster', 'cMuscleRelative', 'ffd', 'nonLinear', 'sculpt', 'wrap', 'tweak']
                """
        if not deformTypes:
            deformTypes = ['sculpt','skinCluster','cMuscleRelative','nonLinear','cluster','blendShape','ffd','wrap','tweak']
        if not meshList:
            meshList = nselected()
        else:
            meshList = [meshList] if type(meshList) != list else meshList
            meshList = list(map(hsNode, meshList))
        for meshObj in meshList:
            meshObj = PyNode(meshObj)
            deformList = []
            for deformType in deformTypes:
                deforms = meshObj.listHistory(type=deformType)
                if deforms:
                    deformList.append(deforms)

            if deformList:
                if len(deformList) > 1:
                    for num in range(0, len(deformList) - 1):
                        for deformNode in deformList[num + 1]:
                            try:
                                reorderDeformers(deformList[num][0], deformNode, meshObj)
                            except:
                                pass

                if len(deformList[0]) > 1:
                    for deformNode in deformList[0][1:]:
                        try:
                            reorderDeformers(str(deformList[0][0]), str(deformNode), str(meshObj))
                        except:
                            pass

    def removeImpliedChild(self, jnt):
        if attributeQuery('mChd', n=jnt, ex=1):
            cmds.deleteAttr(jnt, at='mChd')
        om.MGlobal.displayInfo('Removed implied child sucessfully ..!')

    def old_progressWin(self, currentItem=None, endProgress=0, showProgressTime=1, useProgress=1, **shArgs):
        global progressHour
        global progressMinute
        global progressSecond
        global progressValue
        if shArgs:
            currentItem = shArgs['ci'] if 'ci' in shArgs else currentItem
            endProgress = shArgs['ep'] if 'ep' in shArgs else endProgress
            showProgressTime = shArgs['spt'] if 'spt' in shArgs else showProgressTime
            useProgress = shArgs['up'] if 'up' in shArgs else useProgress
        if not useProgress:
            return
        if progressValue < 100:
            progressValue += float(progressAddValue)
        else:
            cmds.progressBar(myProgressBar, e=1, endProgress=endProgress)
            if window('as_myProgressWin', ex=1):
                deleteUI('as_myProgressWin', window=True)
        if showProgressTime:
            progressHour = int(timerX(startTime=startTm) / 3600)
            progressMinute = int(timerX(startTime=startTm) / 60 % 60)
            progressSecond = int(timerX(startTime=startTm) % 60)
            cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue + ' <----------> Elapsed Time : %d Hr %d Min %d Sec' % (progressHour, progressMinute, progressSecond)))
        else:
            cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue))
        cmds.progressBar(myProgressBar, edit=1, progress=progressValue)
        if currentItem:
            frameLayout('as_myProgressFL', e=1, l=(str(currentItem)))
        cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue + '%sElapsed Time : %d Hr %d Min %d Sec' % ('     ', progressHour, progressMinute, progressSecond)))

    def progressReset(self):
        global topProgressValue
        topProgressValue = 0

    def progressWin(self, currentItem=None, endProgress=0, showProgressTime=0, innerObjs=False, innerList=None, refreshView=0, useProgress=1, outerList=None, **shArgs):
        global progressHour
        global progressMinute
        global progressSecond
        global progressValue
        global topProgressHour
        global topProgressMinute
        global topProgressSecond
        global topProgressValue
        if shArgs:
            currentItem = shArgs['ci'] if 'ci' in shArgs else currentItem
            endProgress = shArgs['ep'] if 'ep' in shArgs else endProgress
            showProgressTime = shArgs['spt'] if 'spt' in shArgs else showProgressTime
            innerObjs = shArgs['io'] if 'io' in shArgs else innerObjs
            innerList = shArgs['il'] if 'il' in shArgs else innerList
            refreshView = shArgs['rv'] if 'rv' in shArgs else refreshView
            useProgress = shArgs['up'] if 'up' in shArgs else useProgress
            outerList = shArgs['ol'] if 'ol' in shArgs else outerList
        if not useProgress:
            return
        if innerList:
            if topProgressValue < 100:
                topProgressValue += float(topProgressAddValue)
            else:
                topProgressValue = topProgressValue % 100.0
                topProgressValue += float(topProgressAddValue)
            if showProgressTime:
                topProgressHour = int(timerX(startTime=topStartTm) / 3600)
                topProgressMinute = int(timerX(startTime=topStartTm) / 60 % 60)
                topProgressSecond = int(timerX(startTime=topStartTm) % 60)
                cmds.text('as_topProgressTxt', e=1, l=('Progress : %0.1f' % topProgressValue + ' <----------> Elapsed Time : %d Hr %d Min %d Sec' % (topProgressHour, topProgressMinute, topProgressSecond)))
            else:
                cmds.text('as_topProgressTxt', e=1, l=('Progress : %0.1f' % topProgressValue))
            cmds.progressBar(topProgressBar, edit=1, progress=topProgressValue)
            if currentItem:
                if type(innerList) == list:
                    frameLayout('as_topProgressFL', e=1, l=('Num Items : {:04d} <--> {}'.format(len(innerList), str(currentItem))))
                else:
                    frameLayout('as_topProgressFL', e=1, l=(str(currentItem)))
            cmds.text('as_topProgressTxt', e=1, l=('Progress : %0.1f' % progressValue + '%sElapsed Time : %d Hr %d Min %d Sec' % ('     ', topProgressHour, topProgressMinute, topProgressSecond)))
        else:
            if progressValue < 100:
                progressValue += float(progressAddValue)
            else:
                cmds.progressBar(myProgressBar, e=1, endProgress=endProgress)
                if window('as_myProgressWin', ex=1):
                    deleteUI('as_myProgressWin', window=True)
            if showProgressTime:
                progressHour = int(timerX(startTime=startTm) / 3600)
                progressMinute = int(timerX(startTime=startTm) / 60 % 60)
                progressSecond = int(timerX(startTime=startTm) % 60)
                cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue + ' <----------> Elapsed Time : %d Hr %d Min %d Sec' % (progressHour, progressMinute, progressSecond)))
            else:
                cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue))
            cmds.progressBar(myProgressBar, edit=1, progress=progressValue)
            if currentItem:
                frameLayout('as_myProgressFL', e=1, l=(str(currentItem)))
            cmds.text('as_myProgressTxt', e=1, l=('Progress : %0.1f' % progressValue + '%sElapsed Time : %d Hr %d Min %d Sec' % ('     ', progressHour, progressMinute, progressSecond)))
        if refreshView:
            HyperSkin.refreshView(1)

    def name(self, mNode):
        """
                Returns the name of the object from last the vertical bar '|' 
                i.e. Returns the name of obj excluding full path
                """
        mNode = PyNode(mNode)
        return mNode.name().split('|')[-1].strip()

    def mFreeze(self, objName, t=1, r=1, s=1):
        select(objName, r=1)
        makeIdentity(apply=True, s=s, r=r, t=t, n=0)

    def mDistance(self, srcObj, destObj, srcType='obj', destType='obj', giveNode=False):
        """
                Objective:
                ----------
                To measure the distance between (two objects) or (two positions) or (one obj and one position or veceversa)
                
                Return Stmnt:
                -------------
                return [mDist, locList, distNode, distShape, distAttr]  #_ If giveNode is True
                return [mDist]                                                                                  #_ If giveNode is False 
                """
        srcPos = HyperSkin.getPos(srcObj, srcType)[0] if type(srcObj) != list else srcObj
        destPos = HyperSkin.getPos(destObj, destType)[0] if type(destObj) != list else destObj
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        if giveNode:
            distShape = distanceDimension(sp=(-100, -100, -100), ep=(100, 100, 100))
            distNode = distShape.getParent()
            distNode.rename(str(destObj) + '_Dist')
            distAttr = distShape + '.distance'
            srcLoc = listConnections(distShape + '.startPoint')[0]
            destLoc = listConnections(distShape + '.endPoint')[0]
            HyperSkin.snapTo_Obj(srcLoc, srcObj)
            HyperSkin.snapTo_Obj(destLoc, destObj)
            if objExists(srcObj):
                if type(srcObj) != list:
                    srcLoc.rename(HyperSkin.name(srcObj) + '_SrcLoc')
                    parent(srcLoc, srcObj)
                if objExists(destObj):
                    if type(destObj) != list:
                        destLoc.rename(HyperSkin.name(destObj) + '_EndLoc')
                        parent(destLoc, destObj)
                        parent(distNode, destObj)
                    locList = [srcLoc, destLoc]
                    return [mDist,locList,distNode,distShape,distAttr]
            return [mDist]

    def mConstrain(self, objList, conList, offSet=True, wVal=1, **kwargs):
        """
                Args:
                -----
                conList = 'point' | 'orient' | 'parent' | 'scale' | 'geometry' | 'normal | 'tangent' | 'aim' | 'poleVector' | 
                
                aimConstrain Example:
                ---------------------
                aimConstraint(worldUpType="none", aimVector=(0, 0, 1), upVector=(0, 1, 0), weight=1, offset=(0, 0, 0))
                
                Returns:
                -------
                if len(conList) == 1 and len(objList) > 2:
                        return [conNode, conNode.getWeightAliasList()]
                else:
                        return [conNode]                
                """
        conList = [conList] if type(conList) != list else conList
        select(cl=1)
        for conType in conList:
            for obj in objList[:-1]:
                if conType != 'poleVector':
                    exec('conNode = ' + conType + 'Constraint("' + obj + '", "' + objList[-1] + '", mo=' + str(offSet) + ', w=' + str(wVal) + ', n="' + str(objList[-1]) + '_' + conType.title() + 'Con", **kwargs)')
                if conType == 'poleVector':
                    exec('conNode = ' + conType + 'Constraint("' + obj + '", "' + objList[-1] + '", w=' + str(wVal) + ', n="' + str(objList[-1]) + '_' + conType.title() + 'Con", **kwargs)')

            if conType == 'parent':
                conNode = PyNode(pm.parentConstraint((objList[-1]), q=1))
            elif conType == 'orient':
                conNode = PyNode(pm.orientConstraint((objList[-1]), q=1))
            elif conType == 'point':
                conNode = PyNode(pm.pointConstraint((objList[-1]), q=1))
            elif conType == 'scale':
                conNode = PyNode(pm.scaleConstraint((objList[-1]), q=1))
            elif conType == 'aim':
                conNode = PyNode(pm.aimConstraint((objList[-1]), q=1))
            else:
                if conType == 'poleVector':
                    conNode = PyNode(pm.poleVectorConstraint((objList[-1]), q=1))
            if not not conType == 'poleVector':
                if conType == 'orient':
                    pass
                conNode.setAttr('interpType', 2)

        if len(conList) == 1:
            if len(objList) > 2:
                return [conNode, conNode.getWeightAliasList()]
        return [conNode]

    def selectFromTF(self, textFld):
        """
                Adds selected object's name as Input in any Window for <== button
                Usage:
                ------
                obj10           # Adds 'obj10' While pressing Enter.. <== button
                box25           # Adds 'box25' While pressing Enter.. <== button
                """
        obj = textField(textFld, q=1, tx=1)
        if objExists(obj):
            if ', ' not in obj:
                cmds.select(obj, tgl=1)
                return obj
        if ', ' in obj:
            objList = obj.split(', ')
            try:
                select(objList, add=1)
                return objList
            except:
                return

        else:
            return
        TranslateToolWithSnapMarkingMenu()

    def selectHI(self, objName, objType='jnt', topSelect=True, includeShapes=False, childImplied=True):
        """
                Objective:
                ----------
                Selects all objects of given type under the given object
                
                Returns:
                --------
                selected()      #_ As per the objType   
                """
        if objType == 'jnt' or objType == 'joint' or objType == '^jnt' or objType == '^joint':
            nType = 'joint'
        elif objType == 'crv' or objType == 'curv' or objType == 'nurbsCurve' or objType == '^crv' or objType == '^curv' or objType == '^nurbsCurve':
            nType = 'nurbsCurve'
        elif objType == 'mesh' or objType == 'obj' or objType == '^mesh' or objType == '^obj':
            nType = 'mesh'
        else:
            nType = objType
        objName = str(objName)
        select(objName, r=1)
        select(hi=1)
        selList = hsN.selected()
        if childImplied:
            asObj = hsNode(objName)
            if asObj.attributeQuery('mChd', n=(asObj.name()), ex=1):
                if asObj.attributeQuery('mChd', n=(asObj.name()), at=1) == 'message':
                    impliedList = asObj.child().selectHI()
                    select(selList, impliedList, r=1)
                if objType.startswith('^'):
                    for node in selected():
                        if nodeType(node) == nType:
                            if nodeType(node) == 'joint':
                                select(node, tgl=1)
                            if nodeType(node) == nType:
                                if not not nodeType(node) == 'nurbsCurve':
                                    if nodeType(node) == 'mesh':
                                        pass
                                    select(node, tgl=1)
                                    node = hsNode(node)
                                    select((node.parent()), tgl=1)

                else:
                    for node in ls(sl=1):
                        if nodeType(node) != nType:
                            select(node, tgl=1)

                if not topSelect:
                    select(objName, d=1)
                if nType == 'joint':
                    return selected()
            if not objType.startswith('^'):
                if nType == 'nurbsCurve' or nType == 'mesh':
                    if not includeShapes:
                        pickWalk(d='up')
                    else:
                        for obj in selected():
                            obj = hsNode(obj)
                            select((obj.parent()), add=1)

                    return selected()

    def isLastJnt(self, jnt, numFromEnd=0, childImplied=True):
        jnt = PyNode(str(jnt))
        asJnt = hsNode(jnt)
        if childImplied:
            chdJnt = asJnt.child()
            if chdJnt:
                if chdJnt.isJnt():
                    return False
                if jnt.nodeType() == 'joint':
                    pass
                else:
                    raise RuntimeError('HyperSkin.isLastJnt: It is Not Joint..')
                if numFromEnd == 0:
                    chdList = jnt.getChildren()
                    if not chdList:
                        return True
                    if HyperSkin.selectHI(jnt, 'jnt', topSelect=False):
                        jnt.select(r=1)
                        return False
                    jnt.select(r=1)
                    return True
                if HyperSkin.getJntNum_fromEnd(jnt) == numFromEnd:
                    jnt.select(r=1)
                    return True
            jnt.select(r=1)
            return False

    def getVisVolume(self):
        latList = cmds.lattice(divisions=[2, 2, 2], objectCentered=1, ldv=[2, 2, 2])
        cmds.delete(latList[-1])
        cmds.setAttr(latList[1] + '.overrideEnabled', 1)
        cmds.setAttr(latList[1] + '.overrideColor', 17)
        cmds.rename(latList[1], 'as_VisualizeVolume_HS')

    def getVtxList(self, objName):
        """
                Returns(hsNodes):
                -----------------
                if self.isNodeType('nurbsCurve'):
                        return cvList
                elif self.isNodeType('mesh'):                   
                        return vtxList
                elif self.isNodeType('nurbsSurface'):
                        return cvList                                                           
                """
        asObj = hsNode(objName)
        if asObj.isNodeType('nurbsCurve'):
            curvFn = MFnNurbsCurve(asObj._MDagPath())
            if self._mayaVer() < 2025:
                numCVs = curvFn.numCVs()
            else:
                numCVs = curvFn.numCVs
            curvForm = asObj.getAttr('form')
            curvDegree = asObj.getAttr('degree')
            if curvForm == 2:
                numCVs -= curvDegree
            cvList = [hsNode(asObj.name() + '.cv[' + str(num) + ']') for num in range(numCVs)]
            select(cvList, r=1)
            return cvList
        if asObj.isNodeType('mesh'):
            polyIt = asObj._MItMeshVertex()
            numVtx = polyIt.count()
            vtxList = [hsNode(asObj.name() + '.vtx[' + str(num) + ']') for num in range(numVtx)]
            return vtxList
        if asObj.isNodeType('nurbsSurface'):
            cvIter = MItSurfaceCV(asObj.shape()._MDagPath())
            cvList = []
            while not cvIter.isDone():
                while not cvIter.isRowDone():
                    utilU = maya.OpenMaya.MScriptUtil()
                    utilU.createFromInt(0)
                    ptrU = utilU.asIntPtr()
                    utilV = maya.OpenMaya.MScriptUtil()
                    utilV.createFromInt(0)
                    ptrV = utilV.asIntPtr()
                    cvIter.getIndex(ptrU, ptrV)
                    cvList.append(musObj.shape().shortName() + '.cv[' + str(utilU.getInt(ptrU)) + '][' + str(utilV.getInt(ptrV)) + ']')
                    next(cvIter)

                cvIter.nextRow()

            select(cvList, r=1)
            cvList = filterExpand(sm=28)
            numCVs = len(cvList)
            return cvList

    def getRot(self, objList):
        objList = [objList] if type(objList) != list else objList
        return [list(getAttr(obj + '.r')) for obj in objList]

    def name(self, mNode):
        """
                Returns the name of the object from last the vertical bar '|' 
                i.e. Returns the name of obj excluding full path
                """
        mNode = PyNode(mNode)
        return mNode.name().split('|')[-1].strip()

    def getPos(self, objList, objType='obj'):
        """
                Returns[list Of Poses]:
                -----------------------
                List of Poses. get single pos with : HyperSkin.getPos(obj)[0]
                For Ex: [[0, 2, 1]] or [[0, 2, 1], [1, 0, 1], ..] etc
                """
        objList = [objList] if type(objList) != list else objList
        posList = []
        for objName in objList:
            if objType.lower() == 'obj':
                transFn = MFnTransform()
                pathDg = HyperSkin.getMPathDg(objName)
                transFn.setObject(pathDg)
                objPos = transFn.rotatePivot(MSpace.kWorld)
            else:
                if objType.lower() == 'vtx' or objType.lower() == 'cv':
                    objPos = xform(objName, q=1, ws=1, t=1)
                elif objType.lower() == 'edg':
                    pos = xform(objName, q=1, ws=1, t=True)
                    xVal = (pos[0] + pos[3]) / 2.0
                    yVal = (pos[1] + pos[4]) / 2.0
                    zVal = (pos[2] + pos[5]) / 2.0
                    objPos = [xVal, yVal, zVal]
                posList.append([objPos[0], objPos[1], objPos[2]])

        return posList

    def openPythonScripting(self):
        HyperSkin.as_AboutHyperSkin()
        web.open('https://www.yogeshnichal.com/')

    def old_getMDagPath(self, obj):
        select(obj, r=1)
        activeList = MSelectionList()
        MGlobal.getActiveSelectionList(activeList)
        pathDg = MDagPath()
        activeList.getDagPath(0, pathDg)
        return pathDg

    def getPos(self, objList, objType='obj'):
        """
                Returns[list Of Poses]:
                -----------------------
                List of Poses. get single pos with : HyperSkin.getPos(obj)[0]
                For Ex: [[0, 2, 1]] or [[0, 2, 1], [1, 0, 1], ..] etc
                """
        objList = [objList] if type(objList) != list else objList
        posList = []
        for objName in objList:
            if objType.lower() == 'obj':
                transFn = MFnTransform()
                pathDg = HyperSkin.getMPathDg(objName)
                transFn.setObject(pathDg)
                objPos = transFn.rotatePivot(MSpace.kWorld)
            else:
                if objType.lower() == 'vtx' or objType.lower() == 'cv':
                    objPos = xform(objName, q=1, ws=1, t=1)
                elif objType.lower() == 'edg':
                    pos = xform(objName, q=1, ws=1, t=True)
                    xVal = (pos[0] + pos[3]) / 2.0
                    yVal = (pos[1] + pos[4]) / 2.0
                    zVal = (pos[2] + pos[5]) / 2.0
                    objPos = [xVal, yVal, zVal]
                posList.append([objPos[0], objPos[1], objPos[2]])

        return posList

    def mDistance(self, srcObj, destObj, srcType='obj', destType='obj', giveNode=False):
        """
                Objective:
                ----------
                To measure the distance between (two objects) or (two positions) or (one obj and one position or veceversa)
                
                Return Stmnt:
                -------------
                return [mDist, locList, distNode, distShape, distAttr]  #_ If giveNode is True
                return [mDist]                                                                                  #_ If giveNode is False 
                """
        srcPos = HyperSkin.getPos(srcObj, srcType)[0] if type(srcObj) != list else srcObj
        destPos = HyperSkin.getPos(destObj, destType)[0] if type(destObj) != list else destObj
        distX = destPos[0] - srcPos[0]
        distY = destPos[1] - srcPos[1]
        distZ = destPos[2] - srcPos[2]
        mDist = math.sqrt(distX ** 2 + distY ** 2 + distZ ** 2)
        if giveNode:
            distShape = distanceDimension(sp=(-100, -100, -100), ep=(100, 100, 100))
            distNode = distShape.getParent()
            distNode.rename(str(destObj) + '_Dist')
            distAttr = distShape + '.distance'
            srcLoc = listConnections(distShape + '.startPoint')[0]
            destLoc = listConnections(distShape + '.endPoint')[0]
            HyperSkin.snapTo_Obj(srcLoc, srcObj)
            HyperSkin.snapTo_Obj(destLoc, destObj)
            if objExists(srcObj):
                if type(srcObj) != list:
                    srcLoc.rename(HyperSkin.name(srcObj) + '_SrcLoc')
                    parent(srcLoc, srcObj)
                if objExists(destObj):
                    if type(destObj) != list:
                        destLoc.rename(HyperSkin.name(destObj) + '_EndLoc')
                        parent(destLoc, destObj)
                        parent(distNode, destObj)
                    locList = [srcLoc, destLoc]
                    return [mDist,locList,distNode,distShape,distAttr]
            return [mDist]

    def getLongestObj(self, src, objList, objType='obj'):
        distanceDict = {}
        for obj in objList:
            if objType == 'obj':
                dist = HyperSkin.mDistance(src, obj, 'obj', 'obj')[0]
            else:
                if objType == 'vtx':
                    dist = HyperSkin.mDistance(src, obj, 'vtx', 'vtx')[0]
                distanceDict[dist] = obj

        longDist = max(distanceDict.keys())
        return distanceDict[longDist]

    def getFaceList(self, objName, sidePos=None, mirrAxis='x'):
        """
                Available sidePos : 'L_', 'R_'
                """
        asObj = hsNode(objName)
        mItPoly = asObj._MItMeshPolygon()
        faceList = []
        sideFaces = []
        while not mItPoly.isDone():
            if not sidePos:
                faceList.append(hsNode(asObj.name() + '.f[' + str(mItPoly.index()) + ']'))
            else:
                point = om.MPoint()
                point = mItPoly.center(MSpace.kWorld)
                posList = [round(point.x, 5), round(point.y, 5), round(point.z, 5)]
                if mirrAxis == 'x':
                    axisVal = posList[0]
                if mirrAxis == 'y':
                    axisVal = posList[1]
                if mirrAxis == 'z':
                    axisVal = posList[2]
                if axisVal >= -0.001:
                    if sidePos == 'L_':
                        sideFaces.append(hsNode(asObj.name() + '.f[' + str(mItPoly.index()) + ']'))
                    if axisVal <= 0.001:
                        if sidePos == 'R_':
                            sideFaces.append(hsNode(asObj.name() + '.f[' + str(mItPoly.index()) + ']'))
                        next(mItPoly)

        if not sidePos:
            return faceList
        mel.eval('changeSelectMode -object')
        select(objName, r=1)
        SelectFacetMask()
        select(sideFaces, r=1)
        return sideFaces

    def getJntNum_fromEnd(self, jnt, jntCount=0, is_hsNode=0):
        if not is_hsNode:
            jnt = hsNode(jnt)
        endJnt = jnt.pickWalkDown(1, 'joint')
        if endJnt:
            is_hsNode = 1
            jntCount += 1
            return HyperSkin.getJntNum_fromEnd(endJnt, jntCount, is_hsNode)
        return jntCount

    def grpIt(self, objName, grpLevel=1, snapPiv=True, grpSufxList=None):
        """
                Returns:(hsNodes)
                -----------------
                if len(grpList) > 1:
                        return grpList  # grp1, grp2, ....grpTop
                else:
                        return grpList[0]
                """
        if grpSufxList:
            grpSufxList = [grpSufxList] if type(grpSufxList) != list else grpSufxList
        objName = hsNode(objName)
        objGrp = objName
        objName.select(r=1)
        if not grpLevel:
            return objName.asObj()
        num = 0
        grpList = []

        def groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList):
            if not grpSufxList:
                grpSufxList = ["'_Grp'", "'_GrpTp'", "'_GrpEx'", "'_TopGp'", "'_TopEx'", "'_RootGp'", "'_RootEx'"]
            else:
                grpTempList = ["'_Grp'", "'_GrpTp'", "'_GrpEx'", "'_TopGp'", "'_TopEx'", "'_RootGp'", "'_RootEx'"]
                grpTempSufxList = [grpSufxList] if type(grpSufxList) != list else grpSufxList
                if len(grpList) > len(grpSufxList):
                    grpSufxList.extend(grpTempList[len(grpSufxList):])
            if num < grpLevel:
                select(objGrp, r=1)
                sufxName = '_' + grpSufxList[num] if (not grpSufxList[num].startswith('_')) else (grpSufxList[num])
                objGrp = hsNode(group(n=(objName + sufxName)))
                grpList.append(objGrp)
                if snapPiv:
                    objGrp.snapPivTo(objName.name())
                num = num + 1
                groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList)
            return grpList

        grpList = groupIt(objName, objGrp, grpLevel, snapPiv, num, grpSufxList, grpList)
        if len(grpList) > 1:
            return grpList
        return grpList[0]

    def centerPiv(self, objName):
        select(objName, r=1)
        mel.CenterPivot()

    def getDupeNode(self, srcNode, dupName, centerPiv=False, grpDupNode=False, grpLevel=1):
        select(srcNode, r=1)
        dupNode = duplicate(rr=1, n=dupName)[0]
        if centerPiv:
            HyperSkin.centerPiv(dupNode)
        if grpDupNode:
            dupGrp = HyperSkin.grpIt(dupNode, grpLevel)
            return [dupNode, dupGrp]
        return [dupNode]

    def old_extractNum(self, objName):
        """
        Returns:
        -------
        The extracted number from the end of the object name

        Usage:
        ------
        obj.vtx[105]  # Returns 105
        obj.e[206]    # Returns 206
        """
        try:
            asObj = hsNode(objName)
            return asObj.extractNum()
        except:
            pass

        objName = str(objName)
        reObj = re.compile(r'([0-9]+)$')
        testObj = reObj.search(objName)
        if testObj:
            num = int(testObj.group())
            numStr = str(num)
            return [num, numStr]
        reObj = re.compile(r'([0-9]+)')
        testObj = reObj.search(objName)
        if testObj:
            num = int(testObj.group())
            numStr = str(num)
            return [num, numStr]
        return

    def extractNum(self, objName, fromEnd=True, skipCount=0):
        """
                Returns: 
                -------
                the extracted number from end of the object name
                
                Usage:
                ------
                obj.vtx[105]  # Returns 105 
                obj.e[206]      # Returns 206 
                """
        objName = str(objName)
        numList = re.findall('\\d+', objName)
        if numList:
            if fromEnd:
                numStr = numList[-1 * (skipCount + 1)]
                num = int(numStr)
                return [num, str(num)]
            numStr = numList[skipCount]
            num = int(numStr)
            return [num, str(num)]
        else:
            return

    def error(self, errorMsg):
        """
                Sends a given error message through confirmDialog window.
                After closing the window, RuntimeError will be raised
                """
        confirmDialog(title='Error..', bgc=(1, 0.5, 0), message=errorMsg, button=['Yes'], defaultButton='Yes')
        raise RuntimeError(errorMsg)

    def endProgressWin(self, numItems=None, stopProgress=False, useProgress=1, **shArgs):
        global startTm
        if shArgs:
            numItems = shArgs['ni'] if 'ni' in shArgs else numItems
            stopProgress = shArgs['sp'] if 'sp' in shArgs else stopProgress
            useProgress = shArgs['up'] if 'up' in shArgs else useProgress
        elif not useProgress:
            return
        else:
            if numItems:
                if type(numItems) == list:
                    numItems = len(numItems)
                frameLayout('as_myProgressFL', e=1, l=('Number Of Items Processed : ' + str(numItems)))
            cmds.progressBar(myProgressBar, e=1, endProgress=stopProgress)
            cmds.progressBar(myProgressBar, e=1, progress=100)
            cmds.progressBar(myProgressBar, e=1, imp=False)
            cmds.text('as_myProgressTxt', e=1, l=('100% ' + 'Done :)\t\t\tTotal Elapsed Time : %d Hr %d Min %d Sec' % (progressHour, progressMinute, progressSecond)))
            if stopProgress:
                try:
                    deleteUI('as_myProgressWin', window=1)
                except:
                    pass

        om.MGlobal.displayInfo('Processed Sucessfully in: %dHr %dMin %dSec' % (progressHour, progressMinute, progressSecond))
        del startTm

    def confirmAction(self, action, raiseErr=False, trueVal='Yes', falseVal='No', ex1Btn=None, ex1Action=None, **shortArgs):
        """
                Requests User to confirm an action shown in confirmDialog window
                """
        if shortArgs:
            action = shortArgs['a'] if 'a' in shortArgs else action
            raiseErr = shortArgs['e'] if 'e' in shortArgs else raiseErr
            trueVal = shortArgs['tv'] if 'tv' in shortArgs else trueVal
            falseVal = shortArgs['fv'] if 'fv' in shortArgs else falseVal
            ex1Btn = shortArgs['eb1'] if 'eb1' in shortArgs else ex1Btn
            ex1Action = shortArgs['ea1'] if 'ea1' in shortArgs else ex1Action
        else:
            if raiseErr:
                confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message=action, button=[trueVal], defaultButton=trueVal)
                raise RuntimeError(action)
            if not ex1Btn:
                confirm = confirmDialog(title='Confirm Action?', message=action, button=[trueVal, falseVal], defaultButton=trueVal, cancelButton=falseVal, dismissString=falseVal)
            else:
                confirm = confirmDialog(title='Confirm Action?', message=action, button=[trueVal, falseVal, ex1Btn], defaultButton=trueVal, cancelButton=falseVal, dismissString=falseVal)
        if confirm == trueVal:
            return True
        if confirm == falseVal:
            return False
        if confirm == ex1Btn:
            if ex1Btn:
                ex1Action()
                return ex1Btn
            return

    def closeWindows(self):
        if cmds.window('scriptEditorPanel1Window', exists=True):
            cmds.deleteUI('scriptEditorPanel1Window')
        else:
            if cmds.window('nodeEditorPanel1Window', exists=True):
                cmds.deleteUI('nodeEditorPanel1Window')
            if mel.eval('isUIComponentVisible("Command Line")'):
                print('Command Line tab is visible')
                mel.toggleUIComponentVisibility('Command Line')
            else:
                print('Command Line tab is not visible')
        eRig.refreshView(1)

    def computeTime(self, killTime=False, processName=None, runCompute=True):
        """
                Returns:
                --------
                [[progressHour, progressMinute, progressSecond], '%dHr %dMin %dSec' % (progressHour, progressMinute, progressSecond)]
                
                For Ex, Returns:
                [[0, 10, 25], '0Hr 10Min 25Sec']
                """
        global _as_HyperSkinMain__start_Time
        if not runCompute:
            return
        _progHour = 0
        _progMinute = 0
        _progSecond = 0
        try:
            _progHour = int(cmds.timerX(startTime=_as_HyperSkinMain__start_Time) / 3600)
            _progMinute = int(cmds.timerX(startTime=_as_HyperSkinMain__start_Time) / 60 % 60)
            _progSecond = int(cmds.timerX(startTime=_as_HyperSkinMain__start_Time) % 60)
            if killTime:
                cmds.warning('Time is stopped.. Need to initiate time again ..!')
                del _as_HyperSkinMain__start_Time
        except NameError:
            cmds.warning('Time is not initiated.. First you need to start time ..!')

        if not _progHour:
            if not _progMinute:
                if not _progSecond:
                    return
        if processName:
            toPrint = 'Total Time After the process "%s" : %dHr %dMin %dSec' % (processName, _progHour, _progMinute, _progSecond)
            om.MGlobal.displayInfo(toPrint)
            HyperSkin.refreshView(1)
            return [[_progHour, _progMinute, _progSecond], toPrint]
        toPrint = 'Total Time : %dHr %dMin %dSec' % (_progHour, _progMinute, _progSecond)
        om.MGlobal.displayInfo(toPrint)
        HyperSkin.refreshView(1)
        return [[_progHour, _progMinute, _progSecond], toPrint]

    def _isNum(self, obj):
        if not type(obj) == int:
            if type(obj) == float or type(obj) == int:
                return True
            return False

    def _isPosList(self, posList):
        """
                if posList == [1, 3, 10.5] | [0.1, 10, 9.5] | [0, 0, 0] | (0, 10, 5): return True
                else:  return False                     
                """
        if type(posList) != list:
            if type(posList) != tuple:
                return False
            if len(posList) != 3:
                return False
            for pos in posList:
                if not HyperSkin._isNum(pos):
                    return False

            return True

    def _mayaVer(self):
        mayaStr = str(cmds.about(v=1))
        first4 = mayaStr[0:4]
        if len(first4) >= 4 and first4.isalnum():
            if first4.startswith('20'):
                return int(first4)
        return None

    def _compileAHSS(self, userFolder='$_Free_AHSS_v4.2'):
        mayaVer = HyperSkin._mayaVer()
        userPath = 'D:/My_Scripts/$_as_HyperSkin/$_Scripts_Sold/{}/'.format(userFolder)
        verPath = userPath + str(mayaVer)
        if not os.path.exists(verPath):
            os.makedirs(verPath)
        scriptPath = 'D:/My_Scripts/as_Scripts_2022/__pycache__'
        pycFiles = ['as_HyperSkinMain.pyc', 'hsNode.pyc']
        exeCom = '\t\t\t\nimport hsNode\nimportlib.reload(hsNode)\nfrom hsNode import *\t\t\n\nfrom as_HyperSkinMain import *\nimport as_HyperSkinMain\nimportlib.reload(as_HyperSkinMain)\n\nfrom as_HyperSkinMain import *\nimport as_HyperSkinMain\nimportlib.reload(as_HyperSkinMain)\n#HyperSkin.as_HyperSkin()\n\t\t'
        exec(exeCom)
        for pycFile in pycFiles:
            srcFile = scriptPath + pycFile
            destFile = verPath + '/' + pycFile
            if os.path.exists(destFile):
                sysFile(destFile, delete=1)
            if pycFile.endswith('.pyc'):
                shutil.move(srcFile, destFile)
            else:
                HyperSkin.error('No Such File Exist At Source Path : {}'.format(pycFile))

        HyperSkin.message('Compiled Successfully !!')
        os.startfile(mel.toNativePath(verPath))

    def _check4Author(self):
        try:
            author01 = button('as_AboutAuthor_HSS_01', q=1, l=1).strip()
            author02 = button('as_AboutAuthor_HSS_02', q=1, l=1).strip()
            author03 = button('as_HyperSkinningSystem', q=1, l=1).strip()
            R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
            L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
            skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
            refCount = 1
            smoothTest = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
        except:
            deleteUI('as_HyperSkinWin')
            HyperSkin._as_HyperSkinMain__confirmAction('Author Info / Window Design has been Deleted/Changed :(')

        if button('as_AboutAuthor_HSS_01', q=1, c=1) != 'python("HyperSkin.as_AboutHyperSkin()")':
            deleteUI('as_HyperSkinWin')
            HyperSkin._as_HyperSkinMain__confirmAction('Author Info / Window Design has been Deleted/Changed :(')
        if button('as_AboutAuthor_HSS_02', q=1, c=1) != 'python("HyperSkin.as_AboutHyperSkin()")':
            deleteUI('as_HyperSkinWin')
            HyperSkin._as_HyperSkinMain__confirmAction('Author Info / Window Design has been Deleted/Changed :(')
        elif author01 == 'Author : Yogesh Nichal' and author02 == 'Author : Yogesh Nichal' and author03 == 'Hyper Speed Skin':
            pass
        else:
            print((author01, author02, author03))
            try:
                deleteUI('as_HyperSkinWin')
            except:
                pass

            HyperSkin._as_HyperSkinMain__confirmAction('Author Name has been Changed/Modified :(')

    def resetSkinnedJoints(self, skinJnts=None):
        """ 
                Reset skin deformation for selected joints 
                """
        jntsGiven = False
        if selected():
            selList = hsN.selected()
            selObj = hsNode(selList[0])
            if selObj.isSkinMesh() or selObj.isCurv():
                textField('as_SkinMesh_TF', e=1, tx=(selObj.name()))
            elif selObj.isJnt():
                jntsGiven = True
                jnt_List = [hsNode(jnt) for jnt in selList]
                skinJnts = [jnt for jnt in jnt_List if jnt.nodeType() == 'joint']
                allJntList = [jnt for jnt in skinJnts]
            else:
                HyperSkin.error('Oops.. Selected Is Not A Mesh | Skinned Mesh..!\nYou need to provide Skin_Mesh')
        if not jntsGiven:
            skinMesh = PyNode(textField('as_SkinMesh_TF', q=1, tx=1))
            skinJnts = HyperSkin.getSkinJnts(skinMesh, allInfs=1)
            skinJnts = list(map(hsNode, skinJnts))
        skinJnts = [skinJnts] if type(skinJnts) != list else skinJnts
        HyperSkin.startProgressWin(skinJnts, rv=1)
        for joint in skinJnts:
            skinClusterPlugs = cmds.listConnections((joint + '.worldMatrix[0]'), type='skinCluster', p=1)
            if skinClusterPlugs:
                for skinClstPlug in skinClusterPlugs:
                    index = skinClstPlug[skinClstPlug.index('[') + 1:-1]
                    skinCluster = skinClstPlug[:skinClstPlug.index('.')]
                    curInvMat = cmds.getAttr(joint + '.worldInverseMatrix')
                    attrDisconnected = False
                    try:
                        (cmds.setAttr)(skinCluster + '.bindPreMatrix[{0}]'.format(index), *curInvMat, **{'type': 'matrix'})
                    except:
                        srcCon = cmds.connectionInfo((skinCluster + '.bindPreMatrix[{0}]'.format(index)), sfd=1)
                        if srcCon:
                            pm.disconnectAttr(srcCon, skinCluster + '.bindPreMatrix[{0}]'.format(index))
                            attrDisconnected = True
                            (cmds.setAttr)(skinCluster + '.bindPreMatrix[{0}]'.format(index), *curInvMat, **{'type': 'matrix'})
                            pm.connectAttr(srcCon, (skinCluster + '.bindPreMatrix[{0}]'.format(index)), f=1)
                        else:
                            mel.warning("Can't set bindPreMatrix for this index no: {}".format(index))

            else:
                print('No skinCluster found on {0}'.format(joint))
            HyperSkin.progressWin(joint)

        HyperSkin.endProgressWin(skinJnts, 1)

    def __confirmAction(self, action):
        """
                try:
                        deleteUI ('as_HyperSkinWin')
                except:
                        pass
                """
        confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message=action, button=['Yes'], defaultButton='Yes')
        raise RuntimeError(action)

    def __aboutHyperSkin(self):
        import datetime as dt
        kissMe = str(dt.date.today())
        reObj = re.compile('(?P<Big>[\\d]{4})-(?P<Mid>[\\d]{1,2})-(?P<Small>[\\d]{1,2})')
        testObj = reObj.match(kissMe)
        yearCheck = int(testObj.group('Big'))
        monthCheck = int(testObj.group('Mid'))
        dayCheck = int(testObj.group('Small'))
        lastDay = 21
        lastMonth = 4
        lastYear = 2013
        nextDay = 21
        nextMonth = 5
        nextYear = 2013
        if not yearCheck >= nextYear or monthCheck >= nextMonth or yearCheck > nextYear:
            if dayCheck >= nextDay or monthCheck > nextMonth:
                return False
            if not yearCheck <= lastYear or monthCheck <= lastMonth or yearCheck < lastYear:
                if dayCheck <= lastDay or monthCheck < lastMonth:
                    return False
            return True

    def create_PolyDisc(self, discName, cRadius, jntAxis=None, hideGuides=False, deleteInnerGuide=False):
        HyperSkin._check4Author()
        if not objExists('as_HyperSkin_DSC_Shd'):
            dscShdr = shadingNode('lambert', asShader=1, n='as_HyperSkin_DSC_Shd')
            setAttr((dscShdr + '.color'), 0.0, 0.5, 0.5, type='double3')
            setAttr((dscShdr + '.transparency'), 0.5, 0.5, 0.5, type='double3')
        else:
            dscShdr = 'as_HyperSkin_DSC_Shd'
        ctrlOuter = circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=32, ch=0, n=(discName + '_Outer'))
        scale(cRadius, cRadius, cRadius, r=1)
        HyperSkin.mFreeze(ctrlOuter)
        ctrlInner = circle(c=(0, 0, 0), nr=(1, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01, s=32, ch=0, n=(discName + '_Inner'))
        scale(0.001, 0.001, 0.001, r=1)
        HyperSkin.mFreeze(ctrlInner)
        polyDisc = hsNode(loft((ctrlOuter[0]), (ctrlInner[0]), c=0, ch=0, d=3, ss=3, rsn=True, ar=1, u=1, rn=3, po=1, n=discName)[0])
        setAttr(ctrlOuter[0] + '.overrideEnabled', 1)
        setAttr(ctrlOuter[0] + '.overrideDisplayType', 2)
        setAttr(ctrlInner[0] + '.overrideEnabled', 1)
        setAttr(ctrlInner[0] + '.overrideDisplayType', 2)
        polyDisc.select(r=1)
        hyperShade(dscShdr, assign='as_HyperSkin_DSC_Shd')
        ctrlShape = listRelatives(polyDisc, shapes=1)
        setAttr(ctrlShape[0] + '.castsShadows', 0)
        setAttr(ctrlShape[0] + '.receiveShadows', 0)
        setAttr(ctrlShape[0] + '.motionBlur', 0)
        setAttr(ctrlShape[0] + '.primaryVisibility', 0)
        setAttr(ctrlShape[0] + '.smoothShading', 0)
        setAttr(ctrlShape[0] + '.visibleInReflections', 0)
        setAttr(ctrlShape[0] + '.visibleInRefractions', 0)
        parent(ctrlOuter[0], polyDisc)
        parent(ctrlInner[0], polyDisc)
        polyDisc.select(r=1)
        if jntAxis:
            if not jntAxis == 'x' or jntAxis == '-x':
                pass
            else:
                if jntAxis == 'y' or jntAxis == '-y':
                    polyDisc.setAttr('rz', 90)
                else:
                    if jntAxis == 'z' or jntAxis == '-z':
                        polyDisc.setAttr('ry', 90)
                polyDisc.freeze()
        if hideGuides:
            if deleteInnerGuide:
                delete(ctrlInner[0])
                HyperSkin.hideNodes(ctrlOuter[0])
            else:
                HyperSkin.hideNodes([ctrlOuter[0], ctrlInner[0]])
        return polyDisc

    def snapDisc2SkinMesh(self, jntDisc, skinMesh, snapRotateTo=None, refineDisc=False):
        skinMesh = hsNode(skinMesh)
        jntDisc = hsNode(jntDisc)
        jntDiscGrp = jntDisc.parent()
        jntDiscName = str(jntDisc.shortName())
        skinMesh.setDisplayType(0, 0, 0)
        outCtrl = hsNode(jntDisc + '_Outer')
        inCtrl = hsNode(jntDisc + '_Inner')
        parent(outCtrl, w=1)
        parent(inCtrl, w=1)
        delete(jntDisc)
        cvList = HyperSkin.getVtxList(outCtrl)
        for cv in cvList:
            asCV = cv
            meshPos = HyperSkin.getClosestPos_Dir(outCtrl, cv, skinMesh, False)
            if meshPos:
                asCV.setPos(meshPos)
            else:
                del asCV

        if refineDisc:
            cvDistList = []
            for cv in cvList:
                cvDistList.append(inCtrl.distanceTo(cv)[0])

            avgDist = sum(cvDistList) / float(len(cvDistList))
            for cv in cvList:
                asCV = hsNode(cv)
                cvDist = inCtrl.distanceTo(asCV)[0]
                if cvDist >= avgDist * 1.33:
                    distVal = -avgDist / cvDist
                    avgPos = HyperSkin.get_2PosExtn(asCV, inCtrl, distVal, None, None)
                    asCV.snapPosTo(avgPos)
                else:
                    del asCV

        skinMesh.template(False)
        if not objExists('as_HyperSkin_DSC_Shd'):
            dscShdr = shadingNode('lambert', asShader=1, n='as_HyperSkin_DSC_Shd')
            setAttr((dscShdr + '.color'), 0.0, 0.5, 0.5, type='double3')
            setAttr((dscShdr + '.transparency'), 0.5, 0.5, 0.5, type='double3')
        else:
            dscShdr = 'as_HyperSkin_DSC_Shd'
        jntDisc = hsNode(loft(outCtrl, inCtrl, c=0, ch=0, d=3, ss=3, rsn=True, ar=1, u=1, rn=3, po=1, n=jntDiscName)[0])
        jntDisc.select(r=1)
        HyperSkin.snapPiv_Obj(jntDisc, outCtrl)
        hyperShade(dscShdr, assign='as_HyperSkin_DSC_Shd')
        rotList = HyperSkin.getRot(outCtrl)[0]
        if snapRotateTo:
            dirJnt = hsNode(snapRotateTo)
            dupMesh = jntDisc.duplicate()[0]
            jntDisc.snapRotTo(dirJnt)
            vtxItDSC = jntDisc._MItMeshVertex()
            vtxItDup = dupMesh._MItMeshVertex()
            while not vtxItDSC.isDone():
                pnt = vtxItDup.position(MSpace.kWorld)
                vtxItDSC.setPosition(pnt, MSpace.kWorld)
                next(vtxItDSC)
                next(vtxItDup)

            delete(dupMesh)
        parent(outCtrl, jntDisc)
        delete(inCtrl)
        HyperSkin.hideNodes([outCtrl])
        jntDisc.parentTo(jntDiscGrp)
        return jntDisc

    def as_AboutHyperSkin(self):
        if window('HyperSkinCreditsWin', ex=1):
            deleteUI('HyperSkinCreditsWin')
        if self._mayaVer() < 2016:
            lineType = 'single'
        else:
            lineType = 'double'

        window('HyperSkinCreditsWin', s=False, rtf=1, t='as_HyperSkin_v4.2 Credits..', wh=(150, 150), mxb=0, mnb=0)
        if self._mayaVer() < 2016:
            frameLayout(l='', bs='in')
        else:
            frameLayout(l='')
        columnLayout(adj=5)
        text('\n**as_HyperSkin_v4.2**\n', fn='boldLabelFont')
        text('About :', fn='boldLabelFont', align='left')
        lineType = 'single'
        separator(st=lineType, h=10, w=25)
        text('Author: Yogesh Nichal')
        text('Rigging Artist & Programmer')
        text(l='')
        text('Visit :', fn='boldLabelFont', align='left')
        separator(st=lineType, h=10, w=25)
        text('http://www.yogeshnichal.com')
        text(l='')
        text('Contact :', fn='boldLabelFont', align='left')
        separator(st=lineType, h=10, w=25)
        text('Mail Id: yogeshnichal@gmail.com')
        text(l='')
        text('Copyright (c) as_HyperSkin :', fn='boldLabelFont', align='left')
        separator(st=lineType, h=10, w=25)
        text('** Yogesh Nichal. All Rights Reserved. **')
        text(l='')
        text('Compiled Only For:', fn='boldLabelFont', align='left')
        separator(st=lineType, h=10, w=25)
        text('** ** Yogesh Nichal <yogeshnichal@gmail.com> ** **')
        text(l='')
        separator(st=lineType, h=10, w=25)
        button(l='<< Close >>', c="deleteUI('HyperSkinCreditsWin')")
        separator(st=lineType, h=10, w=25)

        if self._mayaVer() < 2015:
            window('HyperSkinCreditsWin', e=1, wh=(320, 300))
        else:
            window('HyperSkinCreditsWin', e=1, wh=(280, 420))
        showWindow('HyperSkinCreditsWin')
        HyperSkin.refreshView(1)
        pause(sec=3)
        deleteUI('HyperSkinCreditsWin')

    def add_CharPrefix(self, txtFldName):
        HyperSkin._check4Author()
        origObjects = ls(sl=1)
        if len(origObjects) > 0:
            reObj = re.compile('[^_]+_')
            test = reObj.match(str(origObjects[0]))
            prefix = test.group()
            textField(txtFldName, e=1, tx=(str(prefix)))
        else:
            textField(txtFldName, e=1, tx='')

    def add_SidePrefix(self, rePattern, txtFldName):
        HyperSkin._check4Author()
        origObjects = ls(sl=1)
        if len(origObjects) > 0:
            eTst = re.search(rePattern, str(origObjects[0]))
            try:
                sidePrefix = eTst.group()
            except:
                HyperSkin.confirmAction('Found No Side Prefix. Enter Manually .!', True)

            textField(txtFldName, e=1, tx=(str(sidePrefix)))
        else:
            textField(txtFldName, e=1, tx='')

    def add_Selection(self, textFld, multiSelect=False):
        """
                Adds selected object's name as Input in any Window for <== button
                Usage:
                ------
                obj10           # Adds 'obj10' While pressing Enter.. <== button
                box25           # Adds 'box25' While pressing Enter.. <== button
                """
        objects = cmds.ls(sl=1, fl=1)
        if multiSelect:
            if len(objects) > 1:
                textField(textFld, e=1, tx=(', '.join(objects)))
            elif len(objects) == 1:
                textField(textFld, e=1, tx=(objects[0]))
            else:
                textField(textFld, e=1, tx='')
        elif len(objects) > 0:
            textField(textFld, e=1, tx=(objects[0]))
        else:
            textField(textFld, e=1, tx='')

    def add_SkinMesh(self, textFld):
        HyperSkin._check4Author()
        if cmds.checkBox('as_MultipleMeshes_CB', q=1, v=1):
            HyperSkin.add_Selection('as_SkinMesh_TF', True)
            return
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
        if prefixOrSuffix != 'Prefix':
            if prefixOrSuffix != 'Suffix':
                prefixOrSuffix = 'Prefix'
            skinMesh = textField(textFld, q=1, tx=1)
            if '.' in skinMesh:
                skinMesh = skinMesh.split('.')[0]
            if objExists(skinMesh):
                setAttr(skinMesh + '.template', 0)
        objects = selected()
        if len(objects) > 0:
            obj = hsN.selected()[0]
            if '.vtx[' in obj:
                obj = obj.asObj()
                if obj.isShape():
                    obj = obj.parent()
            skinClust = listHistory((obj.shortName()), type='skinCluster')
            if skinClust:
                textField(textFld, e=1, tx=(obj.shortName()))
                jntList = skinCluster((skinClust[0]), wi=1, q=1)
                jntList = list(map(hsNode, jntList))
                sidePrfx_L = None
                leftJnts = []
                for jnt in jntList:
                    if not jnt.isRightSide():
                        if jnt.isMiddleSide():
                            continue
                        else:
                            leftJnts.append(jnt)

                for jnt in jntList:
                    if not jnt.isRightSide():
                        if jnt.isMiddleSide():
                            continue
                        if prefixOrSuffix == 'Prefix':
                            invTst = re.search('^((?<=^)|(^[^Ll][_a-zA-Z\\d]*_))(r_|[rR]ight|Rt|(RT|R)|r)(?(4)([^_a-z]*_|)|_?)', str(jnt))
                            try:
                                invPrfx = invTst.group()
                                continue
                            except:
                                pass

                            eTst = re.search('^((?<=^)|(^[^Rr][_a-zA-Z\\d]*_))(l_|[lL]eft|Lt|(LT|L)|l)(?(4)([^_a-z]*_|)|_?)', str(jnt))
                        else:
                            eTst = re.search('_((?<=^)|(?<=[^_]_))[L|l][^_a-z]*$', str(jnt))
                        try:
                            sidePrfx_L = eTst.group()
                        except:
                            continue

                        if sidePrfx_L:
                            textField('as_LSidePrefix_TF', e=1, tx=(str(sidePrfx_L)))
                            break

                if not sidePrfx_L:
                    textField('as_LSidePrefix_TF', e=1, tx=(str(sidePrfx_L)))
                sidePrfx_R = None
                rightJnts = []
                for jnt in jntList:
                    if not jnt.isLeftSide():
                        if jnt.isMiddleSide():
                            continue
                        else:
                            rightJnts.append(jnt)

                for jnt in jntList:
                    if not jnt.isLeftSide():
                        if jnt.isMiddleSide():
                            continue
                        if prefixOrSuffix == 'Prefix':
                            invTst = re.search('^((?<=^)|(^[^Rr][_a-zA-Z\\d]*_))(l_|[lL]eft|Lt|(LT|L)|l)(?(4)([^_a-z]*_|)|_?)', str(jnt))
                            try:
                                invPrfx = invTst.group()
                                continue
                            except:
                                pass

                            eTst = re.search('^((?<=^)|(^[^Ll][_a-zA-Z\\d]*_))(r_|[rR]ight|Rt|(RT|R)|r)(?(4)([^_a-z]*_|)|_?)', str(jnt))
                        else:
                            eTst = re.search('_((?<=^)|(?<=[^_]_))[R|r][^_a-z]*$', str(jnt))
                        try:
                            sidePrfx_R = eTst.group()
                        except:
                            continue

                        if sidePrfx_R:
                            textField('as_RSidePrefix_TF', e=1, tx=(str(sidePrfx_R)))
                            break

                if not sidePrfx_R:
                    textField('as_RSidePrefix_TF', e=1, tx=(str(sidePrfx_R)))
            else:
                HyperSkin.confirmAction('No SkinCluster Found on %s' % obj.shortName(), True)
        else:
            textField(textFld, e=1, tx='')
        wrongJnts_L = []
        if leftJnts and sidePrfx_L:
            wrongJnts_L = [jnt for jnt in leftJnts if not jnt.shortName().startswith(sidePrfx_L)]
            if wrongJnts_L:
                cmds.select(wrongJnts_L, r=1)
                msgTxt = 'Attention!! [Left Joints]\n\n'
                msgTxt += 'For better results, All left side skinned joints should have same prefix\n'
                msgTxt += 'Please check the selected joints manually for same prefix on all left side joints\n\n'
                cmds.warning(msgTxt)
        elif not sidePrfx_L:
            msgTxt = "Oops ..!!\n\nAuto detection of 'Left Prefix' is not found\nPlease enter it manually\n\n"
            msgTxt += "Ignore if left side joints doesn't exist in bind joints\n"
            cmds.warning(msgTxt)
        if rightJnts and sidePrfx_R:
            wrongJnts_R = [jnt for jnt in rightJnts if not jnt.shortName().startswith(sidePrfx_R)]
            if wrongJnts_R:
                cmds.select(wrongJnts_R, r=1)
                if wrongJnts_L:
                    cmds.select(wrongJnts_L, add=1)
                msgTxt = 'Attention!! [Right Joints]\n\n'
                msgTxt += 'For better results, All right side skinned joints should have same prefix\n'
                msgTxt += 'Please check the selected joints manually for same prefix on all right side joints\n'
                cmds.warning(msgTxt)
        elif not sidePrfx_R:
            msgTxt = "Oops ..!!\n\nAuto detection of 'Right Prefix' is not found\nPlease enter it manually\n\n"
            msgTxt += "Ignore if right side joints doesn't exist in bind joints\n"
            cmds.warning(msgTxt)

    def confirmSkinMesh(self, skinMesh=None):
        """
                return [skinMesh, skinClust[0]]
                """
        if not skinMesh:
            skinMesh = textField('as_SkinMesh_TF', q=1, tx=1)
            if objExists(skinMesh):
                skinMesh = PyNode(skinMesh)
            elif selected():
                skinMesh = selected()[0]
                textField('as_SkinMesh_TF', e=1, tx=(str(skinMesh)))
            else:
                HyperSkin.confirmAction('Skinned Mesh needs to be provided at Skin_Mesh in AHSS window ', True)
        else:
            textField('as_SkinMesh_TF', e=1, tx=(str(skinMesh)))
        asSkinMesh = hsNode(skinMesh)
        skinClust = listHistory(skinMesh, type='skinCluster')
        if not skinClust:
            HyperSkin.error('Oops ..!\n, "%s" is not a Skinned Mesh ..!\nSkinned Mesh needs to be provided at Skin_Mesh in AHSS window' % str(skinMesh))
        reObj = re.compile(asSkinMesh.shortName() + '_\\d+_SC')
        if HyperSkin.extractNum(skinClust[0]) and reObj.match(str(skinClust[0])):
            pass
        else:
            if cmds.objExists('as_HyperSkin_Grp'):
                ahssGrp = hsNode('as_HyperSkin_Grp')
                numGrps = ahssGrp.numChildren()
            else:
                numGrps = 0
            skinClustName = asSkinMesh.shortName() + '_' + '%d' % (numGrps + 1) + '_SC'
            if not objExists(skinClustName):
                rename(skinClust[0], skinClustName)
            else:
                for num in range(numGrps, 200):
                    try:
                        select((asSkinMesh.shortName() + '_' + '%d' % num + '_SC'), r=1)
                    except:
                        rename(skinClust[0], asSkinMesh.shortName() + '_' + '%d' % num + '_SC')
                        break

        skinClust = listHistory(skinMesh, type='skinCluster')
        return [skinMesh, skinClust[0]]

    def selectSkinVertices(self, sidePrefix=None):
        global lastSelectedVtx
        if selected():
            skinMesh = pm.filterExpand(sm=31)
            if not skinMesh:
                skinMesh = selected()[0]
            lastSelectedVtx = HyperSkin.getMeshVtx(skinMesh, sidePrefix)
        else:
            skinMesh = HyperSkin.confirmSkinMesh()[0]
            lastSelectedVtx = HyperSkin.getMeshVtx(skinMesh, sidePrefix)

    def solveEndJnts(self):
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        topJnts = hsN.selected()
        jntList = []
        for topJnt in topJnts:
            jntList.append(topJnt.selectHI('joint')[-1])

        numParents = len(topJnts[0].selectHI('joint')[:-1])
        skinMesh, skinClust = HyperSkin.confirmSkinMesh()
        skinJntList = skinCluster(skinClust, q=1, inf=1)
        for jnt in jntList:
            asJnt = hsNode(jnt)
            prntList = asJnt.pickWalkUp(numParents, 'joint', parentImplied=1)
            if numParents == 1:
                prntList = [prntList]
            else:
                for pJnt in prntList:
                    if pJnt not in skinJntList:
                        if not HyperSkin.isLastJnt(pJnt):
                            HyperSkin.error('%s is not the endJnt of Skin Jnts' % str(jnt))

        if not jntList:
            HyperSkin.error('You need to select atleast one topJnt')
        else:
            jntList = [hsNode(jnt) for jnt in jntList]
        if len(jntList) >= 2:
            for jnt in jntList:
                solveLocName = jnt.shortName() + '_Solve'
                if not jnt.isLastJnt():
                    if not jnt.isJnt():
                        jnt.select(r=1)
                        HyperSkin.error('"%s" is not end Joint .!' % jnt.shortName())
                    else:
                        if objExists(jnt.shortName() + '_Solve'):
                            delete(solveLocName)
                        endLoc = jnt.getPosLoc(True, False, True, jnt.shortName() + '_Solve')[0]
                        endLoc.hide()
                        endLoc.addAttr('numParents', dv=numParents, min=0, max=50, at='double', k=True)

        else:
            for jnt in jntList:
                solveLocName = jnt.shortName() + '_Solve'
                if objExists(solveLocName):
                    delete(solveLocName)
                else:
                    endLoc = jnt.getPosLoc(True, False, True, solveLocName)[0]
                    endLoc.hide()
                    endLoc.addAttr('numParents', dv=numParents, min=0, max=50, at='double', k=True)

            select((jntList[0]), r=1)
            self._selectEndVertices_4Solving()
            return

        def create_FingerVtxSets(endJntList, skinMesh):
            global allVtxSets_ForCheck
            global endVtxSets_Final
            endJntList = [hsNode(jnt) for jnt in endJntList]
            endVtxList = []
            endVtxSets = []
            allVtxSets_ForCheck = []
            HyperSkin.startProgressWin((len(endJntList)), 'Solving End Jnts ..!', None, False, rv=1)
            for jnt in endJntList:
                endVtx = HyperSkin.nearestVtx_OnMesh(jnt, skinMesh)[0]
                endVtxList.append(endVtx)
                if objExists(jnt.shortName() + '_VtxSet'):
                    endVtxSet = PyNode(jnt.shortName() + '_VtxSet')
                else:
                    endVtxSet = sets(endVtx, n=(jnt.shortName() + '_VtxSet'))
                endVtxSets.append(endVtxSet)
                allVtxSets_ForCheck.append(endVtxSet)
                HyperSkin.progressWin(jnt.shortName(), False, _as_HyperSkinMain__showProgressTime)
            HyperSkin.endProgressWin(len(endJntList), 1)
            endVtxSets_Final = []

            def growEndVtx_Sets(endVtxSets):
                currentVtxSet_Dict = {}
                for endVtx_Set in endVtxSets:
                    select(endVtx_Set, r=1)
                    GrowPolygonSelectionRegion()
                    select(endVtx_Set, d=1)
                    currentVtx_Set = filterExpand(sm=31)
                    sets(endVtx_Set, fe=currentVtx_Set)
                    currentVtxSet_Dict[str(endVtx_Set)] = currentVtx_Set
                select(cl=1)
                nonGrowSets_List = []
                for num in range(len(endVtxSets) - 1):
                    for loopNum in range(len(allVtxSets_ForCheck)):
                        if endVtxSets[num] == allVtxSets_ForCheck[loopNum]:
                            continue
                        if endVtxSets[num].intersectsWith(allVtxSets_ForCheck[loopNum]):
                            endVtxSets[num].removeMembers(currentVtxSet_Dict[str(endVtxSets[num])])
                            currentVtxSet = allVtxSets_ForCheck[loopNum]
                            try:
                                allVtxSets_ForCheck[loopNum].removeMembers(currentVtxSet_Dict[str(currentVtxSet)])
                            except:
                                pass
                            if endVtxSets[num] not in endVtxSets_Final:
                                endVtxSets_Final.append(endVtxSets[num])
                            if endVtxSets[num] not in nonGrowSets_List:
                                nonGrowSets_List.append(endVtxSets[num])
                if nonGrowSets_List:
                    for vtxSet in nonGrowSets_List:
                        endVtxSets.remove(vtxSet)
                if len(endVtxSets) > 1:
                    growEndVtx_Sets(endVtxSets)
                else:
                    endVtxSets[-1].removeMembers(currentVtxSet_Dict[str(endVtxSets[-1])])
                    endVtxSets_Final.append(endVtxSets[-1])

            growEndVtx_Sets(endVtxSets)
            allEndVtxDict = {}
            for vSet in endVtxSets_Final:
                try:
                    allEndVtxDict[str(vSet)] = hsNode(vSet.split('_VtxSet')[0])
                except:
                    HyperSkin.deleteUnwanted()
                    HyperSkin.error('No Object Matches Name "%s"' % vSet.split('_VtxSet')[0])
            return allEndVtxDict

        create_FingerVtxSets(jntList, skinMesh)

    def smoothEdgeLoops(self):
        gc.disable()
        cmds.undoInfo(openChunk=True, chunkName='Process Objects')
        eList = cmds.filterExpand(sm=32)
        eList = list(map(hsNode, eList))
        HyperSkin.startProgressWin(len(eList), 'Smoothing Edge Loops !!')
        for edg in eList:
            edg.select()
            mel.eval('SelectEdgeLoopSp;')
            HyperSkin.refreshView(1)
            mel.eval('weightHammerVerts;')
            HyperSkin.progressWin(edg)
            HyperSkin.refreshView(1)

        HyperSkin.endProgressWin(eList, 1)
        cmds.select(eList, r=1)
        cmds.undoInfo(closeChunk=True)

    def smoothNearest(self):
        vtxList = filterExpand(sm=31)
        if vtxList:
            if '.vtx[' not in vtxList[0]:
                HyperSkin.error('Oops.. \nNo Mesh Vertex Is Selected ..')
        else:
            HyperSkin.error('Oops.. \nNo Mesh Vertex Is Selected ..')
        mel.eval('doSmoothSkinWeightsArgList 3 {"0.0001", "5", "0", "0"}')
        mel.GrowPolygonSelectionRegion()
        select((list(set(filterExpand(sm=31)) ^ set(vtxList))), r=1)
        mel.eval('doSmoothSkinWeightsArgList 3 {"0.0001", "5", "0", "0"}')

    def as_EasySmooth(self, vtx=None):
        if vtx:
            cmds.select(vtx, r=1)
            mel.eval('doSmoothSkinWeightsArgList 3 {"0.0001", "5", "0", "0"}')
            return
        vtxList = cmds.filterExpand(sm=31)
        if vtxList:
            if '.vtx[' not in vtxList[0]:
                error('Oops.. \nNo Mesh Vertex Is Selected ..')
        else:
            self.confirmAction('Oops.. \nNo Mesh Vertex Is Selected ..!!\n\nYou need to select at least one skinned vertex\nbefore running the script from button ..!!', True)
        mel.eval('doSmoothSkinWeightsArgList 3 {"0.0001", "5", "0", "0"}')
        GrowPolygonSelectionRegion()
        cmds.select((list(set(filterExpand(sm=31)) ^ set(vtxList))), r=1)
        expandList = cmds.filterExpand(sm=31)
        mel.eval('doSmoothSkinWeightsArgList 3 {"0.0001", "5", "0", "0"}')
        for vtx in vtxList:
            HyperSkin.as_EasySmooth(vtx)

        cmds.select(expandList, r=1)

    def applyObjColor():
        shortArgs = cmds.optionVar(query="HyperSkinApplyColor")

        if not shortArgs:
            return

        if 'cl' in shortArgs:
            ctrlList = shortArgs['cl']
        if 'cn' in shortArgs:
            colorNum = shortArgs['cn']
        if 'lp' in shortArgs:
            LPrefix = shortArgs['lp']
        if 'rp' in shortArgs:
            RPrefix = shortArgs['rp']
        if 'cp' in shortArgs:
            CPrefix = shortArgs['cp']

        if not ctrlList:
            ctrlList = hsN.selected()

        if not ctrlList:
            return

        if type(ctrlList) != list:
            ctrlList = [ctrlList]

        ctrlList = list(map(hsNode, ctrlList))

        for ctrl in ctrlList:
            ctrlShapes = ctrl.getShape() if ctrl.hasAttr("drawOverride") else []

            if LPrefix and ctrl.startswith(LPrefix):
                if ctrl.isCurv():
                    LPrefix = ['L', 6]
                elif ctrl.isJnt():
                    LPrefix = ['L', 5]
                elif ctrl.isMesh():
                    LPrefix = ['L', 6]

            if RPrefix and ctrl.startswith(RPrefix):
                if ctrl.isCurv():
                    RPrefix = ['R', 13]
                elif ctrl.isJnt():
                    RPrefix = ['R', 4]
                elif ctrl.isMesh():
                    RPrefix = ['R', 13]

            if CPrefix and ctrl.startswith(CPrefix):
                if ctrl.isCurv():
                    CPrefix = ['C', 6]
                elif ctrl.isJnt():
                    CPrefix = ['C', 5]
                elif ctrl.isMesh():
                    CPrefix = ['C', 6]

            if ctrl.isCurv():
                setAttr(ctrl + '.overrideEnabled', 1)
                setAttr(ctrl + '.overrideColor', LPrefix[1])
            elif ctrl.isJnt():
                setAttr(ctrl + '.overrideEnabled', 1)
                setAttr(ctrl + '.overrideColor', RPrefix[1])
            elif ctrl.isMesh():
                setAttr(ctrl + '.overrideEnabled', 1)
                setAttr(ctrl + '.overrideColor', 16)

            for shp in ctrlShapes:
                shp.setAttr('overrideEnabled', 1)
                shp.setAttr('overrideColor', LPrefix[1])

            cmds.select(ctrlList, replace=True)
            cmds.select(ctrlList, add=True, ne=True)

    def averageSelectedVtx(self):
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        vtxList = filterExpand(sm=31)
        if vtxList:
            if '.vtx[' not in vtxList[0]:
                if '.e[' not in vtxList[0] or '.f[' not in vtxList[0]:
                    HyperSkin.error('Oops.. \nNo Mesh Vertex, Edges or Faces Are Selected ..')
                else:
                    mel.PolySelectConvert(3)
                    vtxList = filterExpand(sm=31)
        else:
            HyperSkin.error('Oops.. \nNo Mesh Vertex Is Selected ..')
        mel.GrowPolygonSelectionRegion()
        select((list(set(filterExpand(sm=31)) ^ set(vtxList))), r=1)
        extnVtxList = filterExpand(sm=31)
        vtxList = [hsNode(vtx) for vtx in vtxList]
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        allJntList = skinCluster(skinMesh, q=1, inf=1)
        dictList = []
        for extnVtx in extnVtxList:
            vtxDict = {}
            for jnt in allJntList:
                skinVal = skinPercent(skinClust, extnVtx, transform=jnt, q=1)
                if skinVal > 0.001:
                    vtxDict[jnt] = skinVal

            dictList.append(vtxDict)

        finalDict = {}
        for jnt in allJntList:
            avgValList = []
            for valDict in dictList:
                if jnt in valDict:
                    avgValList.append(valDict[jnt])

            if avgValList:
                finalDict[jnt] = sum(avgValList) / 2.0

        avgList = HyperSkin.sortByDict(finalDict, 'down')
        HyperSkin.startProgressWin((len(vtxList)), 'Please Wait ..!', None, False, rv=1)
        for vtxName in vtxList:
            a = 0
            totalVal = 0.0
            for jnt in avgList:
                if a <= 4:
                    setAttr(jnt + '.liw', 0)
                    try:
                        totalVal += finalDict[jnt]
                        skinPercent(skinClust, vtxName, tv=(jnt, finalDict[jnt]))
                    except:
                        pass

                    setAttr(jnt + '.liw', 1)
                else:
                    if totalVal < 1.0:
                        setAttr(jnt + '.liw', 0)
                        try:
                            skinPercent(skinClust, vtxName, tv=(jnt, 1.0 - totalVal))
                        except:
                            pass

                        setAttr(jnt + '.liw', 1)
                    a += 1

            HyperSkin.progressWin(vtxName.name(), False, _as_HyperSkinMain__showProgressTime)

        HyperSkin.endProgressWin(len(vtxList), 1)
        select(vtxList, r=1)

    def averageVtxWeight(self, vtxName, skinMesh, skinClust, allJntList):
        vtxName.select(r=1)
        mel.GrowPolygonSelectionRegion()
        select((list(set(filterExpand(sm=31)) ^ set([vtxName]))), r=1)
        extnVtxList = filterExpand(sm=31)
        dictList = []
        for extnVtx in extnVtxList:
            vtxDict = {}
            for jnt in allJntList:
                skinVal = skinPercent(skinClust, extnVtx, transform=jnt, q=1)
                if skinVal > 0.001:
                    vtxDict[jnt] = skinVal

            dictList.append(vtxDict)

        finalDict = {}
        for jnt in allJntList:
            avgValList = []
            for valDict in dictList:
                if jnt in valDict:
                    avgValList.append(valDict[jnt])

            if avgValList:
                finalDict[jnt] = sum(avgValList) / 2.0

        avgList = HyperSkin.sortByDict(finalDict, 'down')
        a = 0
        totalVal = 0.0
        for jnt in avgList:
            if a <= 4:
                setAttr(jnt + '.liw', 0)
                try:
                    totalVal += finalDict[jnt]
                    skinPercent(skinClust, vtxName, tv=(jnt, finalDict[jnt]))
                except:
                    pass

                setAttr(jnt + '.liw', 1)
            else:
                if totalVal < 1.0:
                    setAttr(jnt + '.liw', 0)
                    try:
                        skinPercent(skinClust, vtxName, tv=(jnt, 1.0 - totalVal))
                    except:
                        pass

                    setAttr(jnt + '.liw', 1)
                a += 1

    def selectSkinJnts(self, wInf=False):
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        if wInf:
            select(skinCluster(skinMesh, q=1, wi=1), r=1)
            jntSet = objExists(HyperSkin.name(skinMesh) + '_WiJnts') or cmds.sets(name=(HyperSkin.name(skinMesh) + '_WiJnts'))
        else:
            select(skinCluster(skinMesh, q=1, inf=1), r=1)
            if not objExists(HyperSkin.name(skinMesh) + '_Jnts'):
                jntSet = cmds.sets(name=(HyperSkin.name(skinMesh) + '_Jnts'))

    def generateCurv(self, curvName, deg=3, step=1, objOrPosList=None, showCVs=True):
        if not objOrPosList:
            objOrPosList = ls(sl=1, fl=1)
        posList = []
        for obj in objOrPosList:
            if HyperSkin._isPosList(obj):
                posList.append(obj)
            else:
                asObj = hsNode(obj)
                posList.append(asObj.getPos())

        numVtx = len(posList)
        reduceList = []
        for num in range(0, numVtx, step):
            reduceList.append(posList[num])

        posList = reduceList
        numVtx = len(posList)
        a = 0
        posDict = {}
        for vtxPos in posList:
            posDict[a] = tuple([round(vtxPos[0], 5), round(vtxPos[1], 5), round(vtxPos[2], 5)])
            if posDict[a] == (0.0, 0.0, 0.0):
                posDict[a] = tuple([round(vtxPos[0], 5), round(vtxPos[1], 5), round(vtxPos[2], 5)])
            else:
                a += 1

        command = 'curve(p=['
        for key in list(posDict.keys()):
            command += str(posDict[key]) + ','

        command = command.strip(',') + '],'
        command += ' k=['
        a = 0
        if deg == 1:
            for num in range(numVtx + deg - 1):
                command += str(a) + ','
                a += 1

        if deg == 2:
            for num in range(numVtx + deg - 1):
                if a < 2:
                    command += '0,'
                elif a >= 2 and a < numVtx - 1:
                    command += str(a - 1) + ','
                else:
                    command += str(numVtx - deg) + ','
                a += 1

        elif deg == 3:
            for num in range(numVtx + deg - 1):
                if a < 3:
                    command += '0,'
                elif a >= 3 and a < numVtx - 1:
                    command += str(a - 2) + ','
                else:
                    command += str(numVtx - deg) + ','
                a += 1

        command = command.strip(',') + '], d=' + str(deg) + ')'
        exec(command)
        rename(selected()[0], curvName)
        curvNode = hsN.selected()[0]
        if showCVs:
            ToggleCVs()
        om.MGlobal.displayInfo(command)
        return curvNode

    def getChild_DSC(self, obj):
        """doc"""
        ncTypes = 'mesh|curv|loc|jnt|trans|^comp'
        obj = hsNode(obj)
        chdList = []
        nameStr = obj.name()
        if obj.attributeQuery('dscChd', n=nameStr, ex=1):
            if obj.attributeQuery('dscChd', n=nameStr, at=1) == 'message':
                chdList = listConnections(nameStr + '.dscChd')
                if chdList:
                    chdStr = chdList[0]
                    if cmds.objExists(str(chdStr)):
                        return hsNode(chdStr)

    def getJntFromDisc(self):
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        skinClustNum = HyperSkin.extractNum(skinClust)[1]
        dscSuffix = '_asSC' + skinClustNum + 'DSC'
        obj = hsN.selected()[0]
        if obj.isMesh():
            jntName = obj.rsplit('_', 1)[0]
            cmds.select(jntName, r=1)
        elif obj.isJnt():
            cmds.select((obj.shortName() + dscSuffix), r=1)

    def getClosestDist(self, vtxName, geoObj):
        HyperSkin._check4Author()
        asVtx = hsNode(vtxName)
        vtxPos = asVtx.getPos()
        toPnt = om.MPoint(vtxPos[0], vtxPos[1], vtxPos[2])
        nearPnt = om.MPoint(0, 0, 0)
        mInt = 0
        asGeo = hsNode(geoObj)
        fnMeshGeo = om.MFnMesh(asGeo._MDagPath())
        try:
            fnMeshGeo.getClosestPoint(toPnt, nearPnt, om.MSpace.kWorld)
        except:
            mVect = om.MVector(0, 0, 0)
            if self._mayaVer() < 2025:
                fnMeshGeo.getClosestPointAndNormal(toPnt, nearPnt, mVect, MSpace.kWorld)
            else:
                (nearPnt, mVect, mInt) = fnMeshGeo.getClosestPointAndNormal(toPnt, MSpace.kWorld)
            del mVect
            del mInt

        return nearPnt.distanceTo(toPnt)

    def selectLastSelectedVtx(self):
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        mel.eval('changeSelectMode -object')
        select(skinMesh, r=1)
        SelectVertexMask()
        select(lastSelectedVtx, r=1)

    def getNearestGeo_orig(self, vtx, geoList):
        HyperSkin._check4Author()
        asVtx = hsNode(vtx)
        distanceDict = {}
        useApi = False
        for geo in geoList:
            vtxPos = asVtx.getPos()
            toPnt = om.MPoint(vtxPos[0], vtxPos[1], vtxPos[2])
            del vtxPos
            nearestPntOnMesh = MPoint(0, 0, 0)
            try:
                if self._mayaVer() <= 2014:
                    geo.getClosestPoint(toPnt, nearestPntOnMesh, MSpace.kWorld)
                else:
                    mVect = om.MVector(0, 0, 0)
                    geo.getClosestPointAndNormal(toPnt, nearestPntOnMesh, mVect, MSpace.kWorld)
                    del mVect
                useApi = True
            except:
                try:
                    asGeo = hsNode(geo)
                    fnMeshGeo = om.MFnMesh(asGeo._MDagPath())
                    if self._mayaVer() < 2025:
                        fnMeshGeo.getClosestPoint(toPnt, nearestPntOnMesh, MSpace.kWorld)
                    else:
                        mVect = om.MVector(0, 0, 0)
                        fnMeshGeo.getClosestPointAndNormal(toPnt, nearestPntOnMesh, mVect, MSpace.kWorld)
                        del mVect
                    del fnMeshGeo
                    del asGeo
                except:
                    continue

            nDist = nearestPntOnMesh.distanceTo(toPnt)
            del nearestPntOnMesh
            del toPnt
            distanceDict[nDist] = geo

        if not distanceDict:
            HyperSkin.deleteUnwanted()
            HyperSkin.error('No GCMs Found..\nMay be selected vertices count is too low..\nTry Again ..')
        shortDist = min(distanceDict.keys())
        if useApi:
            nearObj = hsNode(distanceDict[shortDist].dagPath().fullPathName().split('|')[-1])
        else:
            nearObj = hsNode(distanceDict[shortDist])
        if nearObj.isShape():
            nearObj = nearObj.parent()
        del asVtx
        return nearObj

    def getNearestCurv(self, vtx, curvList):
        HyperSkin._check4Author()
        asVtx = hsNode(vtx)
        distanceDict = {}
        for curv in curvList:
            nearestPntOnMesh = asVtx.nearestPointOn(curv, 'crv', 0)
            nDist = asVtx.distanceTo(nearestPntOnMesh)[0]
            distanceDict[nDist] = curv

        if not distanceDict:
            HyperSkin.error('No GCMs Found..\nMay be selected vertices count is too low..\nTry Again ..')
        shortDist = min(distanceDict.keys())
        nearCurv = hsNode(distanceDict[shortDist]._MDagPath().fullPathName().split('|')[-1])
        del asVtx
        if nearCurv.isShape():
            nearCurv = nearCurv.parent()
        return nearCurv

    def getNearestGeo02(self, vtx, geoList, manageJunk=False):
        gc.disable()
        if manageJunk:
            cmds.undoInfo(openChunk=True, chunkName='Process-Objects')
        HyperSkin._check4Author()
        asVtx = hsNode(vtx)
        counter = 1
        for geo in geoList:
            vtxPos = asVtx.getPos()
            toPnt = om2.MPoint(vtxPos[0], vtxPos[1], vtxPos[2])
            nearestPntOnMesh = om2.MPoint(0, 0, 0)
            (nearestPntOnMesh, _) = geo.getClosestPoint(toPnt, om2.MSpace.kWorld)
            nDist = nearestPntOnMesh.distanceTo(toPnt)
            if counter == 1:
                nearestDist = nDist
                nearObj = geo
            else:
                if nDist < nearestDist:
                    nearestDist = nDist
                    nearObj = geo
                counter += 1

        nearObj = hsNode(nearObj.dagPath().fullPathName().split('|')[-1])
        if nearObj.isShape():
            nearObj = nearObj.parent()
        if manageJunk:
            cmds.undoInfo(closeChunk=True)
        pm.select(vtx, nearObj)
        return nearObj

    def getNearestGeo(self, vtx, geoList, manageJunk=True):
        gc.disable()
        if manageJunk:
            cmds.undoInfo(openChunk=True, chunkName='Process-Objects')
        HyperSkin._check4Author()
        asVtx = hsNode(vtx)
        counter = 1
        for geo in geoList:
            vtxPos = asVtx.getPos()
            toPnt = om.MPoint(vtxPos[0], vtxPos[1], vtxPos[2])
            nearestPntOnMesh = MPoint(0, 0, 0)
            mVect = om.MVector(0, 0, 0)
            geo.getClosestPointAndNormal(toPnt, nearestPntOnMesh, mVect, MSpace.kWorld)
            nDist = nearestPntOnMesh.distanceTo(toPnt)
            if counter == 1:
                nearestDist = nDist
                nearObj = geo
            else:
                if nDist < nearestDist:
                    nearestDist = nDist
                    nearObj = geo
                counter += 1

        nearObj = hsNode(nearObj.dagPath().fullPathName().split('|')[-1])
        if nearObj.isShape():
            nearObj = nearObj.parent()
        if manageJunk:
            cmds.undoInfo(closeChunk=True)
        return nearObj

    def getNearestGeo_(self, vtx, geoList):
        cmds.undoInfo(openChunk=True, chunkName='Process Objects')
        HyperSkin._check4Author()
        asVtx = hsNode(vtx)
        distanceDict = {}
        counter = 1
        gc.disable()
        for geo in geoList:
            vtxPos = asVtx.getPos()
            toPnt = om.MPoint(vtxPos[0], vtxPos[1], vtxPos[2])
            nearestPntOnMesh = MPoint(0, 0, 0)
            mVect = om.MVector(0, 0, 0)
            geo.getClosestPoint(toPnt, nearestPntOnMesh, MSpace.kWorld)
            nDist = nearestPntOnMesh.distanceTo(toPnt)
            distanceDict[nDist] = geo

        if not distanceDict:
            HyperSkin.error('No GCMs Found..\nMay be selected vertices count is too low..\nTry Again ..')
        shortDist = min(distanceDict.keys())
        nearObj = hsNode(distanceDict[shortDist].dagPath().fullPathName().split('|')[-1])
        del asVtx
        if nearObj.isShape():
            nearObj = nearObj.parent()
        return nearObj

    def get_GeoCentricLoc(self, baseLoc, baseGeo, giveLoc=True, gcmSuffix='_asSC1000GCM'):
        baseLoc = PyNode(baseLoc)
        geo1_Loc = HyperSkin.get_ClosestGeoLoc(baseLoc, baseGeo, 'Geo1_Loc')
        extnLoc = HyperSkin.get_2PosExtn(geo1_Loc, baseLoc, 2, 'Extn1_Loc')
        geo2_Loc = HyperSkin.get_ClosestGeoLoc(extnLoc, baseGeo, 'Geo2_Loc')
        centerLoc = HyperSkin.get_2PosExtn(geo1_Loc, geo2_Loc, -0.5, baseLoc.split('|')[-1] + '_' + gcmSuffix + 'Loc')
        delete(extnLoc)
        if nodeType(baseLoc) == 'joint':
            if HyperSkin.isLastJnt(baseLoc):
                longJnt = baseLoc.getParent()
            else:
                chdJntList = baseLoc.getChildren(type='joint')
                if chdJntList:
                    if len(chdJntList) > 1:
                        longJnt = HyperSkin.getLongestObj(baseLoc, chdJntList)
                    else:
                        longJnt = chdJntList[0]
            norm_Loc = HyperSkin.get_NormLoc(centerLoc, longJnt, geo1_Loc, 'Norm1_Loc')
            normGeo1_Loc = HyperSkin.get_ClosestGeoLoc(norm_Loc, baseGeo, 'NormGeo1_Loc')
            normExtnLoc = HyperSkin.get_2PosExtn(normGeo1_Loc, centerLoc, 1, 'Extn2_Loc')
            normGeo2_Loc = HyperSkin.get_ClosestGeoLoc(normExtnLoc, baseGeo, 'NormGeo2_Loc')
            delete(centerLoc)
            delete(geo1_Loc, geo2_Loc)
            CenterLoc = HyperSkin.get_2PosExtn(normGeo1_Loc, normGeo2_Loc, -0.5, baseLoc.split('|')[-1] + '_' + gcmSuffix + 'Loc')
            delete(normExtnLoc, norm_Loc)
            centerLoc = CenterLoc
            delete(normGeo1_Loc, normGeo2_Loc)
        else:
            delete(geo1_Loc, geo2_Loc)
        if giveLoc == True:
            return centerLoc
        locPos = xform(centerLoc, q=1, ws=1, t=1)
        delete(centerLoc)
        return locPos

    def add_NoDiscAttrs(self):
        jntsGiven = False
        if selected():
            selList = hsN.selected()
            selObj = hsNode(selList[0])
            if selObj.isSkinMesh():
                textField('as_SkinMesh_TF', e=1, tx=(selObj.name()))
            elif selObj.isJnt():
                jntsGiven = True
                jnt_List = [hsNode(jnt) for jnt in selList]
                jntList = [jnt for jnt in jnt_List if jnt.nodeType() == 'joint']
                allJntList = [jnt for jnt in jntList]
            else:
                HyperSkin.error('Oops.. Selected Is Not A Mesh | Skinned Mesh..!\nYou need to provide Skin_Mesh')
        if not jntsGiven:
            skinMesh = PyNode(textField('as_SkinMesh_TF', q=1, tx=1))
            jntList = HyperSkin.getSkinJnts(skinMesh, allInfs=1)
            jntList = list(map(hsNode, jntList))
        for jnt in jntList:
            try:
                jnt.setAttr(['v', 'radius'], k=0, channelBox=0)
                jnt.addAttrDivider('___________')
                jnt.addAttrDivider('Blend_Attrs')
                jnt.addAttr('baseBlend', min=0, max=1.0, dv=0, k=1, at='double')
                jnt.addAttr('tailBlend', min=0, max=1.0, dv=0, k=1, at='double')
                jnt.addAttrDivider('________________')
                jnt.addAttrDivider('Volume_Preserve')
                jnt.addAttr('moreVolume', en='None:BaseEnd:TailEnd:BothEnds', at='enum', dv=0, k=1)
                jnt.addAttrDivider()
            except:
                pass

        cmds.select(jntList, r=1)
        HyperSkin.message('Added No Disc Attributes On All Skinned Joints Successfully !!')

    def as_BakeDeformers(self):
        try:
            pass
        except:
            HyperSkin.error("Oops..!!\nIt's not part of HyperSkin\nNeed to purchase 'as_HyperRig'")

        HyperRig.as_BakeDeformers_ToSkinClust()

    def as_CreateGCMs(self):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        _as_HyperSkinMain__freeVersion = 0
        blendVal = 0.0
        refCount = 1
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1).strip()
        if prefixOrSuffix != 'Prefix':
            if prefixOrSuffix != 'Suffix':
                prefixOrSuffix = 'Prefix'
        usingJntAxis = False
        extractGCMs = checkBox('as_ExtractGCMs_CB', q=1, v=1)
        noDiscSkin = cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1)
        excludeJntName = 'Fan'
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1).strip()
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1).strip()
        skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
        jntsGiven = False
        allJntList = []
        if selected():
            selObj = hsNode(selected()[0])
            if selObj.isSkinMesh():
                textField('as_SkinMesh_TF', e=1, tx=(selObj.strip()))
            else:
                if selObj.isJnt():
                    jntsGiven = True
                    jnt_List = [hsNode(jnt) for jnt in selected()]
                    jntList = [jnt for jnt in jnt_List if jnt.nodeType() == 'joint']
                    allJntList = [jnt for jnt in jntList]
                else:
                    HyperSkin.error('Oops.. Selected Is Not A Mesh | Skinned Mesh..!\nYou need to provide Skin_Mesh')
        elif not noDiscSkin:
            if not objExists('as_HyperSkin_GCM_Shd'):
                GCMShader = shadingNode('lambert', asShader=1, n='as_HyperSkin_GCM_Shd')
                setAttr((GCMShader + '.color'), 0.0, 0.5, 0.8, type='double3')
            else:
                GCMShader = 'as_HyperSkin_GCM_Shd'
        skinMesh, skinClust = HyperSkin.confirmSkinMesh()
        existedGCMs = None
        try:
            select(('*_asSC' + HyperSkin.extractNum(skinClust)[1] + 'GCM'), r=1)
            existedGCMs = selected()
        except:
            pass

        if existedGCMs:
            HyperSkin.error('GCMs Are Already Created ..!')
        existedDSCs = None
        try:
            select(('*_asSC' + HyperSkin.extractNum(skinClust)[1] + 'DSC'), r=1)
            existedDSCs = selected()
        except:
            pass

        if existedDSCs:
            if not jntsGiven:
                HyperSkin.error('Jnt Discs Are Already Created ..!')
        select(cl=1)
        if not jntsGiven:
            jnt_List = [hsNode(jnt) for jnt in skinCluster(skinClust, inf=1, q=1)]
            jntList = [jnt for jnt in jnt_List if jnt.nodeType() == 'joint']
            allJntList = [jnt for jnt in jntList]
        skinMesh.select()
        latList = lattice(divisions=(2, 5, 2), ldv=(2, 2, 2), objectCentered=True)
        asLat = hsNode(latList[1])
        asLatShp = latList[0]
        ffdNode = asLat.getOutputs('ffd')
        if ffdNode:
            cmds.setAttr(ffdNode + '.envelope', 0)
        asLat.hide()
        asLat.scaleBy([1.1, 1.1, 1.1])
        asLat.show()
        reduceList = []
        AllJntListRemove = allJntList.remove
        JntListRemove = jntList.remove
        ReduceListAppend = reduceList.append
        for jnt in allJntList:
            splitLocList = jnt.jntSplit(4, nameSufx='_PosLoc', getPos=1, getEnds=1)
            containsLoc = False
            for splitLoc in splitLocList:
                if containsLoc or asLat.contains(splitLoc):
                    containsLoc = True

            if not containsLoc:
                ReduceListAppend(jnt)

        if reduceList:
            if len(reduceList) > 5:
                if HyperSkin.confirmAction('No Of Unwanted Skinned Joints Are More Than {}\nIgnore Unwanted Joints?'.format(len(reduceList))):
                    for jnt in reduceList:
                        AllJntListRemove(jnt)
                        JntListRemove(jnt)

                else:
                    asLat.delete()
                    if usingJntAxis:
                        for jnt in jntList:
                            if not jnt.jntAxis():
                                jnt.startswith(R_Prfx) or jnt.endswith(R_Prfx) or jnt.select(r=1)
                                HyperSkin.error("Joint: '%s' Is Not Aimed Properly.\n" % str(jnt.shortName()))

                    HyperSkin.startProgressWin(jntList, 'Checking Joint Hierarchy !!', rv=1)
                    for baseJnt in jntList:
                        if HyperSkin.isLastJnt(baseJnt):
                            continue
                        else:
                            if prefixOrSuffix == 'Prefix' and not baseJnt.startswith(R_Prfx):
                                if prefixOrSuffix == 'Suffix' and baseJnt.endswith(R_Prfx):
                                    continue
                                else:
                                    chdJnts = baseJnt.getChildren('joint')
                                    chdJnt_ = chdJnts or baseJnt.pickWalkDown(1, 'joint')
                                    if chdJnt_:
                                        cmds.select(chdJnt_, baseJnt, r=1)
                                        HyperSkin.parentChild_ByImplied()
                                        chdJnts = baseJnt.getChildren('joint')
                                    if chdJnts:
                                        numJnts = len(chdJnts)
                                        if numJnts == 1:
                                            chdJnts[0].setSibIndex(0)
                                        else:
                                            for jnt in chdJnts:
                                                if not jnt.isJnt():
                                                    jnt.setSibIndex(numJnts - 1)
                                                else:
                                                    if not (prefixOrSuffix == 'Prefix' and jnt.startswith(L_Prfx)):
                                                        if prefixOrSuffix == 'Suffix':
                                                            if jnt.endswith(L_Prfx):
                                                                jnt.setSibIndex(0)
                                                                break
                                                        jnt.startswith(L_Prfx) or jnt.startswith(R_Prfx) or jnt.endswith(L_Prfx) or jnt.endswith(R_Prfx) or jnt.setSibIndex(0)
                                                        break

                                    else:
                                        select(baseJnt, r=1)
                                        errStr = 'This Joint "%s" doesn\'t have any child / directional joint'
                                        errStr += '\nSolution: Keep the child joint directly under this joint "%s"'
                                        HyperSkin.error(errStr % (str(baseJnt), str(baseJnt)))
                            HyperSkin.progressWin(None, 0, _as_HyperSkinMain__showProgressTime)

                    HyperSkin.endProgressWin(jntList, True)
                    select(jntList, r=1)
                    FrameSelected()
                    skinMesh.setAttr('template', 1)
                    HyperSkin.refreshView(refCount)
                    if noDiscSkin:
                        gcmSuffix = '_asSCnoGCM'
                        dscSuffix = '_asSCnoDSC'
                    else:
                        gcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'GCM'
                        dscSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'DSC'
                    select(cl=1)
                    hyperSkinGrp = group(em=1, n='as_HyperSkin_Grp') if not objExists('as_HyperSkin_Grp') else PyNode('as_HyperSkin_Grp')
                    skinClustNum = HyperSkin.extractNum(skinClust)[1]
                    asMeshGrpName = 'as_' + HyperSkin.name(skinMesh) + '_MeshGrp'
                    asMeshGrp = group(em=1, n=asMeshGrpName, p=hyperSkinGrp) if not objExists(asMeshGrpName) else PyNode(asMeshGrpName)
                    C_GCMGrpName = 'as_C_GCM_SC' + skinClustNum + '_Grp'
                    C_GCMGrp = group(em=1, n=C_GCMGrpName, p=asMeshGrp) if not objExists(C_GCMGrpName) else PyNode(C_GCMGrpName)
                    L_GCMGrpName = 'as_L_GCM_SC' + skinClustNum + '_Grp'
                    L_GCMGrp = group(em=1, n=L_GCMGrpName, p=asMeshGrp) if not objExists(L_GCMGrpName) else PyNode(L_GCMGrpName)
                    C_DSCGrpName = 'as_C_DSC_SC' + skinClustNum + '_Grp'
                    C_DSCGrp = hsNode(group(em=1, n=C_DSCGrpName, p=asMeshGrp)) if not objExists(C_DSCGrpName) else hsNode(C_DSCGrpName)
                    L_DSCGrpName = 'as_L_DSC_SC' + skinClustNum + '_Grp'
                    L_DSCGrp = hsNode(group(em=1, n=L_DSCGrpName, p=asMeshGrp)) if not objExists(L_DSCGrpName) else hsNode(L_DSCGrpName)
                    R_DSCGrpName = 'as_R_DSC_SC' + skinClustNum + '_Grp'
                    R_DSCGrp = hsNode(group(em=1, n=R_DSCGrpName, p=asMeshGrp)) if not objExists(R_DSCGrpName) else hsNode(R_DSCGrpName)
                    clustGrpName = 'as_Clust_SC' + skinClustNum + '_Grp'
                    clustGrp = hsNode(group(em=1, n=clustGrpName, p=asMeshGrp)) if not objExists(clustGrpName) else hsNode(clustGrpName)
                    tempGCMGrp = hsNode(group(em=1, n='as_TempGCM_Grp', p=asMeshGrp)) if not objExists('as_TempGCM_Grp') else hsNode('as_TempGCM_Grp')
                    RHJntList = []
                    lastJntList = []
                    fanSknEndJnts = []
                    excludeJntList = []
                    HyperSkin.startProgressWin(jntList, 'Collecting Joints Info !!', rv=1)
                    for jnt in jntList:
                        asJnt = hsNode(jnt)
                        if not (prefixOrSuffix == 'Prefix' and jnt.startswith(R_Prfx)):
                            if prefixOrSuffix == 'Suffix':
                                if jnt.endswith(R_Prfx):
                                    RHJntList.append(jnt)
                            if prefixOrSuffix == 'Prefix':
                                if (jnt.startswith(R_Prfx) or HyperSkin.isIt_LastSkinJnt)(jnt, jntList) and not jntsGiven:
                                    if HyperSkin.isLastJnt(jnt):
                                        fanSknEndJnts.append(jnt)
                                        continue
                                    lastJntList.append(asJnt.pickWalkDown(1, 'joint'))
                                else:
                                    pass
                                if prefixOrSuffix == 'Suffix' and not jnt.endswith(R_Prfx):
                                    if HyperSkin.isIt_LastSkinJnt(jnt, jntList):
                                        if HyperSkin.isLastJnt(jnt):
                                            fanSknEndJnts.append(jnt)
                                            continue
                                        lastJntList.append(asJnt.pickWalkDown(1, 'joint'))
                                    if excludeJntName in str(jnt):
                                        excludeJntList.append(jnt)
                                    HyperSkin.progressWin(None, 0, _as_HyperSkinMain__showProgressTime)

                    HyperSkin.endProgressWin(jntList, True)
                    jntList = [str(jnt) for jnt in jntList]
                    if fanSknEndJnts:
                        for fanJnt in fanSknEndJnts:
                            jntList.remove(str(fanJnt))

                    if excludeJntList:
                        for exJnt in excludeJntList:
                            jntList.remove(str(exJnt))

                    if RHJntList:
                        for rhJnt in RHJntList:
                            jntList.remove(str(rhJnt))

                    select(fanSknEndJnts, r=1)
                    libPath = sceneName().parent + '/AHSS_Lib'
                    if not os.path.exists(libPath):
                        sysFile(libPath, makeDir=True)
                    lastJntList = []
                    lastJntsAppend = lastJntList.append
                    IsIt_LastSkinJnt = HyperSkin.isIt_LastSkinJnt
                    IsLastJnt = HyperSkin.isLastJnt
                    skipPath = libPath + '/' + skinMesh + '_SkipInfo.txt'
                    if not os.path.exists(skipPath):
                        HyperSkin.startProgressWin((len(allJntList)), 'Updating The Hierarchy ..!!', rv=1)
                        for jnt in allJntList:
                            HyperSkin.progressWin(None, 0, _as_HyperSkinMain__showProgressTime)
                            if IsIt_LastSkinJnt(jnt, allJntList, 0, False, True) and IsLastJnt(jnt):
                                lastJntsAppend(jnt)
                                continue

                        HyperSkin.endProgressWin(1, True)
                        exListStr = ''
                        if lastJntList:
                            exList = [str(jnt) for jnt in lastJntList]
                            exListStr = ', '.join(exList)
                            select(skinMesh, r=1)
                            for lastJnt in lastJntList:
                                try:
                                    skinCluster(skinClust, e=1, ri=(str(lastJnt)))
                                except:
                                    pass

                        fileIO = open(skipPath, 'w')
                        fileIO.writelines(exListStr)
                        fileIO.close()
                    else:
                        with open(skipPath, 'r') as (f):
                            fTxt = f.readline()
                        if fTxt:
                            jntsList = fTxt.split(', ')
                            try:
                                lastJntList = list(map(hsNode, jntsList))
                            except:
                                if HyperSkin.confirmAction('Remove this file "{}"to start Hyper Skin again'.format(skipPath)):
                                    sysFile(skipPath, delete=True)
                                HyperSkin.error('Content of "AHSS_Lib\\{meshName\\}_SkipInfo.txt" has been modified')

                        else:
                            lastJntList = []
                        for jnt in lastJntList:
                            if not IsLastJnt(jnt):
                                try:
                                    os.startfile(mel.toNativePath(libPath))
                                except:
                                    try:
                                        os.system('xdg-open "%s"' % libPath)
                                    except:
                                        subprocess.Popen(['xdg-open', libPath])

                                fileName = skinMesh + '_SkipInfo.txt'
                                skipMsg = 'Oops ..!!\n\nAHSS_Lib Content | Rig Hierarchy has been modified. \n'
                                skipMsg += 'Remove | Backup (By Renaming) The File "{}"\n'.format(fileName)
                                skipMsg += 'And Run \n"Create Hyper Discs" from AHSS UI Again\n\n'
                                skipMsg += 'Error :\n=======\n'
                                skipMsg += '"{}" is not last joint'.format(jnt.name())
                                cmds.setAttr(skinMesh + '.template', 0)
                                HyperSkin.error(skipMsg)

                        select(skinMesh, r=1)
                        for lastJnt in lastJntList:
                            try:
                                skinCluster(skinClust, e=1, ri=(str(lastJnt)))
                            except:
                                pass

                if _as_HyperSkinMain__freeVersion:
                    freeJntList = [jnt for jnt in jntList]
                    if skinSide == 'LT':
                        if prefixOrSuffix == 'Prefix':
                            freeJntList = [jnt for jnt in jntList if not jnt.startswith(R_Prfx)]
            else:
                freeJntList = [jnt for jnt in jntList if not jnt.endswith(R_Prfx)]
        else:
            if skinSide == 'RT':
                if prefixOrSuffix == 'Prefix':
                    freeJntList = [jnt for jnt in jntList if not jnt.startswith(L_Prfx)]
                else:
                    freeJntList = [jnt for jnt in jntList if not jnt.endswith(L_Prfx)]
            cmds.select(freeJntList, r=1)
            jntCount = len(freeJntList)
            if jntCount > 23:
                HyperSkin.deleteUnwanted()
                web.open('https://www.yogeshnichal.com/')
                errorMsg = 'This Is Limited Version Of AHSS !!\nJoints Count (Left | Right & Center) Should Be Less Than 24 ..!'
                errorMsg += '\n\nIf you need unlimited version right now ?  Please reach me at : yogeshnichal.com for more details !!'
                self._as_HyperSkinMain__confirmAction(errorMsg)
                return
            GCMList = []
            DSCList = []
            a = 0
            HyperSkin.startProgressWin((len(jntList)), 'Creating Hyper Discs !!', None, False, rv=1)
            for jnt in jntList:
                jnt = PyNode(jnt)
                asJnt = hsNode(jnt)
                if usingJntAxis:
                    jntAxis = asJnt.jntAxis()[1]
                if HyperSkin.isLastJnt(jnt):
                    jntsGiven or mel.warning(str(jnt) + ' Is End Joint. Skipping..')
                else:
                    if prefixOrSuffix == 'Prefix' and str(jnt).startswith(R_Prfx):
                        toPrint = str(jnt) + ' To Be Mirrored Later. Skipping..'
                        om.MGlobal.displayInfo(toPrint)
                    else:
                        if prefixOrSuffix == 'Suffix' and str(jnt).endswith(R_Prfx):
                            toPrint = str(jnt) + ' To Be Mirrored Later. Skipping..'
                            om.MGlobal.displayInfo(toPrint)
                        else:
                            try:
                                chdJnt = jnt.getChildren(type='joint')[0]
                            except:
                                chdJnt = asJnt.pickWalkDown(1, 'joint')

                if not chdJnt:
                    if jntsGiven:
                        chdJnt = asJnt.parent()
                    else:
                        dist = HyperSkin.mDistance(jnt, chdJnt)[0]
                        try:
                            jntShDist = HyperSkin.getClosestDist(jnt, skinMesh)
                        except:
                            pm.select(jnt, r=1)
                            HyperSkin.error("Can't get the nearest dist for {0} and {1}".format(jnt, skinMesh))

                        chdShDist = HyperSkin.getClosestDist(chdJnt, skinMesh) if chdJnt.endswith('_Jnt') else jntShDist
                        flareRatio = float(chdShDist) / jntShDist
                        if objExists(jnt.name() + dscSuffix):
                            delete(jnt.name() + dscSuffix)
                        if usingJntAxis:
                            polyDisc = HyperSkin.create_PolyDisc(jnt.name() + dscSuffix, jntShDist * 0.2, jntAxis)
                            HyperSkin.snapTo_Obj(polyDisc, jnt)
                        else:
                            polyDisc = HyperSkin.create_PolyDisc(jnt.name() + dscSuffix, jntShDist * 0.2, None)
                            polyDiscGrp = HyperSkin.grpIt(polyDisc)
                            HyperSkin.snapTo_Obj(polyDiscGrp, jnt)
                            aimCon = aimConstraint(chdJnt, polyDiscGrp, worldUpType='none', aimVector=(1,0,0), upVector=(0,1,0), weight=1, offset=(0,0,0))
                            delete(aimCon)
                        polyDisc = HyperSkin.snapDisc2SkinMesh(polyDisc, skinMesh, jnt, refineDisc=False)
                        polyDisc.setAttr(['v'], k=0, channelBox=0)
                        if not noDiscSkin:
                            polyDisc.addAttrDivider('___________')
                            polyDisc.addAttrDivider('Blend_Attrs')
                            polyDisc.addAttr('baseBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
                            polyDisc.addAttr('tailBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
                            polyDisc.addAttrDivider('_____________')
                            polyDisc.addAttrDivider('Replace_Discs')
                            polyDisc.addAttr('copyDisc', en='None:Parent:Child', at='enum', dv=0, k=1)
                            polyDisc.addAttr('discShape', en='None:Circle:Square', at='enum', dv=0, k=1)
                            polyDisc.addAttrDivider('_______')
                            polyDisc.addAttrDivider('Scaling')
                            polyDisc.addAttr('scale_X', en='False:True', at='enum', dv=0, k=1)
                            polyDisc.addAttr('scale_Y', en='False:True', at='enum', dv=0, k=1)
                            polyDisc.addAttr('scale_Z', en='False:True', at='enum', dv=0, k=1)
                            polyDisc.addAttrDivider('____________')
                            polyDisc.addAttrDivider('Orientation')
                            polyDisc.addAttr('snapRotTo', en='None:DiscJoint:Parent:Child:ChildNParent', at='enum', dv=0, k=1)
                            polyDisc.addAttrDivider('________________')
                            polyDisc.addAttrDivider('Volume_Preserve')
                            polyDisc.addAttr('moreVolume', en='None:BaseEnd:TailEnd:BothEnds', at='enum', dv=0, k=1)
                            polyDisc.addAttrDivider()
                        polyDisc.select(r=1)
                        if noDiscSkin:
                            mel.setPolygonDisplaySettings('fNormal')
                            HyperSkin.applyObjColor(polyDisc, LPrefix=[L_Prfx, 6], RPrefix=[L_Prfx, 13])
                        else:
                            hyperShade(GCMShader, assign='as_HyperSkin_GCM_Shd')
                    gcmShp = polyDisc.getShape()
                    setAttr(gcmShp + '.castsShadows', 0)
                    setAttr(gcmShp + '.receiveShadows', 0)
                    setAttr(gcmShp + '.motionBlur', 0)
                    setAttr(gcmShp + '.primaryVisibility', 0)
                    setAttr(gcmShp + '.smoothShading', 0)
                    setAttr(gcmShp + '.visibleInReflections', 0)
                    setAttr(gcmShp + '.visibleInRefractions', 0)
                    HyperSkin.refreshView(refCount)
                    if asJnt.pickWalkDown(1, 'joint') not in jntList and not noDiscSkin:
                        lastChdJnt = asJnt.pickWalkDown(1, 'joint')
                        if not lastChdJnt:
                            if jntsGiven:
                                lastChdJnt = asJnt.parent()
                        else:
                            lastDiscName = lastChdJnt.shortName() + dscSuffix
                            if not pm.objExists(lastDiscName):
                                polyLastDiscGrp = polyDiscGrp.duplicate()[0]
                                polyLastDisc = polyLastDiscGrp.child()
                                HyperSkin.snapTo_Obj(polyLastDiscGrp, jnt)
                                polyLastDisc = polyLastDisc.rename(lastDiscName)
                                polyLastDiscGrp = polyLastDiscGrp.rename(polyLastDisc + '_Grp')
                                polyLastDisc.child(1).rename(polyLastDisc.shortName() + '_Outer')
                                HyperSkin.snapTo_Obj(polyLastDiscGrp, asJnt.pickWalkDown(1, 'joint').shortName())
                                if prefixOrSuffix == 'Prefix':
                                    if not jnt.startswith(L_Prfx) or prefixOrSuffix == 'Suffix' or jnt.endswith(L_Prfx) or polyDisc.endswith(L_Prfx + dscSuffix):
                                        polyLastDiscGrp.parentTo(L_DSCGrp)
                                else:
                                    polyLastDiscGrp.parentTo(C_DSCGrp)
                                polyLastDiscGrp.constrainTo(lastChdJnt)
                                polyLastDiscGrp.scaleBy([0.85, 0.85, 0.85])
                            else:
                                polyDisc._appendTo(DSCList)
                                if not prefixOrSuffix == 'Prefix' or jnt.startswith(L_Prfx) or prefixOrSuffix == 'Suffix' and jnt.endswith(L_Prfx) or polyDisc.endswith(L_Prfx + dscSuffix):
                                    polyDiscGrp.parentTo(L_DSCGrp)
                            polyDiscGrp.parentTo(C_DSCGrp)
                        polyDiscGrp.constrainTo(jnt)
                    a += 1
                    HyperSkin.progressWin('Generating GCM "%s"' % (jnt.name() + gcmSuffix), False, _as_HyperSkinMain__showProgressTime)

            HyperSkin.endProgressWin(len(jntList), True)
            select(DSCList, r=1)
            FrameSelected()
            HyperSkin.message('Generated Hyper Discs Sucessfully !!')

    def as_MirrorGCMs(self):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        refCount = 1
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        skinMesh.setAttr('template', 1)
        skinClustNum = HyperSkin.extractNum(skinClust)[1]

        def unhideNodes(nodeList):
            nodeList = [nodeList] if type(nodeList) != list else nodeList
            for node in [hsNode(obj) for obj in nodeList]:
                node.setAttr('v', lock=0, channelBox=1, keyable=1)
                if node.isMesh():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 0)
                    nodeShape.setAttr('lodVisibility', 1)
                    nodeShape.setAttr('visibility', 1)
                    nodeShape.setAttr('template', 0)
                    nodeShape.setAttr('overrideEnabled', 0)
                    nodeShape.setAttr('overrideDisplayType', 0)
                    nodeShape.setAttr('overrideLevelOfDetail', 0)
                    nodeShape.setAttr('overrideVisibility', 1)
                    nodeShape.setAttr('displayVertices', 0)
                    nodeShape.setAttr('displayUVs', 0)
                if node.isCurv():
                    nodeShape = node.getShape()
                    nodeShape.setAttr('intermediateObject', 0)
                    nodeShape.setAttr('lodVisibility', 1)
                    nodeShape.setAttr('visibility', 1)
                    nodeShape.setAttr('template', 0)
                    nodeShape.setAttr('overrideEnabled', 0)
                    nodeShape.setAttr('overrideDisplayType', 0)
                    nodeShape.setAttr('overrideLevelOfDetail', 0)
                    nodeShape.setAttr('overrideVisibility', 1)
                if HyperSkin.isMesh(node) or HyperSkin.isJnt(node) or node.isCurv():
                    node.setAttr('lodVisibility', 1)
                    node.setAttr('visibility', 1)
                    node.setAttr('template', 0)
                    node.setAttr('overrideEnabled', 0)
                    node.setAttr('overrideDisplayType', 0)
                    node.setAttr('overrideLevelOfDetail', 0)
                    node.setAttr('overrideVisibility', 1)
                if HyperSkin.isJnt(node):
                    node.setAttr('drawStyle', 2)
                    node.setAttr('radius', 0)
                if HyperSkin.isMesh(node):
                    if not objExists('my_Shader'):
                        myShdr = shadingNode('lambert', asShader=1, n='my_Shader')
                        myShdr.setAttr('color', 0, 0, 0, type='double3')
                    else:
                        myShdr = PyNode('my_Shader')
                    select(node, r=1)
                    hyperShade('my_Shader', assign='my_Shader')
                    myShdr.setAttr('transparency', 1, 1, 1, type='double3')

        R_GCMGrpName = 'as_R_DSC_SC' + skinClustNum + '_Grp'
        L_GCMGrpName = 'as_L_DSC_SC' + skinClustNum + '_Grp'
        try:
            delete(R_GCMGrpName)
        except:
            pass

        RGeoGrp = HyperSkin.getDupeNode(L_GCMGrpName, R_GCMGrpName)[0]
        HyperSkin.searchReplaceAll(RGeoGrp, L_Prfx, R_Prfx)
        gcmList = [hsNode(gcm) for gcm in HyperSkin.selectHI(RGeoGrp, 'obj')]
        for gcm in gcmList:
            gcm.setAttr('v', 0)

        HyperSkin.selectHI(RGeoGrp, 'parentConstraint')
        delete()
        HyperSkin.selectHI(RGeoGrp, 'transform')
        curvList = [curv for curv in selected() if curv.endswith('_Outer')]
        unhideNodes(curvList)
        RGeoGrp.setAttr('sx', -1)
        HyperSkin.mFreeze(RGeoGrp)
        for gcm in gcmList:
            jnt = gcm.split('_asSC' + skinClustNum + 'DSC')[0]
            if not objExists(jnt):
                actionStr = 'Check for whether Skin_Mesh, L_Prfx, R_Prfx is entered correctly or not\\hsN._selected "%s" doesn\'t have Joint?\nContinue' % str(gcm)
                if not HyperSkin.confirmAction(actionStr):
                    delete(gcm)
                    continue
            else:
                jnt = PyNode(jnt)
            chdList = jnt.getChildren(type='joint')
            if chdList:
                chdJnt = chdList[0]
            else:
                chdJnt = jnt.getParent()
            HyperSkin.unfreezeRotation(gcm, 0, chdJnt, 'obj')
            polyNormal(gcm, ch=1, userNormalMode=0, normalMode=0)

        HyperSkin.startProgressWin(len(gcmList), 'Mirroring DSCs|GCMs', None, False)
        for gcm in gcmList:
            HyperSkin.progressWin(gcm, False, _as_HyperSkinMain__showProgressTime)
            jnt = gcm.shortName().split('_asSC' + skinClustNum + 'DSC')[0]
            if not objExists(jnt) or HyperSkin.confirmAction("Maya Node '%s' Doesn't  Exists\nContinue?" % jnt):
                pass
            else:
                HyperSkin.hideNodes(curvList)
                delete(RGeoGrp)
                HyperSkin.error('Action Terminated ..!')
            gcm.getParent().snapPosTo(jnt)
            HyperSkin.mConstrain([jnt, gcm.getParent()], 'parent')
            gcm.setAttr('v', 1)
            gcm.select(r=1)
            HyperSkin.refreshView(1)

        HyperSkin.endProgressWin(len(gcmList), True)
        gcmsExists = False
        try:
            select(('*_asSC' + skinClustNum + 'GCM'), r=1)
            gcmsExists = True
        except:
            pass

        if gcmsExists:
            R_GCMGrpName = 'as_R_GCM_SC' + skinClustNum + '_Grp'
            L_GCMGrpName = 'as_L_GCM_SC' + skinClustNum + '_Grp'
            try:
                delete(R_GCMGrpName)
            except:
                pass

            RGeoGrp = HyperSkin.getDupeNode(L_GCMGrpName, R_GCMGrpName)[0]
            HyperSkin.searchReplaceAll(RGeoGrp, L_Prfx, R_Prfx)
            gcmList = HyperSkin.selectHI(RGeoGrp, 'obj')
            for gcm in gcmList:
                gcm.setAttr('v', 0)

            HyperSkin.selectHI(RGeoGrp, 'parentConstraint')
            delete()
            HyperSkin.selectHI(RGeoGrp, 'transform')
            curvList = [curv for curv in selected() if curv.endswith('_Outer')]
            unhideNodes(curvList)
            RGeoGrp.setAttr('sx', -1)
            HyperSkin.mFreeze(RGeoGrp)
            for gcm in gcmList:
                jnt = gcm.split('_asSC' + skinClustNum + 'GCM')[0]
                if not objExists(jnt):
                    HyperSkin.confirmAction('Selected "%s" doesn\'t have Joint' % str(gcm))
                    continue
                else:
                    jnt = PyNode(jnt)
                chdList = jnt.getChildren(type='joint')
                if chdList:
                    chdJnt = chdList[0]
                else:
                    chdJnt = jnt.getParent()
                try:
                    HyperSkin.unfreezeRotation(gcm, 0, chdJnt, 'obj')
                except:
                    pass

                polyNormal(gcm, ch=1, userNormalMode=0, normalMode=0)

            for gcm in gcmList:
                jnt = gcm.split('_asSC' + skinClustNum + 'GCM')[0]
                if not objExists(jnt) or HyperSkin.confirmAction("Maya Node '%s' Doesn't  Exists\nContinue?" % jnt):
                    pass
                else:
                    HyperSkin.hideNodes(curvList)
                    delete(RGeoGrp)
                    HyperSkin.error('Action Terminated ..!')
                HyperSkin.mConstrain([jnt, gcm], 'parent')
                gcm.setAttr('v', 1)
                gcm.select(r=1)
                HyperSkin.refreshView(1)

        HyperSkin.hideNodes(curvList)

    def as_MirrorSelectedGCMs(self):
        gcmList = selected()
        HyperSkin._check4Author()
        refCount = 1
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        skinMesh.setAttr('template', 1)
        skinClustNum = HyperSkin.extractNum(skinClust)[1]
        R_GCMGrpName = 'as_R_GCM_SC' + skinClustNum + '_Grp'
        L_GCMGrpName = 'as_L_GCM_SC' + skinClustNum + '_Grp'
        if not objExists(R_GCMGrpName):
            RGeoGrp = HyperSkin.getDupeNode(L_GCMGrpName, R_GCMGrpName)[0]
            HyperSkin.searchReplaceAll(RGeoGrp, L_Prfx, R_Prfx)
            gcList = HyperSkin.selectHI(RGeoGrp, 'obj')
            for gcm in gcList:
                gcm.setAttr('v', 0)

            HyperSkin.selectHI(RGeoGrp, 'parentConstraint')
            delete()
            RGeoGrp.setAttr('sx', -1)
            HyperSkin.mFreeze(RGeoGrp)
        else:
            RGeoGrp = PyNode(R_GCMGrpName)
        RGcmList = []
        for gcm in gcmList:
            try:
                delete(gcm.replace(L_Prfx, R_Prfx))
                HyperSkin.refreshView(refCount)
            except:
                pass

            (RGcm, RGcmGrp) = HyperSkin.getDupeNode(gcm, gcm.replace(L_Prfx, R_Prfx), False, True, 1)
            delete(parentConstraint(RGcm, q=1, n=1))
            HyperSkin.snapPiv_Obj(RGcmGrp)
            RGcmGrp.setAttr('sx', -1)
            HyperSkin.mFreeze(RGcmGrp)
            parent(RGcm, RGeoGrp)
            RGcmList.append(RGcm)
            delete(RGcmGrp)
            jnt = RGcm.split('_asSC' + skinClustNum + 'GCM')[0]
            if not objExists(jnt):
                actionStr = 'Check for whether Skin_Mesh, L_Prfx, R_Prfx is entered correctly or not\nSelected "%s" doesn\'t have Joint?\nContinue' % str(RGcm)
                HyperSkin.confirmAction(actionStr)
                continue
            else:
                jnt = PyNode(jnt)
            chdList = jnt.getChildren(type='joint')
            if chdList:
                if len(chdList) > 1:
                    chdJnt = HyperSkin.getLongestObj(jnt, chdList)
                else:
                    chdJnt = chdList[0]
                HyperSkin.unfreezeRotation(RGcm, 0, chdJnt, 'obj')
            else:
                jnt.select(r=1)
                HyperSkin.confirmAction('Found No Child Jnt For "%s"' % str(jnt))

        for gcm in RGcmList:
            jnt = gcm.split('_asSC' + skinClustNum + 'GCM')[0]
            HyperSkin.mConstrain([jnt, gcm], 'parent')
            gcm.setAttr('v', 1)
            HyperSkin.refreshView(refCount + 1)

    def as_UpdateGCMs(self):
        HyperSkin._check4Author()
        refCount = 1
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        gcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'GCM'
        dscSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'DSC'
        try:
            select(('*' + dscSuffix), r=1)
        except:
            HyperSkin.confirmAction('Oops.. Found No Hyper Discs !!\nHyper Discs Needs to be Created First !!', True)

        GCMeshes = selected()
        if not GCMeshes:
            HyperSkin.error('Oops ..! \nDSCs are not yet created.')
        for DSC in GCMeshes:
            pCon = parentConstraint(DSC, q=1, n=1)
            try:
                pConTrgt = parentConstraint(pCon, q=1, tl=1)[0]
            except:
                select(DSC, r=1)
                HyperSkin.error('Parent Constraint Is Not Provided On This DSC "%s"' % str(DSC))

            parentConstraint(pConTrgt, pCon, maintainOffset=1, e=1)

        MGlobal.displayInfo('DSCs are updated ..!')

    def updateUI_Options(self):
        if cmds.optionMenu('as_HS_Template_OM', q=1, v=1) == 'EasyRig':
            cmds.textField('as_LSidePrefix_TF', e=1, tx='L_')
            cmds.textField('as_RSidePrefix_TF', e=1, tx='R_')
            cmds.optionMenu('as_PrefixOrSuffix_OM', e=1, v='Prefix')
        else:
            cmds.textField('as_LSidePrefix_TF', e=1, tx='_L')
            cmds.textField('as_RSidePrefix_TF', e=1, tx='_R')
            cmds.optionMenu('as_PrefixOrSuffix_OM', e=1, v='Suffix')
        om.MGlobal.displayInfo('Updated HyperSkin UI options')

    def updateVtxCount(self):
        vtxList = filterExpand(sm=31)
        if vtxList:
            textField('as_VtxCount_TF', e=1, tx=(str(len(vtxList))))
        else:
            textField('as_VtxCount_TF', e=1, tx='None')

    def updateDSCs(self):
        cmds.select('*DSC', r=1)
        for polyDisc in hsN.selected():
            try:
                blendVal = polyDisc.getAttr('blendValue')
                blendMethod = polyDisc.getAttr('blendMethod')
                try:
                    cmds.deleteAttr(polyDisc, at='blendMethod')
                    cmds.deleteAttr(polyDisc, at='blendValue')
                except:
                    HyperSkin.message('Already Updated !!')
                    return
                else:
                    if attributeQuery('baseBlend', n=polyDisc, ex=1):
                        cmds.deleteAttr(polyDisc, at='baseBlend')
                    if attributeQuery('tailBlend', n=polyDisc, ex=1):
                        cmds.deleteAttr(polyDisc, at='tailBlend')
                    polyDisc.addAttrDivider('___________')
                    polyDisc.addAttrDivider('blend_Attrs')
                    if blendMethod == 0:
                        polyDisc.addAttr('baseBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
                        polyDisc.addAttr('tailBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
                    elif blendMethod == 1:
                        polyDisc.addAttr('baseBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
                        polyDisc.addAttr('tailBlend', min=0, max=1.0, dv=0, k=1, at='double')
                    else:
                        if blendMethod == 2:
                            polyDisc.addAttr('baseBlend', min=0, max=1.0, dv=0, k=1, at='double')
                            polyDisc.addAttr('tailBlend', min=0, max=1.0, dv=blendVal, k=1, at='double')
            except:
                pass

            polyDisc.addAttrDivider('_____________')
            polyDisc.addAttrDivider('Replace_Discs')
            polyDisc.addAttr('copyDisc', en='None:Parent:Child', at='enum', dv=0, k=1)
            polyDisc.addAttr('discShape', en='None:Circle:Square', at='enum', dv=0, k=1)
            polyDisc.addAttrDivider('_______')
            polyDisc.addAttrDivider('Scaling')
            polyDisc.addAttr('scale_X', en='False:True', at='enum', dv=0, k=1)
            polyDisc.addAttr('scale_Y', en='False:True', at='enum', dv=0, k=1)
            polyDisc.addAttr('scale_Z', en='False:True', at='enum', dv=0, k=1)
            polyDisc.addAttrDivider('____________')
            polyDisc.addAttrDivider('Orientation')
            polyDisc.addAttr('snapRotTo', en='None:DiscJoint:Parent:Child:ChildNParent', at='enum', dv=0, k=1)
            polyDisc.addAttrDivider('________________')
            polyDisc.addAttrDivider('Volume_Preserve')
            polyDisc.addAttr('moreVolume', en='None:BaseEnd:TailEnd:BothEnds', at='enum', dv=0, k=1)
            polyDisc.addAttrDivider()

        HyperSkin.message('Updated Sucessfully !!')

    def as_ReplaceGCMs(self, snapRot=True, discShape=None):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        refCount = 1
        usingJntAxis = False
        gcMeshes = selected()
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        noDiscSkin = cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1)
        if not objExists('as_HyperSkin_GCM_Shd'):
            GCMShader = shadingNode('lambert', asShader=1, n='as_HyperSkin_GCM_Shd')
            setAttr((GCMShader + '.color'), 0.0, 0.5, 0.8, type='double3')
        else:
            GCMShader = 'as_HyperSkin_GCM_Shd'
        skinDSCGrp = gcMeshes[0].getParent(2)
        if not skinDSCGrp.endswith('_MeshGrp'):
            skinDSCGrp = gcMeshes[0].getParent(3)
        else:
            skinTempGrp = skinDSCGrp.split('as_')[1]
            skinMesh = skinTempGrp.split('_MeshGrp')[0]
            if not objExists(skinMesh):
                HyperSkin.confirmAction('Oops.. Skin Mesh "%s" Not Found | %s has been renamed' % (skinMesh, skinDSCGrp), True)
            else:
                textField('as_SkinMesh_TF', e=1, tx=(str(skinMesh)))
            skinMesh, skinClust = HyperSkin.confirmSkinMesh()
            skinClustNum = HyperSkin.extractNum(skinClust)[1]
            skinMesh.setAttr('template', 1)
            if noDiscSkin:
                gcmSuffix = '_asSCnoGCM'
                dscSuffix = '_asSCnoDSC'
            else:
                gcmSuffix = '_asSC' + skinClustNum + 'GCM'
            dscSuffix = '_asSC' + skinClustNum + 'DSC'
        HyperSkin.refreshView(refCount)
        hyperSkinGrp = group(em=1, n='as_HyperSkin_Grp') if not objExists('as_HyperSkin_Grp') else PyNode('as_HyperSkin_Grp')
        allGCMs = ls('*_asSC' + skinClustNum + 'GCM')
        for gcm in allGCMs:
            gcm.setAttr('v', 0)

        asMeshGrpName = 'as_' + HyperSkin.name(skinMesh) + '_MeshGrp'
        asMeshGrp = group(em=1, n=asMeshGrpName, p=hyperSkinGrp) if not objExists(asMeshGrpName) else PyNode(asMeshGrpName)
        C_GCMGrpName = 'as_C_GCM_SC' + skinClustNum + '_Grp'
        C_GCMGrp = group(em=1, n=C_GCMGrpName, p=asMeshGrp) if not objExists(C_GCMGrpName) else PyNode(C_GCMGrpName)
        L_GCMGrpName = 'as_L_GCM_SC' + skinClustNum + '_Grp'
        L_GCMGrp = group(em=1, n=L_GCMGrpName, p=asMeshGrp) if not objExists(L_GCMGrpName) else PyNode(L_GCMGrpName)
        R_GCMGrpName = 'as_R_GCM_SC' + skinClustNum + '_Grp'
        R_GCMGrp = group(em=1, n=R_GCMGrpName, p=asMeshGrp) if not objExists(R_GCMGrpName) else PyNode(R_GCMGrpName)
        C_DSCGrpName = 'as_C_DSC_SC' + skinClustNum + '_Grp'
        C_DSCGrp = hsNode(group(em=1, n=C_DSCGrpName, p=asMeshGrp)) if not objExists(C_DSCGrpName) else hsNode(C_DSCGrpName)
        L_DSCGrpName = 'as_L_DSC_SC' + skinClustNum + '_Grp'
        L_DSCGrp = group(em=1, n=L_DSCGrpName, p=asMeshGrp) if not objExists(L_DSCGrpName) else PyNode(L_DSCGrpName)
        R_DSCGrpName = 'as_R_DSC_SC' + skinClustNum + '_Grp'
        R_DSCGrp = hsNode(group(em=1, n=R_DSCGrpName, p=asMeshGrp)) if not objExists(R_DSCGrpName) else hsNode(R_DSCGrpName)
        locGrpName = 'as_JntLoc_SC' + skinClustNum + '_Grp'
        locGrp = group(em=1, n=locGrpName, p=asMeshGrp) if not objExists(locGrpName) else PyNode(locGrpName)
        clustGrpName = 'as_Clust_SC' + skinClustNum + '_Grp'
        clustGrp = group(em=1, n=clustGrpName, p=asMeshGrp) if not objExists(clustGrpName) else hsNode(clustGrpName)
        jntList = []
        prevValDict = {}
        for gcMesh in gcMeshes:
            jntName = hsNode(gcMesh.split('_asSC')[0])
            if objExists(jntName):
                jntList.append(PyNode(jntName))
                if len(gcMeshes) == 2:
                    trgtGrp = gcMeshes[1].getParent()
                    polyDiscGrp = hsNode(trgtGrp).duplicate()[0]
                    polyDisc = polyDiscGrp.child()
                    if HyperSkin.isLastJnt(jntName):
                        polyDisc.scaleBy([0.8, 0.8, 0.8])
                        polyDiscGrp.snapRotTo(jntName.parent())
                    else:
                        if snapRot:
                            polyDiscGrp.snapRotTo(jntName)
                        else:
                            HyperSkin.snapTo_Obj(polyDiscGrp, gcMesh)
                            gcMeshName = hsNode(gcMesh).shortName()
                            gcMeshGrp = gcMesh.getParent()
                            if not noDiscSkin:
                                prevBaseBlend = gcMesh.getAttr('baseBlend')
                                prevTailBlend = gcMesh.getAttr('tailBlend')
                                prevCopyDisc = gcMesh.getAttr('copyDisc')
                                prevDiscShape = gcMesh.getAttr('discShape')
                                prevSnapXYZ = gcMesh.getAttr('snapRotTo')
                                prevMoreVolume = gcMesh.getAttr('moreVolume')
                                prevScaleX = gcMesh.getAttr('scale_X')
                                prevScaleY = gcMesh.getAttr('scale_Y')
                                prevScaleZ = gcMesh.getAttr('scale_Z')
                            else:
                                if gcMeshGrp.endswith('_Grp'):
                                    delete(gcMeshGrp)
                                else:
                                    delete(gcMesh)
                                polyDisc = polyDisc.rename(gcMeshName)
                                polyDiscGrp = polyDiscGrp.rename(gcMeshName + '_Grp')
                                polyDisc.child(1).rename(polyDisc.shortName() + '_Outer')
                                try:
                                    polyDisc.child(2).deleteNode()
                                except:
                                    pass

                                chdList = polyDiscGrp.getChildren()
                                for chd in chdList:
                                    if chd.nodeType() == 'parentConstraint':
                                        chd.deleteNode()

                                polyDiscGrp.constrainTo(jntName)
                                if polyDiscGrp.startswith(L_Prfx):
                                    if polyDiscGrp.parent() != L_DSCGrp:
                                        parent(polyDiscGrp, L_DSCGrp)
                                elif polyDiscGrp.startswith(R_Prfx):
                                    if polyDiscGrp.parent() != R_DSCGrp:
                                        parent(polyDiscGrp, R_DSCGrp)
                                elif polyDiscGrp.parent() != C_DSCGrp:
                                    parent(polyDiscGrp, C_DSCGrp)
                            if snapRot:
                                polyDisc.snapRotTo(polyDiscGrp)
                            noDiscSkin or polyDisc.setAttr('baseBlend', prevBaseBlend)
                            polyDisc.setAttr('tailBlend', prevTailBlend)
                            polyDisc.setAttr('copyDisc', prevCopyDisc)
                            polyDisc.setAttr('discShape', prevDiscShape)
                            polyDisc.setAttr('snapRotTo', prevSnapXYZ)
                            polyDisc.setAttr('moreVolume', prevMoreVolume)
                            polyDisc.setAttr('scale_X', prevScaleX)
                            polyDisc.setAttr('scale_Y', prevScaleY)
                            polyDisc.setAttr('scale_Z', prevScaleZ)
                        if noDiscSkin:
                            HyperSkin.applyObjColor(polyDisc, LPrefix=[L_Prfx, 6], RPrefix=[L_Prfx, 13])
                            polyDisc.select(r=1)
                            mel.setPolygonDisplaySettings('fNormal')
                        return
                if not noDiscSkin:
                    prevBaseBlend = gcMesh.getAttr('baseBlend')
                    prevTailBlend = gcMesh.getAttr('tailBlend')
                    prevCopyDisc = gcMesh.getAttr('copyDisc')
                    prevDiscShape = gcMesh.getAttr('discShape')
                    prevSnapXYZ = gcMesh.getAttr('snapRotTo')
                    prevMoreVolume = gcMesh.getAttr('moreVolume')
                    prevScaleX = gcMesh.getAttr('scale_X')
                    prevScaleY = gcMesh.getAttr('scale_Y')
                    prevScaleZ = gcMesh.getAttr('scale_Z')
                if not HyperSkin.isLastJnt(jntName) or discShape:
                    if not noDiscSkin:
                        prevBaseBlend = gcMesh.getAttr('baseBlend')
                        prevTailBlend = gcMesh.getAttr('tailBlend')
                        prevValDict[gcMesh.shortName()] = [prevTailBlend, prevBaseBlend]
                    else:
                        gcMeshGrp = gcMesh.getParent()
                        if gcMeshGrp.endswith('_Grp'):
                            delete(gcMeshGrp)
                        else:
                            delete(gcMesh)
            else:
                HyperSkin.confirmAction('For "%s", "%s" not exists ..!' % (gcMesh, jntName), True)

        select(cl=1)
        GCMList = []
        a = 0
        HyperSkin.startProgressWin(len(jntList), 'Please Wait ..!', None, False)
        for jnt in jntList:
            jnt = PyNode(jnt)
            asJnt = hsNode(jnt)
            if HyperSkin.isLastJnt(jnt):
                discShape or mel.warning(str(jnt) + ' Is End Joint. Skipping..')
            else:
                if R_Prfx in str(jnt):
                    toPrint = str(jnt) + ' To Be Mirrored Later. Skipping..'
                    om.MGlobal.displayInfo(toPrint)
                else:
                    chdJnts = asJnt.getChildren(type='joint')
                    if chdJnts:
                        chdJnt = chdJnts[0]
                    else:
                        chdJnt = asJnt.parent()
                        if not chdJnt:
                            continue
                        else:
                            dist = HyperSkin.mDistance(jnt, chdJnt)[0]
                            jntShDist = HyperSkin.getClosestDist(jnt, skinMesh)
                            chdShDist = HyperSkin.getClosestDist(chdJnt, skinMesh) if chdJnt.endswith('_Jnt') else jntShDist
                            flareRatio = float(chdShDist) / jntShDist
                            if usingJntAxis:
                                polyDisc = HyperSkin.create_PolyDisc(jnt.name() + dscSuffix, jntShDist * 2, jntAxis, True, True)
                                HyperSkin.snapTo_Obj(polyDisc, jnt)
                                polyDisc.constrainTo(asJnt)
                            else:
                                polyDisc = hsNode(HyperSkin.create_PolyDisc(jnt.name() + dscSuffix, jntShDist * 2, None, True, True))
                                polyDiscGrp = polyDisc.grpIt()[0]
                                HyperSkin.snapTo_Obj(polyDiscGrp, jnt)
                                aimCon = aimConstraint(chdJnt, polyDiscGrp, worldUpType='none', aimVector=(1,0,0), upVector=(0,1,0), weight=1, offset=(0,0,0))
                                delete(aimCon)
                                polyDiscGrp.constrainTo(asJnt)
                            blendVal = 0
                            polyDisc.setAttr(['v'], k=0, channelBox=0)
                            if not noDiscSkin:
                                polyDisc.addAttrDivider('___________')
                                polyDisc.addAttrDivider('blend_Attrs')
                                polyDisc.addAttr('baseBlend', min=0, max=1.0, dv=prevBaseBlend, k=1, at='double')
                                polyDisc.addAttr('tailBlend', min=0, max=1.0, dv=prevTailBlend, k=1, at='double')
                                polyDisc.addAttrDivider('_____________')
                                polyDisc.addAttrDivider('Replace_Discs')
                                polyDisc.addAttr('copyDisc', en='None:Parent:Child', at='enum', dv=prevCopyDisc, k=1)
                                polyDisc.addAttr('discShape', en='None:Circle:Square', at='enum', dv=prevDiscShape, k=1)
                                polyDisc.addAttrDivider('_______')
                                polyDisc.addAttrDivider('Scaling')
                                polyDisc.addAttr('scale_X', en='False:True', at='enum', dv=prevScaleX, k=1)
                                polyDisc.addAttr('scale_Y', en='False:True', at='enum', dv=prevScaleY, k=1)
                                polyDisc.addAttr('scale_Z', en='False:True', at='enum', dv=prevScaleZ, k=1)
                                polyDisc.addAttrDivider('____________')
                                polyDisc.addAttrDivider('Orientation')
                                polyDisc.addAttr('snapRotTo', en='None:DiscJoint:Parent:Child:ChildNParent', at='enum', dv=prevSnapXYZ, k=1)
                                polyDisc.addAttrDivider('________________')
                                polyDisc.addAttrDivider('Volume_Preserve')
                                polyDisc.addAttr('moreVolume', en='None:BaseEnd:TailEnd:BothEnds', at='enum', dv=prevMoreVolume, k=1)
                                polyDisc.addAttrDivider()
                            else:
                                if noDiscSkin:
                                    HyperSkin.applyObjColor(polyDisc, LPrefix=[L_Prfx, 6], RPrefix=[L_Prfx, 13])
                                    polyDisc.select(r=1)
                                    mel.setPolygonDisplaySettings('fNormal')
                                    cmds.select(cl=1)
                                if polyDiscGrp.startswith(L_Prfx):
                                    parent(polyDiscGrp, L_DSCGrp)
                                else:
                                    if polyDiscGrp.startswith(R_Prfx):
                                        parent(polyDiscGrp, R_DSCGrp)
                                    else:
                                        parent(polyDiscGrp, C_DSCGrp)
                        GCMList.append(polyDisc)
            a += 1
            HyperSkin.progressWin('Generating Inner Mesh', False, _as_HyperSkinMain__showProgressTime)

        HyperSkin.endProgressWin(len(jntList), True)
        select(GCMList, r=1)

    def as_DeleteGCMs(self):
        HyperSkin._check4Author()
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        if HyperSkin.confirmAction('Delete All GCMs Relating To %s' % str(skinMesh)):
            asMeshGrpName = 'as_' + HyperSkin.name(skinMesh) + '_MeshGrp'
            if objExists(asMeshGrpName):
                delete(asMeshGrpName)
            else:
                HyperSkin.confirmAction('%s Has No GCMs ..!' % str(skinMesh), True)

    def isIt_LastSkinJnt(self, jnt, skinJntList, numFromEnd=0, useSeries=False, hsNodes_given=False):
        jnt = hsNode(jnt)
        skinJntList = [hsNode(sknJnt) for sknJnt in skinJntList] if (not hsNodes_given) else skinJntList
        skinJntsSet = set(skinJntList)
        if jnt.nodeType() != 'joint':
            return False
        if jnt not in skinJntsSet:
            return False
        if not any([jnt.isParentOf(sknJnt) for sknJnt in skinJntsSet]):
            if not numFromEnd:
                return True
            hiJntList = HyperSkin.selectHI(jnt, 'jnt', topSelect=False)
            if hiJntList:
                hiJntList = list(map(hsNode, hiJntList))
            if numFromEnd == 0:
                chdList = jnt.getChildren()
                if not chdList:
                    if useSeries:
                        if jnt.nextSeriesNode():
                            if jnt.nextSeriesNode() in skinJntsSet:
                                return False
                            return True
                        else:
                            return True
                    else:
                        return True
                if hiJntList:
                    hiCheck = True
                    for endJnt in hiJntList:
                        if endJnt in skinJntsSet:
                            hiCheck = False
                            break

                    return hiCheck
                return True
            if hiJntList:
                endSknJntList = []
                for endJnt in hiJntList:
                    if endJnt in skinJntsSet:
                        endSknJntList.append(endJnt)

                if endSknJntList:
                    if len(endSknJntList) == numFromEnd:
                        return True
                    return False
                else:
                    return False
            return False

    def getSkinJntsList(self, vtxList):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        jntList = skinCluster((vtxList[0]), q=1, wi=1)
        skinClust = listHistory((vtxList[0].split('.')[0]), type='skinCluster')[0]
        skinJnts = []
        HyperSkin.startProgressWin(len(vtxList), 'Plese Wait ..!', None, False)
        for vtx in vtxList:
            HyperSkin.progressWin(str(vtx), False, _as_HyperSkinMain__showProgressTime)
            for jnt in jntList:
                if jnt not in skinJnts:
                    if skinPercent(skinClust, vtx, q=1, t=jnt) > 0.5:
                        select(jnt, r=1)
                        HyperSkin.refreshView(1)
                        skinJnts.append(jnt)

        HyperSkin.endProgressWin(len(vtxList), 1)
        select(skinJnts, r=1)
        return skinJnts

    def as_ToggleSkinMesh(self):
        HyperSkin._check4Author()
        skinMesh = cmds.textField('as_SkinMesh_TF', q=1, tx=1)
        if not cmds.objExists(skinMesh):
            HyperSkin.confirmAction('Enter Skinned Mesh Only..!', True)
        if cmds.getAttr(skinMesh + '.template'):
            cmds.setAttr(skinMesh + '.template', 0)
        else:
            cmds.setAttr(skinMesh + '.template', 1)

    def as_ToggleSkinJnts(self):
        HyperSkin._check4Author()
        skinMesh = cmds.textField('as_SkinMesh_TF', q=1, tx=1)
        if not cmds.objExists(skinMesh):
            HyperSkin.confirmAction('Enter Skinned Mesh Only..!', True)
        skinJnts = HyperSkin.getSkinJnts(skinMesh)
        if skinJnts:
            for skinJnt in skinJnts:
                if cmds.getAttr(skinJnt + '.template'):
                    cmds.setAttr(skinJnt + '.template', 0)
                else:
                    cmds.setAttr(skinJnt + '.template', 1)

        cmds.select(skinJnts, r=1)

    def as_ToggleInMesh(self, endSuffix):
        HyperSkin._check4Author()
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        jntList = skinCluster(skinClust, q=1, wi=1)
        dscOrGcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + endSuffix
        cmds.select('*DSC', r=1)
        inMeshList = selected()
        if not inMeshList:
            HyperSkin.confirmAction('Found No %ss' % endSuffix, True)
        if getAttr(inMeshList[0] + '.v'):
            for inMesh in inMeshList:
                try:
                    setAttr(inMesh + '.v', 0)
                except:
                    pass

        else:
            for inMesh in inMeshList:
                try:
                    setAttr(inMesh + '.v', 1)
                except:
                    pass

        select(inMeshList, r=1)

    def as_LockJoints(self, jntList=None, skinMesh=None, lockAll=0, unlockAll=0, invLock=1):
        if not jntList:
            jntList = hsN.selected()
        jntList = list(map(hsNode, jntList))
        if not skinMesh:
            skinMesh = HyperSkin.confirmSkinMesh()[0]
        skinMesh = hsNode(skinMesh)
        jntListAll = skinMesh.getSkinJnts()[0]
        if lockAll:
            for jnt in jntListAll:
                jnt.setAttr('liw', 1)

            return
        if unlockAll:
            for jnt in jntListAll:
                jnt.setAttr('liw', 0)

            return
        for jnt in jntListAll:
            if invLock:
                if jnt in jntList:
                    jnt.setAttr('liw', 0)
                else:
                    jnt.setAttr('liw', 1)
            elif jnt in jntList:
                jnt.setAttr('liw', 1)
            else:
                jnt.setAttr('liw', 0)

    def as_MakeVisibleGCM(self, endSuffix, makeVis=True):
        HyperSkin._check4Author()
        skinMesh = PyNode(textField('as_SkinMesh_TF', q=1, tx=1))
        skinClust = listHistory(skinMesh, type='skinCluster')
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        if not skinClust:
            HyperSkin.confirmAction('Initial Skinning Is Required On "%s" ..!' % str(skinMesh), True)
        else:
            jntList = skinCluster((skinClust[0]), q=1, wi=1)
        gcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + endSuffix
        gcmList = []
        for jnt in jntList:
            if objExists(jnt + gcmSuffix):
                gcmList.append(jnt + gcmSuffix)

        if not gcmList:
            HyperSkin.confirmAction('Oops!!\nFound No GCMs', True)
        for gcm in gcmList:
            try:
                setAttr(gcm + '.v', makeVis)
            except:
                pass

    def _selectNearestFaces(self):
        global selectedGCM

        def getModelPanel():
            for panel in getPanel(all=1):
                try:
                    if modelPanel(panel, q=1, camera=1) == lookThru(q=1):
                        return modelPanel(panel, q=1, me=1)
                except:
                    pass

        selectedGCM = selected()
        if not selectedGCM:
            confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message='Cancelled Action.. Select GCM For Editing ..!', button=['OK'], defaultButton='OK')
            raise RuntimeError('Select GCM For Editing ..!')
        else:
            selectedGCM = selectedGCM[0]
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        skinMesh.setAttr('template', 0)
        mPanel = getModelPanel()
        modelEditor(mPanel, e=1, allObjects=0)
        modelEditor(mPanel, e=1, polymeshes=1)
        modelEditor(mPanel, e=1, joints=1)
        jntList = skinCluster(skinClust, wi=1, q=1)
        if jntList:
            for jnt in jntList:
                asJnt = hsNode(jnt)
                asJnt.template(False)

        gcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'GCM'
        if not selectedGCM.endswith(gcmSuffix):
            confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message='Cancelled Action.. Select "GCM Only" For Editing ..!', button=['OK'], defaultButton='OK')
            raise RuntimeError("Select 'GCM Only' For Editing ..!")
        HyperSkin.as_MakeVisibleGCM('GCM', False)
        HyperSkin.as_MakeVisibleGCM('DSC', False)
        select(skinMesh, r=1)
        mel.SelectFacetMask()
        melGlobals.initVar('string', 'gLasso')
        setToolTo(melGlobals['gLasso'])

    def _snap2NearestFaces(self):
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        skinMesh.setAttr('template', 0)
        gcmParent = selectedGCM.getParent()
        origGCMName = HyperSkin.name(selectedGCM)
        origName = HyperSkin.name(skinMesh)
        origClustName = skinClust.name()
        origJnts = skinCluster(skinClust, wi=1, q=1)
        if skinMesh.getParent():
            origSkinGrp = skinMesh.getParent()
        else:
            origSkinGrp = None
        DuplicateFace()
        dupList = [obj for obj in selected() if nodeType(obj) == 'transform']
        mel.DeleteHistory()
        if origSkinGrp:
            for dupObj in dupList:
                parent(dupObj, origSkinGrp)

        else:
            for dupObj in dupList:
                parent(dupObj, w=1)

        delete(skinMesh)
        areaDict = {}
        for obj in dupList:
            areaDict[polyEvaluate(obj, a=1)] = obj

        origMesh = areaDict[max(areaDict.keys())]
        origMesh.rename(origName)
        skinMesh = origMesh
        dupList.remove(origMesh)
        snapType = optionMenu('as_SnapType_OM', q=1, v=1)
        for reqdGCM in dupList:
            if snapType == 'Exact':
                pause(sec=2)
                polyReduce(reqdGCM, keepQuadsWeight=1, keepBorder=1, keepMapBorder=1, keepHardEdge=1, keepOriginalVertices=0, uvWeights=0, triangulate=0, cachingReduce=1, ch=1, compactness=1.0, replaceOriginal=1, percentage=10, colorWeights=0)
            elif snapType == 'High':
                polyReduce(reqdGCM, keepQuadsWeight=1, keepBorder=1, keepMapBorder=1, keepHardEdge=1, keepOriginalVertices=0, uvWeights=0, triangulate=0, cachingReduce=1, ch=1, compactness=1.0, replaceOriginal=1, percentage=30, colorWeights=0)
            else:
                if snapType == 'Medium':
                    polyReduce(reqdGCM, keepQuadsWeight=1, keepBorder=1, keepMapBorder=1, keepHardEdge=1, keepOriginalVertices=0, uvWeights=0, triangulate=0, cachingReduce=1, ch=1, compactness=1.0, replaceOriginal=1, percentage=50, colorWeights=0)
            if snapType == 'Low':
                polyReduce(reqdGCM, keepQuadsWeight=1, keepBorder=1, keepMapBorder=1, keepHardEdge=1, keepOriginalVertices=0, uvWeights=0, triangulate=0, cachingReduce=1, ch=1, compactness=1.0, replaceOriginal=1, percentage=70, colorWeights=0)

        reqdGCM = None
        for fMesh in dupList:
            select(fMesh, r=1)
            HyperSkin.refreshView(1)
            if HyperSkin.confirmAction('This is what you want ..?'):
                reqdGCM = selected()[0]
                break
            continue

        if not reqdGCM:
            for fMesh in dupList:
                select(fMesh, r=1)
                HyperSkin.refreshView(1)
                if HyperSkin.confirmAction('This is what you want ..?'):
                    reqdGCM = selected()[0]
                    break
                continue

        if not reqdGCM:
            delete(dupList)
            select(origJnts, skinMesh, r=1)
            SmoothBindSkin()
            mel.eval('changeSelectMode -object')
            skinClust = listHistory(skinMesh, type='skinCluster')[0]
            skinClust.rename(origClustName)
            HyperSkin.confirmAction('Cancelled Action\nTry Again With Another Snap Option\nBest Of Luck :)', True)
        else:
            dupList.remove(reqdGCM)
            if dupList:
                delete(dupList)
        delete(selectedGCM)
        reqdGCM.rename(origGCMName)
        parent(reqdGCM, gcmParent)
        select(origJnts, skinMesh, r=1)
        SmoothBindSkin()
        skinClust = listHistory(skinMesh, type='skinCluster')[0]
        skinClust.rename(origClustName)
        if not objExists('as_HyperSkin_GCM_Shd'):
            GCMShader = shadingNode('lambert', asShader=1, n='as_HyperSkin_GCM_Shd')
            setAttr((GCMShader + '.color'), 0.0, 0.5, 0.8, type='double3')
        else:
            GCMShader = 'as_HyperSkin_GCM_Shd'
        jntList = skinCluster(skinClust, wi=1, q=1)
        if jntList:
            for jnt in jntList:
                asJnt = hsNode(jnt)
                asJnt.setDisplayType(0, 0, 0)

        select(reqdGCM, r=1)
        hyperShade(GCMShader, assign='as_HyperSkin_GCM_Shd')
        mel.eval('changeSelectMode -object')

    def _selectEndVertices_4Solving(self):
        global selectedJnt_Solved
        selectedJnt_Solved = hsN.selected()
        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
        select(skinMesh, r=1)
        nVtx = HyperSkin.nearestVtx_OnMesh(selectedJnt_Solved, skinMesh)[0]
        skinMesh.select(r=1)
        mel.SelectVertexMask()
        select(nVtx, r=1)

    def _createVtxSet_Solved(self):
        vtxList = filterExpand(sm=31)
        selList = hsN.selected()[-1]
        selList = HyperSkin.selectHI(selList, 'joint')
        selList = list(map(hsNode, selList))
        selectedJnt = selList[-1]
        if selectedJnt.nodeType() != 'joint':
            HyperSkin.error('Selected object is not joint')
        vtxSetName = selectedJnt.shortName() + '_VtxSet'
        if objExists(vtxSetName):
            delete(vtxSetName)
        if objExists(selectedJnt.shortName() + '_Solve'):
            delete(selectedJnt.shortName() + '_Solve')
        endLoc = selectedJnt.getPosLoc(True, False, True, selectedJnt.shortName() + '_Solve')[0]
        endLoc.hide()
        endLoc.addAttr('numParents', dv=(len(selList) - 1), min=0, max=100, at='double', k=True)
        cmds.select(vtxList, r=1)
        sets(vtxList, n=vtxSetName)
        mel.eval('changeSelectMode -object')

    def as_DoReSkin(self):
        HyperSkin._check4Author()
        skinMesh = PyNode(textField('as_SkinMesh_TF', q=1, tx=1))
        skinClust = listHistory(skinMesh, type='skinCluster')
        if skinClust:
            skinClust = skinClust[0]
            skinClustName = skinClust.name()
        else:
            HyperSkin.confirmAction('Initial Skinning Required!! \nThen Re-Skinning Can Be Done:)')
        jntList = skinCluster(skinClust, inf=1, q=1)
        skinMesh.select(r=1)
        mel.doDetachSkin('2', ['1', '1'])
        select(jntList, r=1)
        skinMesh.select(add=1)
        SmoothBindSkin()
        skinClust = listHistory(skinMesh, type='skinCluster')[0]
        skinClust.rename(skinClustName)
        HyperSkin.reorderDeformers(str(skinMesh), ['deltaMush', 'skinCluster'])
        select(jntList, r=1)

    def hideNodes(self, nodeList):
        nodeList = [nodeList] if type(nodeList) != list else nodeList
        for node in [hsNode(obj) for obj in nodeList]:
            if node.isMesh():
                nodeShape = node.getShape()
                nodeShape.setAttr('intermediateObject', 1)
                nodeShape.setAttr('lodVisibility', 0)
                nodeShape.setAttr('visibility', 0)
                nodeShape.setAttr('template', 1)
                nodeShape.setAttr('overrideEnabled', 1)
                nodeShape.setAttr('overrideDisplayType', 1)
                nodeShape.setAttr('overrideLevelOfDetail', 1)
                nodeShape.setAttr('overrideVisibility', 0)
                nodeShape.setAttr('displayVertices', 1)
                nodeShape.setAttr('vertexSize', 10000000)
                nodeShape.setAttr('displayUVs', 1)
                nodeShape.setAttr('uvSize', 10000000)
            elif node.isCurv():
                nodeShape = node.getShape()
                nodeShape.setAttr('intermediateObject', 1)
                nodeShape.setAttr('lodVisibility', 0)
                nodeShape.setAttr('visibility', 0)
                nodeShape.setAttr('template', 1)
                nodeShape.setAttr('overrideEnabled', 1)
                nodeShape.setAttr('overrideDisplayType', 1)
                nodeShape.setAttr('overrideLevelOfDetail', 1)
                nodeShape.setAttr('overrideVisibility', 0)
            if not HyperSkin.isMesh(node):
                if HyperSkin.isJnt(node) or node.isCurv():
                    node.setAttr('lodVisibility', 0)
                    node.setAttr('visibility', 0)
                    node.setAttr('template', 1)
                    node.setAttr('overrideEnabled', 1)
                    node.setAttr('overrideDisplayType', 1)
                    node.setAttr('overrideLevelOfDetail', 1)
                    node.setAttr('overrideVisibility', 0)
                if HyperSkin.isJnt(node):
                    node.setAttr('drawStyle', 2)
                    node.setAttr('radius', 0)
                else:
                    if HyperSkin.isMesh(node):
                        if not objExists('my_Shader'):
                            myShdr = shadingNode('lambert', asShader=1, n='my_Shader')
                            myShdr.setAttr('color', 0, 0, 0, type='double3')
                        else:
                            myShdr = PyNode('my_Shader')
                        select(node, r=1)
                        hyperShade('my_Shader', assign='my_Shader')
                        myShdr.setAttr('transparency', 1, 1, 1, type='double3')
                    node.setAttr('v', lock=True, channelBox=False, keyable=False)

    def deleteUnwanted(self):
        try:
            delete('as_TempGCM_Grp*')
        except:
            pass

        try:
            delete('*GCM')
        except:
            pass

        try:
            delete('All_Fingers_VtxSet')
        except:
            pass

    def deleteEdgeLoops(self):
        if not HyperSkin.confirmAction('Remove Unwanted Edge Loops ??'):
            om.MGlobal.displayWarning('Action Terminated !!')
            return
        edgeList = list(map(hsNode, cmds.filterExpand(sm=32)))
        loopList = []
        for edg in edgeList:
            cmds.select(edg, r=1)
            mel.SelectEdgeLoop()
            HyperSkin.refreshView(1)
            loopList.extend(cmds.filterExpand(sm=32))

        cmds.select(loopList, r=1)
        cmds.DeleteEdge()
        cmds.select(cl=1)

    def getSkinWeights(self, vtxMesh, vtxName, skinClust, get_hsNodes=False):
        valList = skinPercent(skinClust, vtxName, q=1, v=1)
        if not valList:
            select(vtxName, r=1)
            return
        indexList = [valList.index(val) for val in valList if val > 0]
        infList = skinCluster(skinClust, q=1, inf=1)
        skinValDict = {}
        for val in indexList:
            if get_hsNodes:
                skinValDict[hsNode(infList[val])] = round(valList[val], 5)
            else:
                skinValDict[str(infList[val])] = round(valList[val], 5)

        return skinValDict

    def getInfluenceJoint(self, skinClust, influenceId):
        clusterNode = cmds.ls((cmds.listHistory(skinClust)), type='skinCluster')[0]
        joints = cmds.skinCluster(skinClust, q=True, inf=0)
        return joints[influenceId]

    def getInfluenceID(self, infJnt, skinClust):
        infJnt = hsNode(infJnt)
        matrixAttrList = infJnt.connectionInfo('worldMatrix[0]', dfs=1)
        clustMatrixAttr = None
        if matrixAttrList:
            for mxAttr in matrixAttrList:
                if str(skinClust) in mxAttr:
                    clustMatrixAttr = mxAttr

        indexID = None
        if clustMatrixAttr:
            splitStr = clustMatrixAttr.split('[')[1]
            indexID = int(splitStr.split(']')[0])
        return [indexID, clustMatrixAttr]

    def getWeightsData(self, skinClust, dataType=1):
        """
                if dataType ==1:
                        {jointName : jointID}
                elif dataType ==2:      {vtx1_ID : {joint1_ID : weightVal, joint2_ID : weightVal}, vtx2_ID : {joint1_ID : weightVal, joint2_ID : weightVal}}
                        {
                         0: {23: 1.0},
                         1: {23: 1.0},
                         2: {23: 1.0}
                         }              
                """
        selList = om.MSelectionList()
        selList.add(skinClust)
        clusterNode = om.MObject()
        selList.getDependNode(0, clusterNode)
        skinFn = oma.MFnSkinCluster(clusterNode)
        infDags = om.MDagPathArray()
        skinFn.influenceObjects(infDags)
        infIds = {}
        infs = []
        for x in range(infDags.length()):
            infPath = infDags[x].fullPathName()
            infId = int(skinFn.indexForInfluenceObject(infDags[x]))
            infIds[infId] = x
            infs.append(infPath)

        wlPlug = skinFn.findPlug('weightList')
        wPlug = skinFn.findPlug('weights')
        wlAttr = wlPlug.attribute()
        wAttr = wPlug.attribute()
        wInfIds = om.MIntArray()
        weightsData = {}
        for vId in range(wlPlug.numElements()):
            vWeights = {}
            wPlug.selectAncestorLogicalIndex(vId, wlAttr)
            wPlug.getExistingArrayAttributeIndices(wInfIds)
            infPlug = om.MPlug(wPlug)
            for infId in wInfIds:
                if dataType == 1:
                    weightsData[HyperSkin.getInfluenceJoint(skinClust, infId)] = infId
                if dataType == 2:
                    infPlug.selectAncestorLogicalIndex(infId, wAttr)
                    try:
                        vWeights[infIds[infId]] = infPlug.asDouble()
                    except KeyError:
                        pass

                    weightsData[vId] = vWeights

        return weightsData

    def setSkinWeights(self, vtxName, jntValDict, addInf=False, skinClust=None, unlockJnts=True, lockJnts=None, speedSkin=False):
        vtxMesh = vtxName.split('.')[0]
        if not skinClust:
            skinClust = listHistory(vtxMesh, type='skinCluster')[0]
        if not jntValDict:
            return

        if addInf:
            jntList = list(jntValDict.keys())
            jntList = [jntList] if type(jntList) != list else jntList
            for jnt in jntList:
                if not HyperSkin.isSkinJnt(jnt, vtxMesh):
                    HyperSkin.addInfluences_skinClust(jnt, vtxMesh, useProgress=0)

        if unlockJnts:
            valList = skinPercent(skinClust, vtxName, q=1, v=1)
            infList = cmds.skinCluster((str(skinClust)), q=1, inf=1)
            skinValDict = dict(list(zip(infList, valList)))
            sknJntList = [key for key, val in list(skinValDict.items()) if val > 0.0]
            [cmds.setAttr(jnt + '.liw', 0) for jnt in sknJntList]

        if lockJnts:
            [cmds.setAttr(jnt + '.liw', 1) for jnt in lockJnts]
        select(cl=1)

        if speedSkin:
            splitStr = vtxName.split('[')[1]
            vtxID = int(splitStr.split(']')[0])
            wlAttr = '%s.weightList[%s]' % (skinClust, vtxID)
            for (infJnt, infValue) in list(jntValDict.items()):
                infID = HyperSkin.getInfluenceID(infJnt, skinClust)[0]
                wAttr = '.weights[%s]' % infID
                cmds.setAttr(wlAttr + wAttr, infValue)
                cmds.setAttr(infJnt + '.liw', 1)

        else:
            tvList = [(jnt, jntValDict[jnt]) for jnt in jntValDict]
            pm.skinPercent(skinClust, vtxName, tv=tvList)

    def exportBlendWeights(self, skinMesh=None, filePath=None, fileName=None):
        if not skinMesh:
            skinMesh = hsN.selected()[0]
        else:
            skinMesh = hsNode(skinMesh)
        vtxList = filterExpand(sm=31)
        bwDictStr = 'bwDict ={'
        if vtxList:
            vtxList = list(map(hsNode, vtxList))
            skinMesh = hsNode(vtxList[0].split('.')[0])
            if skinMesh.isShape():
                skinMesh = skinMesh.parent()
            skinClust = listHistory(skinMesh, type='skinCluster')[0]
            vtxNums = [vtx.extractNum()[0] for vtx in vtxList]
            for num in vtxNums:
                bWgt = getAttr(skinClust + '.blendWeights[%d]' % round(num, 6))
                if num != vtxNums[-1]:
                    bwDictStr += str(num) + ' : %f, ' % bWgt
                else:
                    bwDictStr += str(num) + ' : %f}' % bWgt

        else:
            fnMesh = MFnMesh(skinMesh._MDagPath())
            vtxCount = fnMesh.numVertices()
            skinClust = listHistory(skinMesh, type='skinCluster')[0]
            for num in range(vtxCount):
                bWgt = getAttr(skinClust + '.blendWeights[%d]' % round(num, 6))
                if num != vtxCount - 1:
                    bwDictStr += str(num) + ' : %f, ' % bWgt
                else:
                    bwDictStr += str(num) + ' : %f}' % bWgt

        if not filePath:
            scnName = sceneName()
            scnPathBase = scnName.rsplit('.', 1)[0]
            folderPath = scnPathBase.rsplit('/', 1)[0]
            filePath = folderPath + '/AHSS_Lib/'
            if not os.path.exists(filePath):
                sysFile(filePath, makeDir=True)
        if not fileName:
            if vtxList:
                asVtx = hsNode(vtxList[0])
                bodyMesh = asVtx.asObj()
            else:
                bodyMesh = skinMesh
            if bodyMesh.isShape():
                bodyMesh.extendToParent()
            fileName = bodyMesh.shortName() + '_blendWeights.py'
        blendFile = filePath + fileName
        if os.path.exists(blendFile):
            if not HyperSkin.confirmAction('File Already Exist !!\nContinue To Overwrite File ?'):
                raise RuntimeError('Action Cancelled !!')
        fileIO = open(blendFile, 'w')
        allLines = fileIO.writelines(bwDictStr)
        fileIO.close()

    def importBlendWeights(self, skinMesh=None, filePath=None, fileName=None):
        if not skinMesh:
            skinMesh_ = hsN.selected()
            if not skinMesh_:
                HyperSkin.error('Oops !! No Action Taken\nSelect Any Mesh To Import Blend Weights !!')
            skinMesh = skinMesh_[0]
        else:
            skinMesh = hsNode(skinMesh)
        if not filePath:
            scnName = sceneName()
            scnPathBase = scnName.rsplit('.', 1)[0]
            folderPath = scnPathBase.rsplit('/', 1)[0]
        if not fileName:
            fileName = skinMesh.shortName() + '_blendWeights.py'
        filePath = folderPath + '/AHSS_Lib/' + fileName
        skinClust = listHistory(skinMesh, type='skinCluster')[0]
        skinClust.setAttr('skinningMethod', 2)
        fileIO = open(filePath, 'r')
        selLine = fileIO.readlines()[0].strip()
        fileIO.close()
        if selLine:
            exec(selLine)
        for key in bwDict:
            setAttr(skinClust + '.blendWeights[%d]' % key, bwDict[key])

        HyperSkin.message('Imported Blend Weights Successfully !!')

    def exportSkinWeights2(self, vtxList=None, filePath=None, fileName=None):
        bothSides = cmds.checkBox('as_BothSides_CB', q=1, v=1)
        importSelList = cmds.checkBox('as_Selection_CB', q=1, v=1)
        if not vtxList:
            vtxList = filterExpand(sm=31)
            if not vtxList:
                selList = hsN.selected()
                if selList:
                    if selList[0].isMesh():
                        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh(selList[0])
                    else:
                        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
                else:
                    (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
                if bothSides:
                    vtxList = HyperSkin.getMeshVtx(skinMesh)
                else:
                    vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
        if not filePath:
            scnName = sceneName()
            scnPathBase = scnName.rsplit('.', 1)[0]
            folderPath = scnPathBase.rsplit('/', 1)[0]
            libPath = folderPath + '/AHSS_Lib'
        if not fileName:
            asVtx = hsNode(vtxList[0])
            bodyMesh = asVtx.asObj()
            if bodyMesh.isShape():
                bodyMesh.extendToParent()
            fileName = bodyMesh.shortName() + '_SkinWeights.py'
        if not libPath.endswith('/'):
            libPath += '/'
        if not os.path.exists(libPath):
            sysFile(libPath, makeDir=True)
        if os.path.exists(libPath + fileName):
            if not HyperSkin.confirmAction('File Already Exist !!\nContinue To Overwrite File ?'):
                raise RuntimeError('Action Cancelled !!')
            (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
            objStr = 'import maya.cmds as mc\n'
            objStr += 'from hsNode import *\n\r'
            vtxList = [vtxList] if type(vtxList) != list else vtxList
            HyperSkin.startProgressWin(vtxList, 'Exporting Skin Weights !!')
            for asVtx in vtxList:
                jntValDict = HyperSkin.getSkinWeights(skinMesh, asVtx, skinClust)
                objStr += "HyperSkin.setSkinWeights('" + str(asVtx) + "', " + str(jntValDict) + ')\n'
                HyperSkin.progressWin(asVtx)

            if importSelList:
                vtxListStr = 'cmds.select(cl=1)\n'
                for vtx in vtxList:
                    vtxListStr += "cmds.select('" + vtx + "', add=1)\n"

                objStr += vtxListStr
            HyperSkin.endProgressWin(vtxList, True)
            if not os.path.exists(libPath):
                sysFile(libPath, makeDir=True)
        fileIO = open(libPath + fileName, 'w')
        allLines = fileIO.writelines(objStr)
        fileIO.close()
        try:
            os.startfile(mel.toNativePath(libPath))
        except:
            try:
                os.system('xdg-open "%s"' % libPath)
            except:
                subprocess.Popen(['xdg-open', libPath])

        try:
            subprocess.Popen(['notepad++', libPath + fileName])
        except:
            pass

        cmds.select(vtxList, r=1)

    def as_ImportSkinDeformer(self):
        meshList = [obj for obj in hsN.selected() if obj.isMesh()]
        if meshList:
            missingList = []
            for (num, mesh) in enumerate(meshList):
                mesh.select()
                HyperSkin.refreshView(1)
                try:
                    if len(meshList) > 1:
                        HyperSkin.importSkinWeights_Deformer(0, 0, 0)
                    else:
                        HyperSkin.importSkinWeights_Deformer(0, 0, 1)
                except:
                    missingList.append(mesh)

                om.MGlobal.displayInfo('Imported {} of {} Meshes'.format(num + 1, len(meshList)))

            HyperSkin.message('Imported Skin Weights Successfully !!')
        if missingList:
            print(('Missing List of Meshes for Import :', missingList))

    def import_skin(self, json_file_path):
        json_file = open(json_file_path, 'r')
        json_data = json.load(json_file)
        for (mesh_name, mesh_data) in list(json_data.items()):
            pm.select(mesh_name)
            skin_cluster = pm.listHistory(mesh_name, type='skinCluster')
            if not skin_cluster:
                print('Mesh "{}" does not have a skin cluster attached.'.format(mesh_name))
                continue
            else:
                HyperSkin.startProgressWin(list(mesh_data.keys()))
                for (vertex_num, vertex_weights) in mesh_data.items():
                    weightsList = [(jnt, value) for jnt, value in list(vertex_weights.items())]
                    vtxName = '{0}.vtx[{1}]'.format(mesh_name, vertex_num)
                    pm.skinPercent((skin_cluster[0]), vtxName, normalize=True, transformValue=weightsList)
                    HyperSkin.progressWin(vtxName, 0, 1)

                HyperSkin.endProgressWin()

        print('Skin weights are imported successfully for selected meshes from this path: {0}'.format(file_path))

    def import_vtx_skin(self, json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        mesh_transform = data['mesh_transform']
        mesh_transform = pm.PyNode(mesh_transform)
        mesh_transform.select()
        vertices = data['vertices']
        mesh = pm.PyNode(mesh_transform)
        skin_cluster = mesh.listHistory(type='skinCluster')
        if not skin_cluster:
            print('No skin cluster found on the selected mesh. Creating a new one...')
            skin_cluster = pm.skinCluster(mesh)
        else:
            skin_cluster = skin_cluster[0]
        mesh_transform.select(d=1)
        HyperSkin.startProgressWin(list(vertices.keys()), 'Importing Skin Weights')
        for (vertex, weights) in list(vertices.items()):
            vertex = int(vertex)
            weights = [(joint, float(weight)) for joint, weight in list(weights.items())]
            pm.skinPercent(skin_cluster, ('{0}.vtx[{1}]'.format(mesh, vertex)), normalize=True, transformValue=weights)
            cmds.select(('{0}.vtx[{1}]'.format(mesh, vertex)), add=True)
            HyperSkin.progressWin(vertex, 0, 1)

        HyperSkin.endProgressWin()
        print('Skin weights are imported successfully to for selected vertices at this path: {0}'.format(file_path))

    def importSkinWeights(self, advImport=False):
        if not advImport:
            meshList = [obj for obj in hsN.selected() if obj.isMesh()]
            meshList = [obj for obj in hsN.selected() if not obj.isMesh() if obj.isCurv() if obj.isMesh() if obj.isCurv()]
        if advImport:
            scnName = sceneName()
            scnPathBase = scnName.rsplit('.', 1)[0]
            folderPath = scnPathBase.rsplit('/', 1)[0]
            libPath = folderPath + '/AHSS_Lib/'
            if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
                fileName = 'AHSS_SkinWeights.json'
                HyperSkin.import_skin(libPath + fileName)
            elif cmds.radioButton('as_Weights_LS_RBG', q=1, sl=1):
                fileName = 'AHSS_LeftWeights.json'
                HyperSkin.import_vtx_skin(libPath + fileName)
            elif cmds.radioButton('as_Weights_RS_RBG', q=1, sl=1):
                fileName = 'AHSS_RightWeights.json'
                HyperSkin.import_vtx_skin(libPath + fileName)
            elif cmds.radioButton('as_SelectedVtx_ESW_RBG', q=1, sl=1):
                fileName = 'AHSS_VtxWeights.json'
                HyperSkin.import_vtx_skin(libPath + fileName)
            return
        if meshList:
            missingList = []
            for (num, mesh) in enumerate(meshList):
                mesh.select()
                HyperSkin.refreshView(1)
                try:
                    if len(meshList) > 1:
                        HyperSkin.importSkinWeights_Sides(0, 0, 0)
                        mesh.select()
                        HyperSkin.importBlendWeights()
                        cmds.select(selList, r=1)
                    else:
                        HyperSkin.importSkinWeights_Sides(0, 0, 1)
                        selList = cmds.ls(sl=1)
                        mesh.select()
                        HyperSkin.importBlendWeights()
                        cmds.select(selList, r=1)
                except:
                    missingList.append(mesh)

                om.MGlobal.displayInfo('Imported {} of {} Meshes'.format(num + 1, len(meshList)))

            if len(meshList) > 1:
                HyperSkin.message('Imported Skin Weights Sucessfully !!')
            if missingList:
                print(('Missing List of Meshes for Import :', missingList))

    def importSkinWeights_Deformer(self, filePath=None, fileName=None, showMessage=True):
        if not hsN.selected():
            HyperSkin.error('No Meshes Are Selected !\nPlease select atleast one mesh !!')
        meshList = hsN.selected()
        scnName = sceneName()
        scnPathBase = scnName.rsplit('.', 1)[0]
        folderPath = scnPathBase.rsplit('/', 1)[0]
        libPath = folderPath + '/AHSS_Lib'
        for mesh in meshList:
            if self._mayaVer() < 2025:
                skn = as_HyperSkinMain(libPath + '/' + mesh + '.hyperSkin')
                skn.importSkinDeformer(mesh + '.hyperSkin', libPath)
            else:
                skn = as_HyperSkinMain(libPath + '/' + mesh + '.xml')
                skn.importSkinDeformer(mesh + '.xml', libPath)

        if showMessage:
            HyperSkin.message('Imported Skin Weights Sucessfully !!')

    def importSkinWeights_Sides(self, filePath=None, fileName=None, showMessage=True):
        selList = hsN.selected()
        asMesh = None
        if selList:
            if selList[0].isMesh():
                asMesh = selList[0]
            if not filePath:
                scnName = sceneName()
                scnPathBase = scnName.rsplit('.', 1)[0]
                folderPath = scnPathBase.rsplit('/', 1)[0]
                libPath = folderPath + '/AHSS_Lib'
            sides = None
            if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
                sides = 'both'
            elif cmds.radioButton('as_Weights_LS_RBG', q=1, sl=1):
                sides = 'left'
            elif cmds.radioButton('as_Weights_RS_RBG', q=1, sl=1):
                sides = 'right'
            elif cmds.radioButton('as_SelectedVtx_ESW_RBG', q=1, sl=1):
                sides = 'vtx'
            if not fileName:
                if asMesh:
                    (bodyMesh, skinClust) = HyperSkin.confirmSkinMesh(asMesh)
                else:
                    (bodyMesh, skinClust) = HyperSkin.confirmSkinMesh()
                if sides == 'both':
                    fileExtn = '_SkinWeights.py'
                elif sides == 'right':
                    fileExtn = '_SkinWeightsR.py'
                elif sides == 'left':
                    fileExtn = '_SkinWeightsL.py'
                elif sides == 'vtx':
                    fileExtn = '_SkinWeightsV.py'
                fileName = bodyMesh.shortName() + fileExtn
            if not libPath.endswith('/'):
                libPath += '/'
            if not os.path.exists(libPath):
                sysFile(libPath, makeDir=True)
            HyperSkin.executeFile(libPath + fileName)
            if showMessage:
                HyperSkin.message('Imported Skin Weights Sucessfully !!')

    def exportAttributes(self, objList, attrList, filePath, fileName=None):
        attrStr = 'import maya.cmds as mc\n\r'
        objList = list(map(hsNode, objList))
        for asObj in objList:
            for attrName in attrList:
                try:
                    attrVal = asObj.getAttr(attrName)
                    attrStr += 'cmds.setAttr ("' + asObj.name() + '.' + attrName + '", ' + str(attrVal) + ')\r'
                except:
                    pass

        if not filePath.endswith('/'):
            if fileName:
                filePath += '/'
        if not fileName:
            fileName = ''
        fileIO = open(filePath + fileName, 'w')
        allLines = fileIO.writelines(attrStr)
        fileIO.close()
        try:
            subprocess.Popen(['notepad', filePath + fileName])
        except:
            pass

    def export_DSCsOrAttrs(self):
        DSCs = HyperSkin.confirmAction('Export Discs or Attrs ??', False, 'Discs', 'Attrs')
        if DSCs:
            HyperSkin.exportDSCs_2File()
        else:
            HyperSkin.exportAttrs_DSCs()

    def exportAttrs_DSCs(self):
        defPath = checkBox('as_Save2FilePath_CB', q=1, v=1)
        noDiscBind = cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1)
        if not noDiscBind:
            try:
                cmds.select('*DSC', r=1)
            except:
                HyperSkin.error('Oops.. \n"Hyper Discs" not found in the scene')

        dscList = hsN.selected()
        jntList = []
        if noDiscBind:
            attrList = ['baseBlend', 'tailBlend', 'moreVolume']
            if dscList:
                jntList = [jnt for jnt in dscList if jnt.isJnt()]
            if not jntList:
                (_, skinClust) = HyperSkin.confirmSkinMesh()
                jntList = pm.skinCluster(skinClust, q=1, inf=1)
        else:
            attrList = ['baseBlend','tailBlend','copyDisc','discShape','scale_X','scale_Y','scale_Z','snapRotTo','moreVolume']
        scnName = sceneName()
        if defPath and scnName:
            filePath = scnName.parent
            libPath = filePath + '/AHSS_Lib'
        else:
            folderPath = promptForFolder()
            if not folderPath.endswith('/AHSS_Lib'):
                libPath = folderPath + '/AHSS_Lib'
            else:
                libPath = folderPath
        if not os.path.exists(libPath):
            sysFile(libPath, makeDir=True)
        if noDiscBind:
            filePath = libPath + '/AHSS_AttrsND.txt'
        else:
            filePath = libPath + '/AHSS_Attrs.txt'
        if os.path.exists(filePath):
            if not HyperSkin.confirmAction('File Exists Already !!\nDo you want to continue to overwrite??'):
                raise RuntimeError('Action Terminated !!')
        if noDiscBind:
            HyperSkin.exportAttributes(jntList, attrList, filePath)
        else:
            HyperSkin.exportAttributes(dscList, attrList, filePath)
        om.MGlobal.displayInfo('File Saved Sucessfully at : {0}'.format(filePath))

    def exportDSCs_2File(self):
        defPath = checkBox('as_Save2FilePath_CB', q=1, v=1)
        scnName = sceneName()
        scnExtn = 'ma'
        if defPath and scnName:
            filePath = scnName.parent
            libPath = filePath + '/AHSS_Lib'
            scnExtn = scnName.split('.')[-1]
        else:
            folderPath = promptForFolder()
            if not folderPath.endswith('/AHSS_Lib'):
                libPath = folderPath + '/AHSS_Lib'
            else:
                libPath = folderPath
        if not os.path.exists(libPath):
            sysFile(libPath, makeDir=True)
        filePath = libPath + '/AHSS_DSCs.' + scnExtn
        if not objExists('as_HyperSkin_Grp'):
            HyperSkin.error('"as_HyperSkin_Grp" not found')
        else:
            hyperSkinGrp = hsNode('as_HyperSkin_Grp')
        hyperSkinGrp.rename(hyperSkinGrp.shortName() + '1')
        dupGrp = hyperSkinGrp.duplicate()[0]
        pCons = dupGrp.selectHI('parentConstraint')
        if pCons:
            delete(pCons)
        dupGrp.rename('as_HyperSkin_Grp')
        dupGrp.selectHI('mesh')
        for dsc in hsN.selected():
            dsc.show()

        if scnExtn == 'ma':
            extnType = 'mayaAscii'
        elif scnExtn == 'mb':
            extnType = 'mayaBinary'
        if os.path.exists(filePath):
            if not HyperSkin.confirmAction('File Exists Already !!\nDo you want to continue to overwrite??'):
                raise RuntimeError('Action Terminated !!')
        dupGrp.select()
        try:
            cmds.file(filePath, pr=1, typ=extnType, force=1, options='v=0;', es=1)
        except:
            dupGrp.delete()
            hyperSkinGrp.rename('as_HyperSkin_Grp')
            raise RuntimeError('Nothing Exported..')

        dupGrp.delete()
        hyperSkinGrp.rename('as_HyperSkin_Grp')
        HyperSkin.message('Exported "Hyper Discs" Successfully ..!')
        os.startfile(libPath)
        om.MGlobal.displayInfo('Exported "Hyper Discs" Sucessfully..!')

    def executeFile(self, filePath, fileName=None):
        if not cmds.file(filePath, q=1, ex=1):
            cmds.warning('File Not Found : "{s}"'.format(filePath))
        numLines = sum((1 for line in open(filePath)))
        with open(filePath, 'r') as fileIO:
            lineNum = 0
            missingLinesList = []
            MissingLinesAppend = missingLinesList.append
            HyperSkin.startProgressWin(numLines, 'Importing Skin Weights', rv=1)
            for selLine in fileIO:
                selLine = selLine.strip()
                if selLine:
                    try:
                        exec(selLine)
                    except:
                        MissingLinesAppend(selLine)

                    HyperSkin.progressWin(0, 0, 1)

            HyperSkin.endProgressWin(numLines, 1)
        if missingLinesList:
            print('Missing Lines List :\n#=================')
            for line in missingLinesList:
                print(line)

            om.MGlobal.displayInfo('Executed File Sucessfully ..!!')

    def import_DSCsOrAttrs(self):
        DSCs = HyperSkin.confirmAction('Import Discs or Attrs ??', False, 'Discs', 'Attrs')
        if DSCs:
            HyperSkin.importDSCs_FromFile()
        else:
            HyperSkin.importAttrs_DSCs()

    def isolateHyperDiscGrps(self):
        selList = hsN.selected()
        if selList:
            grpList = [hsNode('as_' + obj.shortName() + '_MeshGrp') for obj in selList]
            hsGrp = grpList[0].parent()
            allGrps = hsGrp.getChildren()
            for grp in grpList:
                grp.show()

            for grp in allGrps:
                if grp not in grpList:
                    grp.hide()
                    meshName_ = grp.split('as_')[1]
                    meshName_ = hsNode(meshName_.split('_MeshGrp')[0])
                    meshName_.template()

        else:
            hsGrp = hsNode('as_HyperSkin_Grp')
            hsGrp.show()
            allGrps = hsGrp.getChildren()
            for grp in allGrps:
                grp.show()
                meshName_ = grp.split('as_')[1]
                meshName_ = hsNode(meshName_.split('_MeshGrp')[0])
                meshName_.untemplate()

    def importAttrs_DSCs(self):
        defPath = checkBox('as_Save2FilePath_CB', q=1, v=1)
        adjustDiscs = checkBox('as_AdjustHyperDisc_CB', q=1, v=1)
        noDiscBind = cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1)
        if not noDiscBind:
            try:
                cmds.select('*DSC', r=1)
            except:
                HyperSkin.error('Oops.. \n"Hyper Discs" not found in the scene')

        dscList = hsN.selected()
        attrList = ['baseBlend','tailBlend','copyDisc','discShape','scale_X','scale_Y','scale_Z','snapRotTo','moreVolume']
        scnName = sceneName()
        if defPath and scnName:
            filePath = scnName.parent
            libPath = filePath + '/AHSS_Lib'
        else:
            folderPath = promptForFolder()
            if not folderPath.endswith('/AHSS_Lib'):
                libPath = folderPath + '/AHSS_Lib'
            else:
                libPath = folderPath
        if not os.path.exists(libPath):
            sysFile(libPath, makeDir=True)
        if noDiscBind:
            filePath = libPath + '/AHSS_AttrsND.txt'
        else:
            filePath = libPath + '/AHSS_Attrs.txt'
        if defPath:
            if not os.path.exists(filePath):
                HyperSkin.confirmAction('File needs to be saved first at this location :\n {0}!!'.format(filePath), 1)
        HyperSkin.executeFile(filePath)
        if adjustDiscs:
            if not noDiscBind:
                if HyperSkin.confirmAction('Imported "Attributes" Sucessfully !!\nDo You Want To Replace & Update Hyper Discs ??'):
                    HyperSkin.scaleDisc_AfterImportAttrs()
                    om.MGlobal.displayInfo('Imported "Attributes" & Adjsuted "Hyper Discs" Sucessfully From : \n{0}'.format(filePath))
            else:
                om.MGlobal.displayInfo('Imported "Attributes" Sucessfully From : \n{0}'.format(filePath))
        else:
            HyperSkin.confirmAction('Imported "Attributes" Sucessfully !!')
            om.MGlobal.displayInfo('Imported "Attributes" Sucessfully From : \n{0}'.format(filePath))

    def importDSCs_FromFile(self):
        defPath = checkBox('as_Save2FilePath_CB', q=1, v=1)
        scnName = sceneName()
        scnExtn = 'ma'
        if defPath and scnName:
            filePath_S = scnName.parent
            libPath = filePath_S + '/AHSS_Lib'
            scnExtn = scnName.split('.')[-1]
            if not os.path.exists(libPath):
                filePath = cmds.fileDialog2(fileFilter='*.m[a|b]', dialogStyle=2, fm=1, cap='Pick Hyper Discs File', dir=filePath_S, okc='Pick Your File')[0]
            else:
                filePath = libPath + '/AHSS_DSCs.' + scnExtn
                if not os.path.exists(filePath):
                    if filePath.endswith('.ma'):
                        filePath = filePath.replace('.ma', '.mb')
                    elif filePath.endswith('.mb'):
                        filePath = filePath.replace('.mb', '.ma')
                    if not os.path.exists(filePath):
                        filePath = cmds.fileDialog2(fileFilter='*.m[a|b]', dialogStyle=2, fm=1, cap='Pick Hyper Discs File', dir=libPath, okc='Pick Your File')[0]
        elif scnName:
            filePath_S = scnName.parent
            filePath = cmds.fileDialog2(fileFilter='*.m[a|b]', dialogStyle=2, fm=1, cap='Pick Hyper Discs File', dir=filePath_S, okc='Pick Your File')[0]
        else:
            filePath = cmds.fileDialog2(fileFilter='*.m[a|b]', dialogStyle=2, fm=1, cap='Pick Hyper Discs File', okc='Pick Your File')[0]
        if filePath.endswith('.ma'):
            extnType = 'mayaAscii'
        elif filePath.endswith('.mb'):
            extnType = 'mayaBinary'
        if objExists('as_HyperSkin_Grp'):
            if HyperSkin.confirmAction('"as_HyperSkin_Grp" Already Exists..\nDelete "as_HyperSkin_Grp" And Continue ??'):
                cmds.delete('as_HyperSkin_Grp')
            else:
                raise RuntimeError('Oops.. \n"as_HyperSkin_Grp" Already Exists\nDelete Existing "as_HyperSkin_Grp" First, Then import again !!')
        try:
            cmds.file((str(filePath)), pr=1, rpr='as', ignoreVersion=1, i=1, type=extnType, loadReferenceDepth='all', mergeNamespacesOnClash=False, options='v=0;')
        except:
            HyperSkin.error('Oops.. \nNothing Imported..\nGiven Path is :\n{0}'.format(filePath))

        try:
            cmds.select('*asSC*DSC', r=1)
        except:
            HyperSkin.error('Oops.. \nFound No Discs..')

        dscList = hsN.selected()
        skipList = []
        for dsc in dscList:
            jnt = dsc.rsplit('_', 1)[0]
            if not objExists(jnt):
                skipList.append(jnt)
            else:
                dscParent = dsc.parent()
                dscParent.snapPosTo(jnt)
                HyperSkin.mConstrain([jnt, dscParent], 'parent')

        if skipList:
            cmds.select(skipList, r=1)
            HyperSkin.error('Oops.. \nFound No Joints For Selected Discs..')
        HyperSkin.message('Hurray.. \nImported "Hyper Discs" And Attached Sucessfully !!')
        om.MGlobal.displayInfo('Imported "Hyper Discs" And Attached Sucessfully..!')

    def getSolvedJntsNGCMs(self, skinJntList, nonSknEndJnts, gcmSuffix=None):
        allEndVtxSets_Solved = []
        allUpLineGCMs_Solved = []
        allUpLineJnts_Solved = []
        fingerEndVtxDict = {}
        fingerEndJntDict = {}
        AllUpLineGCMs_SolvedExtend = allUpLineGCMs_Solved.extend
        AllUpLineJnts_SolvedExtend = allUpLineJnts_Solved.extend
        endJnts_Solved = []
        EndJnts_SolvedAppend = endJnts_Solved.append
        for jnt in skinJntList:
            if jnt not in endJnts_Solved:
                try:
                    for chd in jnt.getChildren():
                        if chd.endswith('_Solve'):
                            EndJnts_SolvedAppend(jnt)

                except:
                    pass

        for jnt in nonSknEndJnts:
            try:
                if jnt.child().endswith('_Solve'):
                    EndJnts_SolvedAppend(jnt)
            except:
                pass

        if endJnts_Solved:
            for fingerEndJnt in endJnts_Solved:
                solvedLoc = fingerEndJnt.child()
                endVtxSet = fingerEndJnt.shortName() + '_VtxSet'
                if objExists(endVtxSet):
                    fingerEndVtxDict[endVtxSet] = fingerEndJnt
                else:
                    HyperSkin.deleteUnwanted()
                    HyperSkin.error('Found No "%s" for "%s" ' % (endVtxSet, fingerEndJnt))
                try:
                    numParents = solvedLoc.getAttr('numParents')
                except:
                    HyperSkin.deleteUnwanted()
                    HyperSkin.error('Oops.. Found No "%s"' % (str(solvedLoc) + '.numParents'))

                upLineJnts_SolvedJnt = fingerEndJnt.parent(numParents, True, 'joint')
                fingerEndJntDict[fingerEndJnt] = upLineJnts_SolvedJnt
                AllUpLineJnts_SolvedExtend(upLineJnts_SolvedJnt)
                if gcmSuffix:
                    for jnt in upLineJnts_SolvedJnt:
                        if not objExists(jnt + gcmSuffix):
                            HyperSkin.deleteUnwanted()
                            HyperSkin.error('Oops.. "%s" -Object Not Exists ..!\nCheck for "Solve >> End Jnts" Option' % str(jnt + gcmSuffix))
                            break

                    upLineGCMs_Solved = [str(jnt + gcmSuffix) for jnt in upLineJnts_SolvedJnt]
                    AllUpLineGCMs_SolvedExtend(upLineGCMs_Solved)
                    continue

            if fingerEndVtxDict:
                select((list(fingerEndVtxDict.keys())), r=1)
                allEndVtxSets_Solved = sets(filterExpand(sm=31), n='All_Fingers_VtxSet')
        else:
            return
        return ['allEndVtxSets_Solved', 'allUpLineGCMs_Solved', 'allUpLineJnts_Solved', 'fingerEndVtxDict', 'fingerEndJntDict']

    def dafaultSkin(self):
        ResetWeightsToDefault()
        HyperSkin.message('Restored Default Skin Sucessfully !!')
        om.MGlobal.displayInfo('Restored Default Skin Sucessfully !!')

    def as_GetJntList_OutsideBB(self, skinMesh):
        select(skinMesh, r=1)
        latList = lattice(divisions=(2, 5, 2), ldv=(2, 2, 2), objectCentered=True)
        asLat = hsNode(latList[1])
        asLatShp = latList[0]

    def as_Generate_HyperSkin(self):
        if not HyperSkin.confirmAction('Proceed to HyperSkin ..?'):
            HyperSkin.error('Action Cancelled !!')
        if cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1):
            HyperSkin.as_Generate_HyperSkin_NoDisc()
        else:
            HyperSkin.as_Generate_HyperSkin_Disc()

    def as_Generate_HyperSkin_NoDisc(self):
        global lastSelectedVtx

        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        _as_HyperSkinMain__showVtxDist = 0
        _as_HyperSkinMain__notForSale = 1
        _as_HyperSkinMain__autoDualSkinning = 0
        if __notForSale:
            HyperSkin.restrictedZone_FreeTool()
        HyperSkin.startTime(__displayTotalTime)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
        quickHyperSkin = checkBox('as_QuickHyperSkin_CB', q=1, v=1)

        def getVtxList_Influenced(infList=None, infMesh=None, selectHI=0, deformType='skinCluster', getMapping=1, dscSuffix=None, **shArgs):
            """
                        Args:
                        -----
                        infList = jntList | clusterList etc
                        infMesh = skinnedMesh | deformedMesh
                        selectHI =select Hierarchy for each component in infList
                        deformType = 1 | skinCluster, 2 | cluster, etc

                        Returns:
                        --------
                        return [vtxList, inf2VtxDict, vtx2InfDict]
                        """
            if shArgs:
                infList = shArgs['il'] if 'il' in shArgs else infList
                infMesh = shArgs['im'] if 'im' in shArgs else infMesh
                selectHI = shArgs['hi'] if 'hi' in shArgs else selectHI
                selectHI = shArgs['sh'] if 'sh' in shArgs else selectHI
                deformType = shArgs['dt'] if 'dt' in shArgs else deformType
                getMapping = shArgs['gm'] if 'gm' in shArgs else getMapping
            selList = hsN.selected()
            if not infList:
                try:
                    if deformType == 1 or deformType == 'skinCluster':
                        infList = [jnt for jnt in selList if jnt.nodeType() == 'joint']
                except:
                    HyperSkin.error('Oops ..!!\nPlease select Skinned Joints and | or Skinned Mesh !!')

            if not infMesh:
                try:
                    infMesh = [jnt for jnt in selList if jnt.nodeType() == 'mesh'][0]
                except:
                    HyperSkin.error('Oops ..!!\nPlease select Skinned Joints and | or Skinned Mesh !!')

            if not infMesh or not infList:
                HyperSkin.error('Oops ..!!\nPlease select Skinned Joints and | or Skinned Mesh !!')
            infList = [infList] if type(infList) != list else infList
            infList = list(map(hsNode, infList))
            infMesh = hsNode(infMesh)
            if selectHI:
                if deformType == 1 or deformType == 'skinCluster':
                    inf_List = []
                    for jnt in infList:
                        addList = jnt.selectHI('jnt')
                        if addList:
                            inf_List.extend(addList)

                    infList = inf_List
            vtxList = []
            vtxList_Jnt = []
            vtx2InfDict = {}
            inf2VtxDict = {}
            if deformType == 1 or deformType == 'skinCluster':
                skinClust = infMesh.getSkinCluster()
                inf_List = list(map(hsNode, cmds.skinCluster(skinClust, q=1, inf=1)))
                for inf in infList:
                    if inf in inf_List:
                        cmds.skinCluster(skinClust, e=1, siv=inf)
                    else:
                        continue
                    vtxList_Jnt = cmds.filterExpand(sm=31)
                    if vtxList_Jnt:
                        vtxList.extend(vtxList_Jnt)
                        if getMapping:
                            inf2VtxDict[inf] = vtxList_Jnt
                            for vtx in vtxList_Jnt:
                                if not objExists(inf.shortName() + dscSuffix):
                                    vtx2InfDict[vtx] = inf.pickWalkUp(1, 'joint')
                                else:
                                    vtx2InfDict[vtx] = inf

            vtxList = list(map(hsNode, vtxList))
            cmds.select(vtxList, r=1)
            return [vtxList_Jnt, vtxList, inf2VtxDict, vtx2InfDict]

        tempSelected = cmds.ls(sl=1, fl=1)
        if tempSelected:
            if '.' not in str(tempSelected[0]):
                selObj = hsNode(tempSelected[0])
                if selObj.isMesh():
                    skinMesh_TF = cmds.textField('as_SkinMesh_TF', q=True, tx=True)
                    selObj = selObj.strip('.tx')
                    skinMesh_TF(e=True, tx=selObj)
                else:
                    HyperSkin.endProgressWin(1, 1)
                    HyperSkin.error('Oops.. Selected Is Not A Mesh..!\nSkinned Mesh needs to be selected')
            else:
                selObj = hsNode(filterExpand(sm=31)[0].split('.')[0])
                if selObj.isMesh():
                    if selObj.isShape():
                        selObj = selObj.parent()
                    textField('as_SkinMesh_TF', e=1, tx=selObj.strip())
                else:
                    HyperSkin.endProgressWin(1, 1)
                    HyperSkin.error('Oops.. Selected Is Not A Mesh..!\nSkinned Mesh needs to be selected')
            cmds.select(tempSelected, r=1)
        vtxSelection = False
        if not filterExpand(sm=31):
            if skinSide == 'LT':
                HyperSkin.selectSkinVertices('L_')
            elif skinSide == 'RT':
                HyperSkin.selectSkinVertices('R_')
            lastSelectedVtx = vtxList = filterExpand(sm=31)
        else:
            vtxSelection = True
            lastSelectedVtx2 = vtxList = filterExpand(sm=31)
            skinMesh, skinClust = HyperSkin.confirmSkinMesh()
            cmds.select(cl=1)
            if skinSide == 'LT':
                HyperSkin.selectSkinVertices('L_')
            else:
                if skinSide == 'RT':
                    HyperSkin.selectSkinVertices('R_')
                lastSelectedVtx = lastSelectedVtx2[:]
                sideVtxList_Ex = filterExpand(sm=31)
                for vtx in vtxList:
                    if vtx in sideVtxList_Ex:
                        sideVtxList_Ex.remove(vtx)

                sideVtxDict_Ex = {}
                for vtx in sideVtxList_Ex:
                    vtxValDict = HyperSkin.getSkinWeights(skinMesh, vtx, skinClust)
                    sideVtxDict_Ex[vtx] = vtxValDict

                skinMesh, skinClust = HyperSkin.confirmSkinMesh()
                pm.select(skinMesh, r=1)
                mel.removeUnusedInfluences()
                if __autoDualSkinning:
                    if not attributeQuery('extraVolume', n=skinMesh.name(), ex=1):
                        asSkinMesh = hsNode(skinMesh)
                        asSkinMesh.addAttrDivider('__________')
                        asSkinMesh.addAttr('extraVolume', en='False:True', at='enum', dv=1, k=1)
                        setAttr(skinMesh + '.' + 'extraVolume', 0)
                        setAttr(skinClust + '.skinningMethod', 0)
                        setDrivenKeyframe(skinClust + '.skinningMethod', currentDriver=skinMesh + '.' + 'extraVolume')
                        setAttr(skinMesh + '.' + 'extraVolume', 1)
                        setAttr(skinClust + '.skinningMethod', 2)
                        setDrivenKeyframe(skinClust + '.skinningMethod', currentDriver=skinMesh + '.' + 'extraVolume')
                all_InfList = [jnt for jnt in skinCluster(skinClust, inf=1, q=1) if nodeType(jnt) == 'joint']
                skinJntList = list(map(hsNode, all_InfList))
                skinJntList_Str = list(map(str, all_InfList))
                allSkinJntList = skinJntList[:]
                for _jnt in skinJntList:
                    if not _jnt.hasAttr('baseBlend') or not _jnt.hasAttr('tailBlend'):
                        _jnt.select()
                    else:
                        continue
                else:
                    HyperSkin.error('Oops ..!!\n\nFound No Hyper Skin Attributes on Joint : "{}"'.format(_jnt))

                if quickHyperSkin:
                    select(vtxList, r=1)
                    latList = lattice(divisions=(2, 5, 2), ldv=(2, 2, 2), objectCentered=True)
                    asLat = hsNode(latList[1])
                    asLatShp = latList[0]
                    ffdNode = asLat.getOutputs('ffd')
                    if ffdNode:
                        cmds.setAttr(ffdNode + '.envelope', 0)
                    asLat.hide()
                    asLat.scaleBy([1.01, 1.01, 1.01])
                    asLat.show()
                    reduceList = []
                    SkinJntListRemove = skinJntList.remove
                    ReduceListAppend = reduceList.append
                    innerJnts = []
                    InnerJntsAppend = innerJnts.append
                    for jnt in skinJntList:
                        splitLocList = jnt.jntSplit(4, nameSufx='_PosLoc', getPos=1, getEnds=1)
                        containsLoc = False
                        for splitLoc in splitLocList:
                            if not containsLoc:
                                if asLat.contains(splitLoc):
                                    containsLoc = True

                        if not containsLoc:
                            ReduceListAppend(jnt)
                        else:
                            InnerJntsAppend(jnt)

                    if reduceList:
                        for rdcJnt in reduceList:
                            if rdcJnt.parent() not in innerJnts and rdcJnt in skinJntList:
                                SkinJntListRemove(rdcJnt)

                    root_Jnt = HyperSkin.getRootJnt_FromJntsList(skinJntList)
                    if root_Jnt:
                        root_Jnt.select()
                        pJnt = root_Jnt.pickWalkUp(1, 'joint')
                        if pJnt:
                            if pJnt in allSkinJntList:
                                skinJntList.append(pJnt)
                    asLat.delete()
                    if reduceList and not vtxSelection:
                        for rdcJnt in reduceList:
                            if rdcJnt.parent() not in innerJnts:
                                if skinSide == 'LT' and rdcJnt.startswith(R_Prfx):
                                    continue
                                if skinSide == 'RT' and rdcJnt.startswith(L_Prfx):
                                    continue
                                HyperSkin.removeInfluences_skinClust(rdcJnt, skinMesh)

                        pm.select(skinMesh, r=1)
                        mel.removeUnusedInfluences()
                for skinJnt in skinJntList:
                    if not skinJnt.hasUniqueName():
                        skinJnt.select(r=1)
                        HyperSkin.deleteUnwanted_ND()
                        HyperSkin.error('More than one joint has same name "%s"' % skinJnt.shortName())

                skinMesh.select()
                skinCluster(skinClust, e=1, mi=1)
                jntVtxDict = {}
                vtx2JntDict = {}
                for jnt in skinJntList:
                    skinJnt = jnt.name()
                    skinCluster(skinClust, selectInfluenceVerts=skinJnt, e=1)
                    vtxList_Jnt = filterExpand(sm=31)
                    if vtxList_Jnt:
                        vtxList_Jnt = list(map(hsNode, vtxList_Jnt))
                        if skinSide == 'LT':
                            if prefixOrSuffix == 'Prefix' and not jnt.startswith(R_Prfx):
                                jntVtxDict[skinJnt] = vtxList_Jnt
                            elif prefixOrSuffix == 'Suffix' and not jnt.endswith(R_Prfx):
                                jntVtxDict[skinJnt] = vtxList_Jnt
                        else:
                            if skinSide == 'RT':
                                if prefixOrSuffix == 'Prefix' and not jnt.startswith(L_Prfx):
                                    jntVtxDict[skinJnt] = vtxList_Jnt
                                elif prefixOrSuffix == 'Suffix' and not jnt.endswith(L_Prfx):
                                    jntVtxDict[skinJnt] = vtxList_Jnt
                            else:
                                jntVtxDict[skinJnt] = vtxList_Jnt
                            for vtx in vtxList_Jnt:
                                vtx2JntDict[vtx] = jnt

                cmds.select(cl=1)
                skinMesh.select()
                skinCluster(skinClust, e=1, mi=3)
                [cmds.setAttr(jnt + '.liw', 0) for jnt in skinJntList]
                vtxJntList = list(jntVtxDict.keys())
                if not vtxJntList:
                    HyperSkin.error('Found No Skinned Joints On Selected Side With Selected Prefix / Suffix')
                HyperSkin.startProgressWin(len(vtxJntList), 'Collecting Required Info', None, False)
                for sknJnt in vtxJntList:
                    if sknJnt in skinJntList:
                        vtx_List = jntVtxDict[sknJnt]
                        if vtx_List:
                            for vtx in vtx_List:
                                skinPercent(skinClust, vtx, tv=(sknJnt, 1))

                    HyperSkin.progressWin(str(sknJnt), 0, __showProgressTime)

                HyperSkin.endProgressWin(len(vtxJntList), 1)
                HyperSkin.computeTime(0, 'Initial Blocking Of Weights', __displayTotalTime)
                dscSuffix = '_asSCnoDSC'
                jnt2dscDict = {jnt:jnt.shortName() + dscSuffix for jnt in skinJntList if cmds.objExists(jnt.shortName() + dscSuffix)}
                if jnt2dscDict:
                    dscJntList = list(jnt2dscDict.keys())
                    dscJntDict = {jnt:jnt.length() for jnt in dscJntList}
                    dscJntList = HyperSkin.sortByDict(dscJntDict, 'dn')
                    redo_vtx2JntDict = 0
                    if __showProgressTime:
                        if vtxSelection:
                            cmds.select(lastSelectedVtx, r=1)
                            HyperSkin.refreshView(1)
                    HyperSkin.startProgressWin(dscJntList, 'Solving Discs (ND Skin)', 'Please Wait', innerObjs=True)
                    excludeVtxWeightList = []
                    for dscJnt in dscJntList:
                        if dscJnt not in skinJntList:
                            continue
                        redo_vtx2JntDict = 1
                        checkJntList = [dscJnt]
                        childJnts = dscJnt.getChildren('joint')
                        if childJnts:
                            chdJnts = [chdJnt for chdJnt in childJnts if HyperSkin.isSkinJnt(chdJnt, skinMesh)]
                            if chdJnts:
                                checkJntList.extend(chdJnts)
                        parentJnts = dscJnt.parent(1, 1, 'joint')
                        if parentJnts:
                            parentJnts = [pJnt for pJnt in parentJnts if HyperSkin.isSkinJnt(pJnt, skinMesh)]
                            if parentJnts:
                                checkJntList.extend(parentJnts)
                        checkJntList = list(set(checkJntList))
                        _, vtxList_dsc, inf2VtxDict, vtx2InfDict = getVtxList_Influenced(checkJntList, skinMesh, dscSuffix=dscSuffix)
                        upJnts = dscJnt.pickWalkUp(2, 'joint')
                        dnJnts = dscJnt.pickWalkDown(2, 'joint')
                        weightedJnts = [dscJnt]
                        upJnts = [upJnts] if type(upJnts) != list else upJnts
                        dnJnts = [dnJnts] if type(dnJnts) != list else dnJnts
                        weightedJnts.extend(upJnts)
                        weightedJnts.extend(dnJnts)
                        for jnt in weightedJnts:
                            if jnt in all_InfList:
                                cmds.setAttr(jnt + '.liw', 0)

                        removeJnts = []
                        weightedJnts_Str = list(map(str, weightedJnts))
                        for jnt in all_InfList:
                            if str(jnt) not in weightedJnts_Str:
                                cmds.setAttr(jnt + '.liw', 1)
                                removeJnts.append(jnt)

                        HyperSkin.startProgressWin(innerList=vtxList, innerNote='Cleaning Non-Relavent Jnt Weights')
                        for vtx in vtxList:
                            if vtx in excludeVtxWeightList:
                                continue
                            HyperSkin.progressWin(ci=vtx, innerList=vtxList, ep=0, spt=__showProgressTime)
                            wDict = self.getSkinWeights(skinMesh, vtx, skinClust)
                            wJnts = self.sortByDict(wDict)
                            if wJnts:
                                dsc = dscJnt.shortName() + dscSuffix
                                if not HyperSkin.hasMeshContainsPos(dsc, str(vtx)):
                                    if removeJnts:
                                        for jnt in removeJnts:
                                            if jnt not in skinJntList and jnt in all_InfList:
                                                HyperSkin.setSkinWeights(str(vtx), {str(jnt): 0}, False, skinClust, unlockJnts=1, speedSkin=1)
                                                excludeVtxWeightList.append(vtx)

                        HyperSkin.progressReset()
                        if vtxList_dsc:
                            dsc = dscJnt.shortName() + dscSuffix
                            if parentJnts:
                                HyperSkin.startProgressWin(innerList=vtxList_dsc)
                                for vtx in vtxList_dsc:
                                    if HyperSkin.hasMeshContainsPos(dsc, vtx):
                                        HyperSkin.setSkinWeights(vtx, {parentJnts[0]: 1})
                                    else:
                                        chdJntExist = False
                                        dictJnts = list(inf2VtxDict.keys())
                                        for chdJnt in childJnts:
                                            if chdJnt in dictJnts:
                                                if vtx in inf2VtxDict[chdJnt]:
                                                    HyperSkin.setSkinWeights(vtx, {chdJnt: 1})
                                                    chdJntExist = True
                                                    break

                                    if not chdJntExist:
                                        HyperSkin.setSkinWeights(vtx, {dscJnt: 1})
                                    HyperSkin.progressWin(ci=vtx, innerList=vtxList_dsc, ep=0, spt=__showProgressTime)

                        HyperSkin.progressWin(dscJnt + dscSuffix, ep=0, spt=__showProgressTime)

                    HyperSkin.endProgressWin(dscJntList, 1)
                    if redo_vtx2JntDict:
                        jntVtxDict = {}
                        vtx2JntDict = {}
                        for jnt in skinJntList:
                            skinJnt = jnt.name()
                            skinCluster(skinClust, selectInfluenceVerts=skinJnt, e=1)
                            vtxList_Jnt = filterExpand(sm=31)
                            if vtxList_Jnt:
                                vtxList_Jnt = list(map(hsNode, vtxList_Jnt))
                                if skinSide == 'LT':
                                    if prefixOrSuffix == 'Prefix' and not jnt.startswith(R_Prfx):
                                        jntVtxDict[skinJnt] = vtxList_Jnt
                                    elif prefixOrSuffix == 'Suffix' and not jnt.endswith(R_Prfx):
                                        jntVtxDict[skinJnt] = vtxList_Jnt
                                else:
                                    if skinSide == 'RT':
                                        if prefixOrSuffix == 'Prefix' and not jnt.startswith(L_Prfx):
                                            jntVtxDict[skinJnt] = vtxList_Jnt
                                        elif prefixOrSuffix == 'Suffix' and not jnt.endswith(L_Prfx):
                                            jntVtxDict[skinJnt] = vtxList_Jnt
                                    else:
                                        jntVtxDict[skinJnt] = vtxList_Jnt
                                    for vtx in vtxList_Jnt:
                                        vtx2JntDict[vtx] = jnt

                    if jntVtxDict:
                        cmds.select(dscJntList[0], r=1)
                        cmds.select(jntVtxDict[dscJntList[0]], add=1)
                HyperSkin.computeTime(0, 'Fix Hyper Discs', __displayTotalTime)
                nonSknEndJnts = []
                NonSknEndJntsAppend = nonSknEndJnts.append
                IsIt_LastSkinJnt = HyperSkin.isIt_LastSkinJnt
                if not vtxSelection:
                    if skinSide == 'LT':
                        lastSelectedVtx = vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
                    elif skinSide == 'RT':
                        lastSelectedVtx = vtxList = HyperSkin.getMeshVtx(skinMesh, 'R_')
                    else:
                        lastSelectedVtx = vtxList = HyperSkin.getMeshVtx(skinMesh)
                vtxList = list(map(hsNode, vtxList))
                if __showProgressTime:
                    cmds.select(skinJntList, r=1)
                    HyperSkin.refreshView(1)
                HyperSkin.startProgressWin(len(skinJntList), 'Analyzing Joints : Level_00', None, False)
                skinJntList_Opp = []
                for jnt in skinJntList:
                    jntChild = None
                    HyperSkin.progressWin(('Num Jnts : {} <--> ').format(len(skinJntList)) + str(jnt), 0, __showProgressTime)
                    if skinSide == 'LT':
                        if prefixOrSuffix == 'Prefix' and jnt.startswith(R_Prfx):
                            cmds.setAttr(jnt + '.liw', 1)
                            skinJntList_Opp.append(jnt)
                            continue
                        elif prefixOrSuffix == 'Suffix' and jnt.endswith(R_Prfx):
                            cmds.setAttr(jnt + '.liw', 1)
                            skinJntList_Opp.append(jnt)
                            continue
                        else:
                            try:
                                jnt_Child = jnt.child()
                                if prefixOrSuffix == 'Prefix' and jnt_Child.startswith(R_Prfx) and prefixOrSuffix == 'Suffix' and jnt_Child.endswith(R_Prfx):
                                    if prefixOrSuffix == 'Prefix':
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.startswith(L_Prfx)]
                                    else:
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.endswith(L_Prfx)]
                                    if jntChildren:
                                        jntChild = jntChildren[0]
                                    else:
                                        select(jnt, r=1)
                                        HyperSkin.error('For "%s", Relative LT_Side Child Joint Is not Available' % jnt.shortName())
                                else:
                                    jntChild = jnt.pickWalkDown(1, 'joint')
                            except:
                                select(jnt, r=1)
                                errMsg = ('Oops ..!!\n\nFor This Skin Joint : "{}", \nFound No Child Joint\n').format(jnt.shortName())
                                errMsg += 'Try again by removing this influence joint from skin cluster\n\n'
                                errMsg += 'Please Note : If it is last joint like finger end or toe end joint,\n'
                                errMsg += 'Then its not needed in Hyper Skinning \\ Regular Skinning :)'
                                HyperSkin.error(errMsg)

                    elif skinSide == 'RT':
                        if prefixOrSuffix == 'Prefix' and jnt.startswith(L_Prfx):
                            cmds.setAttr(jnt + '.liw', 1)
                            skinJntList_Opp.append(jnt)
                            continue
                        elif prefixOrSuffix == 'Suffix' and jnt.endswith(L_Prfx):
                            cmds.setAttr(jnt + '.liw', 1)
                            skinJntList_Opp.append(jnt)
                            continue
                        else:
                            try:
                                jnt_Child = jnt.child()
                                if prefixOrSuffix == 'Prefix' and jnt_Child.startswith(L_Prfx) and prefixOrSuffix == 'Suffix' and jnt_Child.endswith(L_Prfx):
                                    if prefixOrSuffix == 'Prefix':
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.startswith(R_Prfx)]
                                    else:
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.endswith(R_Prfx)]
                                    if jntChildren:
                                        jntChild = jntChildren[0]
                                    else:
                                        select(jnt, r=1)
                                        HyperSkin.error('For "%s", Relative LT_Side Child Joint Is not Available' % jnt.shortName())
                                else:
                                    jntChild = jnt.pickWalkDown(1, 'joint')
                            except:
                                select(jnt, r=1)
                                errMsg = ('Oops ..!!\n\nFor This Skin Joint : "{}", \nFound No Child Joint\n').format(jnt.shortName())
                                errMsg += 'Try again by removing this influence joint from skin cluster\n\n'
                                errMsg += 'Please Note : If it is last joint like finger end or toe end joint,\n'
                                errMsg += 'Then its not needed in Hyper Skinning \\ Regular Skinning :)'
                                HyperSkin.error(errMsg)

                    else:
                        try:
                            jntChildren = [chd for chd in jnt.getChildren()]
                            if jntChildren:
                                jntChild = jntChildren[0]
                            else:
                                select(jnt, r=1)
                                HyperSkin.error('For "%s", Relative LT_Side Child Joint Is not Available' % jnt.shortName())
                            if not jntChild:
                                jntChild = jnt.pickWalkDown(1, 'joint')
                        except:
                            select(jnt, r=1)
                            errMsg = ('Oops ..!!\n\nFor This Skin Joint : "{}", \nFound No Child Joint\n').format(jnt.shortName())
                            errMsg += 'Try again by removing this influence joint from skin cluster\n\n'
                            errMsg += 'Please Note : If it is last joint like finger end or toe end joint,\n'
                            errMsg += 'Then its not needed in Hyper Skinning \\ Regular Skinning :)'
                            HyperSkin.error(errMsg)

                    if IsIt_LastSkinJnt(jnt, allSkinJntList):
                        if jntChild:
                            NonSknEndJntsAppend(jntChild)

                HyperSkin.endProgressWin(len(skinJntList), 1)
                HyperSkin.computeTime(0, 'Analyzing Joints', __displayTotalTime)
                jntCurvDict = {}
                cmds.delete('AHSS_ND_Curv_Grp') if cmds.objExists('AHSS_ND_Curv_Grp') else None
                ndCurvGrp = cmds.group(em=1, n='AHSS_ND_Curv_Grp')
                for jnt in skinJntList:
                    curvName = jnt.shortName() + '_NDCurv'
                    if not cmds.objExists(curvName):
                        posList = jnt.jntSplit(4, nameSufx='_PosLoc', getPos=1, getEnds=1)
                        try:
                            jntCurv = HyperSkin.generateCurv(curvName, 1, 1, posList)
                        except:
                            jnt.select(r=1)
                            HyperSkin.error("Can't generate curv")

                        jntCurv.parentTo(ndCurvGrp)
                        numSpans = jntCurv.getAttr('spans')
                        cmds.rebuildCurve(jntCurv, rt=0, ch=0, end=1, d=1, kr=0, s=numSpans, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
                        jntCurvDict[jnt.shortName()] = jntCurv

                if vtxSelection:
                    if __showProgressTime:
                        cmds.select(lastSelectedVtx, r=1)
                        HyperSkin.refreshView(1)
                HyperSkin.startProgressWin(vtxList, 'Hyper Skin Weighting (ND)..!!')
                for vtx in vtxList:
                    HyperSkin.progressWin(vtx)
                    try:
                        baseJnt = vtx2JntDict[vtx]
                    except:
                        continue

                    vtxNum = HyperSkin.extractNum(vtx)[0]
                    baseParentJnt = baseJnt.pickWalkUp(1, 'joint', parentImplied=1)
                    if not baseParentJnt:
                        continue
                    chdJnt = baseJnt.pickWalkDown(1, 'joint')
                    if not chdJnt:
                        continue
                    try:
                        baseBlend = baseJnt.getAttr('baseBlend')
                        if baseBlend <= 0.1:
                            baseBlend = 0.1
                        if baseBlend >= 0.9:
                            baseBlend = 0.9
                        baseBlend = baseBlend / 2.0
                        tailBlend = baseJnt.getAttr('tailBlend')
                        if tailBlend <= 0.1:
                            tailBlend = 0.1
                        if tailBlend >= 0.9:
                            tailBlend = 0.9
                        tailBlend = tailBlend / 2.0
                        moreVolume = baseJnt.getAttr('moreVolume')
                    except:
                        HyperSkin.deleteUnwanted_ND()
                        HyperSkin.error("%s's attribute 'baseBlend' | 'tailBlend' | 'moreVolume' is not available" % asDSC.shortName())

                    maxRangeVal = 1 - tailBlend
                    minRangeVal = baseBlend
                    isLastBaseSknJnt = HyperSkin.isLastJnt(baseJnt, 1, 0)
                    if cmds.objExists(baseJnt + dscSuffix):
                        jntLength = HyperSkin.mDistance(baseJnt + dscSuffix, chdJnt)[0]
                    else:
                        jntLength = baseJnt.distanceTo(chdJnt)[0]
                    vtxDist = 0
                    if cmds.objExists(baseJnt + dscSuffix) or cmds.objExists(chdJnt + dscSuffix):
                        if cmds.objExists(baseJnt + dscSuffix):
                            vtxDist = HyperSkin.getClosestDist(vtx, baseJnt + dscSuffix)
                        elif cmds.objExists(chdJnt + dscSuffix):
                            vtxDist = HyperSkin.getClosestDist(vtx, chdJnt + dscSuffix)
                            if vtxDist < jntLength:
                                vtxDist = jntLength - vtxDist
                            else:
                                vtxDist = 0.01
                    if not vtxDist:
                        nPnt = vtx.nearestPointOn(jntCurvDict[baseJnt.shortName()], 'crv', 0)
                        vtxDist = baseJnt.distanceTo(nPnt)[0]
                    if not isLastBaseSknJnt:
                        maxJntLength = jntLength * maxRangeVal
                        minJntLength = jntLength * minRangeVal
                        if vtxDist >= jntLength * minRangeVal and vtxDist <= jntLength * maxRangeVal:
                            setAttr(baseJnt + '.liw', 0)
                            skinPercent(skinClust, vtx, tv=(baseJnt, 1))
                            setAttr(baseJnt + '.liw', 1)
                        elif vtxDist < minJntLength:
                            skinPVal = HyperSkin.mapRange(vtxDist, 0, minJntLength, 0.5, 0.95)
                            setAttr(baseJnt + '.liw', 0)
                            skinPercent(skinClust, vtx, tv=(baseJnt, skinPVal))
                            setAttr(baseJnt + '.liw', 1)
                            if HyperSkin.isSkinJnt(baseParentJnt, skinMesh):
                                setAttr(baseParentJnt + '.liw', 0)
                                skinPercent(skinClust, vtx, tv=(baseParentJnt, 1 - skinPVal))
                            setAttr(skinClust + '.blendWeights[%d]' % vtxNum, 1)
                            if HyperSkin.isSkinJnt(baseParentJnt, skinMesh):
                                setAttr(baseParentJnt + '.liw', 1)
                        elif vtxDist > maxJntLength:
                            if vtxDist > jntLength / 2.0:
                                skinPVal = HyperSkin.mapRange(vtxDist, maxJntLength, jntLength, 0.99, 0.5)
                                setAttr(baseJnt + '.liw', 0)
                                skinPercent(skinClust, vtx, tv=(baseJnt, skinPVal))
                                setAttr(baseJnt + '.liw', 1)
                                if HyperSkin.isSkinJnt(chdJnt, skinMesh):
                                    setAttr(chdJnt + '.liw', 0)
                                    skinPercent(skinClust, vtx, tv=(chdJnt, 1 - skinPVal))
                                    setAttr(chdJnt + '.liw', 1)
                            else:
                                setAttr(baseJnt + '.liw', 0)
                                skinPercent(skinClust, vtx, tv=(baseJnt, 1))
                                setAttr(baseJnt + '.liw', 1)
                        minVal = 0.25
                        blendVtx = skinClust + '.blendWeights[%d]' % vtxNum
                        if moreVolume and __autoDualSkinning:
                            setAttr(blendVtx, 0)
                            if moreVolume == 1:
                                if vtxDist > 0 and vtxDist < jntLength / 2.0:
                                    blendVal = 1 - HyperSkin.mapRange(vtxDist, 0, jntLength, minVal, 1.0) + minVal
                                    setAttr(blendVtx, blendVal)
                            elif moreVolume == 2:
                                if vtxDist > jntLength / 2.0:
                                    blendVal = HyperSkin.mapRange(vtxDist, 0, jntLength, minVal, 1.0)
                                    setAttr(blendVtx, blendVal)
                            elif moreVolume == 3:
                                if vtxDist > 0 and vtxDist < jntLength / 2.0:
                                    blendVal = 1 - HyperSkin.mapRange(vtxDist, 0, jntLength / 2.0, minVal, 1.0) + minVal
                                    setAttr(blendVtx, blendVal)
                                elif vtxDist > jntLength / 2.0:
                                    blendVal = HyperSkin.mapRange(vtxDist, jntLength / 2.0, jntLength, minVal, 1.0)
                                    setAttr(blendVtx, blendVal)
                        else:
                            setAttr(blendVtx, 0)
                        if __showVtxDist:
                            if HyperSkin.extractNum(vtx)[0] == __showVtxDist:
                                warnignMsg = 'Normal Weighting\n================\n'
                                warnignMsg += ('Vertex Distance To "{}" Is : ').format(str(nearest_DSC)) + str(vtxDist)
                                warnignMsg += '\nMinimim Range Is : ' + str(jntLength * minRangeVal)
                                warnignMsg += '\nMaximim Range Is : ' + str(jntLength * maxRangeVal)
                                warnignMsg += '\nBaseJnt Weight : ' + str(skinPVal)
                                warnignMsg += ('\nJoint Length Is : {0}, {1}, {2}\n================\n').format(str(jntLength), baseJnt + dscSuffix, chdJnt + dscSuffix)
                                if moreVolume:
                                    warnignMsg2 = 'Blend Weighting\n\n----------------\n'
                                    warnignMsg2 += ('Vertex Distance To "{}" Is : ').format(str(nearest_DSC)) + str(vtxDist)
                                select(vtx, baseJnt, chdJnt, r=1)
                                cmds.sets(n='Distance Nodes')
                                om.MGlobal.displayWarning(warnignMsg)
                                return

                HyperSkin.endProgressWin(vtxList, 1)
                cmds.delete(ndCurvGrp)
                HyperSkin.computeTime(0, 'Hyper Skin Weighting (ND)', __displayTotalTime)
                allEndVtxSets_Solved = None
                allUpLineJnts_Solved = None
                fingerEndJntDict = {}
                if nonSknEndJnts:
                    for nonSknJnt in nonSknEndJnts:
                        if not nonSknJnt.hasUniqueName():
                            HyperSkin.deleteUnwanted()
                            nonSknJnt.select(r=1)
                            HyperSkin.error('More than one joint has same name "%s"' % nonSknJnt.shortName())

                    allEndVtxSets_Solved, allUpLineGCMs_Solved, allUpLineJnts_Solved, fingerEndVtxDict, fingerEndJntDict = ([], [], [], {}, {})
                    solvedList = HyperSkin.getSolvedJntsNGCMs(skinJntList, nonSknEndJnts)
                    if solvedList:
                        print(('solvedList :', solvedList))
                        allEndVtxSets_Solved, allUpLineGCMs_Solved, allUpLineJnts_Solved, fingerEndVtxDict, fingerEndJntDict = solvedList
                    else:
                        if vtxSelection:
                            if __showProgressTime:
                                cmds.select(sideVtxList_Ex, r=1)
                                HyperSkin.refreshView(1)
                            if HyperSkin.confirmAction('Paint Non-Selected Vertices ??'):
                                HyperSkin.startProgressWin(sideVtxList_Ex, 'Painting Non-Selected Vtx(s) !!')
                                for vtx in sideVtxList_Ex:
                                    HyperSkin.progressWin(vtx)
                                    HyperSkin.setSkinWeights(vtx, sideVtxDict_Ex[vtx])

                                HyperSkin.endProgressWin(sideVtxList_Ex, 1)
                        if skinJntList_Opp:
                            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList_Opp]
                        [cmds.setAttr(jnt + '.liw', 0) for jnt in all_InfList if jnt not in skinJntList_Opp]
                        skinMesh.select()
                        smoothTest = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
                        if smoothTest:
                            cmds.select(cl=1)
                            if skinSide == 'All':
                                if vtxSelection:
                                    HyperSkin.as_Generate_HyperSmooth(1, jntList=skinJntList)
                                else:
                                    HyperSkin.as_Generate_HyperSmooth(1)
                            elif vtxSelection:
                                HyperSkin.as_Generate_HyperSmooth(jntList=skinJntList)
                            else:
                                HyperSkin.as_Generate_HyperSmooth()
                        [cmds.setAttr(jnt + '.liw', 0) for jnt in all_InfList]
                        HyperSkin.computeTime(1, 'Hyper Smooth completed !!', __displayTotalTime)
                        return
                    select(allUpLineJnts_Solved, r=1)
                    select(allEndVtxSets_Solved, add=1)
                HyperSkin.computeTime(0, 'Level_00 : Finding End UpLine Joints', __displayTotalTime)
                HyperSkin.startProgressWin(vtxList, 'Solve Joints : Level_01', 'Level_01 : Solve Joints', False)
                if allEndVtxSets_Solved:
                    skinJntList_nonSolved = list(set(skinJntList) - set(allUpLineJnts_Solved))
                nearestJntDict = {}
                allSolvedJntList = []
                allNonSolvedVtxList = []
                solvedVtx_WentToSide = []
                solvedJnt_WentToSide = []
                endJnt2JntsDict = {}
                endJnt2LocsDict = {}
                endCurv2JntDict = {}
                endJnt2CurvsDict = {}
                splitLoc2JntDict = {}
                if __showProgressTime:
                    cmds.select(vtxList, r=1)
                    HyperSkin.refreshView(1)
                for vtx in vtxList:
                    HyperSkin.progressWin('Solve Joints - Level 01', False, __showProgressTime)
                    if allEndVtxSets_Solved:
                        if sets(allEndVtxSets_Solved, isMember=vtx):
                            for vtxSet in list(fingerEndVtxDict.keys()):
                                if sets(vtxSet, isMember=vtx):
                                    vtxEndJnt = hsNode(fingerEndVtxDict[vtxSet])
                                    try:
                                        numParents = vtxEndJnt.child().getAttr('numParents')
                                    except:
                                        HyperSkin.error('Oops.. Found No "%s"' % (str(vtxEndJnt.child()) + '.numParents'))

                                    break

                            if vtxEndJnt not in endJnt2JntsDict:
                                endJnt2JntsDict[vtxEndJnt] = []
                                upLineJnts_SolvedJnt = vtxEndJnt.parent(numParents, True, 'joint')
                                endJnt2JntsDict[vtxEndJnt] = upLineJnts_SolvedJnt
                                allSolvedJntList.extend(upLineJnts_SolvedJnt)
                                allSolvedJntList = list(set(allSolvedJntList))
                            if vtxEndJnt not in endJnt2LocsDict:
                                endJnt2LocsDict[vtxEndJnt] = []
                                for jnt in upLineJnts_SolvedJnt:
                                    splitLocList = jnt.jntSplit(4, nameSufx='_PosLoc', getLoc=1, getEnds=1)
                                    for splitLoc in splitLocList:
                                        splitLoc2JntDict[splitLoc] = jnt

                                    endJnt2LocsDict[vtxEndJnt].extend(splitLocList)

                            if vtxEndJnt not in endJnt2CurvsDict:
                                endJnt2CurvsDict[vtxEndJnt] = []
                                for jnt in upLineJnts_SolvedJnt:
                                    jntChild = jnt.child()
                                    splitCurv = HyperSkin.generateCurv(jnt.shortName() + '_Curv', 1, 1, [jnt, jntChild])
                                    endCurv2JntDict[splitCurv] = jnt
                                    endJnt2CurvsDict[vtxEndJnt].append(splitCurv)

                            currentSetJntsList = endJnt2JntsDict[vtxEndJnt]
                            currentSetLocsList = endJnt2LocsDict[vtxEndJnt]
                            currentSetCurvsList = endJnt2CurvsDict[vtxEndJnt]
                            nonSetJntsList = list(set(skinJntList) - set(currentSetJntsList))
                            wDict = HyperSkin.getSkinWeights(skinMesh, vtx, skinClust)
                            sknJnt = list(wDict.keys())[0]
                            if sknJnt in nonSetJntsList:
                                [cmds.setAttr(jnt + '.liw', 0) for jnt in currentSetJntsList]
                                solvedVtx_WentToSide.append(vtx)
                                solvedJnt_WentToSide.append(sknJnt)
                                nearCurv = HyperSkin.getNearestCurv(vtx, currentSetCurvsList)
                                sknJnt = endCurv2JntDict[nearCurv]
                                HyperSkin.setSkinWeights(vtx, {sknJnt: 1})
                        else:
                            allNonSolvedVtxList.append(vtx)
                    else:
                        allNonSolvedVtxList.append(vtx)

                for endJnt in list(endJnt2LocsDict.keys()):
                    delete(endJnt2LocsDict[endJnt])

                for endJnt in list(endJnt2CurvsDict.keys()):
                    delete(endJnt2CurvsDict[endJnt])

            HyperSkin.endProgressWin(vtxList, 1)
            HyperSkin.computeTime(0, 'Level_01 : Paint Solved Joints', __displayTotalTime)
            select(allNonSolvedVtxList, r=1)
            HyperSkin.refreshView(1)
            if allEndVtxSets_Solved:
                skinJntList_nonSolved = list(set(skinJntList) - set(allUpLineJnts_Solved))
            allNonSolvedJntList = None
            if allSolvedJntList:
                allNonSolvedJntList = list(set(skinJntList) - set(allSolvedJntList))
                if allNonSolvedJntList:
                    [cmds.setAttr(jnt + '.liw', 0) for jnt in allNonSolvedJntList if jnt not in skinJntList_Opp]
            [cmds.setAttr(jnt + '.liw', 1) for jnt in skinJntList_Opp]
            [cmds.setAttr(jnt + '.liw', 1) for jnt in allSolvedJntList]
            select(allNonSolvedVtxList, r=1)
            select(allNonSolvedJntList, add=1)
            nonSolvedJntList = []
            nonSolvedJntList_Opp = []
            if allNonSolvedJntList:
                for nonSolveJnt in allNonSolvedJntList:
                    if skinSide == 'LT':
                        if prefixOrSuffix == 'Prefix' and not nonSolveJnt.startswith(R_Prfx):
                            nonSolvedJntList.append(nonSolveJnt)
                        elif prefixOrSuffix == 'Suffix' and not nonSolveJnt.endswith(R_Prfx):
                            nonSolvedJntList.append(nonSolveJnt)
                        else:
                            nonSolvedJntList_Opp.append(nonSolveJnt)
                    elif prefixOrSuffix == 'Prefix' and not nonSolveJnt.startswith(L_Prfx):
                        nonSolvedJntList.append(nonSolveJnt)
                    elif prefixOrSuffix == 'Suffix' and not nonSolveJnt.endswith(L_Prfx):
                        nonSolvedJntList.append(nonSolveJnt)
                    else:
                        nonSolvedJntList_Opp.append(nonSolveJnt)

                select(nonSolvedJntList, r=1)
            HyperSkin.startProgressWin(len(allNonSolvedVtxList), 'Solve Joints : Level_02', 'Paint Non-Solved Vertices', False)
            for vtx in allNonSolvedVtxList:
                HyperSkin.progressWin('Solve Joints - Level 02', False, __showProgressTime)
                wDict = HyperSkin.getSkinWeights(skinMesh, vtx, skinClust)
                infList = list(wDict.keys())
                if not infList:
                    continue
                sknJnt = infList[0]
                if sknJnt in allSolvedJntList:
                    mDict = {key:0 for key in wDict}
                    HyperSkin.setSkinWeights(vtx, mDict)

        HyperSkin.endProgressWin(allNonSolvedVtxList, 1)
        HyperSkin.computeTime(0, 'Level_02 : Painting Non Solved Joints', __displayTotalTime)
        if vtxSelection:
            if HyperSkin.confirmAction('Paint Non-Selected Vertices ??'):
                if __showProgressTime:
                    cmds.select(sideVtxList_Ex, r=1)
                    HyperSkin.refreshView(1)
                HyperSkin.startProgressWin(sideVtxList_Ex, 'Paint Non-Selected : Level_03', 'Paint Non-Solved Vertices')
                for vtx in sideVtxList_Ex:
                    HyperSkin.progressWin(vtx)
                    HyperSkin.setSkinWeights(vtx, sideVtxDict_Ex[vtx])

                HyperSkin.endProgressWin(sideVtxList_Ex, 1)
        [cmds.setAttr(jnt + '.liw', 0) for jnt in all_InfList]
        smoothTest = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
        if smoothTest:
            if skinJntList_Opp:
                for jnt in skinJntList_Opp:
                    skinJntList.remove(jnt)

            cmds.select(cl=1)
            skinMesh.select()
            if fingerEndJntDict:
                endJntList = list(fingerEndJntDict.keys())
                for jnt in endJntList:
                    exList = endJntList[:]
                    exList.remove(jnt)
                    for exJnt in exList:
                        [cmds.setAttr(exJnt + '.liw', 1) for exJnt in fingerEndJntDict[exJnt]]

                    HyperSkin.as_Generate_HyperSmooth(jl=fingerEndJntDict[jnt], pw=0)
                    for exJnt in exList:
                        [cmds.setAttr(exJnt + '.liw', 0) for exJnt in fingerEndJntDict[exJnt]]

            if allEndVtxSets_Solved:
                select(allEndVtxSets_Solved, r=1)
                solvedVtxWgtsDict = {}
                for vtx in filterExpand(sm=31):
                    solvedVtxWgtsDict[vtx] = HyperSkin.getSkinWeights(skinMesh, vtx, skinClust)

            if nonSolvedJntList_Opp:
                [cmds.setAttr(jnt + '.liw', 1) for jnt in nonSolvedJntList_Opp]
            select(cl=1)
            skinJntList_fromVtxList = HyperSkin.getSkinJntsList(vtxList)
            HyperSkin.as_Generate_HyperSmooth(False, None, skinJntList_fromVtxList)
            if allEndVtxSets_Solved:
                select(cl=1)
                for vtx in list(solvedVtxWgtsDict.keys()):
                    HyperSkin.setSkinWeights(vtx, solvedVtxWgtsDict[vtx])

                select(allEndVtxSets_Solved, r=1)
        HyperSkin.computeTime(1, 'Hyper Smooth completed !!', __displayTotalTime)
        return

    def as_Generate_HyperSkin_Disc(self):
        global lastSelectedVtx
        gc.disable()
        cmds.undoInfo(openChunk=True, chunkName='Process Objects')
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 0
        _as_HyperSkinMain__displayTotalTime = 0
        _as_HyperSkinMain__showInnerGCMs = 0
        _as_HyperSkinMain__showVtxDist = 0
        _as_HyperSkinMain__showGCMs_AndStop = 0
        _as_HyperSkinMain__freeVersion = 0
        _as_HyperSkinMain__autoDualSkinning = 1
        if _as_HyperSkinMain__showInnerGCMs or _as_HyperSkinMain__showGCMs_AndStop:
            confirm = HyperSkin.confirmAction('Hyper GCMs Will Be Visible !!\nContinue To Hyper Skin?', eb1='Default Skin', ea1=(HyperSkin.dafaultSkin))
            confirm or HyperSkin.error('Action Cancelled !!')
        else:
            if confirm == 'Default Skin':
                return
            else:
                HyperSkin.refreshView(1)
                R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
                L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
                skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
                refCount = 1
                prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
                if prefixOrSuffix != 'Prefix' and prefixOrSuffix != 'Suffix':
                    prefixOrSuffix = 'Prefix'
            extractGCMs = checkBox('as_ExtractGCMs_CB', q=1, v=1)
            smoothTest = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
            quickHyperSkin = checkBox('as_QuickHyperSkin_CB', q=1, v=1)
            excludeJntName = 'Fan'
            tempSelected = cmds.ls(sl=1, fl=1)
            if tempSelected:
                if '.' not in str(tempSelected[0]):
                    selObj = hsNode(tempSelected[0])
                    if selObj.isMesh():
                        textField('as_SkinMesh_TF', e=1, tx=(selObj.strip()))
                    else:
                        HyperSkin.endProgressWin(1, 1)
                        HyperSkin.error('Oops.. Selected Is Not A Mesh..!\nSkinned Mesh needs to be selected')
                else:
                    selObj = hsNode(filterExpand(sm=31)[0].split('.')[0])
                    if selObj.isMesh():
                        if selObj.isShape():
                            selObj = selObj.parent()
                        textField('as_SkinMesh_TF', e=1, tx=(selObj.strip()))
                    else:
                        HyperSkin.endProgressWin(1, 1)
                        HyperSkin.error('Oops.. Selected Is Not A Mesh..!\nSkinned Mesh needs to be selected')
                cmds.select(tempSelected, r=1)
            vtxSelection = False
            if not filterExpand(sm=31):
                if skinSide == 'LT':
                    HyperSkin.selectSkinVertices('L_')
                else:
                    if skinSide == 'RT':
                        HyperSkin.selectSkinVertices('R_')
                    lastSelectedVtx = vtxList = filterExpand(sm=31)
                    cmds.select(cl=1)
            else:
                vtxSelection = True
                lastSelectedVtx = vtxList = filterExpand(sm=31)
            if not _as_HyperSkinMain__showInnerGCMs:
                if not _as_HyperSkinMain__showProgressTime:
                    if extractGCMs:
                        if not HyperSkin.confirmAction('Proceed to Extract Proxy Mesh\nOn "%s" Side ..?' % skinSide):
                            HyperSkin.endProgressWin(1, 1)
                            raise RuntimeError('Action terminated ..!')
            HyperSkin.refreshView(1)
            HyperSkin.startTime(_as_HyperSkinMain__displayTotalTime)

            def unhideNodes(nodeList):
                nodeList = [nodeList] if type(nodeList) != list else nodeList
                for node in [hsNode(obj) for obj in nodeList]:
                    node.setAttr('v', lock=0, channelBox=1, keyable=1)
                    if node.isMesh():
                        nodeShape = node.getShape()
                        nodeShape.setAttr('intermediateObject', 0)
                        nodeShape.setAttr('lodVisibility', 1)
                        nodeShape.setAttr('visibility', 1)
                        nodeShape.setAttr('template', 0)
                        nodeShape.setAttr('displayVertices', 0)
                        nodeShape.setAttr('displayUVs', 0)
                    if node.isCurv():
                        nodeShape = node.getShape()
                        nodeShape.setAttr('intermediateObject', 0)
                        nodeShape.setAttr('lodVisibility', 1)
                        nodeShape.setAttr('visibility', 1)
                        nodeShape.setAttr('template', 0)
                        nodeShape.setAttr('overrideEnabled', 0)
                        nodeShape.setAttr('overrideDisplayType', 0)
                        nodeShape.setAttr('overrideLevelOfDetail', 0)
                        nodeShape.setAttr('overrideVisibility', 1)
                    if HyperSkin.isMesh(node) or HyperSkin.isJnt(node) or node.isCurv():
                        node.setAttr('lodVisibility', 1)
                        node.setAttr('visibility', 1)
                        node.setAttr('template', 0)
                        node.setAttr('overrideEnabled', 0)
                        node.setAttr('overrideDisplayType', 0)
                        node.setAttr('overrideLevelOfDetail', 0)
                        node.setAttr('overrideVisibility', 1)
                    if HyperSkin.isJnt(node):
                        node.setAttr('drawStyle', 2)
                        node.setAttr('radius', 0)
                    if HyperSkin.isMesh(node):
                        if not objExists('my_Shader'):
                            myShdr = shadingNode('lambert', asShader=1, n='my_Shader')
                            myShdr.setAttr('color', 0, 0, 0, type='double3')
                        else:
                            myShdr = PyNode('my_Shader')
                        select(node, r=1)
                        hyperShade('my_Shader', assign='my_Shader')
                        myShdr.setAttr('transparency', 1, 1, 1, type='double3')

            if objExists('as_TempGCM_Grp'):
                delete('as_TempGCM_Grp')
            tempGCMGrp = hsNode(group(em=1, n='as_TempGCM_Grp'))
        if vtxList:
            skinMesh = PyNode(vtxList[0].split('.')[0])
        else:
            skinMesh = PyNode(textField('as_SkinMesh_TF', q=1, tx=1))
            if skinSide == 'LT':
                lastSelectedVtx = vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
            else:
                if skinSide == 'RT':
                    lastSelectedVtx = vtxList = HyperSkin.getMeshVtx(skinMesh, 'R_')
            asSkinMesh = hsNode(skinMesh)
            skinClust = listHistory(skinMesh, type='skinCluster')[0]
            skinClustNum = HyperSkin.extractNum(skinClust)[1]
            gcmSuffix = '_asSC' + skinClustNum + 'GCM'
            dscSuffix = '_asSC' + skinClustNum + 'DSC'
        if _as_HyperSkinMain__autoDualSkinning:
            if not attributeQuery('extraVolume', n=(skinMesh.name()), ex=1):
                asSkinMesh.addAttrDivider('__________')
                asSkinMesh.addAttr('extraVolume', en='False:True', at='enum', dv=1, k=1)
                setAttr(skinMesh + '.' + 'extraVolume', 0)
                setAttr(skinClust + '.skinningMethod', 0)
                setDrivenKeyframe((skinClust + '.skinningMethod'), currentDriver=(skinMesh + '.' + 'extraVolume'))
                setAttr(skinMesh + '.' + 'extraVolume', 1)
                setAttr(skinClust + '.skinningMethod', 2)
                setDrivenKeyframe((skinClust + '.skinningMethod'), currentDriver=(skinMesh + '.' + 'extraVolume'))
            all_InfList = [jnt for jnt in skinCluster(skinClust, inf=1, q=1) if nodeType(jnt) == 'joint']
            skinJntList = list(map(hsNode, all_InfList))
            allSkinJntList = skinJntList[:]
            if _as_HyperSkinMain__freeVersion:
                vtxCount = len(vtxList)
                cmds.select(vtxList, r=1)
                if vtxCount >= 6000:
                    HyperSkin.deleteUnwanted()
                    web.open('https://www.yogeshnichal.com')
                    errorMsg = 'This Is Limited Version Of AHSS !!\nVertex Count ([Left | Right] & Center) Should Be Less Than 3000 ..!!'
                    errorMsg += '\n\nIf you need unlimited version right now ?  Please contact at : yogeshnichal.com for more details !!'
                    self._as_HyperSkinMain__confirmAction(errorMsg)
                    return
                freeJntList = [jnt for jnt in allSkinJntList]
                if skinSide == 'LT':
                    if prefixOrSuffix == 'Prefix':
                        freeJntList = [jnt for jnt in allSkinJntList if not jnt.startswith(R_Prfx)]
            else:
                freeJntList = [jnt for jnt in allSkinJntList if not jnt.endswith(R_Prfx)]
        else:
            if skinSide == 'RT':
                if prefixOrSuffix == 'Prefix':
                    freeJntList = [jnt for jnt in allSkinJntList if not jnt.startswith(L_Prfx)]
                else:
                    freeJntList = [jnt for jnt in allSkinJntList if not jnt.endswith(L_Prfx)]
            else:
                cmds.select(freeJntList, r=1)
                jntCount = len(freeJntList)
                if jntCount > 60:
                    HyperSkin.deleteUnwanted()
                    web.open('https://www.yogeshnichal.com')
                    errorMsg = 'This Is Limited Version Of AHSS !!\nJoints Count ([Left | Right] & Center) Should Be Less Than 30 ..!'
                    errorMsg += '\n\nIf you need unlimited version right now ?  Please contact at : yogeshnichal.com for more details !!'
                    self._as_HyperSkinMain__confirmAction(errorMsg)
                    return
                select(vtxList, r=1)
                latList = lattice(divisions=(2, 5, 2), ldv=(2, 2, 2), objectCentered=True)
                asLat = hsNode(latList[1])
                asLatShp = latList[0]
                if quickHyperSkin:
                    ffdNode = asLat.getOutputs('ffd')
                    if ffdNode:
                        cmds.setAttr(ffdNode + '.envelope', 0)
                    asLat.hide()
                    asLat.scaleBy([1.05, 1.05, 1.05])
                    asLat.show()
                    reduceList = []
                    SkinJntListRemove = skinJntList.remove
                    ReduceListAppend = reduceList.append
                    for jnt in skinJntList:
                        splitLocList = jnt.jntSplit(4, nameSufx='_PosLoc', getPos=1, getEnds=1)
                        containsLoc = False
                        for splitLoc in splitLocList:
                            if containsLoc or asLat.contains(splitLoc):
                                containsLoc = True

                        if not containsLoc:
                            ReduceListAppend(jnt)

                    if reduceList:
                        for jnt in reduceList:
                            SkinJntListRemove(jnt)

                    top_Jnt = HyperSkin.getRootJnt_FromJntsList(skinJntList)
                    if top_Jnt:
                        top_Jnt.select()
                        pJnt = top_Jnt.pickWalkUp(1, 'joint')
                        if pJnt:
                            if pJnt in allSkinJntList:
                                skinJntList.append(pJnt)
                    asLat.hide()
                for skinJnt in skinJntList:
                    if not skinJnt.hasUniqueName():
                        skinJnt.select(r=1)
                        HyperSkin.error('More than one joint has same name "%s"' % skinJnt.shortName())

                if not extractGCMs:
                    infJntList = skinCluster(skinClust, inf=1, q=1)
                    for jnt in infJntList:
                        if prefixOrSuffix == 'Prefix':
                            if jnt.startswith(R_Prfx):
                                setAttr(jnt + '.liw', 1)
                            elif jnt.endswith(R_Prfx):
                                setAttr(jnt + '.liw', 1)

                    for vtx in vtxList:
                        valList = skinPercent(skinClust, vtx, q=1, v=1)
                        if not valList:
                            HyperSkin.error('Please check if selection of vertices are made from more than one mesh !!')
                        for num in range(len(valList)):
                            if prefixOrSuffix == 'Prefix':
                                if valList[num] > 0.0 and infJntList[num].startswith(R_Prfx):
                                    skinPercent(skinClust, vtx, tv=(infJntList[num], 0.0))
                                elif valList[num] > 0.0:
                                    if infJntList[num].endswith(R_Prfx):
                                        skinPercent(skinClust, vtx, tv=(infJntList[num], 0.0))

                else:
                    libPath = sceneName().parent + '/AHSS_Lib'
                    skipPath = libPath + '/' + skinMesh + '_SkipInfo.txt'
                    if not os.path.exists(libPath):
                        sysFile(libPath, makeDir=True)
                    lastJntList = []
                    excludeJntList = []
                    lastJntsAppend = lastJntList.append
                    excludeJntsAppend = excludeJntList.append
                    IsIt_LastSkinJnt = HyperSkin.isIt_LastSkinJnt
                    IsLastJnt = HyperSkin.isLastJnt
                    if not os.path.exists(skipPath):
                        if vtxSelection:
                            _skinJntList = allSkinJntList[:]
                        else:
                            _skinJntList = skinJntList[:]
                        HyperSkin.startProgressWin(len(_skinJntList), 'Collecting Required Info ..!!')
                        for jnt in _skinJntList:
                            HyperSkin.progressWin(None, 0, _as_HyperSkinMain__showProgressTime, rv=0)
                            if R_Prfx not in jnt and IsIt_LastSkinJnt(jnt, _skinJntList, 0, False, True):
                                if IsLastJnt(jnt):
                                    lastJntsAppend(jnt)
                                    continue
                                if excludeJntName in str(jnt):
                                    excludeJntsAppend(jnt)

                        HyperSkin.endProgressWin(1, True)
                        exListStr = ''
                        if lastJntList:
                            select(lastJntList, r=1)
                            exList = [str(jnt) for jnt in lastJntList]
                            exListStr = ', '.join(exList)
                        fileIO = open(skipPath, 'w')
                        fileIO.writelines(exListStr)
                        fileIO.close()
                    else:
                        with open(skipPath, 'r') as (f):
                            fTxt = f.readline()
                        if fTxt:
                            jntsList = fTxt.split(', ')
                            try:
                                lastJntList = list(map(hsNode, jntsList))
                            except:
                                if HyperSkin.confirmAction('Remove this file "{}"to start Hyper Skin again'.format(skipPath)):
                                    sysFile(skipPath, delete=True)
                                HyperSkin.error('Content of "AHSS_Lib\\{meshName\\}_SkipInfo.txt" has been modified')

                        else:
                            lastJntList = []
                        for jnt in lastJntList:
                            if not IsLastJnt(jnt):
                                if HyperSkin.confirmAction('Remove this file "{}"to start Hyper Skin again'.format(skipPath)):
                                    sysFile(skipPath, delete=True)
                                HyperSkin.error('Content of "AHSS_Lib\\{meshName\\}_SkipInfo.txt" has been modified. \n"{}" is not last joint'.format(jnt.name()))

                        select(skinMesh, r=1)
                        for lastJnt in lastJntList:
                            try:
                                skinCluster(skinClust, e=1, ri=(str(lastJnt)))
                            except:
                                pass

                SkinJntsRemove = skinJntList.remove
                if lastJntList:
                    for lastJnt in lastJntList:
                        if not lastJnt.hasUniqueName():
                            if HyperSkin.confirmAction('More than one joint has same name "%s"\nRename and Continue?' % lastJnt.shortName()):
                                lastJnt.nextUniqueName(True, True)
                            else:
                                HyperSkin.error('More than one joint has same name "%s"' % lastJnt.shortName())
                        select(lastJnt, r=1)
                        try:
                            SkinJntsRemove(lastJnt)
                        except:
                            pass

                [SkinJntsRemove(fanJnt) for fanJnt in excludeJntList if fanJnt in skinJntList] if excludeJntList else None
                if vtxSelection:
                    if _as_HyperSkinMain__showProgressTime:
                        cmds.select(lastSelectedVtx, r=1)
                        HyperSkin.refreshView(1)
                nonSknEndJnts = []
                NonSknEndJntsAppend = nonSknEndJnts.append
                if _as_HyperSkinMain__showInnerGCMs:
                    asSkinMesh.template()
                HyperSkin.startProgressWin(len(skinJntList), 'Level_00: Generating GCMs', None, False)
                for jnt in skinJntList:
                    HyperSkin.progressWin((str(jnt)), 0, _as_HyperSkinMain__showProgressTime, rv=0)
                    if skinSide == 'LT':
                        if prefixOrSuffix == 'Prefix':
                            if jnt.startswith(R_Prfx):
                                cmds.setAttr(jnt + '.liw', 1)
                                continue
                            elif prefixOrSuffix == 'Suffix' and jnt.endswith(R_Prfx):
                                cmds.setAttr(jnt + '.liw', 1)
                                continue
                        else:
                            try:
                                jnt_Child = jnt.child()
                                if prefixOrSuffix == 'Prefix' and jnt_Child.startswith(R_Prfx) and prefixOrSuffix == 'Suffix' and jnt_Child.endswith(R_Prfx):
                                    if prefixOrSuffix == 'Prefix':
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.startswith(L_Prfx)]
                                    else:
                                        jntChildren = [chd for chd in jnt.getChildren() if chd.endswith(L_Prfx)]
                                    if jntChildren:
                                        jntChild = jntChildren[0]
                                    else:
                                        HyperSkin.deleteUnwanted()
                                        select(jnt, r=1)
                                        HyperSkin.error('For "%s", Relative LT_Side Child Joint Is not Available' % jnt.shortName())
                                else:
                                    jntChild = jnt.pickWalkDown(1, 'joint')
                            except:
                                HyperSkin.deleteUnwanted()
                                select(jnt, r=1)
                                HyperSkin.error('For This Skin Joint : "{0:s}", \nFound No Child Joint' % jnt.shortName())

                    else:
                        if skinSide == 'RT':
                            if prefixOrSuffix == 'Prefix':
                                if not jnt.startswith(L_Prfx) or prefixOrSuffix == 'Suffix' or jnt.endswith(L_Prfx):
                                    cmds.setAttr(jnt + '.liw', 1)
                                    continue
                                else:
                                    if jnt.child().startswith(L_Prfx) or jnt.child().endswith(L_Prfx):
                                        jntChildren = [chd for chd in jnt.getChildren() if not chd.startswith(R_Prfx) if chd.endswith(R_Prfx)]
                                        if jntChildren:
                                            jntChild = jntChildren[0]
                                        else:
                                            HyperSkin.deleteUnwanted()
                                            select(jnt, r=1)
                                            HyperSkin.error('For "%s", Relative RT_Side Child Joint Is not Available' % jnt.shortName())
                                    else:
                                        jntChild = jnt.pickWalkDown(1, 'joint')
                            else:
                                NonSknEndJntsAppend(jntChild) if IsIt_LastSkinJnt(jnt, allSkinJntList) else None
                                try:
                                    ctrlOuter_Jnt = hsNode(jnt.shortName() + dscSuffix + '_Outer')
                                except:
                                    HyperSkin.deleteUnwanted()
                                    checkBox('as_QuickHyperSkin_CB', e=1, v=1)
                                    if quickHyperSkin:
                                        asLat.delete()
                                    modificationMsg = 'You might have chosen option "Ignore Unwanted Skinned Joints",'
                                    modificationMsg += '\n during "Create Hyper Discs" or '
                                    modificationMsg += '\n\nTry Again With "Quick Skin" Option "On" !!'
                                    HyperSkin.message(modificationMsg)
                                    modificationMsg = 'And.. \nNew influence joints might be added after discs are already created'
                                    modificationMsg += '\nIf so, Run "Create" from "Hyper Discs" section by selecting newly/ recently added joint'
                                    modificationMsg += '\n\nPlease check for selected joint now, it might be newly added influence'
                                    HyperSkin.message(modificationMsg)
                                    select(jnt, r=1)
                                    HyperSkin.error('Oops..!\n"%s" -Object not exists\nOr It has non-unique name' % (jnt.shortName() + dscSuffix + '_Outer'))

                            if objExists(ctrlOuter_Jnt.name()):
                                if not (objExists(jnt.shortName() + dscSuffix) and ctrlOuter_Jnt.isCurv()):
                                    HyperSkin.deleteUnwanted()
                                    checkBox('as_QuickHyperSkin_CB', e=1, v=1)
                                    if quickHyperSkin:
                                        asLat.delete()
                                    modificationMsg = 'You might have chosen option "Ignore Unwanted Skinned Joints",'
                                    modificationMsg += '\n during "Create Hyper Discs" or '
                                    modificationMsg += '\n\nTry Again With "Quick Skin" Option "On" !!'
                                    HyperSkin.message(modificationMsg)
                                    modificationMsg = 'And.. \nNew influence joints might be added after discs are already created'
                                    modificationMsg += '\nIf so, Run "Create" from "Hyper Discs" section by selecting newly/ recently added joint'
                                    modificationMsg += '\n\nPlease check for selected joint now, it might be newly added influence'
                                    HyperSkin.message(modificationMsg)
                                    select(jnt, r=1)
                                    HyperSkin.error('Oops..!\n"%s" or "%s" -Object not Exists\nOr It is modified' % (jnt.shortName() + dscSuffix, ctrlOuter_Jnt))
                        else:
                            try:
                                if not attributeQuery('dscChd', n=(jnt.name()), ex=1):
                                    ctrlOuter_JntChd = hsNode(jntChild.shortName() + dscSuffix + '_Outer')
                                else:
                                    dscChdJnt = HyperSkin.getChild_DSC(jnt)
                                    ctrlOuter_JntChd = hsNode(dscChdJnt.shortName() + dscSuffix + '_Outer')
                            except:
                                HyperSkin.deleteUnwanted()
                                checkBox('as_QuickHyperSkin_CB', e=1, v=1)
                                if quickHyperSkin:
                                    asLat.delete()
                                modificationMsg = 'You might have chosen option "Ignore Unwanted Skinned Joints",'
                                modificationMsg += '\n during "Create Hyper Discs" or '
                                modificationMsg += '\n\nTry Again With "Quick Skin" Option "On" !!'
                                HyperSkin.message(modificationMsg)
                                modificationMsg = 'And.. \nNew influence joints might be added after discs are already created'
                                modificationMsg += '\nIf so, Run "Create" from "Hyper Discs" section by selecting newly/ recently added joint'
                                modificationMsg += '\n\nPlease check for selected joint now, it might be newly added influence'
                                modificationMsg += '\n\nTry running "Hyper Skin"\tAgain'
                                HyperSkin.message(modificationMsg)
                                select(jnt, r=1)
                                if jntChild:
                                    HyperSkin.error('Oops..!\n"%s" -Object not exists\nOr It has non-unique name' % (jntChild.shortName() + dscSuffix + '_Outer'))
                                else:
                                    if os.path.exists(skipPath):
                                        sysFile(skipPath, delete=1)
                                    HyperSkin.error('Oops..!\n"%s" -Object not exists\nOr It has non-unique name\nOr End joint is skinned' % ('NoJntChild' + dscSuffix + '_Outer'))

                            if objExists(ctrlOuter_JntChd):
                                if not (objExists(jntChild.shortName() + dscSuffix) and ctrlOuter_JntChd.isCurv()):
                                    HyperSkin.deleteUnwanted()
                                    checkBox('as_QuickHyperSkin_CB', e=1, v=1)
                                    if quickHyperSkin:
                                        asLat.delete()
                                    modificationMsg = 'You might have chosen option "Ignore Unwanted Skinned Joints",'
                                    modificationMsg += '\n during "Create Hyper Discs" or '
                                    modificationMsg += '\n\nTry Again With "Quick Skin" Option "On" !!'
                                    HyperSkin.message(modificationMsg)
                                    modificationMsg = 'And.. \nNew influence joints might be added after discs are already created'
                                    modificationMsg += '\nIf so, Run "Create" from "Hyper Discs" section by selecting newly/ recently added joint'
                                    modificationMsg += '\n\nPlease check for selected joint now, it might be newly added influence'
                                    modificationMsg += '\n\nTry running "Hyper Skin"\tAgain'
                                    HyperSkin.message(modificationMsg)
                                    select(jnt, r=1)
                                    if jntChild:
                                        HyperSkin.error('Oops..!\n"%s" -Object not Exists\nOr It is modified' % (jntChild.shortName() + dscSuffix))
                                    else:
                                        if os.path.exists(skipPath):
                                            sysFile(skipPath, delete=1)
                                        HyperSkin.error('Oops..!\n"%s" -Object not Exists\nOr It is modified\nOr End joint is skinned' % ('NoJntChild' + dscSuffix))
                                discName = jnt.shortName() + gcmSuffix
                                if objExists(discName):
                                    delete(discName)
                                unhideNodes([ctrlOuter_Jnt, ctrlOuter_JntChd])
                                jntGCM = hsNode(loft(ctrlOuter_Jnt, ctrlOuter_JntChd, c=0, ch=0, d=1, ss=1, rsn=True, ar=1, u=1, rn=0, po=1, n=discName)[0])
                                jntGCM.centerPivot()
                                if _as_HyperSkinMain__showInnerGCMs:
                                    jntGCM.select()
                                    HyperSkin.refreshView(1)
                            else:
                                HyperSkin.hideNodes([ctrlOuter_Jnt, ctrlOuter_JntChd])
                        jntGCM.parentTo(tempGCMGrp)

                HyperSkin.endProgressWin(len(skinJntList), 1)
                if _as_HyperSkinMain__showInnerGCMs:
                    pass
                if nonSknEndJnts:
                    for nonSknJnt in nonSknEndJnts:
                        if not nonSknJnt.hasUniqueName():
                            HyperSkin.deleteUnwanted()
                            nonSknJnt.select(r=1)
                            HyperSkin.error('More than one joint has same name "%s"' % nonSknJnt.shortName())

                skinGCMList = []
                allGCMList = []
                SkinGCMsAppend = skinGCMList.append
                SkinGCMsRemove = skinGCMList.remove
                AllGCMsAappend = allGCMList.append
                for jnt in skinJntList:
                    if objExists(jnt.shortName() + gcmSuffix):
                        asJntGCM = hsNode(jnt + gcmSuffix)
                        HyperSkin.mConstrain([jnt, asJntGCM], 'parent')
                        SkinGCMsAppend(asJntGCM)
                        AllGCMsAappend(asJntGCM)

                if extractGCMs:
                    HyperSkin.hideNodes(allGCMList)
                    asMeshGrpName = 'as_' + HyperSkin.name(skinMesh) + '_MeshGrp'
                    asMeshGrp = hsNode(group(em=1, n=asMeshGrpName, p=hyperSkinGrp)) if not objExists(asMeshGrpName) else hsNode(asMeshGrpName)
                    C_GCMGrpName = 'as_C_GCM_SC' + skinClustNum + '_Grp'
                    C_GCMGrp = hsNode(group(em=1, n=C_GCMGrpName, p=asMeshGrp)) if not objExists(C_GCMGrpName) else hsNode(C_GCMGrpName)
                    L_GCMGrpName = 'as_L_GCM_SC' + skinClustNum + '_Grp'
                    L_GCMGrp = hsNode(group(em=1, n=L_GCMGrpName, p=asMeshGrp)) if not objExists(L_GCMGrpName) else hsNode(L_GCMGrpName)
                    R_GCMGrpName = 'as_R_GCM_SC' + skinClustNum + '_Grp'
                    R_GCMGrp = hsNode(group(em=1, n=R_GCMGrpName, p=asMeshGrp)) if not objExists(R_GCMGrpName) else hsNode(R_GCMGrpName)
                    HyperSkin.startProgressWin(len(allGCMList), 'Collecting Joints ..!', None, False)
                    for gcm in allGCMList:
                        HyperSkin.progressWin(gcm, False, _as_HyperSkinMain__showProgressTime, rv=0)
                        unhideNodes(gcm)
                        if not prefixOrSuffix == 'Prefix' or gcm.startswith(L_Prfx) or prefixOrSuffix == 'Suffix' and gcm.endswith(L_Prfx):
                            parent(gcm, L_GCMGrp)
                        else:
                            if not (prefixOrSuffix == 'Prefix' and gcm.startswith(R_Prfx)):
                                if not prefixOrSuffix == 'Suffix' or gcm.endswith(R_Prfx):
                                    parent(gcm, R_GCMGrp)
                                else:
                                    gcm.parentTo(C_GCMGrp)
                            meshVtx = MeshVertex(gcm)
                            for num in range(meshVtx.count()):
                                HyperSkin.move2ClosestPoint(gcm + '.vtx[' + str(num) + ']', skinMesh)

                            HyperSkin.mConstrain([gcm.split(gcmSuffix)[0], gcm], 'parent')
                            select(gcm, r=1)

                    HyperSkin.endProgressWin(len(allGCMList), 1)
                    select(allGCMList, r=1)
                    faceList = HyperSkin.getFaceList(skinMesh, 'L_')
                    gcmDict = {}
                    apiGCMList = [MFnMesh(obj._MDagPath()) for obj in allGCMList]
                    for gcm in allGCMList:
                        gcmDict[gcm] = []

                    HyperSkin.startProgressWin(len(faceList), 'Analyzing Faces..', None, False)
                    for face in faceList:
                        HyperSkin.progressWin(face, False, _as_HyperSkinMain__showProgressTime, rv=0)
                        as_nearestGeo = HyperSkin.getNearestGeo(face, apiGCMList)
                        gcmDict[as_nearestGeo].append(face)

                    HyperSkin.endProgressWin(len(faceList), 1)
                    HyperSkin.startProgressWin(len(list(gcmDict.keys())), 'Making FaceSets..', None, False)
                    faceSets = []
                    for gcm in list(gcmDict.keys()):
                        HyperSkin.progressWin(None, False, _as_HyperSkinMain__showProgressTime, rv=0)
                        try:
                            select((gcmDict[gcm]), r=1)
                            endFaceSet = sets((gcmDict[gcm]), n=(str(gcm) + '_FaceSet'))
                            faceSets.append(endFaceSet)
                        except:
                            pass

                    HyperSkin.endProgressWin(len(faceList), 1)
                    try:
                        delete('as_TempGCM_Grp')
                    except:
                        pass

                    delete(allGCMList)
                    asSkinMesh = hsNode(skinMesh)
                    asSkinMesh.template(False)
                    jntGCMs = []
                    HyperSkin.startProgressWin(len(faceSets), 'Extracting Faces..', None, False)
                    for faceSet in faceSets:
                        select(faceSet, r=1)
                        dupFaceList = ['as_SkinMesh_Dup.' + face.split('.')[1] for face in filterExpand(sm=34)]
                        dupSkinMesh = asSkinMesh.duplicate(n='as_SkinMesh_Dup')[0]
                        dupSkinMesh.show()
                        polyChipOff(dupFaceList, dup=True, ltz=0)
                        polySeparate(dupSkinMesh, ch=0, rs=1)
                        polyChipList = hsN.selected()
                        areaDict = {}
                        for polyChip in polyChipList:
                            areaDict[polyChip] = polyEvaluate(polyChip, a=1)

                        polyChips = HyperSkin.sortByDict(areaDict)
                        polyChips.pop().deleteNode()
                        reqdGCM = polyChips.pop()
                        relativeJnt = faceSet.split(gcmSuffix + '_FaceSet')[0]
                        reqdGCM = reqdGCM.rename(relativeJnt + gcmSuffix)
                        if polyChips:
                            delete(polyChips)
                        else:
                            reqdGCM._appendTo(jntGCMs)
                            if not prefixOrSuffix == 'Prefix' or reqdGCM.startswith(L_Prfx) or prefixOrSuffix == 'Suffix' and reqdGCM.endswith(L_Prfx):
                                reqdGCM.parentTo(L_GCMGrp)
                            else:
                                gcmName = reqdGCM.shortName()
                                dupGCM, gcmGrp = reqdGCM.duplicate(False, 1)
                                gcmGrp.setAttr('sx', -1)
                                gcmGrp.freeze()
                                dupGCM.parentTo()
                                polyNormal(dupGCM, ch=1, userNormalMode=0, normalMode=0)
                                gcmGrp.deleteNode()
                                reqdGCM = hsNode(polyUnite(dupGCM, reqdGCM, ch=0, mergeUVSets=1)[0])
                                reqdGCM = reqdGCM.rename(gcmName)
                                reqdGCM.parentTo(C_GCMGrp)
                        delete('as_SkinMesh_Dup')
                        HyperSkin.snapPiv_Obj(reqdGCM, reqdGCM.split(gcmSuffix)[0])
                        HyperSkin.mConstrain([relativeJnt, reqdGCM], 'parent')
                        select(reqdGCM, r=1)
                        HyperSkin.refreshView(1)
                        HyperSkin.progressWin(faceSet, False, _as_HyperSkinMain__showProgressTime, rv=0)

                    HyperSkin.endProgressWin(len(faceSets), 1)
                    delete(faceSets)
                    select(jntGCMs, r=1)
                    ToggleBorderEdges()
                    ToggleTextureBorderEdges()
                    HyperSkin.computeTime(1, 'Optimized : Extracted Cut Mesh ..!', _as_HyperSkinMain__displayTotalTime)
                    return
                allUpLineGCMs_Solved = None
                allEndVtxSets_Solved = None
                allUpLineJnts_Solved = None
                fingerEndVtxDict = None
                fingerEndJntDict = None
                if nonSknEndJnts:
                    allEndVtxSets_Solved, allUpLineGCMs_Solved, allUpLineJnts_Solved, fingerEndVtxDict = ([], [], [], {})
                    solvedList = HyperSkin.getSolvedJntsNGCMs(skinJntList, nonSknEndJnts, gcmSuffix)
                    if solvedList:
                        allEndVtxSets_Solved, allUpLineGCMs_Solved, allUpLineJnts_Solved, fingerEndVtxDict, fingerEndJntDict = solvedList
                if allUpLineGCMs_Solved:
                    for upLineGCM_Solved in allUpLineGCMs_Solved:
                        try:
                            SkinGCMsRemove(upLineGCM_Solved)
                        except:
                            pass

                asLat.show()
                reduceList = []
                ReduceListAppend = reduceList.append
                for gcm in skinGCMList:
                    if not asLat.contains(gcm):
                        asLat.intersects(gcm) or ReduceListAppend(gcm)

                delete(asLat)
                if reduceList:
                    for gcm in reduceList:
                        try:
                            SkinGCMsRemove(gcm)
                        except:
                            pass

                apiGCMList = [MFnMesh(obj._MDagPath()) for obj in skinGCMList]
                apiGCMList2 = [om2.MFnMesh(obj._MDagPath2()) for obj in skinGCMList]
                apiDagPaths2 = [obj._MDagPath2() for obj in skinGCMList]
                HyperSkin.computeTime(0, 'Optimized : Solving Fingers', _as_HyperSkinMain__displayTotalTime)
                if objExists('All_Fingers_VtxSet'):
                    cmds.select('All_Fingers_VtxSet', r=1)
                    allSolvedVtxSet = set(cmds.filterExpand(sm=31))
                    allVtxSet = set(vtxList)
                    nonSolvedVtxList = list(set(allVtxSet - allSolvedVtxSet))
                    [setAttr(jnt + '.liw', 1) for jnt in allUpLineJnts_Solved]
                    for vtx in nonSolvedVtxList:
                        [skinPercent(skinClust, vtx, tv=(jnt, 0.0)) for jnt in allUpLineJnts_Solved]

                    [setAttr(jnt + '.liw', 0) for jnt in allUpLineJnts_Solved]
                if _as_HyperSkinMain__showGCMs_AndStop:
                    return
                    asSkinMesh.template()
                    HyperSkin.refreshView(1)
                    nearestJntDict = {}
                    nearestGCMDict = {}
                    nearestDSCDict = {}
                    jntList = []
                    JntsAppend = jntList.append
                    gcmList = []
                    GcmsAppend = gcmList.append
                    HyperSkin.startProgressWin(len(vtxList), 'Level_01: Getting Nearest Discs', 'Level_01 : HSS', False)
                    if allEndVtxSets_Solved:
                        skinGCMList_nonSolved = list(set(skinGCMList) - set(allUpLineGCMs_Solved))
                        apiGCMList_nonSolved = [MFnMesh(obj._MDagPath()) for obj in skinGCMList_nonSolved]
                    else:
                        for vtx in vtxList:
                            HyperSkin.progressWin(('L01: Get Nearest Discs For {}'.format(vtx)), False, _as_HyperSkinMain__showProgressTime, rv=0)
                            if allEndVtxSets_Solved:
                                if sets(allEndVtxSets_Solved, isMember=vtx):
                                    for vtxSet in list(fingerEndVtxDict.keys()):
                                        if sets(vtxSet, isMember=vtx):
                                            vtxEndJnt = hsNode(fingerEndVtxDict[vtxSet])
                                            try:
                                                numParents = vtxEndJnt.child().getAttr('numParents')
                                            except:
                                                HyperSkin.deleteUnwanted()
                                                HyperSkin.error('Oops.. Found No "%s"' % (str(vtxEndJnt.child()) + '.numParents'))

                                            break

                                    upLineJnts_SolvedJnt = vtxEndJnt.parent(numParents, True, 'joint')
                                    for jnt in upLineJnts_SolvedJnt:
                                        if not objExists(jnt + gcmSuffix):
                                            HyperSkin.deleteUnwanted()
                                            HyperSkin.error('Oops.. "%s" -Object Not Exists ..!\nCheck for "Solve >> End Jnts" Option' % str(jnt + gcmSuffix))
                                            break

                                    upLineGCMs_Solved = [hsNode(jnt + gcmSuffix) for jnt in upLineJnts_SolvedJnt]
                                    upLineGCMs_Solved = [MFnMesh(obj._MDagPath()) for obj in upLineGCMs_Solved]
                                    nearestGeo = HyperSkin.getNearestGeo(vtx, upLineGCMs_Solved)
                                else:
                                    try:
                                        nearestGeo = HyperSkin.getNearestGeo(vtx, apiGCMList_nonSolved)
                                    except:
                                        HyperSkin.deleteUnwanted()
                                        select(vtx, r=1)
                                        HyperSkin.error('Oops.. Found No GCM For This Vtx "%s"\nTry without "Quick Hyper Skin" option !!' % str(vtx))

                            else:
                                try:
                                    nearestGeoList10, apiGCMList10 = HyperSkin.getNearestGeoList02(vtx, apiDagPaths2, 15)
                                    apiGCMList2 = [om2.MFnMesh(obj) for obj in nearestGeoList10]
                                    try:
                                        nearestGeo = HyperSkin.getNearestGeo02(vtx, apiGCMList2)
                                    except:
                                        nearestGeo = HyperSkin.getNearestGeo(vtx, apiGCMList)

                                except:
                                    HyperSkin.deleteUnwanted()
                                    select(vtx, r=1)
                                    HyperSkin.error('Oops.. Found No GCM For This Vtx "%s"\nTry without "Quick Hyper Skin" option !!' % str(vtx))

                                nearestGCMDict[vtx] = nearestGeo
                                nearestJntDict[vtx] = hsNode(nearestGeo.split(gcmSuffix)[0])
                                nearestDSCDict[vtx] = hsNode(nearestGeo.replace('GCM', 'DSC'))
                            if nearestGeo not in gcmList:
                                GcmsAppend(nearestGeo)
                                JntsAppend(nearestGeo.split(gcmSuffix)[0])

                        HyperSkin.endProgressWin(None, True)
                        for gcMesh in allGCMList:
                            try:
                                HyperSkin.hideNodes(gcMesh)
                            except:
                                gcMesh.setAttr('v', 0)

                        try:
                            delete(allEndVtxSets_Solved)
                        except:
                            pass

                        HyperSkin.computeTime(0, 'Optimized : Level01 Completed', _as_HyperSkinMain__displayTotalTime)
                        HyperSkin.refreshView(1)
                        try:
                            panelName = melGlobals['panelName']
                            modelEditor(panelName, edit=1, displayAppearance='smoothShaded', activeOnly=False)
                        except:
                            pass

                        HyperSkin.refreshView(2)
                        [cmds.setAttr(jnt + '.liw', 0) for jnt in jntList]
                        asSkinMesh.untemplate()
                        HyperSkin.refreshView(1)
                        [unhideNodes(gcMesh) for gcMesh in allGCMList]
                        HyperSkin.startProgressWin(len(vtxList), 'Level_02: Hyper Skinning', 'Level_02 : HSS', False)
                        apiGCMList_level02 = [MFnMesh(hsNode(obj)._MDagPath()) for obj in gcmList]
                        select(cl=1)
                        for vtx in vtxList:
                            vtxNum = HyperSkin.extractNum(vtx)[0]
                            HyperSkin.progressWin(('L02 - Calculate & HyperSkin - {}'.format(vtx)), False, _as_HyperSkinMain__showProgressTime, rv=0)
                            baseJnt = nearestJntDict[vtx]
                            baseParentJnt = baseJnt.pickWalkUp(1, 'joint', parentImplied=1)
                            if not baseParentJnt:
                                gcmList.remove(nearestGCMDict[vtx])
                                parentGCM = HyperSkin.getNearestGeo(baseJnt, apiGCMList_level02)
                                gcmList.append(nearestGCMDict[vtx])
                                baseParentJnt = parentGCM.split(gcmSuffix)[0]
                            else:
                                if quickHyperSkin:
                                    if baseParentJnt not in allSkinJntList:
                                        gcmList.remove(nearestGCMDict[vtx])
                                        parentGCM = HyperSkin.getNearestGeo(baseJnt, apiGCMList_level02)
                                        gcmList.append(nearestGCMDict[vtx])
                                        baseParentJnt = parentGCM.split(gcmSuffix)[0]
                                    else:
                                        if baseParentJnt not in jntList:
                                            gcmList.remove(nearestGCMDict[vtx])
                                            parentGCM = HyperSkin.getNearestGeo(baseJnt, apiGCMList_level02)
                                            gcmList.append(nearestGCMDict[vtx])
                                            baseParentJnt = parentGCM.split(gcmSuffix)[0]
                                        else:
                                            chdJnt = baseJnt.pickWalkDown(1, 'joint')
                                            if not chdJnt:
                                                chdJnts = baseJnt.getChildren('joint')
                                                if chdJnts:
                                                    chdJnts[0].setSibIndex(0)
                                                    chdJnt = chdJnts[0]
                                                else:
                                                    select(baseJnt, r=1)
                                                    errStr = 'This Joint "%s" doesn\'t have any child / directional joint'
                                                    errStr += '\nSolution: Keep the child joint directly under this joint "%s"'
                                                    HyperSkin.error(errStr % (str(baseJnt), str(baseJnt)))
                                    if chdJnt not in jntList and not baseJnt.isLastJnt(1):
                                        if not quickHyperSkin:
                                            gcmList.remove(nearestGCMDict[vtx])
                                            chdGCM = HyperSkin.getNearestGeo(chdJnt, apiGCMList_level02)
                                            gcmList.append(nearestGCMDict[vtx])
                                            chdJnt = chdGCM.split(gcmSuffix)[0]
                                        if not attributeQuery('dscChd', n=(baseJnt.name()), ex=1):
                                            jntLength = HyperSkin.mDistance(baseJnt + dscSuffix, chdJnt + dscSuffix)[0]
                                        else:
                                            dscChdJnt = HyperSkin.getChild_DSC(baseJnt)
                                            jntLength = HyperSkin.mDistance(baseJnt + dscSuffix, dscChdJnt + dscSuffix)[0]
                                        nearest_DSC = nearestDSCDict[vtx]
                                        if not nearest_DSC.isMesh():
                                            HyperSkin.deleteUnwanted()
                                            HyperSkin.error('"%s" -Object not Exists Or It is modified' % nearest_DSC.shortName())
                                else:
                                    select(vtx, nearest_DSC, r=1)
                                    vtxDist = HyperSkin.getClosestDist(vtx, nearest_DSC)
                                    asDSC = hsNode(baseJnt + dscSuffix)
                                    try:
                                        baseBlend = asDSC.getAttr('baseBlend')
                                        if baseBlend <= 0.1:
                                            baseBlend = 0.1
                                        if baseBlend >= 0.9:
                                            baseBlend = 0.9
                                        baseBlend = baseBlend / 2.0
                                        tailBlend = asDSC.getAttr('tailBlend')
                                        if tailBlend <= 0.1:
                                            tailBlend = 0.1
                                        if tailBlend >= 0.9:
                                            tailBlend = 0.9
                                        tailBlend = tailBlend / 2.0
                                        moreVolume = asDSC.getAttr('moreVolume')
                                    except:
                                        HyperSkin.deleteUnwanted()
                                        asDSC.select(r=1)
                                        HyperSkin.error("%s's attribute 'baseBlend' | 'tailBlend' | 'moreVolume' is not available" % asDSC.shortName())

                                maxRangeVal = 1 - tailBlend
                                minRangeVal = baseBlend
                                isLastBaseSknJnt = HyperSkin.isLastJnt(baseJnt, 1, 0)
                                if not isLastBaseSknJnt:
                                    maxJntLength = jntLength * maxRangeVal
                                    minJntLength = jntLength * minRangeVal
                                    if vtxDist >= jntLength * minRangeVal and vtxDist <= jntLength * maxRangeVal:
                                        setAttr(baseJnt + '.liw', 0)
                                        skinPercent(skinClust, vtx, tv=(baseJnt, 1))
                                        setAttr(baseJnt + '.liw', 1)
                                    else:
                                        if vtxDist < minJntLength:
                                            skinPVal = HyperSkin.mapRange(vtxDist, 0, minJntLength, 0.5, 0.95)
                                            setAttr(baseJnt + '.liw', 0)
                                            skinPercent(skinClust, vtx, tv=(baseJnt, skinPVal))
                                            setAttr(baseJnt + '.liw', 1)
                                            setAttr(baseParentJnt + '.liw', 0)
                                            skinPercent(skinClust, vtx, tv=(baseParentJnt, 1 - skinPVal))
                                            setAttr(skinClust + '.blendWeights[%d]' % vtxNum, 1)
                                            setAttr(baseParentJnt + '.liw', 1)
                                        else:
                                            if vtxDist > maxJntLength:
                                                if vtxDist > jntLength / 2.0:
                                                    skinPVal = HyperSkin.mapRange(vtxDist, maxJntLength, jntLength, 0.99, 0.5)
                                                    setAttr(baseJnt + '.liw', 0)
                                                    skinPercent(skinClust, vtx, tv=(baseJnt, skinPVal))
                                                    setAttr(baseJnt + '.liw', 1)
                                                    try:
                                                        setAttr(chdJnt + '.liw', 0)
                                                        skinPercent(skinClust, vtx, tv=(chdJnt, 1 - skinPVal))
                                                        setAttr(chdJnt + '.liw', 1)
                                                    except:
                                                        pass

                                                else:
                                                    setAttr(baseJnt + '.liw', 0)
                                                    skinPercent(skinClust, vtx, tv=(baseJnt, 1))
                                                    setAttr(baseJnt + '.liw', 1)
                                            minVal = 0.25
                                            blendVtx = skinClust + '.blendWeights[%d]' % vtxNum
                                            if moreVolume and _as_HyperSkinMain__autoDualSkinning:
                                                setAttr(blendVtx, 0)
                                                if moreVolume == 1:
                                                    if vtxDist > 0 and vtxDist < jntLength / 2.0:
                                                        blendVal = 1 - HyperSkin.mapRange(vtxDist, 0, jntLength, minVal, 1.0) + minVal
                                                        setAttr(blendVtx, blendVal)
                                            elif moreVolume == 2:
                                                if vtxDist > jntLength / 2.0:
                                                    blendVal = HyperSkin.mapRange(vtxDist, 0, jntLength, minVal, 1.0)
                                                    setAttr(blendVtx, blendVal)
                                            elif moreVolume == 3:
                                                if vtxDist > 0 and vtxDist < jntLength / 2.0:
                                                    blendVal = 1 - HyperSkin.mapRange(vtxDist, 0, jntLength / 2.0, minVal, 1.0) + minVal
                                                    setAttr(blendVtx, blendVal)
                                            elif vtxDist > jntLength / 2.0:
                                                blendVal = HyperSkin.mapRange(vtxDist, jntLength / 2.0, jntLength, minVal, 1.0)
                                                setAttr(blendVtx, blendVal)
                                else:
                                    setAttr(blendVtx, 0)
                            if _as_HyperSkinMain__showVtxDist and HyperSkin.extractNum(vtx)[0] == _as_HyperSkinMain__showVtxDist:
                                warnignMsg = 'Normal Weighting\n================\n'
                                warnignMsg += 'Vertex Distance To "{}" Is : '.format(str(nearest_DSC)) + str(vtxDist)
                                warnignMsg += '\nMinimim Range Is : ' + str(jntLength * minRangeVal)
                                warnignMsg += '\nMaximim Range Is : ' + str(jntLength * maxRangeVal)
                                warnignMsg += '\nBaseJnt Weight : ' + str(skinPVal)
                                warnignMsg += '\nJoint Length Is : {0}, {1}, {2}\n================\n'.format(str(jntLength), baseJnt + dscSuffix, chdJnt + dscSuffix)
                                if moreVolume:
                                    warnignMsg2 = 'Blend Weighting\n\n----------------\n'
                                    warnignMsg2 += 'Vertex Distance To "{}" Is : '.format(str(nearest_DSC)) + str(vtxDist)
                                select(vtx, baseJnt, chdJnt, r=1)
                                cmds.sets(n='Distance Nodes')
                                om.MGlobal.displayWarning(warnignMsg)
                                return
                            else:
                                if vtxDist >= jntLength * minRangeVal:
                                    setAttr(baseJnt + '.liw', 0)
                                    skinPercent(skinClust, vtx, tv=(baseJnt, 1))
                                    setAttr(baseJnt + '.liw', 1)
                                else:
                                    if vtxDist < jntLength * minRangeVal:
                                        skinPVal = HyperSkin.mapRange(vtxDist, 0, jntLength * minRangeVal, 0.5, 0.95)
                                        setAttr(baseJnt + '.liw', 0)
                                        skinPercent(skinClust, vtx, tv=(baseJnt, skinPVal))
                                        setAttr(baseJnt + '.liw', 1)
                                        setAttr(baseParentJnt + '.liw', 0)
                                        skinPercent(skinClust, vtx, tv=(baseParentJnt, 1 - skinPVal))
                                        setAttr(baseParentJnt + '.liw', 1)
                                    else:
                                        blendVtx = skinClust + '.blendWeights[%d]' % vtxNum
                                        if moreVolume and _as_HyperSkinMain__autoDualSkinning:
                                            minVal = 0.25
                                            if vtxDist > 0 and vtxDist < jntLength / 2.0:
                                                if moreVolume == 1 or moreVolume == 3:
                                                    blendVal = 1 - HyperSkin.mapRange(vtxDist, 0, jntLength / 2.0, minVal, 1.0) + minVal
                                                    setAttr(blendVtx, blendVal)
                                                else:
                                                    setAttr(blendVtx, 0)
                                            else:
                                                setAttr(blendVtx, 0)
                                        else:
                                            setAttr(blendVtx, 0)
                                    if _as_HyperSkinMain__showVtxDist:
                                        if HyperSkin.extractNum(vtx)[0] == _as_HyperSkinMain__showVtxDist:
                                            warnignMsg = 'Vertex Distance Is : ' + str(vtxDist) + '\nMinimim Range Is : ' + str(jntLength * minRangeVal)
                                            select(vtx, baseJnt, baseParentJnt, r=1)
                                            cmds.sets(n='Distance Nodes')
                                            om.MGlobal.displayWarning(warnignMsg)
                                            return
                                    setAttr(baseJnt + '.liw', 0)
                                    setAttr(baseParentJnt + '.liw', 0)
                            if not isLastBaseSknJnt:
                                try:
                                    setAttr(chdJnt + '.liw', 0)
                                except:
                                    pass

                        HyperSkin.endProgressWin(None, True)
                        HyperSkin.hideNodes(allGCMList)
                        [cmds.setAttr(jnt + '.liw', 0) for jnt in infJntList]
                        HyperSkin.computeTime(0, 'Optimized : Level02 Completed', _as_HyperSkinMain__displayTotalTime)
                        HyperSkin.refreshView(1)
                        if smoothTest:
                            smoothCount = roundNum = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
                            select(skinMesh, r=1)
                            wList = []
                            for geo in gcmList:
                                wList.append(geo.split(gcmSuffix)[0])

                            ArtPaintSkinWeightsToolOptions()
                            artAttrSkinPaintCtx((currentCtx()), radius=0.1, e=1)
                            artAttrSkinPaintCtx((currentCtx()), e=1, opacity=0.5)
                            mel.artAttrPaintOperation('artAttrSkinPaintCtx', 'Smooth')
                            try:
                                mel.artUpdateStampProfile('solid', 'artAttrSkinPaintCtx')
                                HyperSkin.refreshView(1)
                            except:
                                try:
                                    mel.artUpdateStampProfile('solid', currentCtx())
                                    HyperSkin.refreshView(1)
                                except:
                                    pass

                            a = 0
                            while a < roundNum:
                                a += 1
                                HyperSkin.startProgressWin(len(wList), 'Please Wait ..!', None, False)
                                for inf in wList:
                                    HyperSkin.progressWin('Hyper Smooth ..!', False, _as_HyperSkinMain__showProgressTime, rv=0)
                                    currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                                    mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

                                HyperSkin.endProgressWin(len(wList), 1)
                                a += 1
                                if a > roundNum:
                                    break
                                else:
                                    HyperSkin.startProgressWin(len(wList), 'Please Wait ..!', None, False)
                                    wList.reverse()
                                    for inf in wList[1:]:
                                        HyperSkin.progressWin('Hyper Smooth ..!', False, _as_HyperSkinMain__showProgressTime, rv=0)
                                        currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                                        mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                                        artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                                        artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

                                    HyperSkin.endProgressWin(len(wList), 1)

                            HyperSkin.deleteUnwanted()
                        else:
                            HyperSkin.deleteUnwanted()
                    select(skinMesh, r=1)
                    ArtPaintSkinWeightsToolOptions()
                    artAttrSkinPaintCtx((currentCtx()), e=1, opacity=1.0)
                    HyperSkin.deleteUnwanted()
                    mel.eval('changeSelectMode -object')
                    if vtxList:
                        select(vtxList, r=1)
                else:
                    skinMesh.select(r=1)
            mel.doPruneSkinClusterWeightsArgList(1, ['0.045'])
            cmds.undoInfo(closeChunk=True)
            gc.enable()
            HyperSkin.computeTime(1, 'Optimized : HyperSmooth Completed', _as_HyperSkinMain__displayTotalTime)

    def as_Generate_HyperSmooth(self, smoothAll=False, vtxList=None, jntList=None, pruneWgts=True, skinSide=None, **shortArgs):
        HyperSkin._check4Author()
        _as_HyperSkinMain__showProgressTime = 1
        _as_HyperSkinMain__displayTotalTime = 0
        if shortArgs:
            smoothAll = shortArgs['sa'] if 'sa' in shortArgs else smoothAll
            vtxList = shortArgs['vl'] if 'vl' in shortArgs else vtxList
            jntList = shortArgs['jl'] if 'jl' in shortArgs else jntList
            pruneWgts = shortArgs['pw'] if 'pw' in shortArgs else pruneWgts
        skinMesh = textField('as_SkinMesh_TF', q=1, tx=1)
        roundNum = int(optionMenu('as_SmoothCount_OM', q=1, v=1))
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
        L_Prfx = textField('as_LSidePrefix_TF', q=1, tx=1)
        R_Prfx = textField('as_RSidePrefix_TF', q=1, tx=1)
        noDiscBind = cmds.checkBox('as_NoDiscHyperSkin_CB', q=1, v=1)
        if not skinSide:
            skinSide = optionMenu('as_HyperSkinSide_OM', q=1, v=1)
        if not objExists(skinMesh):
            confirmDialog(title='Warning..', bgc=(1, 0.5, 0), message='Cancelled Action.. , Enter Skinned Mesh ..!', button=['OK'], defaultButton='OK')
            raise RuntimeError('Enter Skinned Mesh ..!')
        else:
            skinMesh = PyNode(skinMesh)
        if jntList:
            jntList = [jntList] if type(jntList) != list else jntList
            wList = jntList
        else:
            skinClust = listHistory(skinMesh, type='skinCluster')[0]
            jntList = skinCluster(skinClust, wi=1, q=1)
            if smoothAll:
                wList = jntList
            else:
                refCount = 1
                if not vtxList:
                    vtxList = filterExpand(sm=31)
                selectedVtx = False
                if not vtxList:
                    if skinSide == 'LT':
                        vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
                    elif skinSide == 'RT':
                        vtxList = HyperSkin.getMeshVtx(skinMesh, 'R_')
                    else:
                        vtxList = HyperSkin.getMeshVtx(skinMesh)
                else:
                    jntList = HyperSkin.getSkinJntsList(vtxList)
                    selectedVtx = True
                gcmSuffix = '_asSC' + HyperSkin.extractNum(skinClust)[1] + 'GCM'
            if smoothAll:
                pass
            elif selectedVtx:
                jntGeoLst = [jnt + gcmSuffix for jnt in jntList]
            else:
                if selectedVtx:
                    jntGeoLst = [jnt + gcmSuffix for jnt in jntList]
                elif skinSide == 'LT':
                    jntGeoLst = [jnt + gcmSuffix for jnt in jntList if R_Prfx not in jnt.name()]
                elif skinSide == 'RT':
                    jntGeoLst = [jnt + gcmSuffix for jnt in jntList if L_Prfx not in jnt.name()]
                if skinSide == 'LT':
                    RJntList = [jnt for jnt in jntList if jnt.shortName().startswith(R_Prfx)]
                    if RJntList:
                        HyperSkin.startProgressWin((len(RJntList)), rv=1)
                        for jnt in RJntList:
                            HyperSkin.progressWin(HyperSkin.name(jnt), False, _as_HyperSkinMain__showProgressTime)
                            setAttr(jnt + '.liw', 1)

                        HyperSkin.endProgressWin(len(RJntList), 1)
                elif skinSide == 'RT':
                    LJntList = [jnt for jnt in jntList if jnt.shortName().startswith(L_Prfx)]
                    if LJntList:
                        HyperSkin.startProgressWin((len(LJntList)), rv=1)
                        for jnt in LJntList:
                            HyperSkin.progressWin(HyperSkin.name(jnt), False, _as_HyperSkinMain__showProgressTime)
                            setAttr(jnt + '.liw', 1)

                        HyperSkin.endProgressWin(len(LJntList), 1)
                if roundNum == 0:
                    roundNum = 2
                if smoothAll:
                    if noDiscBind:
                        HyperSkin.startProgressWin((len(jntList)), 'Please Wait ..!', None, False, rv=1)
                        for jnt in jntList:
                            jnt = hsNode(jnt)
                            smoothJnts = [jnt]
                            pickCount = 1
                            _jntParent = jnt.pickWalkUp(pickCount, 'joint')
                            if _jntParent:
                                if pickCount > 1:
                                    smoothJnts.extend(_jntParent)
                                else:
                                    smoothJnts.append(_jntParent)
                            _jntChild = jnt.pickWalkDown(pickCount, 'joint')
                            if _jntChild:
                                if pickCount > 1:
                                    smoothJnts.extend(_jntChild)
                                else:
                                    smoothJnts.append(_jntChild)
                            HyperSkin.as_LockJoints(smoothJnts, skinMesh)
                            HyperSkin.as_Generate_HyperSmooth(None, None, jnt, pw=0)
                            HyperSkin.progressWin('Hyper Smooth (No Disk)', False, _as_HyperSkinMain__showProgressTime)

                        HyperSkin.endProgressWin(len(wList), 1)
                    elif skinSide == 'RT':
                        if prefixOrSuffix == 'Prefix':
                            wList_LC = [jnt for jnt in jntList if not jnt.startswith(R_Prfx)]
                            wList_R = [jnt for jnt in jntList if jnt.startswith(R_Prfx)]
                        elif prefixOrSuffix == 'Suffix':
                            wList_LC = [jnt for jnt in jntList if not jnt.endswith(R_Prfx)]
                            wList_R = [jnt for jnt in jntList if jnt.endswith(R_Prfx)]
                        if wList_R:
                            [cmds.setAttr(jnt + '.liw', 1) for jnt in wList_LC]
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_R]
                            HyperSkin.as_Generate_HyperSmooth(None, None, wList_R, pw=0)
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_LC]
                        else:
                            HyperSkin.error('Found No Right Side Joints')
                        if wList_LC:
                            [cmds.setAttr(jnt + '.liw', 1) for jnt in wList_R]
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_LC]
                            HyperSkin.as_Generate_HyperSmooth(None, None, wList_LC, pw=0)
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_R]
                        else:
                            pass
                    else:
                        if skinSide == 'LT':
                            if prefixOrSuffix == 'Prefix':
                                wList_RC = [jnt for jnt in jntList if not jnt.startswith(L_Prfx)]
                                wList_L = [jnt for jnt in jntList if jnt.startswith(L_Prfx)]
                            elif prefixOrSuffix == 'Suffix':
                                wList_RC = [jnt for jnt in jntList if not jnt.endswith(L_Prfx)]
                                wList_L = [jnt for jnt in jntList if jnt.endswith(L_Prfx)]
                            if wList_L:
                                [cmds.setAttr(jnt + '.liw', 1) for jnt in wList_RC]
                                [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_L]
                                HyperSkin.as_Generate_HyperSmooth(None, None, wList_L, pw=0)
                                [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_RC]
                        else:
                            pass
                        if wList_RC:
                            [cmds.setAttr(jnt + '.liw', 1) for jnt in wList_L]
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_RC]
                            HyperSkin.as_Generate_HyperSmooth(None, None, wList_RC, pw=0)
                            [cmds.setAttr(jnt + '.liw', 0) for jnt in wList_L]
                        else:
                            pass
                    return
                wList = [geo.split(gcmSuffix)[0] for geo in jntGeoLst]
        select(skinMesh, r=1)
        ArtPaintSkinWeightsToolOptions()
        artAttrSkinPaintCtx((currentCtx()), radius=0.1, e=1)
        artAttrSkinPaintCtx((currentCtx()), e=1, op=0.5)
        mel.artAttrPaintOperation('artAttrSkinPaintCtx', 'Smooth')
        try:
            mel.artUpdateStampProfile('solid', 'artAttrSkinPaintCtx')
            HyperSkin.refreshView(1)
        except:
            try:
                mel.artUpdateStampProfile('solid', currentCtx())
                HyperSkin.refreshView(1)
            except:
                pass

        a = 0
        while a < roundNum:
            a += 1
            HyperSkin.startProgressWin((len(wList)), 'Please Wait ..!', None, False, up=(not noDiscBind), rv=1)
            for inf in wList:
                HyperSkin.progressWin('Hyper Smooth ..!', False, _as_HyperSkinMain__showProgressTime, up=(not noDiscBind))
                currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

            HyperSkin.endProgressWin((len(wList)), 1, up=(not noDiscBind))
            a += 1
            if a > roundNum:
                break
            else:
                HyperSkin.startProgressWin((len(wList)), 'Please Wait ..!', None, False, up=(not noDiscBind), rv=1)
                wList.reverse()
                for inf in wList[1:]:
                    HyperSkin.progressWin('Hyper Smooth ..!', False, _as_HyperSkinMain__showProgressTime, up=(not noDiscBind))
                    currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                    mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

                HyperSkin.endProgressWin((len(wList)), 1, up=(not noDiscBind))

        artAttrSkinPaintCtx((currentCtx()), e=1, opacity=1.0)
        mel.eval('changeSelectMode -object')
        if vtxList:
            select(vtxList, r=1)
        else:
            skinMesh.select(r=1)
        if not smoothAll:
            if pruneWgts:
                mel.doPruneSkinClusterWeightsArgList(1, ['0.045'])
        skinMesh.select(r=1)

    def transferSkinning(self, transferType=2, **shArgs):
        _as_HyperSkinMain__freeVersion = 0
        if shArgs:
            transferType = shArgs['tt'] if 'tt' in shArgs else transferType
        if _as_HyperSkinMain__freeVersion:
            HyperSkin.restrictedZone_FreeTool()
        if cmds.radioButton('as_SkinTransferM2M_RB', q=1, sl=1):
            HyperSkin.transferSkin_Mesh2Mesh()
        elif cmds.radioButton('as_SkinTransferM2M_Multi_RB', q=1, sl=1):
            HyperSkin.transferSkin_OneToMany_Mesh(tt=transferType)
        elif cmds.radioButton('as_SkinTransferM2M_I2O_RB', q=1, sl=1):
            HyperSkin.transferSkin_Overlap(None, None, transferType='I2O')
        elif cmds.radioButton('as_SkinTransferM2M_O2I_RB', q=1, sl=1):
            HyperSkin.transferSkin_Overlap(None, None, transferType='O2I')
        elif cmds.radioButton('as_SkinTransferJ2J_RB', q=1, sl=1) or cmds.radioButton('as_SkinTransferJ2J_O2O_RB', q=1, sl=1):
            HyperSkin.transferSkin_Jnt2Jnt()
        elif cmds.radioButton('as_Many2One_RB', q=1, sl=1):
            HyperSkin.transferSkin_ManyToOne_Mesh(tt=transferType)
        elif cmds.radioButton('as_Many2Many_RB', q=1, sl=1):
            HyperSkin.transferSkin_ManyToMany_Mesh(tt=transferType)
        elif cmds.radioButton('as_SkinTransferM2V_RB', q=1, sl=1):
            HyperSkin.transferSkin_MeshToVtxList()
        elif cmds.radioButton('as_TransferRig2Skeleton_RB', q=1, sl=1):
            HyperSkin.transferSkin_Jnts2Jnts(tt=transferType)
        elif cmds.radioButton('as_TransferRig2Skeleton_RB', q=1, sl=1):
            action = HyperSkin.confirmAction('Select Transfer Type !!', 0, 'Selected', 'All')
            if action:
                print('Selected')
                HyperSkin.transferSkin_NearestJnts2Jnts()
            else:
                print('All')
                HyperSkin.transferSkin_NearestJnts2Jnts(ta=1)
        elif cmds.radioButton('as_SkinTransferV2V_RB', q=1, sl=1):
            HyperSkin.transferSkin_Vtx2Vtx()
        elif cmds.radioButton('as_SkinTransferV2V_One2Many_RB', q=1, sl=1):
            HyperSkin.transferSkin_Vtx2ManyVtx()
        elif cmds.radioButton('as_SkinTransferV2V_M2M_RB', q=1, sl=1):
            HyperSkin.transferSkin_ManyVtx2ManyVtx()

    def transferSkin_Mesh2Mesh(self, fromMesh=None, toMesh=None, transferType=2, showProgress=False, **shArgs):
        if shArgs:
            fromMesh = shArgs['fm'] if 'fm' in shArgs else fromMesh
            toMesh = shArgs['tm'] if 'tm' in shArgs else toMesh
            transferType = shArgs['tt'] if 'tt' in shArgs else transferType
        else:
            _as_HyperSkinMain__showProgressTime = 0
            _as_HyperSkinMain__displayTotalTime = 0
            meshType = 'Polygon'
            influObjCheck = checkBox('as_InfluObj_CB', q=1, v=1)
            if not fromMesh:
                if not toMesh:
                    meshList = selected()
                    fromMesh = meshList[0]
                    toMesh = meshList[1]
            fromMesh = PyNode(fromMesh)
            toMesh = PyNode(toMesh)
            meshList = [fromMesh, toMesh]
        fromShape = fromMesh.getShape()
        conList = []
        skin = ''
        if meshType == 'Nurbs':
            skin = connectionInfo((fromShape + '.create'), sfd=1).split('.')[0]
        else:
            if meshType == 'Polygon':
                histNodes = listHistory(fromMesh, pdo=1, il=1)
                try:
                    skin = ls(histNodes, type='skinCluster')[0]
                except:
                    skin = ''

                if not skin:
                    raise NameError('Skin Cluster Is Not Found on ' + fromMesh.name())
                jntList = skinCluster(skin, q=1, wi=1)
                scriptEditorInfo(ch=1)
                print('-----------------------------')
                print('Details Of Skinning Transfer !')
                print('-----------------------------')
                print('\nTotal Weight Influences : ' + str(len(jntList)))
                print('-----------------------------')
                pprint.pprint(jntList)
                print('\n')
                influList = []
                for jnt in jntList:
                    if PyNode(jnt).getShape():
                        influList.append(jnt)

                for influ in influList:
                    jntList.remove(influ)

                print('No of Jnts for Skinning : ' + str(len(jntList)))
                print('-----------------------------')
                pprint.pprint(jntList)
                print('\n')
                select(jntList, r=1)
                select((meshList[1]), add=1)
                mel.SmoothBindSkin()
                if influObjCheck == 1:
                    print('No of Influence Objects : ' + str(len(influList)))
                    print('-----------------------------')
                    pprint.pprint(influList)
                    print('\n')
                    if influList:
                        if showProgress:
                            HyperSkin.startProgressWin(len(influList), 'Please Wait ..!', None, False)
                        for influObj in influList:
                            select((meshList[1]), r=1)
                            select(influObj, add=1)
                            HyperSkin.refreshView(1)
                            if showProgress:
                                HyperSkin.progressWin(influObj, False, _as_HyperSkinMain__showProgressTime)
                            mel.skinClusterInfluence(1, '-dr 8.5 -ps 0 -ns 10')

                        if showProgress:
                            HyperSkin.endProgressWin(len(influList), 1)
            else:
                om.MGlobal.displayInfo('# There are no influence objects on base mesh.. ')
            select((meshList[0]), r=1)
            select((meshList[1]), add=1)
        if transferType == 1:
            try:
                copySkinWeights(surfaceAssociation='closestPoint', influenceAssociation='closestJoint', noMirror=1)
            except:
                HyperSkin.error('Target Mesh Is Not Skinned.\nCheck whether joints are bound at different pose !!')

        else:
            if transferType == 2:
                try:
                    copySkinWeights(surfaceAssociation='closestPoint', influenceAssociation=['closestJoint', 'oneToOne', 'closestJoint'], noMirror=1)
                except:
                    HyperSkin.error('Target Mesh Is Not Skinned.\nCheck whether joints are bound at different pose !!')

            om.MGlobal.displayInfo('# Transfered Skinning Sucessfully.!  Check Script Editor For Details At Top.!')

    def transferSkin_OneToMany_Mesh(self, transferType=2, **shArgs):
        if shArgs:
            transferType = shArgs['tt'] if 'tt' in shArgs else transferType
        selList = hsN.selected()
        if not selList:
            HyperSkin.error('Nothing Selected ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
        if selList:
            if len(selList) < 2:
                HyperSkin.error('Select at least 2 meshes  ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
            skinMesh = selList[-1]
            if not HyperSkin.isSkinned(skinMesh):
                HyperSkin.error('Source Mesh Is Not Skinned ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
            HyperSkin.startProgressWin(selList[:-1], 'Transfer Skinning')
            for obj in selList[:-1]:
                select(skinMesh, r=1)
                if not HyperSkin.isMesh(obj):
                    continue
                else:
                    select(obj, add=1)
                    HyperSkin.transferSkin_Mesh2Mesh(tt=transferType)
                    HyperSkin.progressWin(obj)

        HyperSkin.endProgressWin(selList[:-1], 1)

    def transferSkin_ManyToOne_Mesh(self):
        selList = hsN.selected()
        if not selList:
            HyperSkin.error('Nothing Selected ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
        if selList:
            if len(selList) < 2:
                HyperSkin.error('Select at least 2 meshes  ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
            skinMesh = selList[-1]
            if not HyperSkin.isSkinned(skinMesh):
                HyperSkin.error('Source Mesh Is Not Skinned ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
            trgtList = selList[:-1]
            vtxList = HyperSkin.getMeshVtx(skinMesh)
            HyperSkin.startProgressWin(vtxList, 'Transfer Skinning')
            for vtx in vtxList:
                vtx = hsNode(vtx)
                nVtxList = []
                meshDict = {}
                clustDict = {}
                for trgt in trgtList:
                    nVtx = HyperSkin.nearestVtx_OnMesh(vtx, trgt)[0]
                    (skinMesh_T, skinClust) = HyperSkin.confirmSkinMesh(trgt)
                    nVtxList.append(nVtx)
                    meshDict[nVtx] = trgt
                    clustDict[nVtx] = skinClust

                nVtx = vtx.nearestObj(nVtxList)
                valDict = HyperSkin.getSkinWeights(meshDict[nVtx], nVtx, clustDict[nVtx])
                HyperSkin.setSkinWeights(vtx, valDict)
                HyperSkin.progressWin(vtx)

        HyperSkin.endProgressWin(vtxList, 1)

    def transferSkin_MeshToVtxList(self):
        meshStr = textField('as_TrgtMeshList_TF', q=1, text=1)
        try:
            meshList = list(map(hsNode, meshStr.split(', ')))
        except:
            HyperSkin.error('Multiple Meshes Are Not Given')

        vtxList = cmds.filterExpand(sm=31)
        if vtxList:
            srcMesh = hsNode(vtxList[0]).asObj()
        else:
            srcMesh = hsN.selected()[0]
            vtxList = srcMesh.getVtxList()[0]
        if not HyperSkin.isSkinned(srcMesh):
            HyperSkin.error('Source Mesh Is Not Skinned ..\nEnter One | More Target Meshes First and Select Skinned Vertices !! ')
        HyperSkin.startProgressWin(vtxList, 'Transfer Skinning')
        for vtx in vtxList:
            vtx = hsNode(vtx)
            nVtxList = []
            meshDict = {}
            clustDict = {}
            for trgt in meshList:
                nVtx = HyperSkin.nearestVtx_OnMesh(vtx, trgt)[0]
                (skinMesh_T, skinClust) = HyperSkin.confirmSkinMesh(trgt)
                nVtxList.append(nVtx)
                meshDict[nVtx] = trgt
                clustDict[nVtx] = skinClust

            nVtx = vtx.nearestObj(nVtxList)
            valDict = HyperSkin.getSkinWeights(meshDict[nVtx], nVtx, clustDict[nVtx])
            HyperSkin.setSkinWeights(vtx, valDict, 1)
            HyperSkin.progressWin(vtx)

        HyperSkin.endProgressWin(vtxList, 1)

    def transferSkin_ManyToMany_Mesh(self, transferType=2, **shArgs):
        if shArgs:
            transferType = shArgs['tt'] if 'tt' in shArgs else transferType
        selList = hsN.selected()
        if not selList:
            HyperSkin.error('Nothing Selected ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
        srcGrp = selList[0]
        destGrp = selList[1]
        trgtPrefix = textField('as_TrgtJntPrefix_TF', q=1, tx=1)
        srcList = srcGrp.selectHI('mesh')
        destList = destGrp.selectHI('mesh')
        destDict = {}
        for destMesh in destList:
            vtxCount = destMesh.getVtxList(0)[1]
            destDict[destMesh] = vtxCount

        skipList = []
        dest_List = []
        HyperSkin.startProgressWin(srcList, 'Transfer Skinning')
        nonSkinSrcMeshList = []
        for skinMesh in srcList:
            if not HyperSkin.isSkinned(skinMesh):
                nonSkinSrcMeshList.append(skinMesh)
                HyperSkin.progressWin(skinMesh)
                continue
            else:
                trgtList = selList[:-1]
                vtxList = HyperSkin.getMeshVtx(skinMesh)
                trgtMesh = trgtPrefix + skinMesh
                if not cmds.objExists(trgtMesh):
                    if '_' in skinMesh:
                        trgtMesh = skinMesh.replace(skinMesh.split('_', 1)[0], trgtPrefix)
            if not not cmds.objExists(trgtMesh):
                if trgtPrefix in skinMesh:
                    trgtMesh = skinMesh.strip(trgtPrefix)
                if not cmds.objExists(trgtMesh):
                    vtxCount = skinMesh.getVtxList(0)[1]
                    for destMesh in destList:
                        if vtxCount == destDict[destMesh]:
                            trgtMesh = destMesh
                            break

                if cmds.objExists(trgtMesh):
                    dest_List.append(trgtMesh)
                    HyperSkin.transferSkin_Mesh2Mesh(skinMesh, trgtMesh, tt=transferType)
                else:
                    skipList.append(skinMesh)
                HyperSkin.progressWin(skinMesh)

        HyperSkin.endProgressWin(srcList, 1)
        if nonSkinSrcMeshList:
            cmds.select(nonSkinSrcMeshList, r=1)
            HyperSkin.message('Source Mesh Is Not Skinned ..\nSelect One | More Target Meshes First and Select Skinned Source Mesh At The End !! ')
        elif skipList:
            cmds.select(skipList, r=1)
            HyperSkin.message('For Selected Meshes\nSkin Transfer Is Not Done !!')
        else:
            cmds.select(dest_List, r=1)
            HyperSkin.message('Skin Transferred Successfully !!')

    def test(self):
        vtx = hsN.selected()[0]
        gcms = ls('*GCM')
        nearestGeo = HyperSkin.getNearestGeo(vtx, gcms)
        select(nearestGeo, r=1)

    def transferUVs(self, srcMesh=None, trgtMesh=None, spaceVal=1, delHistory=True, getMatchPercent=0, bestMatch=0, deleteMap=False):
        global testVtx
        if not (srcMesh and trgtMesh):
            startSelection = hsN.selected()
            (srcMesh, trgtMesh) = startSelection
        elif not srcMesh:
            trgtMesh = hsNode(trgtMesh)
            trgtShapes = trgtMesh.getShapes()
            for shp in trgtShapes:
                uvInput = listHistory(shp, type='transferAttributes')
                if uvInput:
                    uvInput = uvInput[0]
                    break

            inputShp = hsNode(connectionInfo((uvInput + '.source[0]'), sfd=1).split('.')[0])
            srcMesh = inputShp.getParent()
            startSelection = list(map(hsNode, [srcMesh, trgtMesh]))
        else:
            startSelection = list(map(hsNode, [srcMesh, trgtMesh]))
        skinClust = trgtMesh.getSkinCluster()
        if skinClust:
            targetShape = listRelatives((startSelection[1]), shapes=1)
            targetOrigin = targetShape[0] + 'Orig'
            select(targetOrigin, r=1)
            setAttr(targetOrigin + '.intermediateObject', 0)
        select(srcMesh, r=1)
        if skinClust:
            select(targetOrigin, add=1)
        else:
            select(trgtMesh, add=1)
        mapNode = transferAttributes(flipUVs=0, transferPositions=0, transferUVs=2, sourceUvSpace='map1', searchMethod=3, transferNormals=0, transferColors=2, targetUvSpace='map1', colorBorders=1, sampleSpace=spaceVal)[0]
        if delHistory:
            if skinClust:
                select(targetOrigin, r=1)
            else:
                select(trgtMesh, r=1)
            mel.DeleteHistory()
        if skinClust:
            setAttr(targetOrigin + '.intermediateObject', 1)
        select(trgtMesh, r=1)
        if getMatchPercent:
            testGeo = hsNode(trgtMesh)
            inputMesh = PyNode(srcMesh)
            testVtx = testGeo.getVtxList()
            select(testGeo, r=1)
            mel.ConvertSelectionToVertices()
            testVtx = ls(sl=1, fl=1)
            vtxCount = len(testVtx)
            matchedUVs = []
            for vtx in testVtx:
                vtx.select(r=1)
                mapUV = mel.polyListComponentConversion(fv=1, tuv=1)[0]
                uvValues = [round(val, 3) for val in polyEditUV(mapUV, q=1)]
                inputVtx = PyNode(inputMesh + '.' + vtx.split('.')[-1])
                inputVtx.select()
                mapUV_In = mel.polyListComponentConversion(fv=1, tuv=1)[0]
                uvValues_In = [round(val, 3) for val in polyEditUV(mapUV_In, q=1)]
                if uvValues == uvValues_In:
                    matchedUVs.append(vtx)

            matchCount = len(matchedUVs)
            matchPercent = matchCount / float(vtxCount)
            if deleteMap:
                try:
                    delete(mapNode)
                except:
                    pass

                return bestMatch or [spaceVal, matchPercent]
        elif deleteMap:
            try:
                delete(mapNode)
            except:
                pass

        else:
            return mapNode
        if bestMatch:
            matchList = []
            for spcVal in range(0, 5):
                matchPair = HyperSkin.transferUVs(srcMesh, trgtMesh, spcVal, True, True, False, True)
                matchList.append(matchPair)

            matchDict = dict(matchList)
            sortedList = sorted((list(matchDict.items())), key=(operator.itemgetter(1)))
            spaceVal = sortedList[-1][0]
            matchList = HyperSkin.transferUVs(srcMesh, trgtMesh, spaceVal, delHistory, True, False, False)
            return [sortedList, matchList]

    def transferSkin(self, srcMesh_Or_VtxList=None, destMesh_Or_VtxList=None, removeSrcClust=False, removeDestClust=True, trgtPrfx=None):
        """
                Alternative One which is tested and proven one
                srcMesh_Or_VtxList =selected()[0]
                destMesh_Or_VtxList =selected()[1]
                
                Testing:
                --------
                HyperSkin.transferSkin(trgtPrfx='Trgt_')
                """
        HyperSkin.closeWindows()
        influObjCheck = checkBox('as_InfluObj_CB', q=1, v=1)
        if trgtPrfx:
            if not srcMesh_Or_VtxList:
                srcMeshList = hsN.selected()
                if not srcMeshList:
                    return
            else:
                srcMeshList = srcMesh_Or_VtxList
            destMeshDict = dict([(srcNode, hsNode(trgtPrfx + srcNode.name())) for srcNode in srcMeshList if cmds.objExists(trgtPrfx + srcNode.name())])
            missingSrcList = [srcNode for srcNode in srcMeshList if not cmds.objExists(trgtPrfx + srcNode.name())]
            if destMeshDict:
                for (srcMesh, destMesh) in list(destMeshDict.items()):
                    HyperSkin.transferSkin(srcMesh, destMesh)

            if missingSrcList:
                cmds.select(missingSrcList, r=1)
            return
        srcMesh = None
        destMesh = None
        if not srcMesh_Or_VtxList:
            if not destMesh_Or_VtxList:
                meshList = hsN.selected()
                if meshList:
                    srcMesh = meshList[0]
                    destMesh = meshList[1]
                else:
                    return
        if type(srcMesh_Or_VtxList) != list:
            if cmds.objExists(srcMesh_Or_VtxList):
                srcMesh = hsNode(srcMesh_Or_VtxList)
            else:
                srcMesh_Or_VtxList = hsNode(srcMesh)
            srcSkinClust = listHistory(srcMesh_Or_VtxList, type='skinCluster')[0]
        else:
            if not srcMesh:
                srcMesh = hsNode(srcMesh_Or_VtxList[0].split('.')[0])
                if srcMesh.isShape():
                    srcMesh.extendToParent()
            srcSkinClust = listHistory(srcMesh, type='skinCluster')[0]
        if type(destMesh_Or_VtxList) != list:
            if cmds.objExists(destMesh_Or_VtxList):
                destMesh = hsNode(destMesh_Or_VtxList)
            else:
                destMesh_Or_VtxList = hsNode(destMesh)
            destSkinClust = listHistory(destMesh_Or_VtxList, type='skinCluster')
            skinTrgt = True
            if destSkinClust:
                skinTrgt = False
                if removeDestClust:
                    select(cl=1)
                    delete(destSkinClust[0])
                    skinTrgt = True
            if skinTrgt:
                sknJnts = cmds.skinCluster((srcSkinClust.name()), q=1, inf=1)
                select(destMesh_Or_VtxList, sknJnts, r=1)
                skinCluster(sknJnts, destMesh_Or_VtxList, tsb=1, bm=0, sm=3, nw=1, mi=4, omi=0, dr=10, rui=0)
        elif not destMesh:
            destMesh = hsNode(destMesh_Or_VtxList[0].split('.')[0])
            if destMesh.isShape():
                destMesh.extendToParent()
        jntList = skinCluster(srcSkinClust, q=1, wi=1)
        print('-----------------------------')
        print('Details Of Skinning Transfer !')
        print('-----------------------------')
        print('\nTotal Weight Influences : ' + str(len(jntList)))
        print('-----------------------------')
        pprint.pprint(jntList)
        print('\n')
        influList = []
        for jnt in jntList:
            if PyNode(jnt).getShape():
                influList.append(jnt)

        for influ in influList:
            jntList.remove(influ)

        print('No of Jnts for Skinning : ' + str(len(jntList)))
        print('-----------------------------')
        pprint.pprint(jntList)
        print('\n')
        if influObjCheck == 1:
            print('No of Influence Objects : ' + str(len(influList)))
            print('-----------------------------')
            pprint.pprint(influList)
            print('\n')
            if influList:
                if not trgtPrfx:
                    HyperSkin.startProgressWin(len(influList), 'Please Wait ..!', None, False)
                for influObj in influList:
                    select(destMesh, r=1)
                    select(influObj, add=1)
                    HyperSkin.refreshView(1)
                    if not trgtPrfx:
                        HyperSkin.progressWin(influObj, False)
                    else:
                        mel.skinClusterInfluence(1, '-dr 8.5 -ps 0 -ns 10')

                if not trgtPrfx:
                    HyperSkin.endProgressWin(len(influList), True)
            else:
                om.MGlobal.displayInfo('# There are no influence objects on base mesh.. ')
            cmds.select(srcMesh_Or_VtxList, r=1)
            cmds.select(destMesh_Or_VtxList, add=1)
            copySkinWeights(noMirror=1, surfaceAssociation='closestPoint', influenceAssociation=['oneToOne', 'oneToOne', 'oneToOne'])
            if removeSrcClust:
                cmds.delete(srcSkinClust)
            select(destMesh, r=1)
            mel.removeUnusedInfluences()

    def transferSkin_Jnt2Jnt(self, skinMesh=None, srcJnt=None, trgtJnt=None, trgtPrefix=None):
        trgtPrefix = trgtPrefix or textField('as_TrgtJntPrefix_TF', q=1, tx=1)
        if cmds.radioButton('as_SkinTransferJ2J_O2O_RB', q=1, sl=1):
            trgtPrefix = ''
        else:
            if cmds.radioButton('as_SkinTransferJ2J_RB', q=1, sl=1):
                trgtPrefix = ''
            else:
                if cmds.radioButton('as_TransferSkinNearJnts_RB', q=1, sl=1):
                    trgtPrefix = ''
                else:
                    infList = srcJnt or trgtJnt or hsN.selected()
                    if len(infList) != 2:
                        hsN._error('You need to select only two influences/Joints !!')
                        return
                        srcJnt, trgtJnt = infList
                    else:
                        if pm.objExists(srcJnt):
                            srcJnt = hsNode(srcJnt)
                        else:
                            return
                    if cmds.checkBox('as_MultipleMeshes_CB', q=1, v=1):
                        meshStr = cmds.textField('as_SkinMesh_TF', q=1, text=1)
                        try:
                            meshList = list(map(hsNode, meshStr.split(', ')))
                        except:
                            HyperSkin.error('Multiple Meshes Are Not Given')

                        cmds.checkBox('as_MultipleMeshes_CB', e=1, v=0)
                        HyperSkin.startProgressWin(meshList)
                        for skinMesh in meshList:
                            HyperSkin.transferSkin_Jnt2Jnt(skinMesh, srcJnt, trgtJnt, trgtPrefix)
                            HyperSkin.progressWin(skinMesh)

                        HyperSkin.endProgressWin(meshList, 1)
                        meshStr = cmds.textField('as_SkinMesh_TF', e=1, text=meshStr)
                        cmds.checkBox('as_MultipleMeshes_CB', e=1, v=1)
                        return
                    if not skinMesh:
                        try:
                            skinMesh, skinClust = HyperSkin.confirmSkinMesh()
                        except:
                            skinMesh = hsNode(skinMesh)
                            skinClust = skinMesh.listHistory(type='skinCluster')
                            if not skinClust:
                                hsN._error('"{0}" is not skinned Mesh'.format(skinMesh))
                            else:
                                skinClust = skinClust[0]

                    else:
                        if pm.objExists(skinMesh):
                            if HyperSkin.isSkinned(skinMesh):
                                cmds.textField('as_SkinMesh_TF', e=1, tx=(str(skinMesh)))
                                skinMesh, skinClust = HyperSkin.confirmSkinMesh()
                            else:
                                HyperSkin.error('Please provide skinMesh in UI')
                        else:
                            HyperSkin.error('Please provide skinMesh in UI')
                allInfList = cmds.skinCluster((str(skinClust)), q=1, inf=1)
                allInfList = list(map(hsNode, allInfList))
        if type(trgtJnt) == list:
            trgtJnt = srcJnt.nearestObj(trgtJnt)[0]
        else:
            if not trgtPrefix:
                if pm.objExists(trgtJnt):
                    trgtJnt = hsNode(trgtJnt)
                else:
                    return
            elif trgtPrefix:
                trgtName = trgtPrefix + srcJnt.name()
                if pm.objExists(trgtName):
                    trgtJnt = hsNode(trgtName)
                else:
                    return
            else:
                allInfList_str = list(map(str, allInfList))
                if str(trgtJnt) not in allInfList_str:
                    cmds.skinCluster((str(skinClust)), ai=(str(trgtJnt)), dr=8.5, wt=0, e=1, lw=True)
                cmds.setAttr(trgtJnt + '.liw', 0)
                for sknJnt in allInfList:
                    if sknJnt != trgtJnt:
                        cmds.setAttr(sknJnt + '.liw', 1)
                    else:
                        cmds.setAttr(sknJnt + '.liw', 0)

                skinMesh.select()
                ArtPaintSkinWeightsToolOptions()
                artAttrSkinPaintCtx((currentCtx()), e=1, op=1)
                mel.artAttrPaintOperation('artAttrSkinPaintCtx', 'Replace')
                try:
                    mel.artUpdateStampProfile('solid', 'artAttrSkinPaintCtx')
                except:
                    HyperSkin.refreshView(5)
                    try:
                        mel.artUpdateStampProfile('solid', currentCtx())
                    except:
                        pass

            artAttrSkinPaintCtx((currentCtx()), e=1, value=0)
            mel.artSkinInflListChanging(srcJnt, 1)
            mel.artSkinInflListChanged('artAttrSkinPaintCtx')
            skinMesh.select()
            ArtPaintSkinWeightsToolOptions()
            HyperSkin.refreshView(1)
            artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
            for sknJnt in allInfList:
                cmds.setAttr(sknJnt + '.liw', 0)

            skinMesh.select()
            mel.removeUnusedInfluences()
            pm.select(srcJnt, trgtJnt, r=1)
            om.MGlobal.displayInfo('Transferred from {} -> {}'.format(srcJnt, trgtJnt))

    def transferSkin_Jnts2Jnts(self, prefix=None, skinMesh=None, transferType=None, **shArgs):
        """
                Useful for creating single hierarchy joint chain for MoCap purpose
                """
        if shArgs:
            prefix = shArgs['p'] if 'p' in shArgs else prefix
            skinMesh = shArgs['sm'] if 'sm' in shArgs else skinMesh
            transferType = shArgs['tt'] if 'tt' in shArgs else transferType
        if not prefix:
            prefix = textField('as_TrgtJntPrefix_TF', q=1, tx=1)
        selList = hsN.selected()
        if not skinMesh:
            if selList:
                if HyperSkin.isSkinned(selList[0]):
                    if selList[0].isMesh():
                        cmds.textField('as_SkinMesh_TF', e=1, tx=(selList[0].name()))
            skinMesh = hsNode(HyperSkin.confirmSkinMesh()[0])
        else:
            skinMesh = hsNode(skinMesh)
        _prefix = True
        _suffix = False
        _replacedPrefix = False
        _replacedSuffix = False
        if selList[0].isJnt():
            skinJnts = [jnt for jnt in selList if jnt.isJnt()]
        else:
            skinJnts = skinMesh.getSkinJnts()[0]
        nJnts = []
        trgtJntDict = {}
        for jnt in skinJnts:
            jntShortName = jnt.shortName()
            trgtJnt = prefix + jntShortName
            jntExist = False
            if cmds.objExists(trgtJnt):
                jntExist = True
                trgtJnt = hsNode(trgtJnt)
            else:
                trgtJntName = prefix + jntShortName
                if cmds.checkBox('as_CreateSingleHI_CB', q=1, v=1):
                    trgtJnt = jnt.duplicate(n=trgtJntName, po=1)[0]
            if cmds.checkBox('as_CreateSingleHI_CB', q=1, v=1):
                HyperSkin.removeParentChild_ImpliedInfo(trgtJnt)
            trgtJntDict[jnt] = trgtJnt
            if not not jntExist:
                if cmds.checkBox('as_CreateSingleHI_CB', q=1, v=1):
                    trgtJnt.parentTo()
                    if cmds.checkBox('as_Jnts2JntsConstrain_CB', q=1, v=1):
                        jnt.mConstrain(trgtJnt, 'parent')
                    nJnts.append(trgtJnt)

        if cmds.checkBox('as_CreateSingleHI_CB', q=1, v=1):
            for jnt in skinJnts:
                pJnt = jnt.parent(nType='joint')
                if pJnt:
                    if pJnt in skinJnts:
                        if pJnt.nodeType() == 'joint':
                            if _prefix:
                                trgtJntDict[jnt].parentTo(prefix + pJnt.shortName())
                            elif _suffix:
                                trgtJntDict[jnt].parentTo(pJnt.shortName() + prefix)
                            else:
                                if _replacedPrefix:
                                    trgtJntDict[jnt].parentTo(prefix + pJnt.shortName().split('_', 1)[1])
                            if _replacedSuffix:
                                trgtJntDict[jnt].parentTo(pJnt.shortName().rsplit('_', 1)[0] + prefix)

        cmds.radioButton('as_SkinTransferJ2J_O2O_RB', e=1, sl=1)
        if HyperSkin.confirmAction('Transfer Skin ??'):
            HyperSkin.startProgressWin(skinJnts, 'Transferring Skin !!')
            for jnt in skinJnts:
                if _prefix:
                    if not HyperSkin.isSkinJnt(jnt, skinMesh):
                        continue
                    elif pm.objExists(prefix + jnt.shortName()):
                        HyperSkin.transferSkin_Jnt2Jnt(skinMesh, jnt, prefix + jnt.shortName())
                else:
                    if _suffix:
                        HyperSkin.transferSkin_Jnt2Jnt(skinMesh, jnt, jnt.shortName() + prefix)
                    elif _replacedPrefix:
                        HyperSkin.transferSkin_Jnt2Jnt(skinMesh, jnt, prefix + pJnt.shortName().split('_', 1)[1])
                    elif _replacedSuffix:
                        HyperSkin.transferSkin_Jnt2Jnt(skinMesh, jnt, jnt.shortName().rsplit('_', 1)[0] + prefix)
                    HyperSkin.progressWin(jnt)

            HyperSkin.endProgressWin(skinJnts, 1)
        cmds.radioButton('as_TransferRig2Skeleton_RB', e=1, sl=1)
        cmds.select(nJnts, r=1)

    def transferSkin_NearestJnts2Jnts(self, skinMeshes=None, trgtJnts=None, transferAll=False, **shArgs):
        """
                :param self:
                :param skinMeshes: Transfer skin for selected/ given skinMeshes
                :param trgtJnts: Transfer skin for selected (non-skinned)/ given joints
                :param transferAll: Transfer skin for selected number of non-skinned joints or for all skinned joints
                :return:
                """
        if shArgs:
            skinMeshes = shArgs['sm'] if 'sm' in shArgs else skinMeshes
            trgtJnts = shArgs['tj'] if 'tj' in shArgs else trgtJnts
            transferAll = shArgs['ta'] if 'ta' in shArgs else transferAll
        skinJnts = []
        selList = hsN.selected()
        if not skinMeshes:
            if selList:
                skinMeshes = [obj for obj in selList if obj.isSkinMesh()]
        if not skinMeshes:
            skinMesh = HyperSkin.confirmSkinMesh()[0]
            skinMeshes = [hsNode(skinMesh)]
        if not trgtJnts:
            if selList:
                trgtJnts = [obj for obj in selList if obj.isJnt()]
        HyperSkin.startProgressWin(skinMeshes, 'Transfer Skinning >>', 'Please Wait', innerObjs=trgtJnts)
        for skinMesh in skinMeshes:
            skinJnts = skinMesh.getSkinJnts()[0]
            if transferAll:
                HyperSkin.startProgressWin(innerList=skinJnts)
                for jnt in skinJnts:
                    HyperSkin.progressWin(ci=jnt, innerList=skinJnts, ep=0)
                    nJnt = jnt.nearestObj(trgtJnts)
                    HyperSkin.transferSkin_Jnt2Jnt(skinMesh, jnt, nJnt)

            else:
                HyperSkin.startProgressWin(innerList=trgtJnts)
                for jnt in trgtJnts:
                    HyperSkin.progressWin(ci=jnt, innerList=trgtJnts, ep=0)
                    nJnt = jnt.nearestObj(skinJnts)
                    HyperSkin.transferSkin_Jnt2Jnt(skinMesh, nJnt, jnt)

            HyperSkin.progressWin(ci=skinMesh)

        HyperSkin.endProgressWin(skinMeshes, 1)
        pm.select(trgtJnts, r=1)
        HyperSkin.refreshView(1)
        HyperSkin.message('Transferred Skinning To Nearest Joints Successfully')

    def transferSkin_Overlap(self, srcMesh=None, destMesh=None, transferType='I2O'):
        if not srcMesh:
            if not destMesh:
                meshList = hsN.selected()
                if meshList:
                    srcMesh = meshList[0]
                    destMesh = meshList[1]
                else:
                    return
        if transferType.lower() == 'o2i':
            vtxList_srcMesh = HyperSkin.getMeshVtx_Overlap(srcMesh, destMesh, 'out')
            vtxList_destMesh = HyperSkin.getMeshVtx_Overlap(srcMesh, destMesh, 'in')
        elif transferType.lower() == 'i2o':
            vtxList_srcMesh = HyperSkin.getMeshVtx_Overlap(destMesh, srcMesh, 'in')
            vtxList_destMesh = HyperSkin.getMeshVtx_Overlap(destMesh, srcMesh, 'out')
        if vtxList_srcMesh:
            cmds.sets(vtxList_srcMesh, n=('SrcVtx_{0}'.format(srcMesh)))
        else:
            HyperSkin.message("Couldn't find vtxList on srcMesh --> '{0}'!\nNo Action Taken !!".format(srcMesh))
            return
        if vtxList_destMesh:
            cmds.sets(vtxList_destMesh, n=('SrcVtx_{0}'.format(destMesh)))
        else:
            HyperSkin.message("Couldn't find vtxList on destMesh --> '{0}'!\nNo Action Taken !!".format(destMesh))
            return
        HyperSkin.transferSkin(vtxList_srcMesh, vtxList_destMesh)
        cmds.select(vtxList_srcMesh, r=1)
        cmds.select(vtxList_destMesh, add=1)

    def transferSkin_Vtx2Vtx(self, src=None, dest=None):
        if not src:
            if not dest:
                vtxList = hsN.selected()
                src = vtxList[0]
                dest = vtxList[1]
        src = hsNode(src)
        dest = hsNode(dest)
        skinClust = src.getSkinCluster()
        stWgts = HyperSkin.getSkinWeights(None, src, skinClust)
        skinClust = dest.getSkinCluster()
        HyperSkin.setSkinWeights(dest, stWgts, 1, skinClust)

    def transferSkin_Vtx2ManyVtx(self):
        destVtxList = cmds.ls(os=1, fl=1)
        srcVtx = cmds.textField('as_TrgtMeshList_TF', q=1, text=1)
        if not cmds.objExists(srcVtx):
            srcVtx = destVtxList[-1]
            destVtxList = destVtxList[:-1]
        HyperSkin.startProgressWin(destVtxList)
        for src in destVtxList:
            HyperSkin.transferSkin_Vtx2Vtx(srcVtx, src)
            HyperSkin.progressWin(src)

        HyperSkin.endProgressWin(destVtxList)

    def transferSkin_ManyVtx2ManyVtx(self):
        destList = hsN.selected()
        vtxStr = cmds.textField('as_TrgtMeshList_TF', q=1, text=1)
        srcList = list(map(hsNode, vtxStr.split(', ')))
        HyperSkin.startProgressWin(destList)
        for destVtx in destList:
            tVtx = HyperSkin.getNearestObj(destVtx, srcList, 'vtx', 'vtx')
            HyperSkin.transferSkin_Vtx2Vtx(tVtx, destVtx)
            HyperSkin.progressWin(destVtx)

        HyperSkin.endProgressWin(destList)

    def transferSkin_VtxDist(self, skinObjs, distVal='BB'):
        for obj in skinObjs[0:-1]:
            select((MeshVertex(obj.getShape())), r=1)
            vtxList_S = filterExpand(sm=31)
            select((MeshVertex(skinObjs[-1].getShape())), r=1)
            vtxList_Dest = filterExpand(sm=31)
            vtxList_D = []
            HyperSkin.startProgressWin(len(vtxList_Dest), 'Please Wait ..!', None, False)
            for vtx in vtxList_Dest:
                HyperSkin.progressWin(vtx, False, _as_HyperSkinMain__showProgressTime)
                if distVal == 'BB':
                    vtxPos = xform(vtx, q=1, ws=1, t=1)
                    if HyperSkin.checkPosIn_BB(obj, vtxPos):
                        vtxList_D.append(vtx)
                else:
                    if not not type(distVal) == int:
                        if type(distVal) == int:
                            pass
                        if HyperSkin.getClosestDist_Obj(vtx, obj) < distVal:
                            vtxList_D.append(vtx)

            HyperSkin.endProgressWin(len(vtxList_Dest), 1)
            select(vtxList_S, r=1)
            select(vtxList_D, add=1)
            copySkinWeights(surfaceAssociation='closestPoint', influenceAssociation=['oneToOne', 'oneToOne'], noMirror=1)

    def mirrorSkin(self, LPrfx='L_', RPrfx='R_', left2right=True, dirAxis='x'):
        prefixOrSuffix = optionMenu('as_PrefixOrSuffix_OM', q=1, v=1)
        if prefixOrSuffix != 'Prefix' or prefixOrSuffix != 'Suffix':
            prefixOrSuffix = 'Prefix'
        else:
            _as_HyperSkinMain__showProgressTime = 0
            if not filterExpand(sm=31):
                if left2right:
                    HyperSkin.selectSkinVertices('L_')
                else:
                    HyperSkin.selectSkinVertices('R_')
                vtxList = [hsNode(vtx) for vtx in filterExpand(sm=31)]
            else:
                vtxList = [hsNode(vtx) for vtx in filterExpand(sm=31)]
        meshList = []
        for vtx in vtxList:
            msh = vtx.asObj()
            if msh not in meshList:
                msh._appendTo(meshList)

        if len(meshList) > 1:
            toPrint = 'Please check for whether Vertices are selected from more than one skin mesh'
            toPrint += '\nVetices might be selected from Selection Set, where vertices might be from duplicated mesh'
            HyperSkin.confirmAction(toPrint, True)
        vMesh = vtxList[0].asObj()
        if vMesh.isShape():
            vMesh.extendToParent()
        skinClust = listHistory((vMesh.name()), type='skinCluster')[0]
        cmds.setAttr(str(skinClust) + '.envelope', 0)
        vMesh.select()
        HyperSkin.refreshView(1)
        oppVtxList = []
        oppVtxNums = []
        skipList = []
        excludeDir = '+' + dirAxis if left2right else '-' + dirAxis
        jntListStr = [str(jnt) for jnt in skinCluster(skinClust, inf=1, q=1)]
        for jnt in jntListStr:
            if not (left2right):
                if not prefixOrSuffix == 'Suffix' or jnt.endswith(LPrfx):
                    RJnt = jnt.replace(LPrfx, RPrfx)
            if not objExists(RJnt):
                if HyperSkin.confirmAction('No Mirror Joint Exists With This Name: "%s"\nDo You Want To Proceed?' % RJnt):
                    if RJnt not in skipList:
                        skipList.append(RJnt)
                    else:
                        HyperSkin.error('Mirror Action Cancelled ..!')
                elif RJnt not in jntListStr:
                    if HyperSkin.confirmAction('"%s" is not attached to skin!\nAttach this joint to skin now?' % RJnt):
                        skinCluster(skinClust, ai=RJnt, dr=8.5, wt=0, e=1, lw=True)
                    else:
                        HyperSkin.error('Mirror Action Cancelled ..!')
                else:
                    if prefixOrSuffix == 'Prefix' and jnt.startswith(RPrfx) or prefixOrSuffix == 'Suffix' and jnt.endswith(RPrfx):
                        pass
                    LJnt = jnt.replace(RPrfx, LPrfx)
                    if (objExists(LJnt) or HyperSkin.confirmAction)('No Mirror Joint Exists With This Name: "%s"\nDo You Want To Continue?' % LJnt):
                        if LJnt not in skipList:
                            skipList.append(LJnt)
                        else:
                            HyperSkin.error('Mirror Action Cancelled ..!')
                    elif LJnt not in jntListStr:
                        if HyperSkin.confirmAction('"%s" is not attached to skin!\nAttach to skin now?' % LJnt):
                            skinCluster(skinClust, ai=LJnt, dr=8.5, wt=0, e=1, lw=True)
                        else:
                            HyperSkin.error('Mirror Action Cancelled ..!')

        jntList = skinCluster(skinClust, wi=1, q=1)
        HyperSkin.startProgressWin(len(vtxList))
        for vtx in vtxList:
            HyperSkin.progressWin(vtx, False, _as_HyperSkinMain__showProgressTime)
            vtxPos = vtx.getPos()
            if left2right:
                if vtxPos[0] <= 0.0:
                    continue
                else:
                    if vtxPos[0] >= 0.0:
                        continue
                    else:
                        vtx.select(r=1)
                        mel.doPruneSkinClusterWeightsArgList(1, ['0.02'])
                        skinDict = {}
                        for jnt in jntList:
                            skinPVal = skinPercent(skinClust, vtx, q=1, t=jnt)
                            if skinPVal > 0.0:
                                skinDict[jnt] = skinPVal

                        vtxPos[0] = -1 * vtxPos[0]
                        oppVtxL = HyperSkin.nearestVtx_OnMesh(vtxPos, vMesh, oppVtxNums, excludeDir)
                        if oppVtxL:
                            oppVtx = oppVtxL[0]
                        else:
                            continue
                    select(oppVtx, r=1)
                    mel.doPruneSkinClusterWeightsArgList(1, ['0.02'])
                    oppJntList = []
                    for jnt in list(skinDict.keys()):
                        if prefixOrSuffix == 'Prefix' and jnt.startswith(LPrfx) or prefixOrSuffix == 'Suffix':
                            if jnt.endswith(LPrfx):
                                RJnt = jnt.replace(LPrfx, RPrfx)
                                try:
                                    setAttr(RJnt + '.liw', 0)
                                    skinPercent(skinClust, oppVtx, transformValue=(RJnt, skinDict[jnt]))
                                    setAttr(RJnt + '.liw', 1)
                                    oppJntList.append(RJnt)
                                except:
                                    if RJnt not in skipList:
                                        if HyperSkin.confirmAction('"%s" is not influence joint for this skin.\nAttach this Joint to skin ?' % RJnt):
                                            try:
                                                skinCluster(skinClust, ai=RJnt, dr=8.5, wt=0, e=1, lw=True)
                                                setAttr(RJnt + '.liw', 0)
                                                skinPercent(skinClust, oppVtx, transformValue=[RJnt, skinDict[jnt]])
                                                setAttr(RJnt + '.liw', 1)
                                                oppJntList.append(RJnt)
                                            except:
                                                HyperSkin.confirmAction('%s is not available to attach to skin' % RJnt)
                                                skipList.append(RJnt)

                                        else:
                                            skipList.append(RJnt)
                                        HyperSkin.refreshView(1)

                        if not (prefixOrSuffix == 'Prefix' and jnt.startswith(RPrfx)):
                            if prefixOrSuffix == 'Suffix':
                                if jnt.endswith(RPrfx):
                                    LJnt = jnt.replace(RPrfx, LPrfx)
                                    try:
                                        setAttr(LJnt + '.liw', 0)
                                        skinPercent(skinClust, oppVtx, transformValue=[LJnt, skinDict[jnt]])
                                        setAttr(LJnt + '.liw', 1)
                                        oppJntList.append(LJnt)
                                    except:
                                        if LJnt not in skipList:
                                            if HyperSkin.confirmAction('"%s" is not influence for this skin.\nAttach this Joint to skin ?' % LJnt):
                                                try:
                                                    skinCluster(skinClust, ai=LJnt, dr=8.5, wt=0, e=1, lw=True)
                                                    setAttr(LJnt + '.liw', 0)
                                                    skinPercent(skinClust, oppVtx, transformValue=[LJnt, skinDict[jnt]])
                                                    setAttr(LJnt + '.liw', 1)
                                                    oppJntList.append(LJnt)
                                                except:
                                                    HyperSkin.confirmAction('%s is not available to attach to skin' % LJnt)
                                                    skipList.append(LJnt)

                                            else:
                                                skipList.append(LJnt)
                                            HyperSkin.refreshView(1)

                            setAttr(jnt + '.liw', 0)
                            skinPercent(skinClust, oppVtx, transformValue=[jnt, skinDict[jnt]])
                            setAttr(jnt + '.liw', 1)
                            oppJntList.append(jnt)

                    if oppJntList:
                        for oppJnt in oppJntList:
                            setAttr(oppJnt + '.liw', 0)

                    oppVtxList.append(oppVtx)
                    oppNum = oppVtx.extractNum()
                if oppNum:
                    oppVtxNums.append(oppNum[0])
                else:
                    oppVtxNums.append(0)

        HyperSkin.endProgressWin(len(vtxList), True)
        cmds.setAttr(str(skinClust) + '.envelope', 1)
        select(oppVtxList, r=1)
        HyperSkin.refreshView(1)

    def isSkinJnt(self, jnt, skinMesh):
        asJnt = hsNode(jnt)
        asMesh = hsNode(skinMesh)
        if not asJnt.isJnt():
            return False
        skinClust = asMesh.listHistory(type='skinCluster')[0]
        if skinClust:
            infList = [str(jnt) for jnt in cmds.skinCluster(skinClust, q=1, inf=1)]
            if str(asJnt) in infList:
                return True
            return False
        else:
            return True

    def removeInfluences_skinClust(self, infList=None, skinMesh=None):
        """
                Purpose:
                ========
                Adds given infList to given skinMesh

                Args:
                =====
                infList =infList to be added to skinMesh
                skinMesh = infList[-1], if skinMesh not given
                useGeoInf = True | False (for 'useGeometry' arg)

                Args (from selection):
                ======================
                If both Args are not given:
                        infList =hsN.selected()[0:-1]
                        skinMesh =hsN.selected()[-1]
                """
        if not infList:
            selList = skinMesh or hsN.selected()
            infList = selList[0:-1]
            skinMesh = selList[-1]
        else:
            if infList:
                infList = skinMesh or ([infList] if type(infList) != list else infList)
                infList = list(map(hsNode, infList[0:-1]))
                skinMesh = hsNode(infList[-1])
            else:
                if infList:
                    if skinMesh:
                        infList = [infList] if type(infList) != list else infList
                        infList = list(map(hsNode, infList))
                        skinMesh = hsNode(skinMesh)
        skinClust = skinMesh.listHistory(type='skinCluster')
        for infObj in infList:
            cmds.skinCluster(skinClust, e=1, ri=infObj)

    def addInfluences_skinClust(self, infList=None, skinMesh=None, useGeoInf=True, useProgress=1):
        """
                Purpose:
                ========
                Adds given infList to given skinMesh

                Args:
                =====
                infList =infList to be added to skinMesh
                skinMesh = infList[-1], if skinMesh not given
                useGeoInf = True | False (for 'useGeometry' arg)

                Args (from selection):
                ======================
                If both Args are not given:
                        infList =hsN.selected()[0:-1]
                        skinMesh =hsN.selected()[-1]
                """
        infList = [infList] if type(infList) != list else infList
        if not infList:
            selList = skinMesh or hsNode(selList[-1])
            infList = [hsNode(sel) for sel in selList[0:-1]]
            skinMesh = hsNode(selList[-1])
        else:
            if infList:
                infList = [hsNode(inf) for inf in (skinMesh or infList[0:-1])]
                skinMesh = hsNode(infList[-1])
            else:
                if skinMesh:
                    infList = [hsNode(inf) for inf in infList]
                    skinMesh = hsNode(skinMesh)
                else:
                    skinClust = skinMesh.listHistory(type='skinCluster')
                    if skinClust:
                        skinClust = skinClust[0]
                        if useGeoInf:
                            cmds.setAttr(skinClust + '.useComponents', 1)
                    else:
                        HyperSkin.error('Last object selected is not skinned !!')
                if useProgress:
                    HyperSkin.startProgressWin(len(infList), 'Adding Infs / Joints To Skin Cluster !!')
                for infObj in infList:
                    if useProgress:
                        HyperSkin.progressWin(infObj)
                    if infObj.isShape():
                        if not HyperSkinFunctions.isSkinJnt(infObj, skinMesh):
                            cmds.skinCluster(skinClust, e=1, ug=1, dr=8.5, ps=True, ns=10, lw=True, wt=0, ai=infObj)
                    else:
                        try:
                            cmds.skinCluster(skinClust, e=1, dr=8.5, ug=0, lw=True, wt=0, ai=infObj)
                        except:
                            pass
                        cmds.setAttr(infObj.node + '.liw', 0)
                if useProgress:
                    HyperSkin.endProgressWin(len(infList), True)

    def expandSkinArea(self, vtxList, valList, infName, skinClust=None, smoothCount=1, prevVtxList=None, **shortArgs):
        """
                """
        if shortArgs:
            vtxList = shortArgs['vl'] if 'vl' in shortArgs else vtxList
            valList = shortArgs['vl'] if 'vl' in shortArgs else valList
            infName = shortArgs['inf'] if 'inf' in shortArgs else infName
            smoothCount = shortArgs['sc'] if 'sc' in shortArgs else smoothCount
        vtxList = [vtxList] if type(vtxList) != list else vtxList
        valList = [valList] if type(valList) != list else valList
        if not skinClust:
            skinMesh = hsNode(listRelatives((vtxList[0]), p=1)[0]).parent()
            skinClust = skinMesh.listHistory(type='skinCluster')[0]
        select(vtxList, r=1)
        mel.GrowPolygonSelectionRegion()
        allVtxList = filterExpand(ex=1, sm=31)
        s1 = set(allVtxList)
        s2 = set(vtxList)
        extnVtxList = list(s1 - s2)
        if prevVtxList:
            s1 = set(extnVtxList)
            s2 = set(prevVtxList)
            extnVtxList = list(s1 - s2)
            prevVtxList.extend(vtxList)
        else:
            prevVtxList = [vtx for vtx in vtxList]
        select(cl=1)
        for vtx in vtxList:
            cmds.skinPercent((str(skinClust)), (str(vtx)), tv=[(str(infName), valList[0])])

        valList.remove(valList[0])
        if valList:
            return HyperSkin.expandSkinArea(extnVtxList, valList, infName, skinClust, 0, prevVtxList)
        if smoothCount:
            HyperSkin.smoothSkinWeights(vtxList, sc=smoothCount)
        return allVtxList

    def smoothSkinWeights(self, vtxListOrMesh=None, jntList=None, smoothCount=1, prefixSide=None, **shortArgs):
        """
                """
        if shortArgs:
            vtxListOrMesh = shortArgs['vlm'] if 'vlm' in shortArgs else vtxListOrMesh
            jntList = shortArgs['jl'] if 'jl' in shortArgs else jntList
            smoothCount = shortArgs['sc'] if 'sc' in shortArgs else smoothCount
            prefixSide = shortArgs['ps'] if 'ps' in shortArgs else prefixSide
        if not vtxListOrMesh:
            vtxListOrMesh = filterExpand(sm=31)
        if vtxListOrMesh:
            vtxList = [vtxListOrMesh] if type(vtxListOrMesh) != list else vtxListOrMesh
            if '.' not in vtxList[0]:
                skinMesh = hsNode(listRelatives((vtxList[0]), p=1)[0]).parent()
            else:
                skinMesh = vtxListOrMesh
            if prefixSide:
                vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
            if not jntList:
                jntList = HyperSkin.getSkinJntsList(vtxList)
            wList = jntList
            skinMesh.select()
            ArtPaintSkinWeightsToolOptions()
            artAttrSkinPaintCtx((currentCtx()), radius=0.1, e=1)
            artAttrSkinPaintCtx((currentCtx()), e=1, op=0.5)
            mel.artAttrPaintOperation('artAttrSkinPaintCtx', 'Smooth')
            a = 0
            while a < smoothCount:
                a += 1
                HyperSkin.startProgressWin(len(wList), 'Please Wait ..!', None, False)
                for inf in wList:
                    HyperSkin.progressWin('Hyper Smooth ..!', False)
                    currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                    mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                    artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

                HyperSkin.endProgressWin(len(wList), 1)
                a += 1
                if a > smoothCount:
                    break
                else:
                    HyperSkin.startProgressWin(len(wList), 'Please Wait ..!', None, False)
                    wList.reverse()
                    for inf in wList[1:]:
                        HyperSkin.progressWin('Hyper Smooth ..!', False)
                        currentInf = artAttrSkinPaintCtx((currentCtx()), q=1, inf=1)
                        mel.artSkinSelectInfluence('artAttrSkinPaintCtx', inf)
                        artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)
                        artAttrSkinPaintCtx((currentCtx()), clear=1, e=1)

                    HyperSkin.endProgressWin(len(wList), 1)

        mel.eval('changeSelectMode -object')

    def as_Generate_LipsSkin(self, jntList=None, vtxList=None, bodyMesh=None):
        HyperSkin._check4Author()
        if not bodyMesh:
            _bodyGeo = hsN.selected()
            if not _bodyGeo:
                bodyGeo = hsNode(HyperSkin.confirmSkinMesh()[0])
            else:
                bodyGeo = _bodyGeo[0]
        if not bodyGeo.isMesh():
            HyperSkin.error('Selected Is A Not Mesh')
        if not bodyGeo.isSkinMesh():
            HyperSkin.error('Selected Is A Mesh But Not Skinned ..\nTool Needs Initial Skinning !!')
        if not jntList:
            jntsStr = textField('as_LipJntsList_TF', q=1, text=1)
            jntList = list(map(hsNode, jntsStr.split(', ')))
        sknClust = listHistory(bodyGeo, type='skinCluster')[0]
        skinJnts_Existing = cmds.skinCluster((sknClust.name()), q=1, inf=1)
        jntLockDict = {}
        for jnt in skinJnts_Existing:
            jntLockDict[jnt] = cmds.getAttr(jnt + '.liw')
            cmds.setAttr(jnt + '.liw', 0)

        if not vtxList:
            vtxStr = textField('as_LipVtxList_TF', q=1, text=1)
            vtxList = vtxStr.split(', ')
            vtxExists = all([cmds.objExists(vtx) for vtx in vtxList])
            if vtxExists:
                vtxList = list(map(hsNode, vtxStr.split(', ')))
        HyperSkin.addInfluences_skinClust(jntList, bodyGeo)
        HyperSkin.startProgressWin(len(jntList), 'Hyper Skinning !!')
        for jnt in jntList:
            HyperSkin.progressWin()
            if vtxExists:
                nVtx = HyperSkin.nearestVtxOnMesh_vtxList(jnt, (bodyGeo.name()), vtxList=vtxList)[0]
                HyperSkin.expandSkinArea(nVtx, [1, 0.75, 0.5], jnt)
            else:
                nVtx = HyperSkin.nearestVtx_OnMesh(jnt, bodyGeo.name())[0]
                HyperSkin.expandSkinArea(nVtx, [1, 0.5, 0.25], jnt)

        HyperSkin.endProgressWin(len(jntList), 1)
        HyperSkin.smoothSkinWeights(bodyGeo.name(), jntList, 1)
        for jnt in skinJnts_Existing:
            cmds.setAttr(jnt + '.liw', jntLockDict[jnt])

    def export_skin(self, file_path, mesh_list=None):
        skin_weights = {}
        if not mesh_list:
            mesh_list = pm.selected()
        mesh_list = (pm.PyNode(mesh) for mesh in mesh_list)
        for mesh in mesh_list:
            skin_cluster = mesh.listHistory(type='skinCluster')[0]
            weights = skin_cluster.getWeights(mesh)
            influence_names = [inf.name() for inf in skin_cluster.influenceObjects()]
            mesh_skin_weights = {}
            for (i, weight_list) in enumerate(weights):
                vertex_num = i
                vertex_weights = {}
                for (j, weight) in enumerate(weight_list):
                    joint_name = influence_names[j]
                    joint_name = joint_name.split('|')[-1]
                    vertex_weights[joint_name] = weight

                mesh_skin_weights[vertex_num] = vertex_weights

            skin_weights[mesh.name()] = mesh_skin_weights

        with open(file_path, 'w') as f:
            json.dump(skin_weights, f, indent=4)
        print('Skin weights are exported successfully for selected meshes at this path: {0}'.format(file_path))

    def export_vtx_skin(self, vertices_list=None, file_path=None, side_vertices=None):
        selection = vertices_list
        if not selection:
            selection = pm.selected(fl=1)
        if not selection:
            raise ValueError('No selection found')
        if selection[0].nodeType() == 'transform':
            HyperSkin.error('Please use "Entire Mesh" option in this case')
        else:
            vertices_list = selection
            mesh = selection[0].node()
        if side_vertices is not None:
            mesh_matrix = mesh.getParent().getMatrix(worldSpace=True)
            if side_vertices.lower() == 'left':
                vertices_list = [v for v in vertices_list if mesh_matrix[0][3] < v.getPosition(space='world')[0]]
            elif side_vertices.lower() == 'right':
                vertices_list = [v for v in vertices_list if mesh_matrix[0][3] > v.getPosition(space='world')[0]]
            skin_cluster = mesh.listHistory(type='skinCluster')[0]
            if not skin_cluster:
                raise ValueError('No skin cluster found on mesh')
            mesh_transform = vertices_list[0].node().getParent().name()
            skin_weights = {'mesh_transform':mesh_transform, 
             'vertices':{}}
            HyperSkin.startProgressWin(vertices_list, 'Exporting Skin Weights')
            for vtx in vertices_list:
                weights = list(list(skin_cluster.getWeights(vtx))[0])
                joint_weights = {}
                for (i, weight) in enumerate(weights):
                    joint_name = skin_cluster.influenceObjects()[i].name()
                    joint_weights[joint_name] = weight

                skin_weights['vertices'][vtx.index()] = joint_weights
                HyperSkin.progressWin(vtx, 0, 1)

            HyperSkin.endProgressWin()
            file_path = file_path or pm.fileDialog2(fileMode=0, caption='Save Skin Weights')
        with open(file_path, 'w') as f:
            json.dump(skin_weights, f, indent=4)
        print('Skin weights are exported successfully to for selected vertices at this path: {0}'.format(file_path))

    def exportSkinWeights(self, vtxList=None, filePath=None, fileName=None, advExport=False):
        if cmds.radioButton('as_SelectedVtx_ESW_RBG', q=1, sl=1):
            if not advExport:
                HyperSkin.exportSkinWeights_Sides()
                return
            if not vtxList:
                vtxList = pm.selected(fl=1)
            meshList = [obj for obj in hsN.selected() if not obj.isMesh() if obj.isCurv() if obj.isMesh() if obj.isCurv()]
            if meshList or vtxList:
                if advExport:
                    scnName = pm.sceneName()
                    scnPathBase = scnName.rsplit('.', 1)[0]
                    folderPath = scnPathBase.rsplit('/', 1)[0]
                    libPath = folderPath + '/AHSS_Lib/'
                    if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
                        fileName = 'AHSS_SkinWeights.json'
                        HyperSkin.export_skin(libPath + fileName, meshList)
                    elif cmds.radioButton('as_Weights_LS_RBG', q=1, sl=1):
                        fileName = 'AHSS_LeftWeights.json'
                        HyperSkin.export_vtx_skin(vtxList, libPath + fileName, 'left')
                    elif cmds.radioButton('as_Weights_RS_RBG', q=1, sl=1):
                        fileName = 'AHSS_RightWeights.json'
                        HyperSkin.export_vtx_skin(vtxList, libPath + fileName, 'right')
                    elif cmds.radioButton('as_SelectedVtx_ESW_RBG', q=1, sl=1):
                        fileName = 'AHSS_VtxWeights.json'
                        HyperSkin.export_vtx_skin(vtxList, libPath + fileName)
                    try:
                        os.startfile(mel.toNativePath(libPath))
                    except:
                        try:
                            os.system('xdg-open "%s"' % libPath)
                        except:
                            subprocess.Popen(['xdg-open', libPath])

                    return
                for mesh in meshList:
                    mesh.select()
                    if not not cmds.radioButton('as_Weights_LS_RBG', q=1, sl=1):
                        if not not cmds.radioButton('as_Weights_RS_RBG', q=1, sl=1):
                            if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
                                pass
                            HyperSkin.exportSkinWeights_Sides()
                            selList = cmds.ls(sl=1)
                            if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
                                mesh.select()
                                if mesh.isMesh():
                                    HyperSkin.exportBlendWeights()
                                cmds.select(selList, r=1)

    def exportSkinWeights_Deformer(self, fileName=None):
        skn = as_HyperSkinMain()
        scnName = sceneName()
        scnPathBase = scnName.rsplit('.', 1)[0]
        folderPath = scnPathBase.rsplit('/', 1)[0]
        libPath = folderPath + '/AHSS_Lib'
        if not os.path.exists(libPath):
            sysFile(libPath, makeDir=True)
        meshList = hsN.selected()
        for bodyMesh in meshList:
            if not fileName:
                if bodyMesh.isShape():
                    bodyMesh.extendToParent()
                fileName = bodyMesh.shortName() + '.hyperSkin'
            if os.path.exists(libPath + './' + fileName):
                if not HyperSkin.confirmAction('File Name "{0}" Already Exist !!\nContinue To Overwrite File ?'.format(fileName)):
                    raise RuntimeError('Action Cancelled !!')

        skn.exportSkinDeformer(libPath, meshList)
        try:
            os.startfile(mel.toNativePath(libPath))
        except:
            try:
                os.system('xdg-open "%s"' % libPath)
            except:
                subprocess.Popen(['xdg-open', libPath])

    def exportSkinWeights_Sides(self, vtxList=None, filePath=None, fileName=None):
        sides = None
        if cmds.radioButton('as_Weights_BS_RBG', q=1, sl=1):
            sides = 'both'
        elif cmds.radioButton('as_Weights_LS_RBG', q=1, sl=1):
            sides = 'left'
        elif cmds.radioButton('as_Weights_RS_RBG', q=1, sl=1):
            sides = 'right'
        elif cmds.radioButton('as_SelectedVtx_ESW_RBG', q=1, sl=1):
            sides = 'vtx'
        importSelList = cmds.checkBox('as_Selection_CB', q=1, v=1)
        if not vtxList:
            vtxList = filterExpand(sm=31)
            if not vtxList:
                selList = hsN.selected()
                if selList:
                    if selList[0].isMesh():
                        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh(selList[0])
                    else:
                        (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
                else:
                    (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
                if sides == 'both':
                    vtxList = HyperSkin.getMeshVtx(skinMesh)
                elif sides == 'right':
                    vtxList = HyperSkin.getMeshVtx(skinMesh, 'R_')
                else:
                    vtxList = HyperSkin.getMeshVtx(skinMesh, 'L_')
        if not filePath:
            scnName = sceneName()
            scnPathBase = scnName.rsplit('.', 1)[0]
            folderPath = scnPathBase.rsplit('/', 1)[0]
            libPath = folderPath + '/AHSS_Lib'
        if not fileName:
            asVtx = hsNode(vtxList[0])
            bodyMesh = asVtx.asObj()
            if bodyMesh.isShape():
                bodyMesh.extendToParent()
            if sides == 'both':
                fileExtn = '_SkinWeights.py'
            elif sides == 'right':
                fileExtn = '_SkinWeightsR.py'
            elif sides == 'left':
                fileExtn = '_SkinWeightsL.py'
            elif sides == 'vtx':
                fileExtn = '_SkinWeightsV.py'
            fileName = bodyMesh.shortName() + fileExtn
        if not libPath.endswith('/'):
            libPath += '/'
        if os.path.exists(libPath + fileName):
            if not HyperSkin.confirmAction('File Name "{0}" Already Exist !!\nContinue To Overwrite File ?'.format(fileName)):
                raise RuntimeError('Action Cancelled !!')
            (skinMesh, skinClust) = HyperSkin.confirmSkinMesh()
            objStr = 'import maya.cmds as mc\n'
            objStr += 'from hsNode import *\n\r'
            vtxList = [vtxList] if type(vtxList) != list else vtxList
            HyperSkin.startProgressWin(vtxList, 'Exporting Skin Weights !!')
            for asVtx in vtxList:
                jntValDict = HyperSkin.getSkinWeights(skinMesh, asVtx, skinClust)
                objStr += "HyperSkin.setSkinWeights('" + str(asVtx) + "', " + str(jntValDict) + ')\n'
                HyperSkin.progressWin(asVtx)

            if importSelList:
                vtxListStr = 'cmds.select(cl=1)\n'
                for vtx in vtxList:
                    vtxListStr += "cmds.select('" + vtx + "', add=1)\n"

                objStr += vtxListStr
            HyperSkin.endProgressWin(vtxList, True)
            if not os.path.exists(libPath):
                sysFile(libPath, makeDir=True)
        fileIO = open(libPath + fileName, 'w')
        allLines = fileIO.writelines(objStr)
        fileIO.close()
        try:
            os.startfile(mel.toNativePath(libPath))
        except:
            try:
                os.system('xdg-open "%s"' % libPath)
            except:
                subprocess.Popen(['xdg-open', libPath])

        try:
            subprocess.Popen(['notepad++', libPath + fileName])
        except:
            pass

        cmds.select(vtxList, r=1)

    class hyperSkinDeformer(object):

        def __init__(self, jointList=None, shape=None, skin=None, vtxList=None):
            self.joints = jointList
            self.shape = shape
            self.skin = skin

    def importSkinDeformer(self, fileName=None, filePath=None):
        for shape in self.skinShapes:
            if cmds.objExists(shape):
                ss = self.skinShapes[shape]
                skinList = ss.joints
                skinList.append(shape)
                cmds.select(skinList, r=True)
                try:
                    mel.doDetachSkin('2', ['1', '1'])
                except:
                    pass

                cluster = cmds.skinCluster(name=(ss.skin), tsb=1)
                pm.deformerWeights(fileName, path=filePath, deformer=(ss.skin), im=1)

        HyperSkin.message('Imported Skin Deformer Sucessfully !!')

    def exportSkinDeformer(self, filePath, meshList):
        t1 = time.time()
        meshDict = {}
        for mesh in meshList:
            sc = mel.eval('findRelatedSkinCluster ' + mesh)
            msh = cmds.listRelatives(mesh, shapes=1)
            if sc != '':
                meshDict[sc] = mesh
            else:
                cmds.warning(mesh + ' is not skinned !!')

        for skin in list(meshDict.keys()):
            print(filePath, skin)
            if self._mayaVer() < 2019:
                pm.deformerWeights((meshDict[skin] + '.hyperSkin'), path=filePath, ex=True, deformer=skin)
            else:
                pm.deformerWeights((meshDict[skin] + '.xml'), path=filePath, ex=True, deformer=skin)

        elapsed = time.time() - t1

    def updateSkinWeights(self, filePath):
        root = xml.etree.ElementTree.parse(filePath).getroot()
        for atype in root.findall('headerInfo'):
            self.fileName = atype.get('fileName')

        for atype in root.findall('weights'):
            jnt = atype.get('source')
            shape = atype.get('shape')
            skinClust = atype.get('deformer')
            if shape not in list(self.skinShapes.keys()):
                self.skinShapes[shape] = self.hyperSkinDeformer(shape=shape, skin=skinClust, jointList=[jnt])
            else:
                s = self.skinShapes[shape]
                s.joints.append(jnt)

HyperSkin = as_HyperSkinMain()