import maya.cmds as cmds
import maya.mel as mel
import TimberBeast_v2.LWS_TimberBeast_v2_controls as controls
#import TimberBeast_v2.LWS_TimberBeast_v2_utils as utils
#reload(utils)



##################################################
##################################################
##################################################
#
# Simple Utils
#
##################################################
##################################################
##################################################
'''
Simple utils for using multiple native commands faster
'''

def snapPivot(target,object):
    piv = cmds.xform (target, piv=True, q=True, ws=True) 
    cmds.xform(object, ws=True, piv=(piv[0], piv[1], piv[2]) ) 
    
def snap(parent,child):
    cmds.parentConstraint(parent,child,n='pCon',mo=0)
    cmds.delete('pCon')
    
def snapPoint(parent,child):
    cmds.pointConstraint(parent,child,n='pCon',mo=0)
    cmds.delete('pCon')
    
def snapOrient(parent,child):
    cmds.orientConstraint(parent,child,n='pCon',mo=0)
    cmds.delete('pCon')
    
def snapScale(parent,child):
    cmds.scaleConstraint(parent,child,n='sCon')
    cmds.delete('sCon')
    cmds.parentConstraint(parent,child,n='pCon')
    cmds.delete('pCon')
    
def snapScaleOnly(parent,child):
    cmds.scaleConstraint(parent,child,n='sCon')
    cmds.delete('sCon')
    
def freeze(obj=''):
    if obj == '' :
        obj = cmds.ls(sl=1)
    cmds.select(obj)
    cmds.makeIdentity(apply=1)

def hold(parent, child) :
    cmds.parentConstraint(parent,child,mo=1)
    cmds.scaleConstraint(parent,child,mo=1)
    
def grpPiv(control):
    group = cmds.group(control, n = 'grp' + control)
    snapPivot(control, group)
    return group
    
def selectBind(self):
    nameSpace = self.NameSpace.text()
    if nameSpace == 'NameSpace' : 
        nameSpace = ''
        
    pfx = nameSpace + 'skn'
    newList = []
    fullList = cmds.ls(type='joint')

    for item in fullList:
       if item.startswith(pfx ):
           newList.append(item)

    cmds.select(newList)
    
    
def orientJoints(joints, side = '',secondaryAxis = True ) :
    
    for joint in joints :
        cmds.select(joint)
        if secondaryAxis == True :
            mel.eval('joint -e  -oj xzy -secondaryAxisOrient zup -ch -zso;')
        else:
            mel.eval('joint -e  -oj xzy -ch -zso;')



##################################################
##################################################
##################################################
#
# Safety Utils
#
##################################################
##################################################
##################################################
'''
Check for items and run other safty precautions
'''
def checkDuplicate(obj) :
    if cmds.objExists(obj) == True :
        return True
    else :
        
        return False


###############
###############

#   ATTR LOCK

###############
###############

def lockAttr(list, vis = False, translate = False, rotate = False, scale = False) :
    
    for item in list :

        if translate == True :
            cmds.setAttr(item + '.tx', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.ty', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.tz', lock = True, keyable = False, channelBox = False)


        if rotate == True :
            cmds.setAttr(item + '.rx', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.ry', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.rz', lock = True, keyable = False, channelBox = False)


        if scale == True :
            cmds.setAttr(item + '.sx', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.sy', lock = True, keyable = False, channelBox = False)
            cmds.setAttr(item + '.sz', lock = True, keyable = False, channelBox = False)
            
        if vis == True :
            cmds.setAttr(item + '.v', lock = True, keyable = False, channelBox = False)


        






##################################################
##################################################
##################################################
#
# Joint Building Utils
#
##################################################
##################################################
##################################################

'''
Comments : a range of functions to build joints, joint chains, and add joints to scenes quickly
'''
##################################################
#
# Add Joints to lists, selection, and other generals 
#
##################################################


        
def joints2List(list, nameSpace, obj, side, pfx = '', chain = True,deleteEnd = False, grp = True,secondaryAxis = True) :

    
    cmds.select(clear = 1)
    count = 01
    joints = []
    for item in list :
        if chain == False :
            cmds.select(clear = 1)
            
        if count < 10 :
            zero = '0'
        else:
            zero = ''
                        
        joint = cmds.joint(n = nameSpace + pfx + obj + zero + str(count) + side)
        snapPoint(item, joint)
        count = count + 1
        joints.append(joint)

    cmds.select(joints[-1])
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
    orientJoints(joints, side,secondaryAxis)
    snapOrient(joints[-2],joints[-1])
    
    if grp == True :
        grp = cmds.group(joints[0], n = nameSpace + 'grp' + pfx + obj + side)
        snapPivot(joints[0],grp)

    if deleteEnd == True:
        cmds.delete(joints[-1])
        joints = joints[:-1]
    return joints


def joints2Ribbon(nameSpace, obj, side, jnum, pfx = '', parent = '', reverse = False) :
    
    
    plane = nameSpace + 'nrb_' + obj + side + 'Plane'

    cmds.select(plane)
    mel.eval('createHair ' + str(jnum) + ' 1 10 0 0 0 0 5 0 1 1 1;')

    cmds.delete('hairSystem1','nucleus1','pfxHair1')
    exCurves =  pfx_ControlList(pfx = 'curve')
    cmds.delete(exCurves)

    grp = cmds.rename('hairSystem1Follicles', nameSpace + obj + '_follicle' + side)


    count = 1
    list =  pfx_ControlList(pfx = nameSpace + 'nrb_' + obj + 'PlaneFollicle')
    if reverse == True :
        list.reverse()
        
    ribJoints = joints2List(nameSpace = nameSpace, list = list,  obj = 'skn_' + obj, side  = side, chain = True,deleteEnd = False, grp = False)    

    for item in ribJoints :
        itemIndex = ribJoints.index(item)
        cmds.parent(item, list[itemIndex])
    
        cmds.setAttr(item + '.tx', 0)
        cmds.setAttr(item + '.ty', 0)
        cmds.setAttr(item + '.tz', 0)
        
    list =  pfx_ControlList(pfx = plane) 
    string = 'Follicle'

    newList = []
    for item in list :
        if item[-12:-4] == string :
            
            newList.append(item)

    for item in newList :
        cmds.setAttr(item[:-12] + string + 'Shape' + item[-4:] + '.lodVisibility', 0 )
    

    cmds.select(ribJoints[-1])
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
    orientJoints(ribJoints, side)

    
    try: 
        cmds.parent(grp, nameSpace + 'grpEX')
    except:
        pass
        
    return grp
        
        

def splineJoints2Curve(nameSpace, obj, jnum, pfx = '', side = '') :
    count = 1
    crv = nameSpace + 'crv_' + obj    
    cmds.select(crv)
    cmds.DeleteHistory()
    cmds.rebuildCurve( rt=0, s=jnum )
        
    #selects the cv's of the curve
    mel.eval('select -r ' + crv + '.cv[0:100] ;')
    list = cmds.filterExpand(sm=28)
    
    cmds.select(cl=1)
    joints = []
    for cv in list :
            if cv == list[1] :
                pass
            elif cv == list[-2] :
                pass
                
            else:
                pos = cmds.pointPosition(cv)
                joint = cmds.joint(n =  nameSpace + pfx + obj + str(count) + '_IK', p=pos)
                count = count + 1
                joints.append(joint)
    
    grp = cmds.group(joints[0], n = nameSpace + 'grp' + pfx + obj)
    snapPivot(joints[0], grp)
         
            
    cmds.select(joints[-1])
    mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
    orientJoints(joints, side)    
    snapOrient(joints[-2],joints[-1])
    return joints
        
        
##################################################
#
# Spine Building Utils
#
##################################################
'''
Comments: 
    
    spineType Options:
        1 = Creates an IK Spline with the pfx 'skn_'. Intended to be used alone to build an IK spline that will be skinned to the geo
        2 = Creates an IK Spline with the pfx 'ik_'. Intended to be used with an FK pair and final result chain
        
        
for FK: joint2Curve(nameSpace, obj = obj, crv = crv, pfx = 'fk_', partName = 'FK',  parent = nameSpace + 'grp' + obj + 'Joints', skipEnds = True, chain = True)

'''
def IKSpline(nameSpace, obj, crv, spineType = 1, baseControls = True, ring = False ) :
    
    
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    
    if spineType == 1:
        pfx = 'skn_'
    elif spineType == 2:
        pfx = 'ik_'
        
    cmds.select(crv)
    cmds.DeleteHistory()
    joint2Curve(nameSpace, obj = obj, crv = crv, pfx = pfx, partName = '_IK',  parent = grpJoints, skipEnds = True, chain = True)
    
    chainIK = pfx_JointList(pfx = nameSpace + pfx + obj)
    
    cmds.select(chainIK[0],chainIK[-1])
    handle = cmds.ikHandle(n= nameSpace + obj + 'IKHandle', sol='ikSplineSolver', c = crv, ccv = False)[0]

    cmds.group(nameSpace + pfx + obj + '_IK01', n =  nameSpace + 'grp' + obj + pfx)
    grpObjEX = cmds.group(crv, handle, n = nameSpace + 'grp' + obj + 'EX')
    cmds.parent(grpObjEX, grpEx)
    
    top = controls.box(nameSpace + obj + 'Top', color = 17)
    topGrp = cmds.group(top, n = nameSpace + 'grp' +  obj + 'Top')
    cmds.setAttr(top + '.sx', 3)  
    cmds.setAttr(top + '.sy', 3)  
    cmds.setAttr(top + '.sz', 3)  
    snap(chainIK[-2], topGrp)
    snapPoint(chainIK[-1], topGrp)
    freeze(top)
    
    mid = controls.ring(nameSpace + obj + 'Mid', size = 2, color = 17)
    midGrp = cmds.group(mid, n = nameSpace + 'grp' +  obj + 'Mid')
    cmds.setAttr(mid + '.rz', -90)  
    snap(chainIK[-2], midGrp)
    freeze(mid)


    if ring == True :
        bottom = controls.fatArc180(nameSpace + obj + 'Bottom', color = 17)
        bottomGrp = cmds.group(bottom, n = nameSpace + 'grp' +  obj + 'Bottom')
        mel.eval('move -r 0 -2.0 0 '+ bottom + '.scalePivot '+ bottom + '.rotatePivot ;')
        snapPivot(bottom,bottomGrp)
        cmds.setAttr(bottom + '.rx', -90)  
        
    else :
        bottom = controls.box(nameSpace + obj + 'Bottom', color = 17)
        bottomGrp = cmds.group(bottom, n = nameSpace + 'grp' +  obj + 'Bottom')
        cmds.setAttr(bottom + '.sx', 3)  
        cmds.setAttr(bottom + '.sy', 3)  
        cmds.setAttr(bottom + '.sz', 3)  
        
    snap(chainIK[0], bottomGrp)
    freeze(bottom)
    
    #IK infulence joints
    cmds.select(cl=1)
    inf1 = cmds.joint(n = nameSpace + 'inf_' + obj + 'IK1')
    cmds.select(cl=1)
    inf2 = cmds.joint(n = nameSpace + 'inf_' + obj + 'IK2')
    cmds.select(cl=1)
    inf3 = cmds.joint(n = nameSpace + 'inf_' + obj + 'IK3')
    
    snap(chainIK[0], inf1)
    snap(chainIK[-1], inf3)
    cmds.pointConstraint(inf1,inf3, inf2, n = 'pCon')
    cmds.delete('pCon')
    grpInf = cmds.group(inf1,inf3, inf2, n = nameSpace + obj + 'InfleunceIK')
    
    spineJoints = cmds.group(grpInf, n = nameSpace + 'grp' + obj + 'Joints')
    
    cmds.select(inf1,inf3, inf2,crv)
    cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )

    cmds.parentConstraint(top, inf3, mo = 1)
    snapPoint(inf2, midGrp)
    freeze(mid)
    cmds.parentConstraint(mid, inf2, mo = 1)
    cmds.parentConstraint(bottom, inf1, mo = 1)
    
    midLoc = cmds.spaceLocator(n = nameSpace + obj + 'MidConnect_Loc')[0]
    snap(mid,midLoc)
    freeze(midLoc)
    cmds.parent(midGrp,midLoc)
    cmds.parentConstraint(top, bottom, midLoc, mo = 1)
    
    
    #Ik Squash and Stretch
    len = cmds.createNode('curveInfo', n = nameSpace + obj + 'Len')
    cmds.connectAttr( crv + '.worldSpace[0]', len + '.inputCurve',force=True,)

    MD = cmds.createNode('multiplyDivide',n=nameSpace + obj + 'Math')
    cmds.connectAttr(len + '.arcLength', MD + '.input1X',force=True)

    lenNumb = cmds.arclen(crv)
    cmds.setAttr(MD + '.input2X',lenNumb)
    cmds.setAttr(MD + '.operation', 2)

    MD2 = cmds.createNode('multiplyDivide',n=nameSpace + obj +'Math2')
    cmds.setAttr(MD2 + '.operation', 3)
    cmds.connectAttr(MD + '.outputX', MD2 + '.input1X', force=True)
    cmds.setAttr(MD2 + '.input2X', .5)

    invert = cmds.createNode('multiplyDivide',n=nameSpace + obj + 'MathInvert')
    cmds.connectAttr(MD2 + '.outputX',invert + '.input2X', force=True)
    cmds.setAttr( invert + '.operation', 2)
    cmds.setAttr(invert + '.input1X', 1)
    
    
    for item in chainIK:
        if item != chainIK[-1]:
            cmds.connectAttr(MD + '.outputX', '%s.scaleX' % item,force=True)
            cmds.connectAttr(invert + '.outputX', '%s.scaleZ' % item,force=True)
            cmds.connectAttr(invert + '.outputX', '%s.scaleY' % item,force=True)
            
    grpIKControls = cmds.group(topGrp, midLoc, bottomGrp, n = nameSpace + 'grp' + obj + 'ControlsIK')

    if baseControls == True:
        main = controls.ring(nameSpace + obj, size = 4, color = 15)
        cmds.setAttr(main + '.rz', 90)
        freeze(main)
        snap(bottom, main)
        secondary = controls.ring(nameSpace + obj + 'Sub', size = 3.5, color = 18)
        cmds.setAttr(secondary + '.rz', 90)
        freeze(secondary)
        snap(bottom, secondary)
        
        cmds.parent(secondary, main)
        freeze(main)
        freeze(secondary)
           
        cmds.parent(grpIKControls, secondary)
        cmds.parent(nameSpace + 'grp' + obj + 'Joints',nameSpace + 'grp' + obj + 'Joints_IK', secondary)



    rollSub = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_RollSubtract')
    cmds.setAttr(rollSub + '.operation', 1)

    
    cmds.connectAttr(top + '.rx', rollSub + '.input1D[0]')
    reverseAttr(bottom + '.rx', rollSub + '.input1D[1]')
    cmds.connectAttr(rollSub + '.output1D', handle + '.twist')
    cmds.connectAttr(bottom + '.rx', handle + '.roll')
    
    
    
    if cmds.objExists(character) :
        try:
            cmds.parent(main, character)
        except:
            pass
        normalizeSpline(obj,output = len,outputAttr = '.arcLength',influence = character ,input = MD,inputAttr = '.input1X',normalizeAttr = '.sy',multipleAttrs = False)

    cmds.setAttr(midLoc + 'Shape.lodVisibility', 0)
    cmds.setAttr(handle + '.v', 0)
    cmds.setAttr(crv + '.v', 0)
    
    

def FKChain(nameSpace, obj, crv, side = '', spineType = 1, jnum = 5,controlType = 1, rebuildCvr = True ) :
    
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    
    if spineType == 1:
        pfx = 'skn_'
    elif spineType == 2:
        pfx = 'fk_'
        
    cmds.select(crv)
    cmds.DeleteHistory()
    if rebuildCvr == True:
        cmds.rebuildCurve( rt=0, s=jnum )

    grp = joint2Curve(nameSpace, obj = obj, crv = crv, pfx = pfx, partName = '_FK',  parent = grpJoints, skipEnds = True, chain = True)
    
    chainFK = pfx_JointList(pfx = nameSpace + pfx + obj)
    
    if controlType == 1:
        buildFKControlChain(nameSpace, obj, side, size = 2, list = chainFK, direction = 1)
    else:
        buildFKControlChainRing(nameSpace, obj, side, size = 2, list = chainFK, direction = 1)

    cmds.parent(nameSpace + 'grp' + obj + 'FK_1', nameSpace + 'grp' + obj + 'Joints_FK')


        
def listBlender(nameSpace, obj, list1, list2, list3 = '', switch = '', skipEndScale = False, parent = '') :
    '''
    list1 and list 2 are the action lists. List3 is the result list
    '''
    if parent == '':
        parent = obj
        
    if list3 != '' :
        blendListRotate = []
        for item in list1 :
            index = list1.index(item)
            blend = cmds.createNode('blendColors', n = nameSpace + obj + 'Blend_Rotate')
            cmds.connectAttr(item + '.r', blend + '.color1')
            cmds.connectAttr(list2[index] + '.r', blend + '.color2')
            cmds.connectAttr(blend + '.output', list3[index] + '.r', f = 1)
            blendListRotate.append(blend)
            cmds.setAttr(item + '.v', 0)
            cmds.setAttr(list2[index] + '.v', 0)
        blendListTranslate = []
        for item in list1 :
            index = list1.index(item)
            blend = cmds.createNode('blendColors', n = nameSpace + obj + 'Blend_Translate')
            cmds.connectAttr(item + '.t', blend + '.color1')
            cmds.connectAttr(list2[index] + '.t', blend + '.color2')
            cmds.connectAttr(blend + '.output', list3[index] + '.t', f = 1)
            blendListTranslate.append(blend)
        if skipEndScale == True :
            list1 = list1[:-1]
        blendListScale = []
        for item in list1 :
            index = list1.index(item)
            blend = cmds.createNode('blendColors', n = nameSpace + obj + 'Blend_Scale')
            cmds.connectAttr(item + '.s', blend + '.color1')
            cmds.connectAttr(list2[index] + '.s', blend + '.color2')
            cmds.connectAttr(blend + '.output', list3[index] + '.s', f = 1)
            blendListScale.append(blend)
            
        try:
            cmds.addAttr( switch, ln  = parent + 'Switch', at =  'double', min = 0, max = 1, dv = 0)
            cmds.setAttr( switch + '.' + parent + 'Switch', e = True, keyable = True)
        except:
            pass
        for item in blendListRotate:
            cmds.connectAttr( switch + '.' + parent + 'Switch', item + '.blender')
        for item in blendListTranslate:
            cmds.connectAttr( switch + '.' + parent + 'Switch', item + '.blender')    
        for item in blendListScale:
            cmds.connectAttr( switch + '.' + parent + 'Switch', item + '.blender')
    else :
        for item in list1: 
            index = list1.index(item)
            cmds.connectAttr(item + '.r', list2[index] + '.r', f = 1)
            cmds.connectAttr(item + '.t', list2[index] + '.t', f = 1)
            cmds.connectAttr(item + '.s', list2[index] + '.s', f = 1)
        


##################################################
#
# Ribbon Building Utils
#
##################################################

def rigRibbon(nameSpace, obj, plane, side = '', jnum = 5, pivot = '', reverse = False) :
    if cmds.objExists(plane) == True :
        
        cmds.setAttr(plane + 'Shape.template', 0)
        
        if reverse == True:
            joints2Ribbon(nameSpace = nameSpace, obj = obj + side, side = '', jnum = jnum, pfx = 'skn_', parent = '', reverse = True)      
        else:    
            joints2Ribbon(nameSpace = nameSpace, obj = obj + side, side = '', jnum = jnum, pfx = 'skn_', parent = '', reverse = False)

        listSkn =  pfx_JointList(pfx = nameSpace + 'skn_' + obj + side)
        listRib = joints2List(listSkn, nameSpace, obj = 'rib_' + obj + side, side = '', chain = True)
        grpRib = nameSpace + 'grprib_' + obj + side 
        cmds.select(plane)
        cmds.DeleteHistory()

        cmds.rebuildSurface(rt=0, su=jnum, sv = 0 )
        for item in listRib :
            cmds.select(item, add = 1)
        cmds.select(plane, add = 1)     
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )


        for item in listRib :
            if item != listRib[0] :
                cmds.parent(item, w=1)
                cmds.parent(item, grpRib)


   
        #addcontrols
        grpControls = cmds.group(n = nameSpace + 'grp' + obj + side, em=1)
        count = 1
        index = 0
        conList = [] 




        for item in listRib :
            ball = controls.ball(nameSpace + 'min_' + obj + str(count) + side, size = .2)
            grp = cmds.group(ball, n = nameSpace + 'grp' + obj + str(count) + side)
            snap(item, grp)
            cmds.parent(item, ball)
            cmds.parent(grp, grpControls)
            cmds.setAttr(item + '.v', 0)
            count = count + 1
            conList.append(ball)
                
            #if item == listRib[-1]:
                #snapOrient(listRib[-2], grp)
            if pivot != '' :
                 snapPivot(pivot, ball)
                 
            cmds.scaleConstraint(ball, listSkn[index],mo=1)
            index = index + 1
            
            
            
                    
        cmds.setAttr(plane + '.v', 0)
        cmds.delete(grpRib)
                
                
        cmds.select(plane)
        cmds.DeleteHistory()
            
        for item in listRib :
            cmds.select(item, add = 1)
        cmds.select(plane, add = 1)     
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )
            
        
    else :
        print 'Can\'t find ' + plane
    
    return conList




def majorRibbonControls(nameSpace, obj, side, nameList, conList, pivot = '', zeroControls = False) :
    
    
    grpConList = []
    for item in conList:
        grp = cmds.group(item, n = nameSpace + 'grpMaj' + obj + item[-3:])
        grpConList.append(grp)
        

    listLen = len(conList)
    listMid = (listLen / 2)
        
    positions = [grpConList[0], grpConList[listMid], grpConList[-1]]
    
    
    majorConList = []
    for item in positions :
        con = controls.square(nameSpace + obj + side)
        grp1 = cmds.group(con, n = nameSpace + 'grpMajControl_' + obj + item[-3:])

        snap(item,grp1)
        if item == positions[-1]:
            snapOrient(majorConList[-1],grp1)

        cmds.setAttr(con + '.rx', 90)
        freeze(con)
        if pivot != '' :
             snapPivot(pivot, con)


        if item == positions[0]:
            con = cmds.rename(nameSpace + obj + nameList[0] + side)
        elif item == positions[1]:
            con = cmds.rename(nameSpace + obj + nameList[1] + side)
        else :
            con = cmds.rename(nameSpace + obj + nameList[2] + side)
        
        nameLen = len(nameSpace)
        grp2 = cmds.group(grp1, n = nameSpace + 'grp' + con[nameLen:])
        
        if zeroControls == True:
            freeze(grp1)
            freeze(grp2)
            
        cmds.parentConstraint(con, item, mo=1)
        cmds.scaleConstraint(con, item, mo=1)
        
        majorConList.append(con)
    return majorConList
    





def joint2Curve(nameSpace, obj, crv, parent, pfx = 'jnt', partName = '', skipEnds = True, chain = False, side = '') :
    
    grp = cmds.group(n = nameSpace + 'grp' + obj + 'Joints' + partName, em = 1)
    cmds.parent(grp, parent)
    
    cmds.select(clear = 1)
    cmds.select( crv + '.cv[0:]', r= 1)
                  
    crv = cmds.ls(sl=True)[0]
    count = 01
    list = cmds.filterExpand(sm=28)
    jointList = []
    for cv in list:
        if skipEnds == True :
            if cv == list[1] :
                pass
            elif cv == list[-2] :
                pass
                
            else:
                
                pos = cmds.pointPosition(cv)
                cmds.select(cl=1)
                joint = cmds.joint(n= nameSpace + pfx + obj + partName + '0' + str(count), p=pos)
                cmds.parent(joint, grp)
            
                if chain == True:
                    if cv != list[0] :
                        parentCount = count -1 
                        cmds.parent(joint, joint[:-1] + str(parentCount))
                count = count + 1
                jointList.append(joint)
        else:
            
            pos = cmds.pointPosition(cv)
            cmds.select(cl=1)
            joint = cmds.joint(n= nameSpace + pfx + obj + partName + '0' + str(count), p=pos)
            cmds.parent(joint, grp)
        
            if chain == True:
                if cv != list[0] :
                    parentCount = count -1 
                    cmds.parent(joint, joint[:-1] + parentCount)
            count = count + 1
            jointList.append(joint)
        
    
    orientJoints(jointList, side)
    snapOrient(jointList[-2], jointList[-1])

    return grp

'''
Builds controls onto joints on curve from function above. Works based on a list: 'jpos'
'''


def joint2Curve_Controls(nameSpace, obj, jpos, parent, partName = '', rotations = True) :
       
     
    
    grp = cmds.group(n = nameSpace + 'grp' + obj + 'Controls' + partName, em = 1)
    if parent != '' :
        cmds.parent(grp, parent)
    count = 01
    for item in jpos: 

        pos = nameSpace + 'jnt' + obj + partName + '0' + str(count)
        
        control = controls.sphere(nameSpace + obj + partName + '0' + str(count),size = .3, color = '')
        snap(pos,control)
        freeze(control)
        cmds.parent(control, grp)
        
        if rotations == True :
            cmds.parentConstraint(control, pos, mo=1)
        else :
            cmds.pointConstraint(control, pos, mo=1)
            
        cmds.scaleConstraint(control, pos, mo=1)
        
        count = count + 1
        

    return grp


    
##################################################
#
# Simple Body Rig Utils
#
##################################################
'''
Builds simple rigs commonly used in body rigging
Takes a list of already built joints and turns them into something useful
'''

def addAttrList( target, attrList, range = [], dv = 0) :
    
    for item in attrList :
        if range != [] :
            cmds.addAttr(target, ln  =  item, at =  'double', max = range[0], min = range[1],dv = dv)
        else :
            cmds.addAttr(target, ln  =  item, at =  'double', dv = dv)
        cmds.setAttr(target + '.' + item, e = True, keyable = True)


def connectAttrList(driver, attrList, target) :
    
    for attr in attrList :
        index = attrList.index(attr)
        cmds.connectAttr(driver + '.' + attr, target[index], f = 1)


def connectAdjust(nameSpace,sknJoints, resultJoints, obj, side = '', switch = '', rotation = 'none') :
        
    count = 1
    chainAdj = []
    for item in sknJoints :
        index = sknJoints.index(item)
        control = controls.ring(nameSpace + obj + '_Adjust' + str(count) + side, size = 2, color = 31)
        if rotation == 'rx':
            cmds.setAttr(control + '.rx', 90)
        elif rotation =='rz' :
            cmds.setAttr(control + '.rz', 90)
        freeze(control)
        
        cGrp = cmds.group(control, n = nameSpace + 'grp' + obj + '_Adjust' + str(count) + side)
        snapPoint(item, cGrp)
        snapPivot(item, cGrp)
        cmds.parent(cGrp, resultJoints[index])


        jGrp = cmds.group(item, n = nameSpace + obj + 'grp' + obj + '_Result' + str(count) + side)
        snapPivot(item, jGrp)
        cmds.parent(jGrp, control)

        
        count = count + 1
        chainAdj.append(control)
        
    if switch == '':
        switch = obj
    try:
        cmds.addAttr(nameSpace + switch, ln  =  'SubControls', at =  'double', min = 0, max = 1, dv = 0)
        cmds.setAttr(nameSpace + switch + '.SubControls', e = True, keyable = True)
    except:
        pass
    for item in chainAdj :
        cmds.connectAttr(nameSpace + switch + '.SubControls', item + '.v')
        
        
        
####
# IK Section
####
'''
Handles all IK Limb based functions
Other IK chain functions not associated with limbs may be found elsewhere

'''


def buildIK(nameSpace, obj, side, list, pole = '', parent = '') :
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
   
    if side == 'RT':
        color = 6
    elif side == 'LF' :
        color = 13
    else :
        color = 30

    srtJoint =  list[0]
    midJoint =  list[1]
    endJoint =  list[2]
    handle = cmds.ikHandle(n= nameSpace + obj + '_IKHandle_' + side, sj = srtJoint, ee = endJoint,sol='ikRPsolver')[0]

    Len = cmds.createNode('curveInfo', n= nameSpace + obj + side + 'Len')

    srtPos = cmds.xform(srtJoint,q=1,t=1,ws=1)
    endPos = cmds.xform(endJoint,q=1,t=1,ws=1)
    distDem = cmds.distanceDimension(sp=srtPos,ep=endPos)

    srtLoc = cmds.rename('locator1', nameSpace + obj + '_Start_DistLoc_' + side)
    endLoc = cmds.rename('locator2',nameSpace + obj + '_End_DistLoc_' + side)
    dist = cmds.rename('distanceDimension1',nameSpace + 'distance_' + obj + side)

    if parent == '' :
        parent = controls.box(nameSpace + obj + 'IK' + side, color = color )
        grpPar = cmds.group(parent, n = nameSpace + 'grp' + obj + 'IK' + side)
        snap(endJoint, grpPar)
        '''
        if obj == 'Arm':
            if side =='RT':
                try:
                    rzVal = cmds.getAttr(nameSpace + 'grpArmIK' + 'LF' + '.rz')
                    cmds.setAttr(grpPar + '.rz', rzVal/-1)
                except:
                    pass
        else:
            '''
        cmds.setAttr(grpPar + '.ry', 0)
        freeze(parent)
        
        
        
    cmds.connectAttr(parent + '.s', endJoint + '.s', f = 1)
    cmds.parent(endLoc,parent)
    cmds.parent(srtLoc,nameSpace + 'grp' + obj + '_IK' + side)
    cmds.parent(handle,parent)

    #measure bone length
    driver = nameSpace + 'distance_' + obj + side + 'Shape.distance'
    srtLen = cmds.getAttr(midJoint + '.tx')
    endLen = cmds.getAttr(endJoint + '.tx')
    limbLen = srtLen + endLen 
    mult = cmds.createNode('multiplyDivide', n = nameSpace + obj + 'IK_StretchMult')
    cond = cmds.createNode('condition', n = nameSpace + obj + 'IK_StretchCondition' + side)
    
    cmds.connectAttr(driver,mult + '.input1X', f = 1)
    cmds.connectAttr(driver,cond + '.firstTerm', f = 1)
    cmds.connectAttr(mult + '.outputX',cond + '.colorIfTrueR', f = 1)
    cmds.setAttr(mult + '.operation', 2)
    cmds.setAttr(cond + '.operation', 2)
    cmds.setAttr(mult + '.input2X', limbLen)
    cmds.setAttr(cond + '.secondTerm', limbLen)

    addUp = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddUp_' + side)
    addDn = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddDn_' + side) 
    cmds.connectAttr(cond + '.outColorR', addUp + '.input1D[0]',  f = 1)
    cmds.connectAttr(cond + '.outColorR', addDn + '.input1D[0]',  f = 1)
    cmds.connectAttr(addUp + '.output1D', srtJoint + '.sx', f = 1)
    cmds.connectAttr(addDn + '.output1D', midJoint + '.sx', f = 1)

    
    
    #hide extra junk
    cmds.setAttr (srtLoc + '.visibility', 0)
    cmds.setAttr (endLoc + '.visibility', 0)
    cmds.setAttr (dist + '.visibility', 0)
    cmds.setAttr (handle + '.visibility', 0)
    
    grp = cmds.group(dist, n = nameSpace + 'grp' + obj + 'Distance')

    if cmds.objExists(nameSpace + 'grpEX') == True :
        cmds.parent(grp, nameSpace + 'grpEX')

    if pole != '' :
        cmds.poleVectorConstraint(pole, handle)
        cmds.parent(pole, parent)
            
    #scale on Y + Z
    cmds.addAttr(parent, ln  =  'Up_ScaleX', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Up_ScaleX', e = True, keyable = True)
    cmds.addAttr(parent, ln  =  'Up_ScaleY', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Up_ScaleY', e = True, keyable = True)
    cmds.addAttr(parent, ln  =  'Up_ScaleZ', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Up_ScaleZ', e = True, keyable = True)

    cmds.addAttr(parent, ln  =  'Dn_ScaleX', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Dn_ScaleX', e = True, keyable = True)
    cmds.addAttr(parent, ln  =  'Dn_ScaleY', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Dn_ScaleY', e = True, keyable = True)
    cmds.addAttr(parent, ln  =  'Dn_ScaleZ', at =  'double', dv = 0)
    cmds.setAttr(parent + '.Dn_ScaleZ', e = True, keyable = True)

    cmds.connectAttr(parent + '.Up_ScaleX', addUp + '.input1D[1]', f = 1)
    cmds.connectAttr(parent + '.Dn_ScaleX', addDn + '.input1D[1]', f = 1)
    
    
    addUpY = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddUpY_' + side)
    addUpZ = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddUpZ_' + side)
    addDnY = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddDnY_' + side)
    addDnZ = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddDnZ_' + side)


    cmds.connectAttr(parent + '.Up_ScaleY', addUpY + '.input1D[1]', f = 1)
    cmds.connectAttr(parent + '.Up_ScaleZ', addUpZ + '.input1D[1]', f = 1)
    cmds.connectAttr(parent + '.Dn_ScaleY', addDnY + '.input1D[1]', f = 1)
    cmds.connectAttr(parent + '.Dn_ScaleZ', addDnZ + '.input1D[1]', f = 1)
    
    cmds.connectAttr( addUpY + '.output1D', srtJoint + '.sy',f = 1)
    cmds.connectAttr( addUpZ + '.output1D', srtJoint + '.sz',f = 1)
    cmds.connectAttr( addDnY + '.output1D', midJoint + '.sy', f = 1)
    cmds.connectAttr( addDnZ + '.output1D', midJoint + '.sz', f = 1)
    
    cmds.setAttr(addUpY + '.input1D[0]', 1)
    cmds.setAttr(addUpZ + '.input1D[0]', 1)
    cmds.setAttr(addDnY + '.input1D[0]', 1)
    cmds.setAttr(addDnZ + '.input1D[0]', 1)

    try:
        normalizeSpline(obj = nameSpace + obj + 'Up' + side,output = dist,outputAttr = '.distance',influence = character,input = cond,inputAttr = '.firstTerm',normalizeAttr = '.sy')
        cmds.connectAttr(nameSpace + obj + 'Up' + side + 'Normailze_MD.outputX', mult + '.input1X', f = 1)
    except :
        print obj + side + ' can not find character node. Please build one and normailze your IK\'s'
    
    orient = cmds.orientConstraint(parent, endJoint, mo = 1)[0]
    cmds.setAttr(orient + '.interpType', 0)
    if obj == 'Leg' :
        cmds.setAttr(orient + '.offsetZ', -90)

    
    
    
    return [addUp, addDn]
    
    
 
    
    
    
def noFlipIK_PoleVector(nameSpace, pv, side,parent, obj) :

    if side == 'RT':
        color = 6
    elif side == 'LF' :
        color = 13
    else :
        color = 30

    ik = nameSpace + obj + 'IK' + side
    handle = nameSpace + obj + '_IKHandle_' + side

    ball = controls.ball(name = nameSpace + obj + 'Pole' + side, size = .4, color = color)
    snap(pv, ball)
    freeze(ball)
    cmds.poleVectorConstraint(ball, handle)
    cmds.parent(ball, cmds.listRelatives(pv, parent = True))
    freeze(ball)
    cmds.parent(pv, ball)

    loc = cmds.spaceLocator(n = nameSpace + obj + 'NonFlip_loc' + side)[0]
    snap(parent, loc)
    cmds.pointConstraint(parent, loc)
    cmds.aimConstraint(ik, loc, mo = 1, weight = 1, aimVector = [0,-1, 0], worldUpType = 'vector',worldUpVector = [0, 1, 0])
    grp = cmds.group(ball, n = nameSpace + 'grp' + obj + 'PoleVecor' + side)
    snapPivot(parent, grp)
    cmds.parentConstraint(loc, grp, mo = 1)
        
    cmds.setAttr(pv + '.v', 1)
    cmds.setAttr(loc + '.v', 0)
    cmds.setAttr(handle + '.v', 0)
    cmds.setAttr(pv + 'Shape.lodVisibility', 0)

    #addTwist
    cmds.addAttr(ik, ln  =  'Twist', at =  'double', dv = 0)
    cmds.setAttr(ik + '.Twist', e = True, keyable = True)
    if side =='LF':
        cmds.connectAttr(ik + '.Twist', handle + '.twist', f = 1)
    elif side == 'RT' :
        reverseAttr(ik + '.Twist', handle + '.twist')
   
    #templeted curve to show obj connection
    curve = cmds.curve(n=nameSpace + 'crv_templetCurve_' + pv , ep=[(0,0,0),(0,0,4)])
    cmds.select(cl=1)
    joint1 = cmds.joint(n = nameSpace + pv + '_templetCurveJoint1' + side)
    cmds.select(cl=1)
    joint2 = cmds.joint(n = nameSpace + pv + '_templetCurveJoint2' + side)
    cmds.setAttr(joint2 + '.tz', 4)
    
    cmds.select(curve, joint1, joint2)
    cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )
    snap(pv, joint2)
    snap(pv, joint1)
    snapPoint(nameSpace + 'res_' + obj + '_Result02' + side ,joint1)
    cmds.parent(joint1, nameSpace + 'res_' + obj + '_Result02' + side)
    cmds.parent(joint2,ball)
    cmds.aimConstraint(joint2, joint1, mo =1)
    cmds.aimConstraint(nameSpace + obj + '_IK02' + side,joint2, mo =1)
    cmds.setAttr(curve +'.template', 1)
    cmds.parent(curve, nameSpace + 'grpEX')
    grpCurve = cmds.group(loc,n = nameSpace + 'grp' + obj + 'NonFlip_loc' + side)
    
    spaceSwitch(nameSpace,name = 'PV_', parentList = [nameSpace + 'Character', nameSpace + 'grpArmPoleVecor' + side,nameSpace + 'HipsIK', nameSpace + 'ChestIK'], child = ball, switch = ball, parentCount = 4,orientOnly = False, default = 1 )    
    
    cmds.parent(grp, w = 1)
    lockAttr([ball], vis = True, rotate = True, scale = True)
    
    return [joint1, joint2]
        
        
def poleSnap(nameSpace, obj, side,addNodes, pv, list, IKJoints) :


        
    srtJoint =  list[0]
    midJoint =  list[1]
    endJoint =  list[2]
    len = cmds.getAttr(nameSpace + obj + 'IK' + '_StretchMult.input1X') 

    srtPos = cmds.xform(srtJoint,q=1,t=1,ws=1)
    midPos = cmds.xform(midJoint,q=1,t=1,ws=1)
    endPos = cmds.xform(endJoint,q=1,t=1,ws=1)
    distDemUp = cmds.distanceDimension(sp=srtPos,ep=midPos)
    distDemDn = cmds.distanceDimension(sp=midPos,ep=endPos)

    distUp = cmds.rename('distanceDimension1',nameSpace + 'distance_UpSnap' + obj + side)
    distDn = cmds.rename('distanceDimension2',nameSpace + 'distance_DnSnap' + obj + side)
    multUp = cmds.createNode('multiplyDivide', n = nameSpace + obj + 'IK_StretchMult_Up')
    multDn = cmds.createNode('multiplyDivide', n = nameSpace + obj + 'IK_StretchMult_Dn')
    blendUp = cmds.createNode('blendColors', n = nameSpace + obj + 'IK_StretchBlend_Up')
    blendDn = cmds.createNode('blendColors', n = nameSpace + obj + 'IK_StretchBlend_Dn')
    
    cmds.connectAttr(distUp + 'Shape.distance', multUp + '.input1X', f =1)
    cmds.connectAttr(distDn + 'Shape.distance', multDn + '.input1X', f =1)
    
    cmds.connectAttr(multUp + '.outputX',blendUp + '.color1R', f =1)
    cmds.connectAttr(multDn + '.outputX',blendDn + '.color1R', f =1)
    
    cmds.connectAttr(nameSpace + obj + 'IK_StretchCondition' + side + '.outColorR',blendUp + '.color2R', f =1)
    cmds.connectAttr(nameSpace + obj + 'IK_StretchCondition' + side + '.outColorR',blendDn + '.color2R', f =1)  
    
    srtLen = cmds.getAttr(IKJoints[1] + '.tx')
    endLen = cmds.getAttr(IKJoints[2] + '.tx')
    limbLen = (srtLen + endLen)/2    
    cmds.setAttr(multUp +'.input2X', limbLen)
    cmds.setAttr(multDn +'.input2X', limbLen)
    cmds.connectAttr(blendUp + '.outputR', addNodes[0] + '.input1D[0]', f =1)
    cmds.connectAttr(blendDn + '.outputR', addNodes[1] + '.input1D[0]', f =1)
    cmds.setAttr(multUp + '.operation', 2)
    cmds.setAttr(multDn + '.operation', 2)

    cmds.addAttr(nameSpace + obj + 'IK' + side, ln  =  'Snap', at =  'double', max = 1, min = 0,dv = 0)
    cmds.setAttr(nameSpace + obj + 'IK' + side + '.Snap', e = True, keyable = True)
    cmds.connectAttr(nameSpace + obj + 'IK'  + side + '.Snap', blendUp + '.blender', f = 1)
    cmds.connectAttr(nameSpace + obj + 'IK'  + side + '.Snap', blendDn + '.blender', f = 1)
    
    cmds.select([distUp, distDn])
    hide()
    lockAttr(list = [distUp, distDn], vis = True)
    cmds.parent(distUp, distDn, nameSpace + 'grpEX')


''' 
Comment : poleSnap FK is not currently working. Once complete, this should be merged with the poleSnap above
'''
def poleSnapFK(nameSpace, obj, side,addNodes, pv, list, joints, rigType = 'FK') :
    

    srtJoint =  list[0]
    midJoint =  list[1]
    endJoint =  list[2]
    len = cmds.getAttr(nameSpace + obj + 'IK' + '_StretchMult.input1X') 

    srtPos = cmds.xform(srtJoint,q=1,t=1,ws=1)
    midPos = cmds.xform(midJoint,q=1,t=1,ws=1)
    endPos = cmds.xform(endJoint,q=1,t=1,ws=1)
    distDemUp = cmds.distanceDimension(sp=srtPos,ep=midPos)
    distDemDn = cmds.distanceDimension(sp=midPos,ep=endPos)

    distUp = cmds.rename('distanceDimension1',nameSpace + 'distance_UpSnap' + obj + rigType + side)
    distDn = cmds.rename('distanceDimension2',nameSpace + 'distance_DnSnap' + obj + rigType + side)
    multUp = cmds.createNode('multiplyDivide', n = nameSpace + obj + rigType + '_StretchMult_Up')
    multDn = cmds.createNode('multiplyDivide', n = nameSpace + obj + rigType + '_StretchMult_Dn')
    blendUp = cmds.createNode('blendColors', n = nameSpace + obj + rigType + '_StretchBlend_Up')
    blendDn = cmds.createNode('blendColors', n = nameSpace + obj + rigType + '_StretchBlend_Dn')
    
    cmds.connectAttr(distUp + 'Shape.distance', multUp + '.input1X', f =1)
    cmds.connectAttr(distDn + 'Shape.distance', multDn + '.input1X', f =1)
    
    cmds.connectAttr(multUp + '.outputX',blendUp + '.color1R', f =1)
    cmds.connectAttr(multDn + '.outputX',blendDn + '.color1R', f =1)
    
    if rigType == 'IK' :
        cmds.connectAttr(nameSpace + obj + 'IK_StretchCondition' + side + '.outColorR',blendUp + '.color2R', f =1)
        cmds.connectAttr(nameSpace + obj + 'IK_StretchCondition' + side + '.outColorR',blendDn + '.color2R', f =1)  
    elif rigType == 'FK' :
        cmds.connectAttr(nameSpace + obj + 'FK_1' + side + '.sx',blendUp + '.color2R', f =1)
        cmds.connectAttr(nameSpace + obj + 'FK_2' + side + '.sx',blendDn + '.color2R', f =1)  
        
        
    srtLen = cmds.getAttr(joints[1] + '.tx')
    endLen = cmds.getAttr(joints[2] + '.tx')
    limbLen = (srtLen + endLen)/2    
    cmds.setAttr(multUp +'.input2X', limbLen)
    cmds.setAttr(multDn +'.input2X', limbLen)
    if rigType == 'IK' :
        cmds.connectAttr(blendUp + '.outputR', addNodes[0] + '.input1D[0]', f =1)
        cmds.connectAttr(blendDn + '.outputR', addNodes[1] + '.input1D[0]', f =1)
    elif rigType == 'FK' :
        cmds.connectAttr(blendUp + '.outputR', joints[0] + '.sx', f =1)
        cmds.connectAttr(blendDn + '.outputR', joints[1] + '.sx', f =1)
            
    cmds.setAttr(multUp + '.operation', 2)
    cmds.setAttr(multDn + '.operation', 2)

    cmds.addAttr(nameSpace + obj + 'IK' + side, ln  =  'Snap', at =  'double', max = 1, min = 0,dv = 0)
    cmds.setAttr(nameSpace + obj + 'IK' + side + '.Snap', e = True, keyable = True)
    cmds.connectAttr(nameSpace + obj + 'IK'  + side + '.Snap', blendUp + '.blender', f = 1)
    cmds.connectAttr(nameSpace + obj + 'IK'  + side + '.Snap', blendDn + '.blender', f = 1)
    
    cmds.select([distUp, distDn])
    hide()
    lockAttr(list = [distUp, distDn], vis = True)
    cmds.parent(distUp, distDn, nameSpace + 'grpEX')
    
        

####
# FK Section
####
'''
Handles all FK Limb based functions
Other FK chain functions not associated with limbs may be found elsewhere
'''

def buildFKControlChainRing(nameSpace, obj, side, list,size = 1, direction = 1) :
    
    if side == 'RT':
        color = 6
    elif side == 'LF' :
        color = 13
    else :
        color = 30
    

    count = 01
    for item in list :
        ring = controls.ring(nameSpace + obj + 'FK_' + str(count) + side, color = color, size = size)
        if direction == 1:
            cmds.setAttr(ring + '.rz', 90)
        elif direction == 2:
            cmds.setAttr(ring + '.ry', 90)
        
        freeze(ring)
        grp = cmds.group(ring, n = nameSpace + 'grp' + obj + 'FK_' + str(count) + side)
        
        snap(item, grp)

        cmds.parentConstraint( ring,  item, mo = 1)
        cmds.connectAttr( ring + '.s',  item + '.s', f = 1)
            
        if item != list[0]:
            
            pCount = count - 1
            pCon = nameSpace + obj + 'FK_' + str(pCount) + side
            cmds.parent(grp, pCon)
                
        count = count + 1


        
        
        
def buildFKControlChain(nameSpace, obj, side, list,size = 1, direction = 1) :
    
    count = 01
    for item in list :
        ring = controls.fatArc180(nameSpace + obj + 'FK_' + str(count) + side, color = 17)
        mel.eval('move -r 0 -2.0 0 '+ ring + '.scalePivot '+ ring + '.rotatePivot ;')
        
        cmds.setAttr(ring + '.rx', -90)
        print 'fk control fat arc rotated'
  
        
        freeze(ring)
        grp = cmds.group(n = nameSpace + 'grp' + obj + 'FK_' + str(count))
     
        snapPivot(ring, grp)
        snap(item, grp)

        cmds.parentConstraint( ring, item, mo = 1)
        cmds.connectAttr( ring + '.s',  item + '.s', f = 1)
            
        if item != list[0]:
            
            pCount = count - 1
            pCon = nameSpace + obj + 'FK_' + str(pCount) + side
            cmds.parent(grp, pCon)

        count = count + 1


def addGimbal(nameSpace, list, side = '') :
    if side == 'RT':
        color = 6
    elif side == 'LF' :
        color = 13
    else :
        color = 30
        
    for item in list :
        nameLen = len(nameSpace)
        control = controls.ring(name = nameSpace + 'Gimbal_' + item[nameLen:], size = 1.4, color = color)
        cmds.setAttr(control + '.rz', 90)
        freeze(control)
        grp = cmds.group(n = nameSpace + 'grp' + 'Gimbal_' + item[nameLen:])
        snap(item, grp)
        
        parent = cmds.listRelatives(item, parent = True)
        parentParent = cmds.listRelatives(parent, parent = True)
        try: 
            cmds.parent(grp, parentParent) 
        except:
            pass
        cmds.parent(parent, control)
###





####
# IK/FK Switching Section
####

def IKFKSwitch(nameSpace, obj, side, IKJoints, FKJoints, resultJoints, switch = '', parent = '') :

    #IK Fk Switching
    if obj == 'Arm' :
        bendPoint = 'Elbow'
    else :
        bendPoint = 'Knee'
    
    if switch == '':
        switch = controls.pin(name = nameSpace + obj + 'Settings' + side, color = 9)
        grpSwitch = cmds.group(switch, n = nameSpace + 'grp' + obj + 'Settings' + side)
        snapPivot(switch,grpSwitch)
        snapPoint(IKJoints[-1],grpSwitch)
          

    listBlender(nameSpace, obj, list1 = FKJoints, list2 = IKJoints, list3 = resultJoints, switch = switch,skipEndScale = False, parent = parent)
    
    if obj in ['Arm','Leg'] :
        cmds.connectAttr(switch + '.' + obj + 'Switch', nameSpace + 'Gimbal_' + obj + 'FK_1' + side + '.v', f = 1)
        cmds.connectAttr(switch + '.' + obj + 'Switch', nameSpace + '' + obj + 'FK_2' + side + '.v', f = 1)
        
        cmds.setDrivenKeyframe (nameSpace + obj + 'IK' + side,cd=switch + '.' + obj + 'Switch',dv=1,attribute='.v',v=0) 
        cmds.setDrivenKeyframe (nameSpace + obj + 'IK' + side,cd=switch + '.' + obj + 'Switch',dv=0,attribute='.v',v=1) 
        cmds.setDrivenKeyframe (nameSpace + obj + 'Pole' + side,cd=switch + '.' + obj + 'Switch',dv=1,attribute='.v',v=0) 
        cmds.setDrivenKeyframe (nameSpace + obj + 'Pole' + side,cd=switch + '.' + obj + 'Switch',dv=0,attribute='.v',v=1)
        cmds.setDrivenKeyframe (nameSpace + 'crv_templetCurve_' + nameSpace + bendPoint + 'Pole_loc' + side,cd=switch + '.' + obj + 'Switch',dv=1,attribute='.v',v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'crv_templetCurve_' + nameSpace + bendPoint + 'Pole_loc' + side,cd=switch + '.' + obj + 'Switch',dv=0,attribute='.v',v=1)
        
        cmds.parent(grpSwitch, resultJoints[-1])
 
    else:
        pass
    
    lockAttr([switch], vis = True, scale = True, rotate = True, translate = True)

            
            

####
# Non-Roll Limb Setup
####
def nonRollLimb(nameSpace, side, obj, resultJoints, jnum = 4, axis = 'x') :
    character = nameSpace + 'Character'

    #twist joints and non-roll shoulder setup
    armUpChain = splineJoints2Curve(nameSpace, obj = obj + 'Up' + side, jnum = jnum, pfx = 'twist_')
    cmds.select(armUpChain[0],armUpChain[1])

    handle = cmds.ikHandle(n= nameSpace + obj + 'UpTwist_IKHandle' + side, sol='ikRPsolver')[0]
    cmds.parent(handle, resultJoints[0])
    cmds.setAttr(handle + '.poleVectorX', 0)
    cmds.setAttr(handle + '.poleVectorY', 0)
    cmds.setAttr(handle + '.poleVectorZ', 0)
    cmds.setAttr(handle + '.v', 0)

    twistLoc = cmds.spaceLocator(n = nameSpace + obj + side + 'Twist_loc')[0]
    twistGrp = cmds.group(twistLoc, n = nameSpace + 'grp' +  obj + side + 'Twist_loc')
    snap(armUpChain[-2],twistGrp,)
    snapPoint(armUpChain[-1],twistGrp)
    freeze(twistGrp)
    cmds.parent(twistGrp, armUpChain[0])
    if obj == 'Arm' :
        freeze(twistGrp)

    orientCon = controls.circleOrient(name = nameSpace + obj + 'Orient' + side,  color = 14)
    #if side == 'RT' :
        #cmds.setAttr(orientCon + '.sz', -1)
        #freeze(orientCon)
    
    orientLoc = cmds.spaceLocator(n = nameSpace + obj + 'Connect_loc_' + side)[0]
    cmds.parent(orientLoc, orientCon)
    orientGrp = cmds.group(orientCon, n = nameSpace + 'grp' + obj + side)
    snapPivot(orientCon,orientGrp)
    snap(armUpChain[0], orientGrp)
    lockAttr([orientCon], vis = True, scale = True)
    cmds.setAttr(orientCon + '.ry', lock = True, keyable = False, channelBox = False)
    cmds.setAttr(orientCon + '.rz', lock = True, keyable = False, channelBox = False)
        
        
    twistDiv = cmds.createNode('multiplyDivide', n = nameSpace + obj + side + 'Twist_Div')
    for item in armUpChain[1:]  :
        cmds.connectAttr(twistDiv + '.outputX',  item + '.rx', f = 1)

    cmds.setAttr(twistDiv + '.operation', 2) 
    cmds.setAttr(twistDiv + '.input2X', 4)
     
         
    elbLoc = cmds.spaceLocator(n = nameSpace + obj + side + 'Elbow_loc')[0]
    elbGrp = cmds.group(elbLoc, n = nameSpace + 'grp' +  obj + side + 'Elbow_loc')
    snap(armUpChain[-2],elbGrp,)
    snapPoint(armUpChain[-1],elbGrp)
    cmds.parent(elbGrp, resultJoints[-2])
    freeze(elbGrp)
    
    elbLocFwd = cmds.spaceLocator(n = nameSpace + obj + side + 'Elbow_locFwd')[0]
    elbGrpFwd = cmds.group(elbLocFwd, n = nameSpace + 'grp' +  obj + side + 'Elbow_locFwd')
    snap(armUpChain[-2],elbGrpFwd,)
    snapPoint(armUpChain[-1],elbGrpFwd)
    cmds.parent(elbGrpFwd, resultJoints[-2])
    freeze(elbGrpFwd)

    if axis == 'y' :
        cmds.setAttr(elbGrp + '.tz', 2)
        cmds.setAttr(elbGrpFwd + '.ty', 2)
        cmds.aimConstraint(elbLoc, twistLoc, mo = 1,weight = 1, aimVector = [0, 1, 0], upVector = [1, 0, 0],worldUpType = "object", worldUpVector = [0, 1, 0], worldUpObject = elbLocFwd)
        reverseAttr(twistLoc + '.ry', twistDiv + '.input1X')

    else :

        cmds.setAttr(elbGrp + '.ty', 2)
        cmds.setAttr(elbGrpFwd + '.tz', 2)
        cmds.aimConstraint(elbLoc, twistLoc, mo = 1,weight = 1, aimVector = [0, 1, 0], upVector = [0, 1, 0],worldUpType = "vector", worldUpVector = [0, 1, 0], worldUpObject = elbLocFwd)
        cmds.connectAttr(twistLoc + '.rx', twistDiv + '.input1X', f = 1)



    #wrist twisting 
    armDnChain = splineJoints2Curve(nameSpace, obj = obj + 'Dn' + side, jnum = jnum, pfx = 'twist_')
    cmds.parent(nameSpace + 'grptwist_' + obj + 'Dn' + side, nameSpace + 'res_' + obj + '_Result02' + side)
    cmds.select(armDnChain[0],armDnChain[1])

    handle = cmds.ikHandle(n= nameSpace + obj + 'DnTwist_IKHandle' + side, sol='ikRPsolver')[0]
    cmds.parent(handle, resultJoints[1])
    cmds.setAttr(handle + '.poleVectorX', 0)
    cmds.setAttr(handle + '.poleVectorY', 0)
    cmds.setAttr(handle + '.poleVectorZ', 0)
    cmds.setAttr(handle + '.v', 0)

    twistLocDn = cmds.spaceLocator(n = nameSpace + obj + side + 'DnTwist_loc')[0]
    twistGrpDn = cmds.group(twistLocDn, n = nameSpace + 'grp' +  obj + side + 'DnTwist_loc')
    snap(armDnChain[-2],twistGrpDn,)
    snapPoint(armDnChain[-1],twistGrpDn)
    cmds.parent(twistGrpDn, armDnChain[0])
    

    twistDivDn = cmds.createNode('multiplyDivide', n = nameSpace + obj + side + 'Twist_Div')
    cmds.connectAttr(twistLocDn + '.rx', twistDivDn + '.input1X', f = 1)
    for item in armDnChain[1:]  :
        cmds.connectAttr(twistDivDn + '.outputX',  item + '.rx', f = 1)

    cmds.setAttr(twistDivDn + '.operation', 2) 
    cmds.setAttr(twistDivDn + '.input2X', 4)
     
         
    wstLoc = cmds.spaceLocator(n = nameSpace + obj + side + 'Wrist_loc')[0]
    wstGrp = cmds.group(wstLoc, n = nameSpace + 'grp' +  obj + side + 'Wrist_loc')
    snap(twistLocDn,wstGrp,)
    snapPoint(armDnChain[-1],wstGrp)
    cmds.parent(wstGrp, resultJoints[-1])

    wstLocFwd = cmds.spaceLocator(n = nameSpace + obj + side + 'Wrist_locFwd')[0]
    wstGrpFwd = cmds.group(wstLocFwd, n = nameSpace + 'grp' +  obj + side + 'Wrist_locFwd')
    snap(twistLocDn,wstGrpFwd,)
    snapPoint(armDnChain[-1],wstGrpFwd)
    cmds.parent(wstGrpFwd, resultJoints[-1])
    
        
    if axis == 'y' :
        cmds.setAttr(wstGrp + '.tx', 2)
        cmds.setAttr(wstGrpFwd + '.tz', 2)
        cmds.aimConstraint(wstLoc, twistLocDn, mo = 1,weight = 1, aimVector = [0, 1, 0], upVector = [0, 0, 1],worldUpType = "object", worldUpVector = [0, 1, 0],worldUpObject = wstLocFwd)

    else :

        cmds.setAttr(wstGrp + '.ty', 2)
        cmds.setAttr(wstGrpFwd + '.tz', 2)
        cmds.aimConstraint(wstLoc, twistLocDn, mo = 1,weight = 1, aimVector = [0, 1, 0], upVector = [0, 0, 1],worldUpType = "object", worldUpVector = [0, 1, 0],worldUpObject = wstLocFwd )

    cmds.pointConstraint(resultJoints[1], armDnChain[0], mo =1)

    count = 1
    for item in armUpChain :
            normalizeSpline(obj = nameSpace + obj + 'UpTwist' + side + str(count),output = resultJoints[0],outputAttr = '.sx',influence = character,input = item,inputAttr = '.sx',normalizeAttr = '.sy')
            count = count + 1
    count = 1
    for item in armDnChain :
            normalizeSpline(obj = nameSpace + obj + 'DnTwist' + side+ str(count),output = resultJoints[1],outputAttr = '.sx',influence = character,input = item,inputAttr = '.sx',normalizeAttr = '.sy')
            count = count + 1

    cmds.orientConstraint(orientLoc, nameSpace + 'grptwist_' + obj + 'Up' + side, mo=1)

    
    cmds.select(twistLocDn, twistLoc, elbLoc, wstLoc, wstLocFwd, orientLoc, elbLocFwd)
    hide()
    
    return orientGrp

### 
#Limb Ribbon
###
def limbRibbon(nameSpace, obj, side, upChain, dnChain, reverse) :
       
    planeUp = nameSpace + 'nrb_' + obj + 'Up' + side + 'Plane'
    
    cmds.setAttr(planeUp + '.sx', lock = False, keyable = True, channelBox = False)
    
    conListUp = rigRibbon(nameSpace = nameSpace, obj = obj + 'Up', plane = planeUp, side = side, jnum = 5, reverse = reverse)
    grpForarmSkinnedUp = cmds.rename(nameSpace + 'grp' + obj + 'Up' + side, nameSpace + 'grp' + obj + 'Up' + side + '_Skinned')

    planeDn = nameSpace + 'nrb_' + obj + 'Dn' + side + 'Plane'
    cmds.setAttr(planeDn + '.sx', lock = False, keyable = True, channelBox = False)

    conListDn = rigRibbon(nameSpace = nameSpace, obj = obj + 'Dn', plane = planeDn, side = side, jnum = 5, reverse = reverse)
    grpForarmSkinnedDn = cmds.rename(nameSpace + 'grp' + obj + 'Dn' + side, nameSpace + 'grp' + obj + 'Dn' + side + '_Skinned')


    if side == 'LF' :
        for item in conListUp :
            cmds.setAttr(item + '.overrideColor', 31) 
        for item in conListDn :
            cmds.setAttr(item + '.overrideColor', 31) 
    else :
        for item in conListUp :
            cmds.setAttr(item + '.overrideColor', 29) 
        for item in conListDn :
            cmds.setAttr(item + '.overrideColor', 29) 


    for item in conListUp:
        index = conListUp.index(item)
        cmds.parent(cmds.listRelatives(item, p = 1), upChain[index])
        cmds.connectAttr(nameSpace + 'res_' + obj + '_Result01' + side + '.sx',  upChain[index] + '.sx', f = 1)
        cmds.connectAttr(nameSpace + 'res_' + obj + '_Result01' + side + '.sy',  upChain[index] + '.sy', f = 1)
        cmds.connectAttr(nameSpace + 'res_' + obj + '_Result01' + side+ '.sz',  upChain[index] + '.sz', f = 1)

    for item in conListDn:
        index = conListDn.index(item)
        cmds.parent(cmds.listRelatives(item, p = 1), dnChain[index])
        #cmds.connectAttr(nameSpace + 'res_' + obj + '_Result02' + side + '.sx',  dnChain[index] + '.sx',f = 1)
        #cmds.connectAttr(nameSpace + 'res_' + obj + '_Result02' + side + '.sy',  dnChain[index] + '.sy',f = 1)
        #cmds.connectAttr(nameSpace + 'res_' + obj + '_Result02' + side + '.sz',  dnChain[index] + '.sz',f = 1)
        mel.eval('CBdeleteConnection '+ dnChain[index] + '.sx'+ ';')
        mel.eval('CBdeleteConnection '+ dnChain[index] + '.sy'+ ';')
        mel.eval('CBdeleteConnection '+ dnChain[index] + '.sz'+ ';')
    cmds.delete(grpForarmSkinnedUp, grpForarmSkinnedDn)

##################################################
##################################################
##################################################
#
# Nameing  Utils
#
##################################################
##################################################
##################################################
'''
Utils for building replacate parts in mover mode. ie, fingers, toes, blah blah blah
'''

def moverRename_sfx(nameSpace, list, index, side):
    
    
    nameLength = len(nameSpace)  
    newIndex = nameLength + index
    
    if side == 'RT' :
        list.reverse()
        
    count = 01
    for item in list :
        cmds.rename(item, item[:newIndex] + '_Move' +  str(count) + side)
        
        count = count + 1
    


##################################################
##################################################
##################################################
#
# List Utils
#
##################################################
##################################################
##################################################
'''
Comment : Functions for populating lists and grabbing items based on names
'''

def pfx_JointList(pfx) :
    
    newList = []
    fullList = cmds.ls(type='joint')

    for item in fullList:
       if item.startswith(pfx):
           newList.append(item)
           
    return newList
    
def pfx_ControlList(pfx) :
    
    newList = []
    fullList = cmds.ls(type='transform')

    for item in fullList:
       if item.startswith(pfx):
           newList.append(item)
           
    return newList


def sfx_JointList(sfx) :
    
    newList = []
    fullList = cmds.ls(type='joint')

    for item in fullList:
       if item.endswith(sfx):
           newList.append(item)
           
    return newList
    
def sfx_ControlList(sfx) :
    
    newList = []
    fullList = cmds.ls(type='transform')

    for item in fullList:
       if item.endswith(sfx):
           newList.append(item)
           
    return newList    
##################################################
##################################################
##################################################
#
# Mover Utils
#
##################################################
##################################################
##################################################
'''
Utils for building replacate parts in mover mode. ie, fingers, toes, blah blah blah
'''

def adjustWoldSpace_RibbonSpline(obj, nameSpace, side, all) :
    
    cmds.delete(nameSpace + 'loc' + obj + side + 'Mid')
    joints =  getSkin(nameSpace + 'nrb_' + obj + side + 'Plane')
    cmds.select(nameSpace + 'nrb_' + obj + side + 'Plane')
    mel.eval('DeleteHistory;')
    
    freeze(all)

    cmds.select(clear = 1)
    cmds.select( joints, nameSpace + 'nrb_'  + obj + side + 'Plane')
    cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )


def multiJoint_Ribbon_Move(nameSpace, obj, jnum, height = '', color = '', size = '', controlType = 'ring', aim = False) :
    
    if height == '':
        height = 5

        
    world = nameSpace + 'World_Move'
    character = nameSpace + 'Character_Move'
    grpJoints = nameSpace + 'grpJoints_Move'
    grpEx = nameSpace + 'grpEX_Move'
        
        
    if  checkDuplicate( nameSpace + 'Character_Move') == False:
        print "Please build a character node first" 
        print "You're awesome"
    
    if  checkDuplicate( nameSpace + obj + 'Move') == False :

        if controlType == 'square' :
            base = controls.square(nameSpace + obj + 'Move', color = color)
        else :
            base = controls.ring(nameSpace + obj + 'Move', size = 3, color = color)
        crv = nameSpace + "crv_" + obj
        cmds.curve(n=crv, ep=[(0,0,0),(0,height,0)])

        cmds.rebuildCurve( rt=0, s=jnum -1 )

        cmds.parent(base, character)

        grpObjEX = cmds.group(n = nameSpace + 'grp_' + obj + 'EX', em = 1)
        cmds.parent(grpObjEX, grpEx)
        
        cmds.parent(crv,grpObjEX)

        # puts joints on curve
        joint2Curve(nameSpace, obj, crv, partName = '_Move', parent = grpJoints)
        jpos =  pfx_JointList(pfx = nameSpace + 'jnt' + obj + '_Move')
        joint2Curve_Controls(nameSpace, obj, jpos = jpos, partName = '_Move', parent = base)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv, add=1)
            
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )

        cmds.setAttr(crv + '.v',0)
        
        #locator for spine mid
        loc = cmds.spaceLocator(n= nameSpace + 'loc' + obj + 'Mid')[0]
        cmds.setAttr(loc + '.translateY',2.5)
        cmds.setAttr(loc + '.translateZ',-2)
        cmds.setAttr(loc + '.v',0)
        cmds.select(loc)
        cmds.makeIdentity(apply=1)
        if jnum > 4 :
            cmds.pointConstraint(jpos[1], jpos[3], loc, mo=1)
        cmds.parent(loc, base)

        #adds nurbs plane to setup for other spine options
        if height > 7 :
            add = height * .1
            plane = cmds.nurbsPlane(u = jnum, ax  = [0, 1, 0,], w = height + add, lr = .2, n = nameSpace + 'nrb_' + obj + 'Plane')[0]
            cmds.setAttr(plane + '.ty', height/2)

        else: 
            plane = cmds.nurbsPlane(u = jnum, ax  = [0, 1, 0,], w = height + 1, lr = .2, n = nameSpace + 'nrb_' + obj + 'Plane')[0]
            cmds.setAttr(plane + '.ty', 2.5)
    
        cmds.setAttr(plane + '.rx', 90)
        cmds.setAttr(plane + '.rz', 90)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(plane, add=1)
            
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )

        cmds.setAttr(plane + 'Shape.template', 1)
        cmds.parent(plane, grpObjEX)

            
            
        print obj + " Movers Built Successfully!"

    else:
        print "Duplcate item may exist"

def multiJoint_Ribbon_Move_Simple(nameSpace, obj, jnum, height = '') :
    
    if height == '':
        height = 5
        
    world = nameSpace + 'World_Move'
    character = nameSpace + 'Character_Move'
    grpJoints = nameSpace + 'grpJoints_Move'
    grpEx = nameSpace + 'grpEX_Move'
        
        
    if  checkDuplicate( nameSpace + 'Character_Move') == False:
        print "Please build a character node first" 
        print "You're awesome"
    
    if  checkDuplicate( nameSpace + obj + 'Move') == False :

    
        base = controls.ring(nameSpace + obj + 'Move', size = '3')
        crv = nameSpace + "crv_" + obj
        cmds.curve(n=crv, ep=[(0,0,0),(0,height,0)])

        cmds.parent(base, character)

        grpObjEX = cmds.group(n = nameSpace + 'grp_' + obj + 'EX', em = 1)
        cmds.parent(grpObjEX, grpEx)
        
        cmds.parent(crv,grpObjEX)

        # puts joints on curve
        joint2Curve(nameSpace, obj, crv, partName = '_Move', parent = grpJoints, skipEnds = True)
        jpos =  pfx_JointList(pfx = nameSpace + 'jnt' + obj + '_Move')
        joint2Curve_Controls(nameSpace, obj, jpos = jpos, partName = '_Move', parent = base, rotations = False)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv, add=1)
            
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )

        cmds.setAttr(crv + '.v',0)
        
        #locator for spine mid
        loc = cmds.spaceLocator(n= nameSpace + 'loc' + obj + 'Mid')[0]
        cmds.setAttr(loc + '.translateY',2.5)
        cmds.setAttr(loc + '.v',0)
        cmds.select(loc)
        cmds.makeIdentity(apply=1)
        cmds.pointConstraint(jpos[0], jpos[1], loc, mo=1)
        cmds.parent(loc, base)

        #adds nurbs plane to setup for other spine options
        if height > 7 :
            add = height * .1
            plane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = height + add, lr = .2, n = nameSpace + 'nrb_' + obj + 'Plane')[0]
            cmds.setAttr(plane + '.ty', height/2)

        else: 
            plane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = height + 1, lr = .2, n = nameSpace + 'nrb_' + obj + 'Plane')[0]
            cmds.setAttr(plane + '.ty', 2.5)
    
        cmds.setAttr(plane + '.rx', 90)
        cmds.setAttr(plane + '.rz', 90)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(plane, add=1)
            
        cmds.skinCluster(mi = 2,dr=1, bm = 0, sm = 0,wd = 0 )

        cmds.setAttr(plane + 'Shape.template', 1)
        cmds.parent(plane, grpObjEX)
        
        cmds.setAttr(jpos[0] + '.tz', .3)
        cmds.aimConstraint('jnt' + obj + '_Move01', jpos[1],mo = 1)
        cmds.aimConstraint('jnt' + obj + '_Move02', jpos[0],mo = 1)

        print obj + " Movers Built Successfully!"

    else:
        print "Duplcate item may exist"


def fingerMove(nameSpace, obj, side, numb, base, thumb = False):
    
    lastNumb = range(numb)[-1]
    firstNumb = range(numb)[0]

    posZ = .5


    for item in obj :
        if side == 'LF' :
            posX = 1 
        else :
            posX = -1
            
        main = controls.pin(nameSpace + item + 'Move' + side,  color = '')
        cmds.setAttr(main + '.rx', 90)
        cmds.setAttr(main + '.sx', .3)
        cmds.setAttr(main + '.sx', .3)
        cmds.setAttr(main + '.sx', .3)

        cmds.setAttr(main + '.tx', posX)
        cmds.setAttr(main + '.tz', posZ)

        if side == 'LF' :
                posX = posX + .3

        else :
                posX = posX + -.3
        
        freeze(main)

        for i in range(numb) :
            
            dig = controls.sphere(nameSpace + item + str(i) +  'Move' + side, size = .1, color = '')
           
                
            cmds.setAttr(dig + '.tx', posX)
            cmds.setAttr(dig + '.tz', posZ)

            if i == firstNumb :
                cmds.parent(dig, main)
                
            else :
                parent = i - 1
                
                cmds.parent(dig, nameSpace + item + str(parent) +  'Move' + side)
                
            if side == 'LF' :
                posX = posX + .3
            else :
                posX = posX + -.3
                
            if i == lastNumb:

                posZ = posZ + -.3

        cmds.parent(main, base)
        
        if thumb == True:
            if side == 'LF' :
                cmds.setAttr(main + '.tx', -1)
            else: 
                cmds.setAttr(main + '.tx', 1)

            freeze(main)


def thumbMove(nameSpace, obj, side, numb, base):
    
    '''
    obj = ['Thumb']
    
    '''


    lastNumb = range(numb)[-1]
    firstNumb = range(numb)[0]
    

    posZ = .5

    for item in obj :

        posX = 0 
        main = controls.pin(nameSpace + item + 'Move' + side, color = '')
        cmds.setAttr(main + '.rx', 90)
        cmds.setAttr(main + '.sx', .3)
        cmds.setAttr(main + '.sx', .3)
        cmds.setAttr(main + '.sx', .3)
        
        cmds.setAttr(main + '.tx', posX)
        cmds.setAttr(main + '.tz', posZ)
        
        if side == 'LF' :
            posX = posX + .3
        else :
            posX = posX + -.3
        

        for i in range(numb) :
            
            dig = controls.sphere(nameSpace + item + str(i) +  'Move' + side, size = .1, color = '')
           
                
            cmds.setAttr(dig + '.tx', posX)
            cmds.setAttr(dig + '.tz', posZ)

            if i == firstNumb :
                cmds.parent(dig, main)
                
            else :
                parent = i - 1
                
                cmds.parent(dig, nameSpace + item + str(parent) +  'Move' + side)
                
                    
                    
        freeze(main)
        
        cmds.parent(main, base)

def legMoveBuilder(nameSpace, side, obj) : 

    if obj == 'Arm' :
        bendPoint = 'Elbow'
        endItem = 'Wrist'
    else :
        bendPoint = 'Knee'
        endItem = 'Ankle'


    world = nameSpace + 'World_Move'
    character = nameSpace + 'Character_Move'
    grpJoints = nameSpace + 'grpJoints_Move'
    grpEx = nameSpace + 'grpEX_Move'

    all = controls.square(nameSpace + obj + '_Move' + side )

    cmds.setAttr(all + '.ty', 8)
    cmds.setAttr(all + '.tz', .5)


    cmds.parent(all, character)

    if side == 'LF' :

        crv_Up = nameSpace + 'crv_' + obj + 'Up' + side
        cmds.curve(n=crv_Up, ep=[(2,8,0),(2,4,.5)])

        crv_Dn = nameSpace + 'crv_' + obj + 'Dn' + side
        cmds.curve(n=crv_Dn, ep=[(2,4,.5),(2,0,0)])

        grpLimbEX = cmds.group(n = nameSpace + 'grp_' + obj + 'EX' + side, em = 1)
        cmds.parent(grpLimbEX, grpEx)

        cmds.setAttr(all + '.tx', 2.5)
        freeze(all)
        
    else :

        crv_Up = nameSpace + 'crv_' + obj + 'Up' + side
        cmds.curve(n=crv_Up, ep=[(-2,8,0),(-2,4,.5)])

        crv_Dn = nameSpace + 'crv_' + obj + 'Dn' + side
        cmds.curve(n=crv_Dn, ep=[(-2,4,.5),(-2,0,0)])
      
        grpLimbEX = cmds.group(n = nameSpace + 'grp_' + obj + 'EX' + side, em = 1)
        cmds.parent(grpLimbEX, grpEx)
        
        cmds.setAttr(all + '.tx', -1.5)
        freeze(all)
        
    cmds.parent(crv_Dn,crv_Up,grpLimbEX)





    joint2Curve(nameSpace, obj = 'Up' + obj , crv = crv_Up, partName = '_Move' + side, parent = grpJoints, skipEnds = True)
    jpos = pfx_JointList(pfx = nameSpace + 'jntUp' + obj + '_Move' + side)
    joint2Curve_Controls(nameSpace, obj = 'Up' + obj, jpos = jpos, partName = '_Move' + side, parent = all, rotations = False)

    cmds.select(cl=1)
    for item in jpos :
        cmds.select(item, add=1)
        cmds.setAttr(item + '.v',0)
        
    cmds.select(crv_Up, add=1)
        
    cmds.skinCluster(mi=1,dr=1)

    cmds.setAttr(crv_Up + '.v', 0)

    forlegPlane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = 4, lr = .1, n = nameSpace + 'nrb_' + obj + 'Up' + side + 'Plane')[0]
    cmds.setAttr(forlegPlane + '.ty', 6)
    cmds.setAttr(forlegPlane + '.tz', .25)
    cmds.setAttr(forlegPlane + '.rz', 90 )
    cmds.setAttr(forlegPlane + '.ry', 6.5 )
    cmds.setAttr(forlegPlane + '.rx', 90 )
    cmds.setAttr(forlegPlane + '.sx', -1.26 )

    if side == 'LF' :
        cmds.setAttr(forlegPlane + '.tx', 2)

    else :
        cmds.setAttr(forlegPlane + '.tx', -2)



    cmds.select(cl=1)
    for item in jpos :
        cmds.select(item, add=1)
        cmds.setAttr(item + '.v',0)
        
    cmds.select(forlegPlane, add=1)
        
    cmds.skinCluster(mi=1,dr=1)

    cmds.setAttr(forlegPlane + 'Shape.template', 1)
    cmds.parent(forlegPlane, grpLimbEX)



    joint2Curve(nameSpace, obj = 'Dn' + obj, crv = crv_Dn, partName = '_Move' + side, parent = grpJoints, skipEnds = True)
    jpos = pfx_JointList(pfx = nameSpace + 'jntDn' + obj + '_Move' + side)
    joint2Curve_Controls(nameSpace, obj = 'Dn' + obj , jpos = jpos, partName = '_Move' + side, parent = all, rotations = False)

    cmds.select(cl=1)
    for item in jpos :
        cmds.select(item, add=1)
        cmds.setAttr(item + '.v',0)
        
    cmds.select(crv_Dn, add=1)
        
    cmds.skinCluster(mi=1,dr=1)

    cmds.setAttr(crv_Dn + '.v', 0)

    LegUpPlane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = 4, lr = .1, n = nameSpace + 'nrb_' + obj + 'Dn' + side + 'Plane')[0]
    cmds.setAttr(LegUpPlane + '.ty', 2)
    cmds.setAttr(LegUpPlane + '.rz', 90 )
    cmds.setAttr(LegUpPlane + '.ry', -6.5 )
    cmds.setAttr(LegUpPlane + '.rx', 90 )
    cmds.setAttr(LegUpPlane + '.tz', .25 )
    cmds.setAttr(LegUpPlane + '.sx',- 1.26 )
    if side == 'LF' :
        cmds.setAttr(LegUpPlane + '.tx', 2)
    else: 
        cmds.setAttr(LegUpPlane + '.tx', -2)


    cmds.select(cl=1)
    for item in jpos :
        cmds.select(item, add=1)
        cmds.setAttr(item + '.v',0)
        
    cmds.select(LegUpPlane, add=1)
        
    cmds.skinCluster(mi=1,dr=1)

    cmds.setAttr(LegUpPlane + 'Shape.template', 1)
    cmds.parent(LegUpPlane, grpLimbEX)  


    cmds.parent(nameSpace + 'Up' + obj + '_Move' + side + '02', nameSpace + 'Dn' + obj + '_Move' + side + '01')
    cmds.setAttr(nameSpace + 'Up' + obj + '_Move' + side + '02.v', 0)

    ank = cmds.rename(nameSpace + 'Dn' + obj + '_Move' + side + '02',nameSpace + 'AnkleJpos' + side)
    knee = cmds.rename(nameSpace + 'Dn' + obj + '_Move' + side + '01',nameSpace + 'KneeJpos' + side)
    leg = cmds.rename(nameSpace + 'Up' + obj + '_Move' + side + '01',nameSpace + '' + obj + 'Jpos' + side)

    
    cmds.aimConstraint(knee,nameSpace + 'jntUp' + obj + '_Move' + side + '01',mo = 1,weight = 1, aimVector = [0, 0, 1], upVector = [0, 0, 1],worldUpType = "vector", worldUpVector = [0, 1, 1], skip = 'y')
    cmds.aimConstraint(knee,nameSpace + 'jntDn' + obj + '_Move' + side + '02',mo = 1,weight = 1, aimVector = [0, 0, 1], upVector = [0, 0, 1],worldUpType = "vector", worldUpVector = [0, 1, 0], skip = 'y')
    cmds.aimConstraint(ank,nameSpace + 'jntDn' + obj + '_Move' + side + '01',mo = 1,weight = 1, aimVector = [0, 0, 1], upVector = [0, 0, 1],worldUpType = "vector", worldUpVector = [0, 1, 0], skip = 'y')
    cmds.aimConstraint(leg,nameSpace + 'jntUp' + obj + '_Move' + side + '02',mo = 1,weight = 1, aimVector = [0, 0, 1], upVector = [0, 0, 1],worldUpType = "vector", worldUpVector = [0, 1, 0], skip = 'y')

    orGrp = cmds.group(nameSpace + 'jntUp' + obj + '_Move' + side + '01', n = nameSpace + 'grpUp' + obj + '_Move' + side + '01')
    snapPivot(leg,orGrp)
    cmds.orientConstraint(leg,orGrp)

    orGrp = cmds.group(nameSpace + 'jntUp' + obj + '_Move' + side + '02', n = nameSpace + 'grpUp' + obj + '_Move' + side + '02')
    snapPivot(knee,orGrp)
    cmds.orientConstraint(knee,orGrp)

    orGrp = cmds.group(nameSpace + 'jntDn' + obj + '_Move' + side + '01', n = nameSpace + 'grpDn' + obj + '_Move' + side + '01')
    snapPivot(knee,orGrp)
    cmds.orientConstraint(knee,orGrp)

    orGrp = cmds.group(nameSpace + 'jntDn' + obj + '_Move' + side + '02', n = nameSpace + 'grpDn' + obj + '_Move' + side + '02')
    snapPivot(ank,orGrp)
    cmds.orientConstraint(ank,orGrp)


    #creates pole vector for knee
    kneeLoc = cmds.spaceLocator(n=nameSpace + bendPoint + 'Pole_loc' + side)[0]
    cmds.setAttr( kneeLoc + '.ty',4)
    cmds.setAttr( kneeLoc + '.tz',10)
    cmds.makeIdentity(apply=1)
    
    cmds.parent(kneeLoc, knee)
    cmds.setAttr(kneeLoc +  '.visibility', 0)
    cmds.aimConstraint(leg,ank,knee,mo=1)




    arrow = controls.arrow(nameSpace + bendPoint + 'Arrow' + side, color = 31)
    snapPoint(knee, arrow)
    cmds.setAttr(arrow + '.template', 1)
    cmds.setAttr(arrow + '.rz', 90)
    cmds.parent(arrow, knee)
    

    anklePointerLoc = cmds.spaceLocator(n=nameSpace + endItem + 'Pointer' + side)[0]
    snap(ank, anklePointerLoc) 
    freeze(anklePointerLoc)
    if side == 'LF' :
        cmds.setAttr(anklePointerLoc + '.ty', -1)
        cmds.setAttr( kneeLoc + '.tx',2)

    else :
        cmds.setAttr(anklePointerLoc + '.ty', -1)
        cmds.setAttr( kneeLoc + '.tx',-2)

    cmds.parent(anklePointerLoc, ank) 
    cmds.setAttr(anklePointerLoc + '.v', 0)

    return all





##################################################
##################################################
##################################################
#
# Rigging Utils
#
##################################################
##################################################
##################################################
'''
Utils for adding rigging to system and builting some custom rigged parts
'''
'''
selected = cmds.ls(sl=1)
parentList = selected[1:]
child = selected[0]
nameSpace = 'Ace_Rigging_RigOnly:'
name = 'Pack'
switch = child
'''

def spaceSwitch(nameSpace,name, parentList, child, switch, parentCount = 3,orientOnly = False, default = 0 ):
    try:
        if name == 'PV_':
            item2 = 'Non-Flip'
        else:
            item2 = parentList[1]
        

        try:
            
            if parentCount == 2:
                cmds.addAttr(switch, ln= name + '_Parent', at='enum', en = parentList[0] + ':' + item2 + ':',dv = default)
                cmds.setAttr( switch + '.' + name + '_Parent', e = 1, keyable=1,)
            elif parentCount == 3:
                cmds.addAttr(switch, ln= name + '_Parent', at='enum', en = parentList[0] + ':' + item2 + ':' + parentList[2] + ':',dv = default)
                cmds.setAttr( switch + '.' + name + '_Parent', e = 1, keyable=1,)
            elif parentCount == 4:
                cmds.addAttr(switch, ln= name + '_Parent', at='enum', en = parentList[0] + ':' + item2 + ':' + parentList[2] + ':' + parentList[3] + ':',dv = default)
                cmds.setAttr( switch + '.' + name + '_Parent', e = 1, keyable=1,)
            elif parentCount == 5:
                cmds.addAttr(switch, ln= name + '_Parent', at='enum', en = parentList[0] + ':' + item2 + ':' + parentList[2] + ':' + parentList[3] + ':' + parentList[4] + ':',dv = default)
                cmds.setAttr( switch + '.' + name + '_Parent', e = 1, keyable=1,)
        except: 
            pass

        locList = []
        for item in parentList :
            loc = cmds.spaceLocator(n = nameSpace + item + '_' + child + 'Spaceloc')[0]
            snap(child, loc)
            cmds.parent(loc, item)
            locList.append(loc)


        grp = cmds.group(child, n =  child + 'SpaceLocGRP')
        snapPivot(child, grp)
        
        if orientOnly == True :
            cmds.orientConstraint(locList, grp, mo = 1)
            constraintType = '_orientConstraint1'
        else:
            cmds.parentConstraint(locList, grp, mo = 1)
            constraintType = '_parentConstraint1'

        if parentCount == 2:
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[0] + 'W0',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[1] + 'W1',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[1] + 'W1',v=1) 
            

        if parentCount == 3:
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[0] + 'W0',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[2] + 'W2',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[1] + 'W1',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[2] + 'W2',v=0) 
            
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[2] + 'W2',v=1) 
            
            
        elif parentCount == 4:


            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[0] + 'W0',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[3] + 'W3',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[1] + 'W1',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[3] + 'W3',v=0) 
            
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[2] + 'W2',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[3] + 'W3',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[3] + 'W3',v=1) 


        elif parentCount == 5:


            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[0] + 'W0',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[3] + 'W3',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=0,attribute='.' + locList[4] + 'W4',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[1] + 'W1',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[3] + 'W3',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=1,attribute='.' + locList[4] + 'W4',v=0) 
            
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[2] + 'W2',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[3] + 'W3',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=2,attribute='.' + locList[4] + 'W4',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[3] + 'W3',v=1) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=3,attribute='.' + locList[4] + 'W4',v=0) 

            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=4,attribute='.' + locList[0] + 'W0',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=4,attribute='.' + locList[1] + 'W1',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=4,attribute='.' + locList[2] + 'W2',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=4,attribute='.' + locList[3] + 'W3',v=0) 
            cmds.setDrivenKeyframe (grp + constraintType,cd=switch + '.' + name + '_Parent',dv=4,attribute='.' + locList[4] + 'W4',v=1) 

        if cmds.objExists(nameSpace + 'grpWorld_SpaceLocs') == False :
            grpWorld = cmds.group(locList[0], n = nameSpace + 'grpWorld_SpaceLocs')
        else :
            cmds.parent(locList[0], nameSpace + 'grpWorld_SpaceLocs')
        cmds.select(locList)
        hide()
    except:
        cmds.warning('SpaceSwitch failed. Probably because we couldn\'t find the parent or something. Call Andy')
                     
def stretchyIK(nameSpace, joints, obj, side, skipScale = False, solver = 'ikSCsolver') :
    character = nameSpace + 'Character'
    cmds.select(joints)
    handle = cmds.ikHandle(n=nameSpace + obj + '_IKHandle' + side,sol=solver)[0]
    if skipScale == False:
        srtJoint = joints[0]
        endJoint = joints[1]

        distDem = cmds.distanceDimension(sp=[0,1,0],ep=[0,2,0])

        srtLoc = cmds.rename('locator1', nameSpace + obj + '_Start_DistLoc_' + side)
        endLoc = cmds.rename('locator2',nameSpace + obj + '_End_DistLoc_' + side)
        dist = cmds.rename('distanceDimension1',nameSpace + 'distance_' + obj + side)
        snap(srtJoint,srtLoc)
        snap(endJoint,endLoc)

        driver = nameSpace + 'distance_' + obj + side + 'Shape.distance'
        limbLen = cmds.getAttr(endJoint + '.tx')
        mult = cmds.createNode('multiplyDivide', n = nameSpace + obj + 'IK_StretchMult')

        cmds.connectAttr(driver,mult + '.input1X', f = 1)
        cmds.setAttr(mult + '.operation', 2)
        cmds.setAttr(mult + '.input2X', limbLen)

        addUp = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddUp_' + side)
        cmds.connectAttr(mult + '.outputX', addUp + '.input1D[1]', f = 1)
        cmds.connectAttr(addUp + '.output1D', srtJoint + '.sx', f = 1)

        multSubtract = cmds.createNode('multiplyDivide', n = nameSpace + obj + 'IK_StretchMinus')
        cmds.setAttr(multSubtract + '.operation', 3)
        cmds.connectAttr(mult + '.outputX', multSubtract + '.input1X')
        cmds.setAttr(multSubtract + '.input2X', -.5)
        
        addUpSubtract = cmds.createNode('plusMinusAverage', n = nameSpace + obj + '_AddUpYZ_' + side)
        cmds.connectAttr(multSubtract + '.outputX', addUpSubtract + '.input1D[1]', f = 1)
        cmds.connectAttr(addUpSubtract + '.output1D', srtJoint + '.sy', f = 1)
        cmds.connectAttr(addUpSubtract + '.output1D', srtJoint + '.sz', f = 1)
        
        normalizeSpline(obj = nameSpace + obj + side,output = dist,outputAttr = '.distance',influence = character,input = mult,inputAttr = '.input1X',normalizeAttr = '.sy')

        grp = cmds.group(endLoc, handle, n = nameSpace + 'grp' + obj + '_IKHandle' + side)
        snapPivot(endLoc, grp)
        disGrp = cmds.group(dist, n = nameSpace + 'grp' + obj + '_Distance' + side)
        srtGrp = cmds.group(srtLoc, n = nameSpace + 'grp' + obj + '_startLoc' + side)
        cmds.select(disGrp,srtGrp,grp)
        hide()
    
    else:
        grp = cmds.group(handle, n = nameSpace + 'grp' + obj + '_IKHandle' + side)
        cmds.setAttr(grp + '.v', 0)
        snapPivot(joints[1], grp)


    return grp


def rebuildCurve(jnum, crv) :
   
    
    for item in crv :
        cmds.rebuildCurve( rt=0, s=jnum )


        nrb = 'nrb_' + item[4:]
        if cmds.objExists(nrb) :
            cmds.select(nrb)
            cmds.rebuildSurface(rt=0, su=jnum, sv = 0 )
    cmds.select(crv)





def normalizeSpline(obj,output,outputAttr,influence,input,inputAttr,normalizeAttr,multipleAttrs = False) :
   
    '''
    obj = 'LipUp'                         # to normalize
    output = 'LipUpLen'                   # where does the chain get it's scale?
    outputAttr = '.arcLength'             #what attr does the length come out?
    influence = 'SkullDnDirect'           # what object is messing things up
    input = 'LipUp_Math'                  #where to put the final scale back into
    inputAttr = '.input1X'                #where to you want it all to end up?
    normalizeAttr = '.sy'                 #what attr from the source to you want to normalize?
    '''

    MD = cmds.createNode('multiplyDivide',n= obj + 'Normailze_MD')
    cmds.connectAttr(output + outputAttr,MD + '.input1X',f=1)
    cmds.connectAttr(influence + normalizeAttr, MD + '.input2X',f=1)
    cmds.setAttr(MD + '.operation',2)
    cmds.connectAttr(MD + '.outputX',input + inputAttr,f=1)
    
        
        
        
        
def randomJoints(mirror = False):
    
    part = raw_input('Enter Joint Name')
    side = 'LF'
    opSide = 'RT'
    jointCount = 0
    crv_point= cmds.ls(sl=True, fl = 1)
    for cv in crv_point:
        if jointCount == 0:
            jointCountString = ''
        else :
            jointCountString = str(jointCount)
            
        pos = cmds.pointPosition(cv)
        cmds.select(cl=1)
        joint = cmds.joint(n= 'jnt' + part + jointCountString + side, p=pos)

        control = controls.ball(name = part + jointCountString + side , size = .1)
        snap(joint, control)
        cmds.select(control)
        cmds.FreezeTransformations()
        cmds.parent(joint, control)
        
        if mirror == True:
            #mirror joint
            opJoint = mel.eval('mirrorJoint -mirrorYZ -mirrorBehavior;')
            opJoint = cmds.rename(opJoint, 'jnt' + part + jointCountString + opSide)


            #mirror control
            opControl = controls.ball(name = part + jointCountString + opSide, size = .1)
            snap(opJoint, opControl)
            cmds.select(control)
            cmds.FreezeTransformations()
            cmds.parent(opJoint, opControl)
            
        
        
        jointCount = 1 + jointCount
        

def addTwist(): 
    selected = cmds.ls(sl=1)

    for item in selected :
        mel.eval('addAttr -ln "Twist"  -at double  -dv 0  ' + item + ';')
        mel.eval('setAttr -e-keyable true ' + item + '.Twist;')
        
        cmds.connectAttr(item + '.Twist', item[0:-3] + 'IKHandle.twist')    
    
def exchangeGroup():
    print "Still in the works"

    selected = cmds.ls(sl=1)
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    print selected
    for item in selected :
        group = cmds.group(item, n = 'grp' + item)
        snapPivot(item, group)
        userDef = cmds.listAttr(item, keyable = 1, sn=1 )
        for attr in reversed(userDef) :
            print attr
            attrVal = cmds.getAttr(item + '.%s' % attr)
            cmds.setAttr(group + '.%s' % attr, attrVal)
            attrVal = cmds.attributeQuery(attr, n = item, ld=1)
            cmds.setAttr(item + '.%s' % attr, attrVal[0])

def hide() :
    selected = cmds.ls(sl=1)

    for item in selected:
        try:
            cmds.setAttr(item + '.v',0)
        except:
            pass
    
def hideLOD():
    selected = cmds.ls(sl=1)

    for item in selected:
        try:
            cmds.setAttr(item + 'Shape.lodVisibility',0)
        except:
            pass
        try: 
            cmds.setAttr(item + '2Shape.lodVisibility',0)
        except:
            pass
        try: 
            cmds.setAttr(item + '3Shape.lodVisibility',0)
        except:
            pass

            
            

def transferUVs():
    print "Collecting very important data.",
    selected = cmds.ls(sl=1)
    good = selected[0]
    
    if cmds.objExists(selected[1] + "ShapeOrig"):
        print "found Orig node"
        bad = selected[1] + "ShapeOrig"
        cmds.setAttr(bad + '.intermediateObject', 0)
        cmds.select(good, bad)
        mel.eval('transferAttributes -transferPositions 0 -transferNormals 0 -transferUVs 2 -transferColors 0 -sampleSpace 5 -sourceUvSpace "map1" -searchMethod 3-flipUVs 0 -colorBorders 1 ;')
        cmds.select(bad)
        cmds.DeleteHistory()
        cmds.setAttr(bad + '.intermediateObject', 1)
        cmds.delete(good)
        print " UV's copied from Good mesh to Rigged Mesh",
        
    else: 
        print "no Orig node. Copying directly to object"
        try:
            bad = selected[1]
            cmds.select(good, bad)
            mel.eval('transferAttributes -transferPositions 0 -transferNormals 0 -transferUVs 2 -transferColors 0 -sampleSpace 5 -sourceUvSpace "map1" -searchMethod 3-flipUVs 0 -colorBorders 1 ;')
            cmds.select(bad)
            cmds.DeleteHistory()
            print " UV's copied from Good mesh to Bad, non-rigged Mesh",
        except:
            print "Totally failed. Sorry.",

def mirror():
    selected = cmds.ls(sl=1,)
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    list_custom_attr = cmds.channelBox(channelBox, q=True, sma=True)
    nameSpace = ''

    
    custom = [nameSpace + 'UpperArmFKLF',nameSpace + 'UpperArmFKRT', nameSpace + 'GIMBAL_UpperArmFKLF', nameSpace + 'GIMBAL_UpperArmFKRT' ]
    custom1 = [nameSpace + 'ElbowFKLF',nameSpace + 'ElbowFKRT' ]

    for item in selected :
        side = item[-1]

        if list_custom_attr == None:
            userDef = cmds.listAttr(item, keyable = 1, sn=1 )
        else:
            userDef = cmds.channelBox(channelBox, q=True, sma=True)

        if item in custom :
            print item
            if side == 'F' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'rx' :
                        attrVal = attrVal / -1
                    elif attr == 'rz' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'RT.%s' % attr, attrVal)

            elif side == 'T' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'rx' :
                        attrVal = attrVal / -1
                    elif attr == 'rz' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'LF.%s' % attr, attrVal)
                    
        if item in custom1 :
            print item
            if side == 'F' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'rx' :
                        attrVal = attrVal / -1
                    elif attr == 'ry' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'RT.%s' % attr, attrVal)

            elif side == 'T' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'rx' :
                        attrVal = attrVal / -1
                    elif attr == 'ry' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'LF.%s' % attr, attrVal)
        else: 
            if side == 'F' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'tx' :
                        attrVal = attrVal / -1
                    elif attr == 'rz' :
                        attrVal = attrVal / -1
                    elif attr == 'ry' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'RT.%s' % attr, attrVal)

            elif side == 'T' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'tx' :
                        attrVal = attrVal / -1
                    elif attr == 'rz' :
                        attrVal = attrVal / -1
                    elif attr == 'ry' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item[0:-2] + 'LF.%s' % attr, attrVal)
                    
            elif side != 'F' or 'T' :
                for attr in userDef :
                    attrVal = cmds.getAttr(item + '.%s' % attr)
                    if attr == 'tx' :
                        attrVal = attrVal / -1
                    elif attr == 'rz' :
                        attrVal = attrVal / -1
                    elif attr == 'ry' :
                        attrVal = attrVal / -1
                    cmds.setAttr(item + '.%s' % attr, attrVal)
            print 'Mirrored: %s' % item 
            
def selectMirror():
    selected = cmds.ls(sl=1,)
    cmds.select(clear=1)
    for item in selected :
        side = item[-1]
        if side == 'F' :
            cmds.select(item[0:-2] + 'RT',add=1)

        elif side == 'T' :
            cmds.select(item[0:-2] + 'LF', add=1)
                
        elif side != 'F' or 'T' :
            cmds.select(item,add=1)
            

def resetSelected():
    controls = cmds.ls(sl=1)
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    list_custom_attr = cmds.channelBox(channelBox, q=True, sma=True)
    
    for item in controls:
        if list_custom_attr == None:
            userDef = cmds.listAttr(item, keyable = 1, sn=1 )
        else:
            userDef = cmds.channelBox(channelBox, q=True, sma=True)
            
        skip = ['overrideEnabled','overrideColor','Influence_tx','Influence_ty','Influence_tz','Influence_t','Influence_rx','Influence_ry','Influence_rz','Influence_r','Influence_sx','Influence_sy','Influence_sz','Influence_s','Isolate','PoleVector','ShowToePivot','ShowHeelPivot','EasyControls','LipPress','SquashSwitch','visibility','Glasses','Parent','MinorControls','StretchControls','ShapeControls','Minor','FKControls','FKLegParent','IKLegParent','IKArmParent','FKArmParent','PVParent','FK_IK_Switch','visibility','Isolate','FingerTips''FingerAll','Palm','Fingers','BendControls','HipControl','StickyFavor','ShapeControls','MinorControls','JawControls','StickyOn','StickyFalloff']
        setTo1 = ['Pupil','Iris','BicepLength','DnArmLength','ForarmLength','ThighLength','ShinLength',]
        for attr in userDef :
            if attr in skip :
                pass
            elif attr in setTo1 :
                try:
                    cmds.setAttr(item + '.%s' % attr, 1)
                except:
                    pass
            else :
                attrVal = cmds.attributeQuery(attr, n = item, ld=1)
                try: 
                    cmds.setAttr(item + '.%s' % attr, attrVal[0])
                except:
                    pass



#reset()
    
def reset():
    select = cmds.select(cmds.ls(type='nurbsCurve'))
    selectNurbs = cmds.select(cmds.ls(type='nurbsSurface'),add=1)
    controls = cmds.ls(sl=1)

    for item in controls:
        parent = cmds.listRelatives(item, parent = 1)
        userDef = cmds.listAttr(parent[0], keyable = 1, unlocked = 1, settable = 1 )
        parent = str(parent[0])
        
        if parent[0:3] == 'crv' :
            pass
        else :
            
            skip = ['Influence_tx','Influence_ty','Influence_tz','Influence_t','Influence_rx','Influence_ry','Influence_rz','Influence_r','Influence_sx','Influence_sy','Influence_sz','Influence_s','Isolate','PoleVector','ShowToePivot','ShowHeelPivot','EasyControls','LipPress','SquashSwitch','visibility','Glasses','Parent','MinorControls','StretchControls','ShapeControls','Minor','FKControls','FKLegParent','IKLegParent','IKArmParent','FKArmParent','PVParent','FK_IK_Switch','visibility','Isolate','FingerTips''FingerAll','Palm','Fingers','BendControls','HipControl','StickyFavor','ShapeControls','MinorControls','JawControls','StickyOn','StickyFalloff']
            setTo1 = ['Pupil','Iris','BicepLength','DnArmLength','ForarmLength','ThighLength','ShinLength',]
            for attr in userDef :
                if attr in skip :
                    pass
                elif attr in setTo1 :
                    cmds.setAttr(parent + '.%s' % attr, 1)
                else :
                    attrVal = cmds.attributeQuery(attr, n = parent, ld=1)
                    cmds.setAttr(parent + '.%s' % attr, attrVal[0])
    cmds.select(clear=1)
    print 'Controls Reset'


def default(): 

    select = cmds.select(cmds.ls(type='nurbsCurve'))
    controls = cmds.ls(sl=1)

    for item in controls:
        parent = cmds.listRelatives(item, parent = 1)
        userDef = cmds.listAttr(parent[0], keyable = 1, unlocked = 1, settable = 1 )
        parent = str(parent[0])
        
        if parent[0:3] == 'crv' :
            pass
        
        else :
            skip = ['Isolate','Influence_tx','Influence_ty','Influence_tz','Influence_t','Influence_rx','Influence_ry','Influence_rz','Influence_r','Influence_sx','Influence_sy','Influence_sz','Influence_s']
            setTo1 = ['Isolate','Parent','SquashSwitch','LipPress','Pupil','Iris','BicepLength','DnArmLength','ForarmLength','ThighLength','ShinLength','FK_IK_Switch']
            setCustom = ['EyeFollow','LidFollow']
            if userDef !=[]: 
                for attr in userDef :
                    try:
                        
                        if attr in setTo1 :
                            cmds.setAttr(parent + '.%s' % attr, 1)
                        elif attr in setCustom :
                            cmds.setAttr(parent + '.%s' % attr, .5)
                        else :
                            attrVal = cmds.attributeQuery(attr, n = parent, ld=1)
                            cmds.setAttr(parent + '.%s' % attr, attrVal[0])
                    except:
                        pass

    cmds.select(clear=1)


def transferAttr():
    
    selected = cmds.ls(sl=1)

    old = selected[0]
    new = selected[1]

    userDef = cmds.listAttr(old, keyable = 1, )

    for item in userDef :
        print item
        if cmds.objExists(new + '.' + item) == True :
            pass
        else:
            try :
                mel.eval('addAttr -ln "' + item + '"  -at double  ' + new + ';')
                mel.eval('setAttr -e-keyable true ' + new + '.' + item + ';')
            except:
                pass
            try:
                print "Connecting Attrs"
                cmds.connectAttr(new + '.' + item,old + '.' + item,f=1)
                
                
            except :
                pass

def moveValues():

    selected = cmds.ls(sl=1)
    clean = selected[0]
    host = selected[1]

    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')

    userDef = cmds.listAttr(clean, keyable = 1, sn=1 )
    print userDef
    for attr in userDef :
        print attr
        if attr[0] == 's' :
            pass
        else:
            attrVal = cmds.getAttr(clean + '.%s' % attr)
            print 'OLD ATTR VAL'
            print attrVal
            cmds.setAttr(host + '.' + attr, attrVal)    
            
            attrVal = cmds.attributeQuery(attr, n = clean, ld=1)
            print 'NEW ATTR VAL'
            print attrVal
            cmds.setAttr(clean + '.%s' % attr, attrVal[0])
                                        
def customSpline(name) :
    crv = "crv_" + name
    cmds.curve(n=crv, ep=[(.1,1.5,0.5),(.6,1.5,0.5)])
    cmds.setAttr(crv + '.overrideEnabled',1)
    cmds.setAttr(crv + '.overrideColor',30)

    cmds.CenterPivot(crv)
    
    
def singleChainIK():
    nameSpace = ''
    obj = 'FourthClav'
    side = 'LF'

    if side == 'RT':
            color = 6
    elif side == 'LF' :
            color = 13
    else :
        color = 30
            
    list = cmds.ls(sl=1)

    clavJoints = joints2List(nameSpace = '', list = list,  obj = 'skn_' + obj + '_IK', side = side, chain = True)    
    handle = stretchyIK(nameSpace = '', joints = clavJoints, obj = obj, side =  side)

    control = controls.pin(name = nameSpace + obj + side, color = color)
    snap(clavJoints[0], control)
    cmds.setAttr(control + '.rx', 90)
    cmds.parentConstraint(control, handle, mo = 1)
            
    
def rigCustomSpline(name):
    #intitial defs
    joint = 'jnt' + name 
    temp = 'Temp'
    part = name
    side = ''
    crv = "crv_" + name
    print crv
    


    
    ##########################################
    # Place Joints along CVs
    ##########################################

    #delete history for curve to avoid warning
    cmds.select(crv)
    cmds.DeleteHistory()

    #rebuilds that curve to be usable in the rig
    mel.eval('select -r ' + crv + '.cv[0:20] ;')

    crv_point= cmds.ls(sl=True)[0]
    for cv in cmds.filterExpand(sm=28):
        pos = cmds.pointPosition(cv)
        cmds.select(cl=1)
        cmds.joint(n=joint + side + temp, p=pos)
        
    # cleans up the extra joints built on the curve
    pfx = joint + side + temp
    newList = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newList.append(item)
    cmds.delete(newList[1],newList[-2])

    #renames joints 
    newList = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newList.append(item)

    for item in newList:
        cmds.select(item)
        cmds.rename(joint + side + '1')
        
    #parent brow joints together
    pfx = joint + side 
    newList = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newList.append(item)

    for item in newList:
        jntNumber = item[-1]
        jntNumberInt = int(jntNumber)
        
        if jntNumberInt >=2:
            parentNumber = jntNumberInt - 1
            parentStr = str(parentNumber)
            parent = pfx + parentStr
            
            cmds.parent(item,parent)
            
    #oreint Leg bind joint
    cmds.select('jnt' + name + '1')
    mel.eval('joint -e  -oj xzy -ch -zso;')

    #Spline IK stuff
    splineStart = newList[0]
    splineEnd = newList[-1]

    cmds.select(splineStart,splineEnd)
    cmds.ikHandle(n=part + 'IKHandle', sol='ikSplineSolver',curve = crv,ccv = 0)



    mel.eval('select -r ' + crv + '.cv[0:20] ;')

    crv_point= cmds.ls(sl=True)[0]
    for cv in cmds.filterExpand(sm=28):
        pos = cmds.pointPosition(cv)
        cmds.select(cl=1)
        cmds.joint(n=part + side + 'SplineTemp1', p=pos)
        
    # cleans up the extra joints built on the curve
    pfx = part + side + 'Spline'
    newListSpline = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newListSpline.append(item)
    cmds.delete(newListSpline[1],newListSpline[-2])

    #renames joints 
    newListSpline = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newListSpline.append(item)

    for item in newListSpline:
        cmds.select(item)
        cmds.rename(part + side + 'Spline' + '1')
        
    #Skins bind joints to IK curve
    cmds.select(clear=1)
    pfx = part + side + 'Spline'
    newListSpline = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
       if item.startswith(pfx ):
           newListSpline.append(item)

    cmds.select(newListSpline,crv ,add=1)
    cmds.skinCluster(n=crv + 'SkinCluster')

    #################################
    #Setup Squash and stretch on Spline
    #################################
    #creates nodes for S and S
    splineLen = cmds.createNode('curveInfo', n = part + side + 'Len')
    cmds.connectAttr(crv + '.worldSpace[0]', splineLen + '.inputCurve',force=True,)

    splineMD = cmds.createNode('multiplyDivide',n=part + side + '_Math')
    cmds.connectAttr(splineLen + '.arcLength',splineMD + '.input1X',force=True)
            
    LenNumb = cmds.arclen(crv)
    cmds.setAttr(splineMD + '.input2X',LenNumb)
    cmds.setAttr(splineMD + '.operation', 2)

    #Connect the output of splineMD into the scale X of each IK joint
    pfx = joint + side
    newList = []
    fullList = cmds.ls(type='joint')
    for item in fullList:
        if item.startswith(pfx ):
           newList.append(item)
           
    for item in newList:
        if item != newList[-1]:
            cmds.connectAttr(splineMD + '.outputX', '%s.scaleX' % item,force=True)

    splineMD2 = cmds.createNode('multiplyDivide',n = part + side + 'Math2')
    cmds.setAttr(splineMD2 + '.operation', 3)
    cmds.connectAttr(splineMD +'.outputX', splineMD2 + '.input1X', force=True)
    cmds.setAttr(splineMD2 + '.input2X', .5)

    splineInvert = cmds.createNode('multiplyDivide',n=part + side + 'MathInvert')
    cmds.connectAttr(splineMD2 + '.outputX',splineInvert + '.input2X', force=True)
    cmds.setAttr(splineInvert + '.operation', 2)
    cmds.setAttr(splineInvert + '.input1X', 1)

    for item in newList:
        if item != newList[-1]:
            cmds.connectAttr(splineInvert + '.outputX', '%s.scaleZ' % item,force=True)
            cmds.connectAttr(splineInvert + '.outputX', '%s.scaleY' % item,force=True)


    ##########################################
    #CONTROL CURVE SECTION!!
    #Edit as desired---Currently, placeholders
    ##########################################
    if side == 'LF' :
        color = 31
    else :
        color = 30
        
    numb = 0
    for item in newListSpline :
        numb = numb + 1
        numbStr = str(numb)
        name = 'Minor' + numbStr
        control = con.minor(part + side + name,color, size = .7)
        
    pfx = part + side + 'Minor'
    newListJPos = []
    fullList = cmds.ls(type='transform')
    for item in fullList:
        if item.startswith(pfx ):
           newListJPos.append(item)
           
    for item in newListJPos : 
        numb = item[-1]
        jointTemp = part + side + 'Spline' + numb
        snapScale(jointTemp,item)
        freeze(item)
        cmds.parent(jointTemp,item)
        
#################
#Fk Contols - Tail
#################

'''
ikFKTail(part = Tail)
'''
def ikFKTail(part):
    
    pfx = part + 'Minor'
    newListMinors = []
    fullList = cmds.ls(type='transform')

    for item in fullList:
        if item.startswith(pfx ):
           newListMinors.append(item)
           
    for item in newListMinors:
        controlNumb = item[-1]
        control = con.faceRing(part + 'FK' + controlNumb, size = 1.5, color = 18)
        snap(item, control)
        cmds.setAttr(control + '.rx', 90)
        cmds.FreezeTransformations()
        
        cmds.parent(item, control)
    
#####
#parents Fk joints together
#####
'''
parentChain(joint = TailFK, side = '', jointControl = 'transform')
'''
def parentChain(joint, jointControl, side = ''):
    pfx = joint + side 
    newList = []
    fullList = cmds.ls(type= jointControl)
    for item in fullList:
       if item.startswith(pfx ):
           newList.append(item)

    for item in newList:
        jntNumber = item[-1]
        jntNumberInt = int(jntNumber)
        
        if jntNumberInt >=2:
            parentNumber = jntNumberInt - 1
            parentStr = str(parentNumber)
            parent = pfx + parentStr
            
            cmds.parent(item,parent)

def chainHookUp(parent, part, side = ''):
    
    partGroup = cmds.group(part + 'FK' + '1', n = 'grp' + part)
    snapPivot('jnt' + part + '1', partGroup)
    
    cmds.pointConstraint(parent, partGroup, mo = 1)
    if cmds.objExists('World'):
        cmds.orientConstraint(parent, 'World', partGroup, mo = 1)
    else:
        cmds.spaceLocator(n='World')
        cmds.orientConstraint(parent, 'World', partGroup, mo = 1)

    cmds.addAttr(parent, ln='Isolate' + part, at='double', min = 0, max = 1)
    cmds.setAttr( parent + '.Isolate' + part, e = 1, keyable=1,)
    
    cmds.connectAttr(parent + '.Isolate' + part, partGroup + '_orientConstraint1.WorldW1')

    mel.eval('setDrivenKeyframe -currentDriver ' + parent + '.Isolate' + part + ' ' + partGroup + '_orientConstraint1.' + parent + 'W0;')
    mel.eval('setAttr "' + parent + '.Isolate' + part + '" 0;')
    mel.eval('setAttr "' + partGroup + '_orientConstraint1.' + parent + 'W0' + '" 1;')
    mel.eval('setDrivenKeyframe -currentDriver ' + parent + '.Isolate' + part + ' ' + partGroup + '_orientConstraint1.' + parent + 'W0;')
    
    '''
    cmds.addAttr(parent, ln='ShowIK', at='double', min = 0, max = 1)
    cmds.setAttr( parent + '.ShowIK', e = 1, keyable=1,)
    
    cmds.addAttr(parent, ln='ShowFK' , at='double', min = 0, max = 1)
    cmds.setAttr( parent + '.ShowFK' , e = 1, keyable=1,)
    '''

def chainCleanup(part, parent, side = '') :
    
    if part[-2:] == 'FK' :
        partShort = part[0:-2]

    else:
        partShort = part
    
    grpControls = cmds.group(n='grp' + part + 'Controls' + side,em=1)
    snapPivot(parent + side, grpControls)
    
    grpJoints = cmds.group(n='grp' + part + 'Joints' + side,em=1)
    snapPivot(parent + side , grpJoints)

    grpIK = cmds.group(n='grp' + part + 'IK_' + side,em=1)
    snapPivot(parent + side, grpIK)

    grpEX = cmds.group(n='grp' + part + 'EX' + side,em=1)
    snapPivot(parent + side , grpEX)

    cmds.parent(grpControls, parent)
    cmds.parent(grpJoints, parent)
    cmds.parent(grpIK, parent)
    cmds.parent(grpEX, 'World')

    cmds.parent('grp' + part , grpControls)
    cmds.parent('jnt' + partShort + '1', grpJoints)
    cmds.parent(partShort + 'IKHandle', grpIK)
    cmds.parent('crv_' + partShort, grpEX)

##################################################
##################################################
##################################################
#
# Skinning Utils
#
##################################################
##################################################
##################################################

def getSkin(skinnedMesh) :
    
    skinCluster = mel.eval('findRelatedSkinCluster ' + skinnedMesh)
    skinnedJoints = cmds.skinCluster(skinCluster,query=True,inf=True)
    
    return skinnedJoints

def matchSkinClusterInfluence() :
    selected = cmds.ls(sl=1)
    skinnedMesh = selected[0]
    skinCluster = mel.eval('findRelatedSkinCluster ' + skinnedMesh)
    skinnedJoints = cmds.skinCluster(skinCluster,query=True,inf=True)

    cmds.select(skinnedJoints)
    
def sameSkinWeights():
    selected = cmds.ls(sl=1)
    skinnedMesh = selected[0]
    newMesh = selected[1]

    skinCluster = mel.eval('findRelatedSkinCluster ' + skinnedMesh)
    skinnedJoints = cmds.skinCluster(skinCluster,query=True,inf=True)

    cmds.select(skinnedJoints, newMesh)
    cmds.skinCluster()

def deleteSkin() :
    selected = cmds.ls(sl=1)
    for item in selected :
        
        skinCluster = mel.eval('findRelatedSkinCluster ' + item)
        cmds.delete(skinCluster)
        



def applyOmniSkin() :
    try:
        pfx ='OMNI__skn'
        newList = []
        fullList = cmds.ls(type='joint')

        for item in fullList:
           if item.startswith(pfx ):
               newList.append(item)
               
        cmds.select(newList)
        try :
            cmds.delete('OMNI__Index_IKHandleLF')
            cmds.delete('OMNI__Index_IKHandleRT')
        except:
            pass

        try :
            cmds.delete('OMNI__Middle_IKHandleLF')
            cmds.delete('OMNI__Middle_IKHandleRT')
        except:
            pass
        try :
            cmds.delete('OMNI__Ring_IKHandleLF')  
            cmds.delete('OMNI__Ring_IKHandleRT')
        except:
            pass
        try :
            cmds.delete('OMNI__Pinky_IKHandleLF')  
            cmds.delete('OMNI__Pinky_IKHandleRT')
        except:
            pass
        try :
            cmds.delete('OMNI__Thumb_IKHandleLF')  
            cmds.delete('OMNI__Thumb_IKHandleRT')
        except:
            pass
            

        print newList
        for item in newList:
            
            try:
                utils.snap(item[6:],item)
            except:
                pass
        print 'Everything went really well with your omni skin thing.'
    except:
        print 'Errors occured. Skin may not have transfered'
            
##################################################
##################################################
##################################################
#
# Misc Utils
#
##################################################
##################################################
##################################################
#addJoint2selected()

def addJoint2selected() :
    selected = cmds.ls(sl=1)
    for item in selected :
        cmds.select(cl=1)
        joint = cmds.joint(n = 'skn_' + item)
        cmds.parent(joint, item)
        snap(item,joint)
        

def reverseAttr(control, endNode) : 
    mult = cmds.createNode('multiplyDivide',n=control + '_Reverse_Mult')
    cmds.setAttr(mult + '.input2X',-1)
    cmds.connectAttr(control, mult + '.input1X',f=1)
    cmds.connectAttr(mult + '.outputX',endNode,f=1)
    
def influenceControl(control,  controlNode, influenceNode, endNode,altControl = '',) :
    if altControl == '' :
        altControl = control 
    mult = cmds.createNode('multiplyDivide',n=control + '_Influence_Mult')
    cmds.connectAttr(control + '.' + controlNode, mult + '.input1X',f=1)
    cmds.connectAttr(altControl + '.' + influenceNode, mult + '.input2X',f=1)
    cmds.connectAttr(mult + '.outputX',endNode,f=1)
    return mult


    
def jointLock(self):
    nameSpace = self.NameSpace.text()
    if nameSpace == 'NameSpace' : 
        nameSpace = ''
        
    allJoints = cmds.ls(type='joint')
    for joint in allJoints:
        cmds.setAttr(joint + '.overrideEnabled',1)
        
        
        if joint.startswith(nameSpace + 'skn_'):
            #pass
            cmds.setAttr(joint + '.overrideDisplayType',1)
            cmds.setAttr(joint + '.radius',2)

        elif joint.startswith(nameSpace + 'twist_') :
            cmds.setAttr(joint + '.overrideDisplayType',1)
            cmds.setAttr(joint + '.radius',.01)
        else:
            cmds.setAttr(joint + '.overrideDisplayType',1)
            cmds.setAttr(joint + '.radius',.01)

    allLocs = cmds.ls(type='locator')
    for loc in allLocs:
        cmds.setAttr(loc + '.overrideEnabled',1)
        cmds.setAttr(loc + '.overrideDisplayType',1)
        
    if cmds.objExists(nameSpace + 'World_Move') :
        cmds.delete(nameSpace + 'World_Move')

        
def jointUnlock(self):
    nameSpace = self.NameSpace.text()
    if nameSpace == 'NameSpace' : 
        nameSpace = ''
        
    allJoints = cmds.ls(type='joint')
    for joint in allJoints:
      
        if joint.startswith(nameSpace + 'skn_'):
            cmds.setAttr(joint + '.overrideDisplayType',0)
        elif joint.startswith(nameSpace + 'twist_') :
            cmds.setAttr(joint + '.overrideDisplayType',0)
            cmds.setAttr(joint + '.radius',1)
        else:
            cmds.setAttr(joint + '.overrideDisplayType',0)
            cmds.setAttr(joint + '.radius',1)
        
    
    allLocs = cmds.ls(type='locator')
    for loc in allLocs:
        cmds.setAttr(loc + '.overrideDisplayType',0)
    
    
def hideInfluence() :
    selected = cmds.ls(type='transform')


    attrList = ['Influence_tx','Influence_ty','Influence_tz','Influence_t','Influence_rx','Influence_ry','Influence_rz','Influence_r','Influence_sx','Influence_sy','Influence_sz','Influence_s']
    for item in selected:
        cmds.setAttr(item + '.' + 'visibility',lock = True, keyable = False, channelBox = False) 
        for attr in attrList :
            try :
                cmds.setAttr(item + '.' + attr,lock = True, keyable = False, channelBox = False) 
            except :
                pass

def addCubes(self):
    nameSpace = self.NameSpace.text()
    if nameSpace == 'NameSpace' : 
        nameSpace = ''
    
    pfx = nameSpace + 'skn_'
    newListCubes = []
    fullList = cmds.ls(type='joint')

    for item in fullList:
       if item.startswith(pfx ):
           newListCubes.append(item)
    cmds.select(cl = 1)
    layer = cmds.createDisplayLayer ( n = 'jCubes' )
    
    cubes = []
    for item in newListCubes :
        cube = cmds.polyCube ( n = 'jCube', d = .5, h = .5, w = .5 )
        cmds.parentConstraint ( item , cube )
        cmds.scaleConstraint ( item , cube )
        
        cmds.select(cube)
        cube = cmds.rename (item + 'Cube')
        cmds.editDisplayLayerMembers( layer, cube )
        cubes.append(cube)
    grp = cmds.group(cubes, n = nameSpace + 'ProxyMesh')
    cmds.parent(grp, nameSpace + 'World')                
    
def combineCurves():
    selected = cmds.ls(sl=1)
    parent = selected[0]

    shapeList = []
    for item in selected :
        freeze(item)
        if item != parent :
            shapes = cmds.listRelatives(item)
            shapeList.append(shapes)
    for item in shapeList :
        cmds.select(item, parent)
        mel.eval('parent -r -s;')
    for item in selected :
        if item != parent :
            cmds.delete(item)
    cmds.select(cl=1)
    
    
##################################################
##################################################
##################################################
#
# Sets Utils
#
##################################################
##################################################
##################################################


def set(self, nameSpace):
    
    toSet = [nameSpace + 'MouthEasyLF',nameSpace +'MouthEasyRT',nameSpace +'MouthAll',nameSpace +'HeadIK',nameSpace +'ChestIK',nameSpace +'HipIK',nameSpace +'FootIKLF',nameSpace +'FootIKRT',nameSpace +'HandIKLF',nameSpace +'HandIKRT']

    for item in toSet : 
        if cmds.objExists(item) :
            cmds.select(item,r=1)
            name = cmds.sets(n='set_' + item)
    try:
        cmds.select(nameSpace + 'Arm_SwitchRT',nameSpace + 'Arm_SwitchLF',r=1)
        name = cmds.sets(n= 'set_' + nameSpace + 'ArmSettings')
    except :
        pass
    try:
        cmds.select(nameSpace + 'Leg_SwitchRT',nameSpace + 'Leg_SwitchLF',r=1)
        name = cmds.sets(n= 'set_' + nameSpace +'LegSettings')
    except :
        pass
        
    try:
        cmds.select(nameSpace + 'LidUpRT',nameSpace + 'LidUpLF',r=1)
        name = cmds.sets(n= 'set_' + nameSpace + 'UpLids')
    except :
        pass
        
    try:
        cmds.select(nameSpace + 'LidDnLF',nameSpace + 'LidDnRT',r=1)
        name = cmds.sets(n= 'set_' + nameSpace + 'DnLids')
    except :
        pass