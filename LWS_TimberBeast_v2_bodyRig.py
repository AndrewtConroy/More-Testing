import maya.cmds as cmds
import maya.mel as mel
import TimberBeast_v2.LWS_TimberBeast_v2_utils as utils
import TimberBeast_v2.LWS_TimberBeast_v2_controls as controls




##########################################################
##########################################################
##########################################################
#
#
#                   BUILT BODY MOVERS
#
#
##########################################################
##########################################################
##########################################################
'''
Comments: Sets up all starting/placement rigs for initial rig setup



Usable Functions:     

#Builds a complete IK spline based on a matching mover
utils.IKSpline(nameSpace, obj, crv, spineType = 1)


#Builds a simple ribbon mover like the ones used in the arms
utils.multiJoint_Ribbon_Move_Simple(nameSpace = '', obj = 'Band', jnum = 4, height = 5)

#Builds a visual spline style ribbon like in the Spine
utils.multiJoint_Ribbon_Move(nameSpace = '', obj = 'Strap', jnum = 4, height = 5)

#Adds joints to specified curve
utils.joint2Curve(nameSpace, obj = 'Forarm', crv = crv_ArmDn, partName = '_Move' + side, parent = grpJoints, skipEnds = True)


#get's list based on pfx
jpos = utils.pfx_JointList(pfx = nameSpace + 'jntForarm_Move' + side)

#Builds controls for the list of joints above. To be used with the "joint2Curve" function
utils.joint2Curve_Controls(nameSpace, obj = 'Forarm', jpos = jpos, partName = '_Move' + side, parent = armAll, rotations = False)




'''


################################
#
#          WORLD MOVER
# 
################################
'''
Comments: builds the world, character ring and other starting points
'''

def characterGroup(self, nameSpace, rig = False) :



    if rig == False:
        sfx = '_Move'
    else :
        sfx = ''


    if utils.checkDuplicate(nameSpace + 'Character' + sfx) == False :

        character = controls.ring(nameSpace + 'Character' + sfx, size = 5, color = 1)
        grpWorld = cmds.group(character, n = nameSpace + 'World' + sfx)
        grpEx = cmds.group(n = nameSpace + 'grpEX' + sfx, em=1)
        grpJoints = cmds.group(n = nameSpace + 'grpJoints' + sfx, em=1)
        grpControls = cmds.group(n = nameSpace + 'grpControls' + sfx, em=1)

        cmds.parent(grpControls, character)
        cmds.parent(grpJoints, grpEx, grpWorld)
            
        if rig == True: 
            utils.snap(character + '_Move', character)


        print "Character Group Built Successfully!"
    
    else:
        print "Duplcate item may exist"


################################
#
#          SPINE MOVER
# 
################################
'''
Comments: Spine movers calls the command below for 95% percent of it's work
    
    
utils.multiJoint_Ribbon_Move_Simple(nameSpace = '', obj = 'BUTT', jnum = 12, height = 5)

'''


def spineMove(self, nameSpace):
    
    if utils.checkDuplicate( nameSpace + "UpperBodyMove") == False :

        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        
        utils.multiJoint_Ribbon_Move(nameSpace , obj = 'Spine', jnum = 3, height = 5, aim = True)
        cmds.setAttr(nameSpace + 'crv_Spine.v', 1)
        cmds.setAttr(nameSpace + 'crv_Spine.template', 1)
        cmds.setAttr(nameSpace + 'nrb_SpinePlane.v', 0)
        
        cmds.setAttr(nameSpace + 'SpineMove.ty', 8)

        if cmds.objExists(nameSpace + 'NeckMove') :
            grp = cmds.group(nameSpace + 'NeckMove', n = nameSpace + 'grpNeckMove')
            utils.snapPivot(nameSpace + 'NeckMove', grp)
            cmds.pointConstraint(nameSpace + 'Spine_Move03',grp )
            cmds.scaleConstraint(nameSpace + 'Spine_Move03',grp)
                   
                   
        elif cmds.objExists(nameSpace + 'Arm_MoveRT') :
            grp = cmds.group(nameSpace + 'Arm_MoveRT', n = nameSpace + 'grpArmMoveRT')
            utils.snapPivot(nameSpace + 'Arm_MoveRT', grp)
            cmds.pointConstraint(nameSpace + 'Spine_Move03',grp )
            cmds.scaleConstraint(nameSpace + 'Spine_Move03',grp)
                   
        elif cmds.objExists(nameSpace + 'Arm_MoveLF') :
            grp = cmds.group(nameSpace + 'Arm_MoveLF', n = nameSpace + 'grpArmMoveLF')
            utils.snapPivot(nameSpace + 'Arm_MoveLF', grp)
            cmds.pointConstraint(nameSpace + 'Spine_Move03',grp )
            cmds.scaleConstraint(nameSpace + 'Spine_Move03',grp)
            
        elif cmds.objExists(nameSpace + 'Leg_MoveRT') :
            grp = cmds.group(nameSpace + 'Leg_MoveRT', n = nameSpace + 'grpLegMoveRT')
            utils.snapPivot(nameSpace + 'Leg_MoveRT', grp)
            cmds.pointConstraint(nameSpace + 'SpineMove',grp , mo = 1)
            cmds.scaleConstraint(nameSpace + 'SpineMove',grp, mo = 1)
            
        elif cmds.objExists(nameSpace + 'Leg_MoveLF') :
            grp = cmds.group(nameSpace + 'Leg_MoveLF', n = nameSpace + 'grpLegMoveLF')
            utils.snapPivot(nameSpace + 'Leg_MoveLF', grp)
            cmds.pointConstraint(nameSpace + 'SpineMove',grp , mo = 1)
            cmds.scaleConstraint(nameSpace + 'SpineMove',grp, mo = 1)
            
                       
        print "Spine Movers Built Successfully!"

    else:
        print "Duplcate item may exist"

################################
#
#          NECK MOVER
# 
################################
'''
Comments: 
'''
def neckMove(self, nameSpace):

    if utils.checkDuplicate( nameSpace + "HeadIK_Move") == False :
        
        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'


        head = controls.ring(nameSpace + 'HeadIK_Move', size = '3')
        cmds.setAttr(head + '.rx', 90)
        cmds.setAttr(head + '.ty', 8)
        utils.freeze(head)

        utils.multiJoint_Ribbon_Move(nameSpace , obj = 'Neck', jnum = 3, height = 5)

        cmds.setAttr(nameSpace + 'crv_Neck.v', 1)
        cmds.setAttr(nameSpace + 'crv_Neck.template', 1)
        cmds.setAttr(nameSpace + 'nrb_NeckPlane.v', 0)

        cmds.parent(head, nameSpace + 'NeckMove')
        grpTopNeck = cmds.group(nameSpace + 'Neck_Move03', n = nameSpace + 'grpNeck_Move03')
        cmds.parentConstraint(head, grpTopNeck, mo = 1)
        
        cmds.setAttr(nameSpace + 'NeckMove.ty',16)
        cmds.setAttr(nameSpace + 'NeckMove.sx',.6)
        cmds.setAttr(nameSpace + 'NeckMove.sy',.6)
        cmds.setAttr(nameSpace + 'NeckMove.sz',.6)
        
          
        if cmds.objExists(nameSpace + 'SpineMove') :
            grp = cmds.group(nameSpace + 'NeckMove', n = nameSpace + 'grpNeckMove')
            utils.snapPivot(nameSpace + 'NeckMove', grp)
            cmds.pointConstraint(nameSpace + 'Spine_Move03',grp )
            cmds.scaleConstraint(nameSpace + 'Spine_Move03',grp)
            
        print "Neck Movers Built Successfully!"

    else:
        print "Duplcate item may exist"

################################
#
#          ARM MOVER
# 
################################
'''
Comments: 
'''
def armMove(self, nameSpace, side):
    


    if utils.checkDuplicate( nameSpace + "Arm_Move" + side) == False :


        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        obj = 'Arm'

        armAll = controls.square(nameSpace + 'Arm_Move' + side )
        cmds.setAttr(armAll + '.rx', 90)
        cmds.setAttr(armAll + '.ry', 90)
        cmds.setAttr(armAll + '.ty', 6)


        cmds.parent(armAll, character)

        if side == 'LF' :

            crv_ArmDn = nameSpace + "crv_ArmDn" + side
            cmds.curve(n=crv_ArmDn, ep=[(6,6,-.5),(10,6,0)])

            crv_ArmUp = nameSpace + "crv_ArmUp" + side
            cmds.curve(n=crv_ArmUp, ep=[(2,6,0),(6,6,-.5)])

            crv_Shoulder = nameSpace + "crv_Shoulder" + side
            cmds.curve(n=crv_Shoulder, ep=[(.5,6,0),(2,6,0)])
            
            grpArmEX = cmds.group(n = nameSpace + 'grp_ArmEX' + side, em = 1)
            cmds.parent(grpArmEX, grpEx)
            
            cmds.setAttr(armAll + '.tx', 2.5)
            cmds.setAttr(armAll + '.tz', .5)
            utils.freeze(armAll)
            
        else :
            crv_ArmDn = nameSpace + "crv_ArmDn" + side
            cmds.curve(n=crv_ArmDn, ep=[(-6,6,-.5),(-10,6,0)])

            crv_ArmUp = nameSpace + "crv_ArmUp" + side
            cmds.curve(n=crv_ArmUp, ep=[(-2,6,0),(-6,6,-.5)])

            crv_Shoulder = nameSpace + "crv_Shoulder" + side
            cmds.curve(n=crv_Shoulder, ep=[(-.5,6,0),(-2,6,0)])

            grpArmEX = cmds.group(n = nameSpace + 'grp_ArmEX' + side, em = 1)
            cmds.parent(grpArmEX, grpEx)

            cmds.setAttr(armAll + '.tx', -1.5)
            cmds.setAttr(armAll + '.tz', .5)
            utils.freeze(armAll)

        cmds.parent(crv_ArmDn,crv_ArmUp,crv_Shoulder,grpArmEX)

        utils.joint2Curve(nameSpace, obj = obj + 'Dn', crv = crv_ArmDn, partName = '_Move' + side, parent = grpJoints, skipEnds = True)
        jpos = utils.pfx_JointList(pfx = nameSpace + 'jnt' + obj + 'Dn_Move' + side)
        utils.joint2Curve_Controls(nameSpace, obj = obj + 'Dn', jpos = jpos, partName = '_Move' + side, parent = armAll, rotations = False)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv_ArmDn, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(crv_ArmDn + '.v', 0)

        forarmPlane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = 4, lr = .1, n = nameSpace + 'nrb_' + obj + 'Dn' +  side + 'Plane')[0]
        cmds.setAttr(forarmPlane + '.ty', 6)
        cmds.setAttr(forarmPlane + '.tz', -.24)
        cmds.setAttr(forarmPlane + '.sx', 1.26 )

        if side == 'LF' :
            cmds.setAttr(forarmPlane + '.tx', 8)
            cmds.setAttr(forarmPlane + '.ry', -7 )
            utils.freeze(forarmPlane)

            
        else :
            cmds.setAttr(forarmPlane + '.tx', -8)
            cmds.setAttr(forarmPlane + '.ry', 7 )
            cmds.setAttr(forarmPlane + '.sx', -1.26 )
            utils.freeze(forarmPlane)



        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(forarmPlane, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(forarmPlane + 'Shape.template', 1)
        cmds.parent(forarmPlane, grpArmEX)



        utils.joint2Curve(nameSpace, obj = 'ArmUp', crv = crv_ArmUp, partName = '_Move' + side, parent = grpJoints, skipEnds = True)
        jpos = utils.pfx_JointList(pfx = nameSpace + 'jntArmUp_Move' + side)
        utils.joint2Curve_Controls(nameSpace, obj = 'ArmUp', jpos = jpos, partName = '_Move' + side, parent = armAll, rotations = False)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv_ArmUp, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(crv_ArmUp + '.v', 0)

        upArmPlane = cmds.nurbsPlane(u = 1, ax  = [0, 1, 0,], w = 4, lr = .1, n = nameSpace + 'nrb_ArmUp' +  side + 'Plane')[0]
        cmds.setAttr(upArmPlane + '.ty', 6)
        cmds.setAttr(upArmPlane + '.tz', -.24)
        if side == 'LF' :
            cmds.setAttr(upArmPlane + '.tx', 4)
            cmds.setAttr(upArmPlane + '.ry', 7 )
            cmds.setAttr(upArmPlane + '.sx', 1.26 )

        else: 
            cmds.setAttr(upArmPlane + '.tx', -4)
            cmds.setAttr(upArmPlane + '.ry', -7 )
            cmds.setAttr(upArmPlane + '.sx', -1.26 )

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(upArmPlane, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(upArmPlane + 'Shape.template', 1)
        cmds.parent(upArmPlane, grpArmEX)

        


        utils.joint2Curve(nameSpace, obj = 'Clav', crv = crv_Shoulder, partName = '_Move' + side, parent = grpJoints, skipEnds = True)
        jpos = utils.pfx_JointList(pfx = nameSpace + 'jntClav_Move' + side)
        utils.joint2Curve_Controls(nameSpace, obj = 'Clav', jpos = jpos, partName = '_Move' + side, parent = armAll, rotations = False)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv_Shoulder, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(crv_Shoulder + '.template', 1)

          


        cmds.parent(nameSpace + obj + 'Dn' + '_Move' + side + '01', nameSpace + 'ArmUp_Move' + side + '02')
        cmds.parent(nameSpace + 'ArmUp_Move' + side + '01', nameSpace + 'Clav_Move' + side + '02')
        cmds.setAttr(nameSpace + obj + 'Dn' + '_Move' + side + '01.v', 0)
        cmds.setAttr(nameSpace + 'ArmUp_Move' + side + '01.v', 0)

        elb = cmds.rename(nameSpace + 'ArmUp_Move' + side + '02',nameSpace + 'ElbowJpos' + side)
        wst = cmds.rename(nameSpace + obj + 'Dn' + '_Move' + side + '02',nameSpace + 'WristJpos' + side)
        arm = cmds.rename(nameSpace + 'Clav_Move' + side + '02',nameSpace + 'ArmJpos' + side)
        clav = cmds.rename(nameSpace + 'Clav_Move' + side + '01',nameSpace + 'ClavJpos' + side)


        cmds.aimConstraint(elb, nameSpace + 'jntArmUp_Move' + side + '01',mo = 1)
        cmds.aimConstraint(elb, nameSpace + 'jnt' + obj + 'Dn' + '_Move' + side + '02',mo = 1)
        cmds.aimConstraint(wst, nameSpace + 'jnt' + obj + 'Dn' + '_Move' + side + '01',mo = 1)
        cmds.aimConstraint(arm, nameSpace + 'jntArmUp_Move' + side + '02',mo = 1)
        cmds.aimConstraint(arm, nameSpace + 'jntClav_Move' + side + '01',mo = 1)
        cmds.aimConstraint(clav, nameSpace + 'jntClav_Move' + side + '02',mo = 1)



        #creates pole vector for knee
        elbowLoc = cmds.spaceLocator(n=nameSpace + 'ElbowPole_loc' + side)[0]
        cmds.setAttr( elbowLoc + '.ty',6)
        cmds.setAttr( elbowLoc + '.tz',-10)
        cmds.makeIdentity(apply=1)

        cmds.parent(elbowLoc, elb)
        cmds.setAttr(elbowLoc +  '.visibility', 0)
        cmds.aimConstraint(arm,wst,elb,mo=1)




        arrow = controls.arrow(nameSpace + 'ElbowArrow' + side, color = 31)
        cmds.setAttr(arrow + '.ry',180) 
        utils.snapPoint(elb, arrow)
        cmds.setAttr(arrow + '.template', 1)
        cmds.parent(arrow, elb)
        
        
        wristPointerLoc = cmds.spaceLocator(n=nameSpace + 'WristPointer' + side)[0]
        utils.snap(wst, wristPointerLoc) 
        utils.freeze(wristPointerLoc)
        if side == 'LF' :
            cmds.setAttr(wristPointerLoc + '.tx', 1)
            cmds.setAttr( elbowLoc + '.tx',6)

        else :
            cmds.setAttr(wristPointerLoc + '.tx', -1)
            cmds.setAttr( elbowLoc + '.tx',-6)

        cmds.parent(wristPointerLoc, wst) 
        cmds.setAttr(wristPointerLoc + '.v', 0)

        cmds.setAttr(armAll + '.ty', 7)

        wst = nameSpace + 'Wrist_Move' + side          
        hand = nameSpace + 'HandMove' + side
        arm = nameSpace + 'WristJpos' + side

        if cmds.objExists(hand) == True:
            mel.eval('addAttr -ln "Quad"  -at double  -min 0 -max 1 -dv 0 ' + arm + ';')
            mel.eval('setAttr -e-keyable true ' + arm + '.Quad;')
            cmds.connectAttr(arm + '.Quad', hand + '.Quad')
            utils.snap(arm,hand)
            utils.snap(arm,wst)
            cmds.parentConstraint(arm, hand, mo=1)
            cmds.setAttr(hand + 'Shape.template', 1)


        if cmds.objExists(nameSpace + 'SpineMove') :
            grp = cmds.group(nameSpace + 'Arm_Move' + side, n = nameSpace + 'grpArm_Move' + side)
            utils.snapPivot(nameSpace + 'Arm_Move' + side, grp)
            cmds.pointConstraint(nameSpace + 'Spine_Move03',grp , mo = 1)
            cmds.scaleConstraint(nameSpace + 'Spine_Move03',grp, mo = 1)
            
            
        print "Arm Movers Built Successfully!"

    else:
        print "Duplcate item may exist"
    
    
    
    


################################
#
#          LEG MOVER
# 
################################
'''
Comments: 
'''
def legMove(self, nameSpace, side):
    
    if utils.checkDuplicate( nameSpace + "Leg_Move" + side) == False :

    
        utils.legMoveBuilder(nameSpace, side, obj = 'Leg')


        if utils.checkDuplicate( nameSpace + "FootMove" +  side) == True :
            utils.snapPoint(nameSpace + 'AnkleJpos' + side,nameSpace + 'FootMove' + side)
            utils.snapPoint(nameSpace + 'AnkleJpos' + side,nameSpace + 'Ankle_Move' + side)
            cmds.parentConstraint(nameSpace + 'Ankle_Move' + side, nameSpace + 'AnkleJpos' + side, mo=1)
            cmds.setAttr(nameSpace + 'AnkleJpos' + side + '.v', 0)
            utils.freeze(nameSpace + 'FootMove' + side)

        if cmds.objExists(nameSpace + 'Leg_Move' + side) :
            grp = cmds.group(nameSpace + 'Leg_Move' + side, n = nameSpace + 'grpLegMove' + side)
            utils.snapPivot(nameSpace + 'Leg_Move' + side, grp)
            cmds.pointConstraint(nameSpace + 'SpineMove',grp, mo = 1 )
            cmds.scaleConstraint(nameSpace + 'SpineMove',grp, mo = 1)
                            
        print "Leg Movers Built Successfully!"

    else:
        print "Duplcate item may exist"

################################
#
#          TAIL MOVER
# 
################################
'''
Comments: 
'''
def tailMove(self, nameSpace):
    
    if utils.checkDuplicate( nameSpace + "TailBaseMove") == False :


        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        

        base = controls.ring(nameSpace + 'TailBaseMove', size = '3')
        cmds.setAttr(base + '.rx', 90)

        crv_Tail = nameSpace + "crv_Tail"
        cmds.curve(n=crv_Tail, ep=[(0,0,0),(0,5,0)])
        cmds.setAttr(crv_Tail + '.rx', -90)

        cmds.rebuildCurve( rt=0, s=3 )

        cmds.parent(base, character)


        # puts joints on curve
        utils.joint2Curve(nameSpace, obj = 'Tail', crv = crv_Tail, partName = '_Move', parent = grpJoints)
        jpos = utils.pfx_JointList(pfx = nameSpace + 'jntTail_Move')
        utils.joint2Curve_Controls(nameSpace, obj = 'Tail', jpos = jpos, partName = '_Move', parent = base)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(crv_Tail, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(crv_Tail + '.v',0)
        
        #locator for tail mid
        tailLoc = cmds.spaceLocator(n= nameSpace + 'locTailMid')[0]
        cmds.setAttr(tailLoc + '.translateY',2.5)
        cmds.setAttr(tailLoc + '.translateZ',-2)
        cmds.setAttr(tailLoc + '.v',0)
        cmds.select(tailLoc)
        cmds.makeIdentity(apply=1)
        cmds.pointConstraint(jpos[1], jpos[3], tailLoc, mo=1)
        cmds.parent(tailLoc, base)

        #adds nurbs plane to setup for other tail options
        
        tailPlane = cmds.nurbsPlane(u = 4, ax  = [0, 1, 0,], w = 6, lr = .2, n = nameSpace + 'nrb_' + 'TailPlane')[0]
        cmds.setAttr(tailPlane + '.ry', 90)
        cmds.setAttr(tailPlane + '.tz', -3)

        cmds.select(cl=1)
        for item in jpos :
            cmds.select(item, add=1)
            cmds.setAttr(item + '.v',0)
            
        cmds.select(tailPlane, add=1)
            
        cmds.skinCluster(mi=1,dr=1)

        cmds.setAttr(tailPlane + 'Shape.template', 1)

        cmds.setAttr(nameSpace + 'TailBaseMove.ty',10)
        
        
        cmds.setAttr(nameSpace + 'TailBaseMove.tz',-3)
        cmds.setAttr(nameSpace + 'TailBaseMove.sx',.8)
        cmds.setAttr(nameSpace + 'TailBaseMove.sy',.8)
        cmds.setAttr(nameSpace + 'TailBaseMove.sz',.8)
        
        cmds.parent(base, nameSpace + 'SpineMove')
        
        grpTailEX = cmds.group(n = nameSpace + 'grp_TailEX', em = 1)
        cmds.parent(grpTailEX, grpEx)
        cmds.parent(crv_Tail, grpTailEX)
        cmds.parent(tailPlane, grpTailEX)


                
        print "Tail Movers Built Successfully!"

    else:
        print "Duplcate item may exist"



################################
#
#          HAND MOVER
# 
################################
'''
Comments: 
'''



def handMove(self, nameSpace, side) :
    

    
    if utils.checkDuplicate( nameSpace + "HandMove" +  side) == False :

            
        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        

        hand = controls.square(nameSpace + 'HandMove' + side)
        if side == 'LF' :        
            cmds.setAttr(hand + '.tx', 1)
            cmds.setAttr(hand + '.tz', .5)
            cmds.setAttr(hand + '.ty', .25)
            cmds.setAttr(hand + '.sx', 1.3)
            cmds.setAttr(hand + '.sy', 1.3)
            cmds.setAttr(hand + '.sz', 1.3)
       
        if side == 'RT' :        
            cmds.setAttr(hand + '.tz', .5)
            cmds.setAttr(hand + '.ty', .25)
            cmds.setAttr(hand + '.sx', 1.3)
            cmds.setAttr(hand + '.sy', 1.3)
            cmds.setAttr(hand + '.sz', 1.3)    
            
        utils.freeze(hand)
        
        wst = controls.sphere(nameSpace + 'Wrist_Move' + side, size = .2, color = '')
        cmds.parent(wst, hand)


        ball = controls.sphere(nameSpace + 'FrontBall_Move' + side, size = .2, color = '')
        cmds.parent(ball, hand)
        
        if side == 'LF' :        
            cmds.setAttr(ball + '.tx', .5)
        else :
            cmds.setAttr(ball + '.tx', -.5)

        
        toe = controls.sphere(nameSpace + 'FrontToe_Move' + side, size = .2, color = '')
        cmds.parent(toe, hand)
        
        if side == 'LF' :        
            cmds.setAttr(toe + '.tx', 1)
        else :
            cmds.setAttr(toe + '.tx', -1)



       
        #adds locators for extra controls
        fingBall =  cmds.spaceLocator(n= nameSpace + 'hand' + side + 'Ball_loc')[0]
        utils.snap(hand,fingBall)
        utils.freeze(fingBall)      
        cmds.setAttr(fingBall + '.ty',.5)   
        cmds.parent(fingBall,hand)  
        cmds.setAttr(fingBall + '.v',0)
        
        
        
        back = cmds.spaceLocator(n=nameSpace + 'handBack_loc' + side)[0]
        utils.snap(hand,back)
        utils.freeze(back)
        cmds.setAttr(back + '.tz',-.5)
        cmds.parent(back,hand)  
        cmds.setAttr(back + '.overrideEnabled',1)
        cmds.setAttr(back + '.overrideColor',4)
        
        
        front = cmds.spaceLocator(n=nameSpace + 'handFront_loc' + side)[0]
        utils.snap(hand,front)
        utils.freeze(front)
        cmds.setAttr(front + '.tz',.5)
        cmds.parent(front,hand)  
        cmds.setAttr(front + '.overrideEnabled',1)
        cmds.setAttr(front + '.overrideColor',4)
        
        
        heel = cmds.spaceLocator(n=nameSpace + 'FrontHeel_loc' + side)[0]
        utils.snap(hand,heel)
        utils.freeze(heel)
        if side == 'LF' :
            cmds.setAttr(heel + '.tx',1.25)
        else: 
            cmds.setAttr(heel + '.tx',-1.25)

        cmds.parent(heel,hand)  
        cmds.setAttr(heel + '.overrideEnabled',1)
        cmds.setAttr(heel + '.overrideColor',4)

        toeLoc = cmds.spaceLocator(n=nameSpace + 'FrontToe_loc' + side)[0]
        utils.snap(hand,toeLoc)
        utils.freeze(toeLoc)
        if side == 'LF' :
            cmds.setAttr(toeLoc + '.tx',-.3)
        else: 
            cmds.setAttr(toeLoc + '.tx',.3)
            
        cmds.parent(toeLoc,hand)  
        cmds.setAttr(toeLoc + '.overrideEnabled',1)
        cmds.setAttr(toeLoc + '.overrideColor',4)
        
        
        
        
        
        cmds.parent(hand,character)
        utils.freeze(hand)


        obj = ['Index','Middle','Ring','Pinky']
        numb = 3        
        
        utils.fingerMove(nameSpace, obj, side, numb, base = wst)
        
        obj = ['Thumb']
        numb = 3        
        utils.fingerMove(nameSpace, obj, side, numb, base = wst, thumb = True)
        
        

        #quadSwitch
        mel.eval('addAttr -ln "Quad"  -at double  -min 0 -max 1 -dv 0 ' + hand + ';')
        mel.eval('setAttr -e-keyable true ' + hand + '.Quad;')
        
        cmds.connectAttr(hand + '.Quad', heel + '.v')
        cmds.connectAttr(hand + '.Quad', toeLoc + '.v')
        cmds.connectAttr(hand + '.Quad', ball + '.v')
        cmds.connectAttr(hand + '.Quad', toe + '.v')
        
        mel.eval('setAttr -lock true -keyable false -channelBox false "' + heel + '.v";')
        mel.eval('setAttr -lock true -keyable false -channelBox false "' + toeLoc + '.v";')
        mel.eval('setAttr -lock true -keyable false -channelBox false "' + ball + '.v";')
        mel.eval('setAttr -lock true -keyable false -channelBox false "' + toe + '.v";')
        





        arm = nameSpace + 'WristJpos' + side
        
        if cmds.objExists(arm) == True:
            try:
                mel.eval('addAttr -ln "Quad"  -at double  -min 0 -max 1 -dv 0 ' + arm + ';')
                mel.eval('setAttr -e-keyable true ' + arm + '.Quad;')
            except:
                pass
            cmds.connectAttr(arm + '.Quad', hand + '.Quad')
            utils.snap(arm,hand)
            utils.snap(arm,wst)
            cmds.parentConstraint(arm, hand, mo=1)
            cmds.setAttr(hand + 'Shape.template', 1)
            

                
        print "Hand" + side + "Movers Built Successfully!"

    else:
        print "Duplcate item may exist"
        
            
################################
#
#          FOOT MOVER
# 
################################
'''
Comments: 
'''

def footMove(self, nameSpace, side) :
    

    
    if utils.checkDuplicate( nameSpace + "FootMove" +  side) == False :


        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        

        foot = controls.square(nameSpace + 'FootMove' + side)
        cmds.setAttr(foot + '.tx', .25)
        cmds.setAttr(foot + '.tz', .5)
        cmds.setAttr(foot + '.sx', 2.5)
        utils.freeze(foot)
        
        ank = controls.sphere(nameSpace + 'Ankle_Move' + side, size = .2, color = '')
        cmds.parent(ank, foot)
        cmds.setAttr(ank + '.tx', -1)

        ball = controls.sphere(nameSpace + 'Ball_Move' + side, size = .2, color = '')
        cmds.parent(ball, foot)
        
        cmds.setAttr(ball + '.tx', .5)
        
        toe = controls.sphere(nameSpace + 'Toe_Move' + side, size = .2, color = '')
        cmds.parent(toe, foot)
        
        cmds.setAttr(toe + '.tx', 1)

        if side == 'LF':
            outside = cmds.spaceLocator(n=nameSpace + 'footBack_loc' + side)[0]
        else:
            outside = cmds.spaceLocator(n=nameSpace + 'footFront_loc' + side)[0]
        utils.snap(foot,outside)
        utils.freeze(outside)
        cmds.setAttr(outside + '.tz',-.5)
        cmds.parent(outside,foot)  
        cmds.setAttr(outside + '.overrideEnabled',1)
        cmds.setAttr(outside + '.overrideColor',4)
        
        if side == 'LF':
            inside = cmds.spaceLocator(n=nameSpace + 'footFront_loc' + side)[0]
        else:
            inside = cmds.spaceLocator(n=nameSpace + 'footBack_loc' + side)[0]
            
        utils.snap(foot,inside)
        utils.freeze(inside)
        cmds.setAttr(inside + '.tz',.5)
        cmds.parent(inside,foot)  
        cmds.setAttr(inside + '.overrideEnabled',1)
        cmds.setAttr(inside + '.overrideColor',4)
        
        '''
        heel = cmds.spaceLocator(n=nameSpace + 'heel_loc' + side)[0]
        utils.snap(foot,heel)
        utils.freeze(heel)
        cmds.setAttr(heel + '.tx',-1.25)
        cmds.parent(heel,foot)  
        cmds.setAttr(heel + '.overrideEnabled',1)
        cmds.setAttr(heel + '.overrideColor',4)

        toe = cmds.spaceLocator(n=nameSpace + 'toe_loc' + side)[0]
        utils.snap(foot,toe)
        utils.freeze(toe)
        cmds.setAttr(toe + '.tx',1.25)
        cmds.parent(toe,foot)  
        cmds.setAttr(toe + '.overrideEnabled',1)
        cmds.setAttr(toe + '.overrideColor',4)
        '''

        cmds.setAttr(foot + '.ry', -90)
        cmds.parent(foot,character)
        utils.freeze(foot)
        
        leg = nameSpace + 'AnkleJpos' + side
        
        if cmds.objExists(leg) == True:
            utils.snapPoint(leg,foot)
            utils.snapPoint(leg,ank)
            cmds.parentConstraint(ank, leg, mo=1)
            cmds.setAttr(leg + '.v', 0)
            utils.freeze(foot)

        
                
        print "Foot" + side + "Movers Built Successfully!"

    else:
        print "Duplcate item may exist"
        
                

################################
#
#          TOE MOVER
# 
################################
'''
Comments: 
'''


def toeMove(self, nameSpace, side) :
    
    
    
    if utils.checkDuplicate( nameSpace + "ToeMove" +  side) == False :


        world = nameSpace + 'World_Move'
        character = nameSpace + 'Character_Move'
        grpJoints = nameSpace + 'grpJoints_Move'
        grpEx = nameSpace + 'grpEX_Move'
        

        toe = controls.square(nameSpace + 'ToeMove' + side)
        cmds.setAttr(toe + '.tx', .25)
        cmds.setAttr(toe + '.tz', .5)
        cmds.setAttr(toe + '.sx', 2.5)
        utils.freeze(toe)


        obj = ['Index_Toe','Middle_Toe','Ring_Toe','Pinky_Toe']
        numb = 3        

        utils.fingerMove(nameSpace, obj, side, numb, base = toe)

        obj = ['Thumb_Toe']
        numb = 3        
        utils.thumbMove(nameSpace, obj, side, numb, base = toe)
        
        

       
        #adds locators for extra controls
        ball =  cmds.spaceLocator(n= nameSpace + 'toe' + side + 'Ball_loc')[0]
        utils.snap(toe,ball)
        utils.freeze(ball)      
        cmds.setAttr(ball + '.ty',.5)   
        cmds.parent(ball,toe)  
        cmds.setAttr(ball + '.v',0)
        
        if side == 'LF' :
            cmds.setAttr(toe + '.ry', -90)
        else: 
            cmds.setAttr(toe + '.ry', 90)

        cmds.parent(toe,character)
        
        utils.freeze(toe)

        
        
        ank = nameSpace + 'Ball_Move' + side
        
        if cmds.objExists(ank) == True:
            utils.snapPoint(ank,toe)
            cmds.parentConstraint(ank, toe, mo=1)
            cmds.setAttr(toe + 'Shape.lodVisibility', 0)
        
        
                
        print "Toe" + side + "Movers Built Successfully!"

    else:
        print "Duplcate item may exist"
        

################################
#
#          PRESETS
# 
################################
'''
Comments: presets like "Quad" have their attr settings here
'''

def quadSet(self, nameSpace) :
       
        
        
    cmds.setAttr(nameSpace + 'SpineMove.ty', 11)
    cmds.setAttr(nameSpace + 'SpineMove.rx', 90)
    cmds.setAttr(nameSpace + 'SpineMove.sx', 1.5)
    cmds.setAttr(nameSpace + 'SpineMove.sy', 1.5)
    cmds.setAttr(nameSpace + 'SpineMove.sz', 1.5)  
    
    cmds.setAttr(nameSpace + 'TailBaseMove.rx', 0)
    cmds.setAttr(nameSpace + 'TailBaseMove.tz', 0)
    cmds.setAttr(nameSpace + 'TailBaseMove.ty', -1)
    
    cmds.setAttr(nameSpace + 'Arm_MoveLF.tx', 0)
    cmds.setAttr(nameSpace + 'Arm_MoveLF.ty', 7.5)
    cmds.setAttr(nameSpace + 'Arm_MoveLF.tz', 0)
    cmds.setAttr(nameSpace + 'Arm_MoveLF.rx', 0)
    cmds.setAttr(nameSpace + 'Arm_MoveLF.ry', 0)
    cmds.setAttr(nameSpace + 'Arm_MoveLF.rz', -90)
    
    cmds.select(nameSpace + 'Arm_MoveLF')
    utils.mirror()
    
    cmds.setAttr(nameSpace + 'WristJposLF.tx', -.25)
    cmds.setAttr(nameSpace + 'WristJposLF.ty', 0)
    cmds.setAttr(nameSpace + 'WristJposLF.tz', 0)
    cmds.setAttr(nameSpace + 'WristJposLF.rx', 90)
    cmds.setAttr(nameSpace + 'WristJposLF.ry', -90)
    cmds.setAttr(nameSpace + 'WristJposLF.rz', 0)
    cmds.setAttr(nameSpace + 'WristJposLF.Quad', 1)

    cmds.select(nameSpace + 'WristJposLF')
    utils.mirror()

    

    
    
    
    
##########################################################
##########################################################
##########################################################
#
#
#                   BUILT BODY RIG
#
#
##########################################################
##########################################################
##########################################################
'''
Comments: Contains all body rigging fuctions unless otherwise noted
'''

################################
#
#          NECK RIG
# 
################################
'''
Comments: Spline based neck rig. Much like the spine
'''

def neckRig(self, nameSpace) :
    
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'

    crv = nameSpace + 'crv_Neck'
    obj = 'Neck'
    
    move = nameSpace + '' + obj + 'Move'

    if cmds.objExists(move) == True:

        #base joint building
        cmds.select(crv)
        cmds.DeleteHistory()
        cmds.rebuildCurve( rt=0, s=3 )

        utils.joint2Curve(nameSpace, obj = obj, crv = crv, pfx = 'skn_', partName = '_Skinned',  parent = grpJoints, skipEnds = True, chain = True)
        utils.IKSpline(nameSpace, obj, crv, spineType = 2, baseControls = False, ring = True)
        cmds.rename(nameSpace + 'NeckTop', nameSpace + 'HeadIK')
        cmds.setAttr(nameSpace + 'grpNeckTop.ry', 0 )
        cmds.rename(nameSpace + 'NeckBottom', nameSpace + 'NeckFK')
        chainIK = utils.pfx_JointList(pfx = nameSpace + 'ik_' + obj)
        chainSkin = utils.pfx_JointList(pfx = nameSpace + 'skn_' + obj)
        spineSkin = utils.pfx_JointList(pfx = nameSpace + 'skn_' + 'Spine')
        utils.snapPivot( nameSpace + 'ChestIK',nameSpace + 'grpNeckBottom')
        

        count = 1
        for item in chainSkin :
            index = chainSkin.index(item)
            control = controls.ring(nameSpace + obj + '_Adjust' + str(count), size = 1, color = 31)
            cGrp = cmds.group(control, n = nameSpace + 'grp' + obj + '_Adjust' + str(count))
            utils.snapPoint(item, cGrp)
            utils.snapPivot(item, cGrp)
            cmds.parent(cGrp, chainIK[index])


            jGrp = cmds.group(item, n = nameSpace + 'grp' + obj + '_Result' + str(count))
            utils.snapPivot(item, jGrp)
            cmds.parent(jGrp, control)

            
            count = count + 1


        chainAdj = utils.pfx_ControlList(pfx = nameSpace + obj + '_Adjust')
        cmds.addAttr(nameSpace + 'HeadIK', ln  =  'SubControls', at =  'double', min = 0, max = 1, dv = 0)
        cmds.setAttr(nameSpace + 'HeadIK' + '.SubControls', e = True, keyable = True)
        for item in chainAdj :
            cmds.connectAttr(nameSpace + 'HeadIK' + '.SubControls', item + '.v')
        
        
        headLoc = cmds.spaceLocator(n = nameSpace + obj + 'PointLoc_Spine')[0]
        worldLoc = cmds.spaceLocator(n = nameSpace + obj + 'PointLoc_World')[0]
        utils.snap( nameSpace + 'HeadIK', headLoc)
        utils.snap( nameSpace + 'HeadIK', worldLoc)

        
        chainFK = utils.pfx_ControlList(pfx = nameSpace + 'Spine' + 'FK')
        cmds.parent(headLoc, nameSpace + 'NeckFK')
        grpHead = cmds.group(nameSpace + 'HeadIK', n = nameSpace + 'grpHeadIK')
        
        
        cmds.orientConstraint(headLoc,worldLoc,grpHead, mo = 1)
        cmds.addAttr(nameSpace +'HeadIK', ln  =  'IsolateRotation', at =  'double', min = 0, max = 1, dv = 1)
        cmds.setAttr(nameSpace +'HeadIK' + '.IsolateRotation', e = True, keyable = True)
        
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_orientConstraint1.' + nameSpace + 'NeckPointLoc_SpineW0',cd=nameSpace + 'HeadIK' + '.IsolateRotation',dv=0,v=1) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_orientConstraint1.' + nameSpace + 'NeckPointLoc_WorldW1',cd=nameSpace + 'HeadIK' + '.IsolateRotation',dv=0,v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_orientConstraint1.' + nameSpace + 'NeckPointLoc_SpineW0',cd=nameSpace + 'HeadIK' + '.IsolateRotation',dv=1,v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_orientConstraint1.' + nameSpace + 'NeckPointLoc_WorldW1',cd=nameSpace + 'HeadIK' + '.IsolateRotation',dv=1,v=1) 

        cmds.pointConstraint(headLoc,worldLoc,grpHead, mo = 1)
        cmds.addAttr(nameSpace +'HeadIK', ln  =  'IsolateTranslation', at =  'double', min = 0, max = 1, dv = 0)
        cmds.setAttr(nameSpace +'HeadIK' + '.IsolateTranslation', e = True, keyable = True)
        
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_pointConstraint1.' + nameSpace + 'NeckPointLoc_SpineW0',cd=nameSpace + 'HeadIK' + '.IsolateTranslation',dv=0,v=1) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_pointConstraint1.' + nameSpace + 'NeckPointLoc_WorldW1',cd=nameSpace + 'HeadIK' + '.IsolateTranslation',dv=0,v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_pointConstraint1.' + nameSpace + 'NeckPointLoc_SpineW0',cd=nameSpace + 'HeadIK' + '.IsolateTranslation',dv=1,v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'grpHeadIK_pointConstraint1.' + nameSpace + 'NeckPointLoc_WorldW1',cd=nameSpace + 'HeadIK' + '.IsolateTranslation',dv=1,v=1) 
        
        
        if cmds.objExists(nameSpace + 'Spine') :
            rotLoc = cmds.spaceLocator(n = nameSpace + obj + 'RotLoc_Spine')[0]
            utils.snap(spineSkin[-1], rotLoc)
            neckRot = cmds.createNode('plusMinusAverage', n = nameSpace + obj + 'Rot_Add')
            cmds.connectAttr(rotLoc + '.rx', neckRot + '.input1D[0]', f = 1)
            cmds.connectAttr(nameSpace + 'NeckFK' + '.rx', neckRot + '.input1D[1]', f = 1)
            cmds.connectAttr( neckRot + '.output1D', nameSpace + 'NeckIKHandle.roll', f = 1)
            cmds.connectAttr( neckRot + '.output1D', nameSpace + 'NeckBottom_rx_Reverse_Mult.input1X', f = 1)
            cmds.parentConstraint(spineSkin[-1], rotLoc, mo = 1)
            cmds.parent(rotLoc, nameSpace + 'SpineSub')
            
            neckGrp = nameSpace + 'grpNeckBottom'
            cmds.pointConstraint(nameSpace + 'ChestIK', chainFK[-1] , neckGrp , mo = 1)
            cmds.orientConstraint(nameSpace + 'ChestIK', chainFK[-1] , neckGrp, mo = 1)
            
            cmds.setAttr(nameSpace + 'Spine.SpineSwitch', 0)
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_pointConstraint1.' +  nameSpace + 'ChestIKW0',cd= nameSpace + 'Spine' + '.SpineSwitch',dv=0,v=1) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_pointConstraint1.' +  chainFK[-1] + 'W1',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=0,v=0) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_orientConstraint1.' + nameSpace + 'ChestIKW0',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=0,v=1) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_orientConstraint1.' +  chainFK[-1] + 'W1',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=0,v=0) 
            cmds.setAttr(nameSpace + 'Spine.SpineSwitch', 1)
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_pointConstraint1.' + nameSpace + 'ChestIKW0',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=1,v=0) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_pointConstraint1.' +  chainFK[-1] + 'W1',cd= nameSpace +'Spine' + '.SpineSwitch',dv=1,v=1) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_orientConstraint1.' + nameSpace + 'ChestIKW0',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=1,v=0) 
            cmds.setDrivenKeyframe (nameSpace +  'grpNeckBottom' + '_orientConstraint1.' +  chainFK[-1] + 'W1',cd=  nameSpace +'Spine' + '.SpineSwitch',dv=1,v=1) 
            cmds.setAttr(nameSpace + 'Spine.SpineSwitch', 0)

            blendIso = cmds.createNode('blendColors', n = nameSpace + 'NeckIsolate_Twist_Blend')
            cmds.connectAttr(nameSpace + 'Neck_RollSubtract.output1D', blendIso + '.color1R', f = 1)
            cmds.connectAttr(nameSpace + 'HeadIK.IsolateRotation', blendIso + '.blender', f = 1)           
            cmds.connectAttr( blendIso + '.outputR', nameSpace + 'NeckIKHandle.twist', f = 1)
            
            addIso = cmds.createNode('plusMinusAverage', n = nameSpace + 'NeckIsolate_Twist_Add')
            cmds.connectAttr(nameSpace + 'HeadIK.rx', addIso + '.input1D[0]', f = 1)
            cmds.setAttr(addIso + '.input1D[1]', -90)
            cmds.connectAttr( addIso + '.output1D', blendIso + '.color2R',f = 1)

            
            cmds.parent(worldLoc, nameSpace + 'Spine')
            cmds.parent( nameSpace + 'grpNeckJoints_IK', nameSpace +  'grpNeckControlsIK', nameSpace + 'grp' + obj + 'Joints', nameSpace + 'SpineSub' )
            
        cmds.delete(nameSpace + 'NeckMove', nameSpace + 'grpNeckJoints_Skinned')

        hide = [nameSpace +  ' grpNeckJoints', worldLoc,headLoc, rotLoc]
        for item in hide :
            try:
                cmds.select(item)
                utils.hide()
            except:
                pass

        chainAdj = utils.pfx_ControlList(pfx = nameSpace + obj + '_Adjust')
        IK = [nameSpace + 'HeadIK', nameSpace + 'NeckFK',nameSpace + obj + 'Mid']

        utils.lockAttr(IK, vis = True)
        utils.lockAttr(chainAdj, vis = True)
    
    
        try: 
            cmds.parent(nameSpace + 'grp_' + obj + 'EX' + side, grpEx)
        except:
            pass    

        try:
            cmds.parentConstraint( nameSpace + 'HeadIK',nameSpace + 'SkullMove', mo = 1)
            cmds.scaleConstraint( nameSpace + 'HeadIK', nameSpace + 'SkullMove',mo = 1)
        except:
            pass
            
            
################################
#
#          SPINE RIG
# 
################################
'''
Comments: Spline based spine rig. Much like the neck
'''

def spineRig(self, nameSpace) :
    
    
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'

    crv = nameSpace + 'crv_Spine'
    obj = 'Spine'

    move = nameSpace + '' + obj + 'Move'

    if cmds.objExists(move) == True:
        
        #base joint building
        cmds.select(crv)
        cmds.DeleteHistory()
        cmds.rebuildCurve( rt=0, s=5 )

        utils.joint2Curve(nameSpace, obj = obj, crv = crv, pfx = 'skn_', partName = '_Skinned',  parent = grpJoints, skipEnds = True, chain = True)
        utils.joint2Curve(nameSpace, obj = obj, crv = crv, pfx = 'res_', partName = '_Result',  parent = grpJoints, skipEnds = True, chain = True)
        utils.FKChain(nameSpace, obj, crv, spineType = 2)
        utils.IKSpline(nameSpace, obj, crv, spineType = 2)
        cmds.rename(nameSpace + 'SpineTop', nameSpace + 'ChestIK')
        cmds.rename(nameSpace + 'SpineBottom', nameSpace + 'HipsIK')

        chainFK = utils.pfx_JointList(pfx = nameSpace + 'fk_' + obj)
        chainIK = utils.pfx_JointList(pfx = nameSpace + 'ik_' + obj)
        chainResult = utils.pfx_JointList(pfx = nameSpace + 'res_' + obj)
        chainSkin = utils.pfx_JointList(pfx = nameSpace + 'skn_' + obj)

        utils.listBlender(nameSpace, obj, list1 = chainFK, list2 = chainIK, list3 = chainResult, switch = nameSpace + obj)

        chainFK = utils.pfx_ControlList(pfx = nameSpace + obj + 'FK')
        for item in chainFK :
            cmds.connectAttr(nameSpace + obj + '.' + obj + 'Switch', item + '.v', f = 1)

        cmds.setDrivenKeyframe (nameSpace + 'ChestIK',cd=nameSpace + obj + '.SpineSwitch',dv=1,attribute='.v',v=0) 
        cmds.setDrivenKeyframe (nameSpace + obj + 'Mid',cd=nameSpace + obj + '.SpineSwitch',dv=1,attribute='.v',v=0) 
        cmds.setDrivenKeyframe (nameSpace + 'HipsIK',cd=nameSpace  +obj + '.SpineSwitch',dv=1,attribute='.v',v=0) 


        cmds.setDrivenKeyframe (nameSpace + 'ChestIK',cd=nameSpace + obj + '.SpineSwitch',dv=0,attribute='.v',v=1) 
        cmds.setDrivenKeyframe (nameSpace + obj + 'Mid',cd=nameSpace + obj + '.SpineSwitch',dv=0,attribute='.v',v=1) 
        cmds.setDrivenKeyframe (nameSpace + 'HipsIK',cd=nameSpace + obj + '.SpineSwitch',dv=0,attribute='.v',v=1) 



        count = 1
        for item in chainSkin :
            index = chainSkin.index(item)
            control = controls.ring(nameSpace + obj + '_Adjust' + str(count), size = 2, color = 25)
            cmds.setAttr(control + '.rz', 90)
            utils.freeze(control)
            cGrp = cmds.group(control, n = nameSpace + 'grp' + obj + '_Adjust' + str(count))
            utils.snap(item, cGrp)
            utils.snapPivot(item, cGrp)
            cmds.parent(cGrp, chainResult[index])


            jGrp = cmds.group(item, n = nameSpace + obj + 'grp' + obj + '_Result' + str(count))
            utils.snapPivot(item, jGrp)
            cmds.parent(jGrp, control)

            
            count = count + 1


        chainAdj = utils.pfx_ControlList(pfx = nameSpace + obj + '_Adjust')
        cmds.addAttr(nameSpace + obj, ln  =  'SubControls', at =  'double', min = 0, max = 1, dv = 0)
        cmds.setAttr(nameSpace + obj + '.SubControls', e = True, keyable = True)
        for item in chainAdj :
            cmds.connectAttr(nameSpace + obj + '.SubControls', item + '.v')


        cmds.parent(nameSpace + 'grp' + obj + 'Joints_Result',nameSpace + 'grp' + obj + 'Joints_Skinned', nameSpace + 'grp' + obj + 'Joints_IK', nameSpace + 'grp' + obj + 'Joints_FK',nameSpace + 'grp' + obj + 'Joints_Result', nameSpace + 'grpSpineJoints')
        cmds.rename(nameSpace + 'grp' + obj + 'FK_1', nameSpace + 'grp' + obj + 'ControlsFK') 
        cmds.group(nameSpace + 'grpSpineControlsFK', nameSpace +  'grpSpineControlsIK', n = nameSpace + 'grpSpineControls')
        cmds.delete(nameSpace + 'grpSpineJoints_Skinned')

        cmds.select(nameSpace + ' SpineInfleunceIK',nameSpace +  ' grpSpineJoints_FK',nameSpace +  ' grpSpineJoints_IK')
        utils.hide()


        chainFK = utils.pfx_ControlList(pfx = nameSpace + obj + 'FK')
        IK = [nameSpace + 'ChestIK', nameSpace + 'HipsIK',nameSpace + obj + 'Mid',nameSpace + obj, nameSpace + obj + 'Sub',]

        utils.lockAttr(chainFK, vis = True, scale = True)
        utils.lockAttr(IK, vis = True, scale = True)
        utils.lockAttr(chainAdj, vis = True)
        
        try: 
            cmds.parent(nameSpace + 'grp_' + obj + 'EX' + side, grpEx)
        except:
            pass    

################################
#
#          ARMS RIG
# 
################################
'''
Comments: Spline based spine rig. Much like the neck
'''

def armRig(self, nameSpace, side) :

    nameList = ['Start','Mid','End']
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    obj = 'Arm'

    if obj == 'Arm' :
        bendPoint = 'Elbow'
        endItem = 'Wrist'
    else :
        bendPoint = 'Knee'
        endItem = 'Ankle'

    move = nameSpace + '' + obj + '_Move' + side

    if cmds.objExists(move) == True:

        armJLocations = [nameSpace + obj + 'Jpos' + side,nameSpace + bendPoint + 'Jpos' + side,nameSpace + endItem + 'Jpos' + side, nameSpace + endItem + 'Pointer' + side ]
        

        IKJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  obj = obj + '_IK', side  = side, chain = True, deleteEnd = True)    
        FKJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  obj = obj + '_FK', side  = side, chain = True,deleteEnd = True)    
        resultJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  pfx = 'res_',obj = obj + '_Result', side  = side, chain = True,deleteEnd = True)    
        utils.snapPivot(IKJoints[0],nameSpace + 'grp' + obj + '_IK' + side)
        utils.snapPivot(FKJoints[0],nameSpace + 'grp' + obj + '_FK' + side)
        utils.snapPivot(resultJoints[0],nameSpace + 'grpres_' + obj + '_Result' + side)

        #creates Ik setup
        addNodes = utils.buildIK(nameSpace, obj, side, list = IKJoints, pole = '', parent = '')
        snapJnts = utils.noFlipIK_PoleVector(nameSpace, pv = nameSpace + bendPoint + 'Pole_loc' + side, side = side, parent = IKJoints[0], obj = obj) 
        utils.poleSnap(nameSpace, obj, side,addNodes = addNodes, pv = nameSpace + bendPoint +'Pole_loc' + side, list = [nameSpace + obj + '_IK01' + side, snapJnts[1] ,nameSpace +  obj + '_IK03' + side], IKJoints = IKJoints)
        #change pv color

        #creates FK setup
        
        utils.buildFKControlChainRing(nameSpace, obj, side, list = FKJoints,size = 1, direction = 1) 
        utils.addGimbal(nameSpace, list = [nameSpace + obj +'FK_3' + side,nameSpace + obj +'FK_1' + side], side = side)
        cmds.parent(nameSpace + 'grp' + obj + '_FK' + side, nameSpace + 'grpJoints')
        #IK Fk Switch
        utils.IKFKSwitch(nameSpace, obj, side, IKJoints, FKJoints, resultJoints)

        #Non-Roll limb setup
        armGrp = utils.nonRollLimb(nameSpace, side, obj, resultJoints, jnum = 4, axis = 'x')

        armUpChain = utils.pfx_JointList(pfx = nameSpace + 'twist_' + obj + 'Up' + side)
        armDnChain = utils.pfx_JointList(pfx = nameSpace + 'twist_' + obj + 'Dn' + side)
        
        if side == 'LF' :
            reverse = False
        else :
            reverse = False
            
        utils.limbRibbon(nameSpace, obj, side, upChain = armUpChain , dnChain = armDnChain, reverse = reverse)

                
        #fix FK armscale to keep Dn arm from doing strange things
        cmds.parent(nameSpace + 'grp' + obj + 'FK_2' + side, nameSpace + 'grpGimbal_' + obj + 'FK_1' + side)
        cmds.parentConstraint(nameSpace + obj + 'FK_1' + side, nameSpace + 'grp' + obj + 'FK_2' + side, mo = 1)

        allGrp = cmds.group(nameSpace + 'grpArmPoleVecor' + side,nameSpace + 'grpArmNonFlip_loc' + side,nameSpace + 'grpGimbal_ArmFK_1' + side,nameSpace + 'grpArmIK' + side,nameSpace + 'grpArm_FK' + side,nameSpace + 'grptwist_ArmUp' + side, nameSpace + 'grpArm_IK' + side, nameSpace + 'grpres_Arm_Result' + side, n = nameSpace + 'grp' + obj + '_RIG' + side)

        cmds.pointConstraint(nameSpace + obj + 'Connect_loc_' + side,allGrp, mo=1)
        clavicleRig(self, nameSpace, side)
        cmds.parent(armGrp, nameSpace + 'Clav' + side)
        clavAll = cmds.group( nameSpace +'grpskn_Clav_IK' + side, nameSpace + 'grpClav' + side,  nameSpace + 'grpClav_startLoc' + side, n = nameSpace + 'grp' + 'ClavAll' + side)
        cmds.parent(allGrp, nameSpace + 'Clav' + side)
        
        #SpaceSwitching on IK and FK
        utils.spaceSwitch(nameSpace,name = obj + 'IK', parentList = [nameSpace +'Character', nameSpace +'ChestIK', nameSpace +'HipsIK',nameSpace +'Spine', nameSpace +'HeadIK'], child = nameSpace + obj + 'IK' + side, switch = nameSpace + obj + 'Settings' + side, parentCount = 5 )
        utils.spaceSwitch(nameSpace,name = obj + 'FK', parentList = [nameSpace +'Character', nameSpace +'ChestIK',nameSpace + 'HipsIK',nameSpace +'Spine', nameSpace +'Clav' + side], child = nameSpace + 'grpGimbal_' + obj + 'FK_1' + side, switch = nameSpace + obj + 'Settings' + side, parentCount = 5, orientOnly = True )
        
        
        try: 
            cmds.parent(clavAll, nameSpace + 'res_Spine_Result06')
            cmds.parent(nameSpace + 'grp' + 'Clav' + '_Distance' + side,nameSpace + 'grp_' + obj + 'EX' + side, grpEx)
        except:
            print obj + side + ' parenting failure'  
            
            
                      
################################
#
#          LEG RIG
# 
################################
'''
Comments: Spline based spine rig. Much like the neck
'''

def legRig(self, nameSpace, side) :


    nameList = ['Start','Mid','End']
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    obj = 'Leg'
    if obj == 'Arm' :
        bendPoint = 'Elbow'
        endItem = 'Wrist'
    else :
        bendPoint = 'Knee'
        endItem = 'Ankle'

    if side == 'RT':
        color = 6
    elif side == 'LF' :
        color = 13
    else :
        color = 30
        
        
    move = nameSpace + '' + obj + '_Move' + side

    if cmds.objExists(move) == True:


        armJLocations = [nameSpace + obj + 'Jpos' + side,nameSpace + bendPoint + 'Jpos' + side,nameSpace + endItem + 'Jpos' + side, nameSpace + endItem + 'Pointer' + side ]

        IKJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  obj = obj + '_IK', side  = side, chain = True, deleteEnd = True)    
        FKJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  obj = obj + '_FK', side  = side, chain = True,deleteEnd = True)    
        resultJoints = utils.joints2List(nameSpace = nameSpace, list = armJLocations,  pfx = 'res_',obj = obj + '_Result', side  = side, chain = True,deleteEnd = True)    
        utils.snapPivot(IKJoints[0],nameSpace + 'grp' + obj + '_IK' + side)
        utils.snapPivot(FKJoints[0],nameSpace + 'grp' + obj + '_FK' + side)
        utils.snapPivot(resultJoints[0],nameSpace + 'grpres_' + obj + '_Result' + side)

        #creates Ik setup
        addNodes = utils.buildIK(nameSpace, obj, side, list = IKJoints, pole = '', parent = '')
        utils.freeze(nameSpace + 'grp' + obj + 'IK' + side)
        snapJnts = utils.noFlipIK_PoleVector(nameSpace, pv = nameSpace + bendPoint + 'Pole_loc' + side, side = side, parent = IKJoints[0], obj = obj) 
        utils.poleSnap(nameSpace, obj, side,addNodes = addNodes, pv = nameSpace + bendPoint +'Pole_loc' + side, list = [nameSpace + obj + '_IK01' + side, snapJnts[1] ,nameSpace +  obj + '_IK03' + side], IKJoints = IKJoints)
        #change pv color

        #creates FK setup
        utils.buildFKControlChainRing(nameSpace, obj, side, list = FKJoints,size = 1, direction = 1) 
        utils.addGimbal(nameSpace, list = [nameSpace + obj +'FK_3' + side,nameSpace + obj +'FK_1' + side], side = side)
        #IK Fk Switch
        utils.IKFKSwitch(nameSpace, obj, side, IKJoints, FKJoints, resultJoints)

        #Non-Roll limb setup
        hipGrp = utils.nonRollLimb(nameSpace, side, obj, resultJoints, jnum = 4, axis = 'y')

        armUpChain = utils.pfx_JointList(pfx = nameSpace + 'twist_' + obj + 'Up' + side)
        armDnChain = utils.pfx_JointList(pfx = nameSpace + 'twist_' + obj + 'Dn' + side)
        utils.limbRibbon(nameSpace, obj, side, upChain = armUpChain , dnChain = armDnChain, reverse = False)

        #fix FK armscale to keep Dn arm from doing strange things       
        cmds.parent(nameSpace + 'grp' + obj + 'FK_2' + side, nameSpace + 'grpGimbal_' + obj + 'FK_1' + side)
        cmds.parentConstraint(nameSpace + obj + 'FK_1' + side, nameSpace + 'grp' + obj + 'FK_2' + side, mo = 1)

        allGrp = cmds.group( nameSpace + 'grpLegPoleVecor' + side,nameSpace + 'grpLegNonFlip_loc' + side,nameSpace + 'grpGimbal_LegFK_1' + side,nameSpace + 'grpLegIK' + side,nameSpace + 'grpLeg_FK' + side,nameSpace + 'grptwist_LegUp' + side, nameSpace + 'grpLeg_IK' + side, nameSpace + 'grpres_Leg_Result' + side, n = nameSpace + 'grp' + obj + '_RIG' + side)

        cmds.pointConstraint(nameSpace + obj + 'Connect_loc_' + side,allGrp, mo=1)
        
        cmds.parent(allGrp,hipGrp,character)
        cmds.parent(nameSpace + 'grp_' + obj + 'EX' + side, grpEx)

        #SpaceSwitching on IK and FK
        utils.spaceSwitch(nameSpace, name = obj + 'IK',parentList = [nameSpace +'Character', nameSpace +'HipsIK',nameSpace + obj + 'Orient' + side], child = nameSpace + obj + 'IK' + side, switch = nameSpace + obj + 'Settings' + side, parentCount = 3 )
        utils.spaceSwitch(nameSpace, name = obj + 'FK', parentList = [nameSpace +'Character', nameSpace +'HipsIK',nameSpace + obj + 'Orient' + side], child = nameSpace + 'grpGimbal_' + obj + 'FK_1' + side, switch = nameSpace + obj + 'Settings' + side, parentCount = 3, orientOnly = True )
        
        
        if cmds.objExists(nameSpace + 'res_Spine_Result01') :
            cmds.parentConstraint(nameSpace + 'HipsIK', nameSpace + 'SpineFK_1',hipGrp, mo = 1)
    
            cmds.setDrivenKeyframe (hipGrp + '_parentConstraint1',cd=nameSpace  + 'Spine'  + '.' + 'Spine' + 'Switch',dv=0,attribute='.HipsIKW0',v=1) 
            cmds.setDrivenKeyframe (hipGrp + '_parentConstraint1',cd=nameSpace  + 'Spine'  + '.' + 'Spine' + 'Switch',dv=1,attribute='.HipsIKW0',v=0) 
            cmds.setDrivenKeyframe (hipGrp + '_parentConstraint1',cd=nameSpace  + 'Spine'  + '.' + 'Spine' + 'Switch',dv=1,attribute='.SpineFK_1W1',v=1) 
            cmds.setDrivenKeyframe (hipGrp + '_parentConstraint1',cd=nameSpace  + 'Spine'  + '.' + 'Spine' + 'Switch',dv=0,attribute='.SpineFK_1W1',v=0) 
                

        



################################
#
#          CLAV RIG
# 
################################
'''
Comments: 
'''
def clavicleRig(self, nameSpace, side) :
    

    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    obj = 'Clav'
    move = nameSpace + 'Arm' + '_Move' + side

    if cmds.objExists(move) == True:
        
        if side == 'RT':
            color = 6
        elif side == 'LF' :
            color = 13
        else :
            color = 30
        
        clavJoints = utils.joints2List(nameSpace = nameSpace, list = [nameSpace + 'ClavJpos' + side,nameSpace + 'ArmJpos' + side],  obj = 'skn_' + obj + '_IK', side  = side, chain = True)    
        handle = utils.stretchyIK(nameSpace, joints = clavJoints, obj = obj, side = side)
        
        control = controls.pin(name = nameSpace + obj + side, color = color)
        utils.snap(clavJoints[0], control)
        cmds.setAttr(control + '.rx', 45)
        
        if side == 'LF' :
            cmds.setAttr(control + '.ry', -90)
        elif side == 'RT' :
            cmds.setAttr(control + '.ry', 90)
        utils.freeze(control)
        cmds.parent(handle, control)

        #spaceSwitch
        if cmds.objExists(nameSpace + 'ChestIK') == False:
            name = ''
        else:
            name = nameSpace 
        
        cmds.parentConstraint(name + 'ChestIK', name + 'SpineFK_6',cmds.group(control,n =  name + 'grp' + obj + side), mo=1)
        cmds.setAttr(name + 'Spine.SpineSwitch', 0)
        cmds.setDrivenKeyframe (name +  'grpClav' + side + '_parentConstraint1.' +  name + 'ChestIKW0',cd= name + 'Spine' + '.SpineSwitch',dv=0,v=1) 
        cmds.setDrivenKeyframe (name +  'grpClav' + side + '_parentConstraint1.' +  name + 'SpineFK_6W1',cd=  name +'Spine' + '.SpineSwitch',dv=0,v=0) 
        cmds.setAttr(name + 'Spine.SpineSwitch', 1)
        cmds.setDrivenKeyframe (name +  'grpClav' + side + '_parentConstraint1.' + name + 'ChestIKW0',cd=  name +'Spine' + '.SpineSwitch',dv=1,v=0) 
        cmds.setDrivenKeyframe (name +  'grpClav' + side + '_parentConstraint1.' + name + 'SpineFK_6W1',cd= name +'Spine' + '.SpineSwitch',dv=1,v=1) 
        cmds.setAttr(name + 'Spine.SpineSwitch', 0)       

        cmds.delete(nameSpace + 'crv_Shoulder' + side)     
        utils.lockAttr([control], vis = True, scale = True)


################################
#
#          FOOT RIG
# 
################################
'''
Comments: 
'''
def footRig(self,nameSpace, side):
    

    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    obj = 'Foot'
    move = nameSpace + 'Foot' + 'Move' + side

    if cmds.objExists(move) == True:
        
        jLocations = [nameSpace + 'Ankle' + '_Move' + side,nameSpace + 'Ball' + '_Move' + side,nameSpace + 'Toe' + '_Move' + side]

        IKJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations,  obj = obj + '_IK', side  = side, chain = True)    
        FKJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations,  obj = obj + '_FK', side  = side, chain = True)    
        resultJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations,  pfx = 'res_',obj = obj + '_Result', side  = side, chain = True)    
        sknJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations,  pfx = 'skn_',obj = obj + '_Skinned', side  = side, chain = True)    
        
        #parent Joint chains together
        cmds.parent(cmds.listRelatives(IKJoints[0], p = 1), nameSpace + 'Leg_IK03' + side )
        cmds.parent(cmds.listRelatives(FKJoints[0], p = 1), nameSpace + 'Leg_FK03' + side )
        cmds.parent(cmds.listRelatives(resultJoints[0], p = 1), nameSpace + 'res_Leg_Result03' + side )
        
        #build FK
        utils.buildFKControlChainRing(nameSpace, obj, side, list = FKJoints,size = 1, direction = 1) 
        cmds.delete(nameSpace + 'FootFK_3' + side)
        cmds.parent(nameSpace + 'grpFootFK_1' + side, nameSpace + 'LegFK_3' + side)
        
        #build IK
        utils.stretchyIK(nameSpace, joints = IKJoints[0:2], obj = 'Ball', side = side, skipScale = True, solver = 'ikRPsolver' ) 
        utils.stretchyIK(nameSpace, joints = IKJoints[1:3], obj = 'Toe', side = side, skipScale = True, solver = 'ikSCsolver') 
        
        #IKfoot groups
        ankleGrp = cmds.group(nameSpace + 'Leg_IKHandle_' + side, n = nameSpace + 'grpHeelIK' + side)
        utils.snapPivot(IKJoints[1],ankleGrp )
       
        ballGrp = cmds.group(nameSpace + 'grpBall_IKHandle' + side,nameSpace + 'grpToe_IKHandle' + side, n = nameSpace + 'grpBallIK' + side)
        utils.snapPivot(IKJoints[1],ballGrp )
        
        toeGrp = cmds.group(ankleGrp, ballGrp,  n = nameSpace + 'grpToeIK' + side)
        utils.snapPivot(IKJoints[2],toeGrp )

        footGrp = cmds.group(toeGrp, n = nameSpace + 'grpFootRoll' + side)
        utils.snapPivot(IKJoints[0],footGrp )
        cmds.parent(footGrp, nameSpace + 'LegIK' + side)

        bankIn = cmds.group(footGrp, n = nameSpace + 'grpFootBankIn' + side)
        utils.snapPivot(nameSpace + 'footFront_loc' + side,bankIn )

        bankOut = cmds.group(footGrp, n = nameSpace + 'grpFootBankOut' + side)
        utils.snapPivot(nameSpace + 'footBack_loc' + side,bankOut )
        
        utils.IKFKSwitch(nameSpace, obj, side, IKJoints, FKJoints, resultJoints, switch = nameSpace + 'LegSettings' + side, parent = 'Leg')
        
        #add attrs to IK
        cmds.addAttr(nameSpace + 'LegIK' + side, ln  =  'Foot', at =  'double')
        cmds.setAttr(nameSpace + 'LegIK' + side + '.' + 'Foot', cb = True, keyable = False, lock = True)
        attrs = ['HeelRaise','HeelRoll','HeelSwivel',
                 'BallSwivel','ToeRaise','ToeSwivel',
                 'ToeBend','ToeTurn','BankIn','BankOut']

        targetList = [toeGrp + '.rx',ankleGrp + '.rx',toeGrp + '.ry',
                     ankleGrp + '.ry',footGrp + '.rx',footGrp + '.ry',
                     ballGrp + '.rx',ballGrp + '.ry',bankIn + '.rz',bankOut + '.rz']

        utils.addAttrList( target = nameSpace + 'LegIK' + side, attrList = attrs, range = [], dv = 0)
        utils.connectAttrList(driver = nameSpace + 'LegIK' + side, attrList = attrs, target = targetList)
        
        #add direct IK controls to foot
        ankleIK = controls.pin(name = nameSpace + 'HeelPivot' + side, color = 28)
        utils.snap(ballGrp, ankleIK)
        utils.freeze(ankleIK)
        cmds.setAttr(ankleIK + '.rz', -90)
        cmds.setAttr(ankleIK + '.rx', 90)
        utils.freeze(ankleIK)
        cmds.parent(ankleIK, ankleGrp) 
        utils.freeze(ankleIK)
        cmds.parent(cmds.listRelatives(ankleGrp, c = 1), ankleIK)

        ballIK = controls.pin(name = nameSpace + 'BallPivot' + side,color = 29)
        utils.snap(ballGrp, ballIK)
        utils.freeze(ballIK)
        cmds.setAttr(ballIK + '.rz', -90)
        cmds.setAttr(ballIK + '.rx', 120)
        utils.freeze(ballIK)
        cmds.parent(ballIK, ballGrp) 
        utils.freeze(ballIK)
        cmds.parent(cmds.listRelatives(ballGrp, c = 1), ballIK)

        toeIK = controls.pin(name = nameSpace + 'ToePivot' + side, color = 30)
        utils.snap(toeGrp, toeIK)
        utils.freeze(toeIK)
        cmds.setAttr(toeIK + '.rz', -90)
        cmds.setAttr(toeIK + '.rx', 160)
        utils.freeze(toeIK)
        cmds.parent(toeIK, ballIK)
        utils.freeze(toeIK)
        cmds.parent(nameSpace + 'grpToe_IKHandle' + side, toeIK)
  
        utils.addAttrList( target = nameSpace + 'LegIK' + side, attrList = ['ShowPivots'], range = [0,1], dv = 0)
        cmds.connectAttr(nameSpace + 'LegIK' + side + '.' + 'ShowPivots', ankleIK + '.v', f = 1)
        cmds.connectAttr(nameSpace + 'LegIK' + side + '.' + 'ShowPivots', ballIK + '.v', f = 1)
        #connect adjust joints to rig 
        utils.connectAdjust(nameSpace,sknJoints, resultJoints, obj, side, switch = 'LegSettings' + side, rotation = 'rx')
        cmds.delete(nameSpace + 'grpskn_Foot_Skinned' + side)
        
        cmds.parent(nameSpace +'Leg_End_DistLoc_' + side, nameSpace + 'HeelPivot' + side)
        
################################
#
#          HAND RIG
# 
################################
'''
Comments: 
'''
def handRig(self,nameSpace, side):
        

    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
    obj = 'Hand'
    move = nameSpace + 'Hand' + 'Move' + side

    if cmds.objExists(move) == True:


        jLocations = [nameSpace + 'Ankle' + '_Move' + side,nameSpace + 'Ball' + '_Move' + side,nameSpace + 'Toe' + '_Move' + side]

        hand = ['Index','Middle','Ring','Pinky','Thumb']
        indexJointsIK = []
        middleJointsIK = []
        ringJointsIK = []
        pinkyJointsIK = []
        thumbJointsIK = []
            
        target = controls.ball(name = nameSpace + obj + 'QuickPose' + side,size = .5, color = 29)
        utils.snap(nameSpace + 'res_Arm_Result03' + side,target)
        cmds.parent(target, nameSpace + 'res_Arm_Result03' + side)
        utils.freeze(target)
        
        cmds.addAttr(target, ln  =  'QuickPose', at =  'double')
        cmds.setAttr(target + '.' + 'QuickPose', cb = True, keyable = False, lock = True)
        attrs = ['Curl','Spread','FanBack','FanFwd', 'PalmCup', 'PalmSpread']
        utils.addAttrList( target = target, attrList = attrs, range = [], dv = 0)
        
        cmds.addAttr(target, ln  =  'Fingers', at =  'double')
        cmds.setAttr(target + '.' + 'Fingers', cb = True, keyable = False, lock = True)
        allGrp = cmds.group( name = nameSpace + 'grpHand' + side, em = 1)
        utils.snapPivot(nameSpace + 'res_Arm_Result03' + side, allGrp)
        cmds.parent(allGrp, nameSpace + 'res_Arm_Result03' + side)
        for finger in hand :
            if cmds.objExists(finger + 'Move' + side) == True:
                jLocations = [nameSpace + 'WristJpos' + side,nameSpace + finger + 'Move' + side,nameSpace + finger + '0Move' + side,nameSpace + finger + '1Move' + side,nameSpace + finger + '2Move' + side]
                IKJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations,  pfx = 'skn_',obj = finger + '_Skinned', side  = side, chain = True, secondaryAxis = True)    
                aimJoints = utils.joints2List(nameSpace = nameSpace, list = jLocations[0:2],  pfx = 'aim_',obj = finger + '', side  = side, chain = True, secondaryAxis = True)    

                aim = utils.stretchyIK(nameSpace, joints = aimJoints, obj = obj + finger, side = side, skipScale = True) 
                utils.buildFKControlChainRing(nameSpace, obj = finger,side = side, list = IKJoints[2:],size = .2, direction = 1) 
                cmds.delete(nameSpace + 'grp' + finger + 'FK_3' + side)
                        
                pin = controls.pin(name = nameSpace + finger + side, color = 27)
                cmds.setAttr(pin + '.rx', 90)

                pinGrp = cmds.group(pin, name = nameSpace + 'grp' + finger + side)
                utils.snapPivot(pin, pinGrp)
                utils.snapPoint(IKJoints[1],pinGrp)
                utils.snapOrient(nameSpace + finger + 'Move' + side,pinGrp)
               
                utils.freeze(pin)
                cmds.parent(nameSpace + 'grp' + finger + 'FK_1' + side,  pin)
                cmds.parentConstraint(pin, IKJoints[1], mo = 1)
                cmds.parent(aim, allGrp)
                cmds.pointConstraint(pin, aim, mo = 1)
                cmds.parent(nameSpace + 'grpaim_' + finger + side, allGrp)
                cmds.orientConstraint(aimJoints[0], IKJoints[0], mo = 1)
                
                #quick posing Attrs and connections
                attrs = [finger + 'Curl',finger +'Spread']
                utils.addAttrList( target = target, attrList = attrs, range = [], dv = 0)
                
                
                for item in [pin, nameSpace + finger + 'FK_1' + side, nameSpace + finger + 'FK_2' + side]:
                    
                    poser = cmds.group(item, n = nameSpace + 'grp' + finger + '_QuickPose' + item[-3:])
                    utils.snapPivot(item, poser)
                    
                    qPoser = cmds.group(item, n = nameSpace + 'grp' + finger + '_QuickPose' + item[-3:])
                    utils.snapPivot(item, qPoser)
                    
                    qPoser2 = cmds.group(item, n = nameSpace + 'grp' + finger + '_FanFwd' + item[-3:])
                    utils.snapPivot(item, qPoser2)
                    qPoser3 = cmds.group(item, n = nameSpace + 'grp' + finger + '_FanBck' + item[-3:])
                    utils.snapPivot(item, qPoser3)
                    
                    
                    if side == 'LF' :
                        cmds.connectAttr(target + '.' + finger + 'Curl', poser + '.rz', f = 1)
                        if finger == hand[4] :
                            pass
                        else:
                            cmds.connectAttr(target + '.' + 'Curl', qPoser + '.rz', f = 1)

                    else:
                        utils.reverseAttr(target + '.' + finger + 'Curl', poser + '.rz')
                        if finger == hand[4] :
                            pass
                        else:
                            utils.reverseAttr(target + '.' + 'Curl', qPoser + '.rz')

                    
                    if item == pin :
                        
                        pinGrpBase = cmds.group(pin, n = nameSpace + 'grp' + finger + '_BasePivot' + side)
                        utils.snapPivot(IKJoints[0], pinGrpBase)
                        if side == 'LF' :
                            cmds.connectAttr(target + '.' +  finger + 'Spread', poser + '.ry', f = 1)

                            if finger == hand[0]:
                                cmds.connectAttr(target + '.' +  'Spread', qPoser + '.ry', f = 1)
                                cmds.connectAttr(target + '.' +  'FanFwd', qPoser2 + '.rz', f = 1)
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                cmds.setAttr(target + '_FanBack_Reverse_Mult.input2X', .1)

                            elif finger == hand[1]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                cmds.connectAttr(target + '_PalmCup_Reverse_Mult.outputX', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_Spread_Reverse_Mult.input2X', .5) 
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult.input2X', .7)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult1.input2X', .4)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult.input2X', .2)
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult.input2X', .2)
                                
                            elif finger == hand[2]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                cmds.connectAttr(target + '_PalmCup_Reverse_Mult1.outputX', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult1.input2X', .4)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult2.input2X', .7)
                                cmds.setAttr(target + '_Spread_Reverse_Mult1.input2X', -.5) 
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult1.input2X', .5) 
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult1.input2X', .6) 
                                
                            elif finger == hand[3]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                cmds.connectAttr(target + '_PalmCup_Reverse_Mult2.outputX', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult2.input2X', .1)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult3.input2X', 1)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult2.input2X', 1)
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult2.input2X', 1)
                                
                            elif finger == hand[4]:
                                pass                    
                        elif side == 'RT' :
                            cmds.connectAttr(target + '.' +  finger + 'Spread', poser + '.ry', f = 1)

                            if finger == hand[0]:
                                utils.reverseAttr(target + '.' +  'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                cmds.setAttr(target + '_Spread_Reverse_Mult.input2X', 1)
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult.input2X', -1)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult.input2X', -.1)

                            elif finger == hand[1]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_Spread_Reverse_Mult1.input2X', .5) 
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult1.input2X', -.7)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult1.input2X', -.4)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult.input2X', -.2)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult1.input2X', .2)
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult.input2X', .2)
                                
                            elif finger == hand[2]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult2.input2X', -.4)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult2.input2X', -.7)
                                cmds.setAttr(target + '_Spread_Reverse_Mult2.input2X', -.5) 
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult2.input2X', -.5) 
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult3.input2X', .5) 
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult1.input2X',.6) 
                                
                            elif finger == hand[3]:
                                utils.reverseAttr(target + '.' + 'Spread', qPoser + '.ry')
                                utils.reverseAttr(target + '.' +  'FanFwd', qPoser2 + '.rz')
                                utils.reverseAttr(target + '.' +  'FanBack', qPoser3 + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rz')
                                utils.reverseAttr(target + '.' +  'PalmCup', pinGrpBase + '.rx')
                                utils.reverseAttr(target + '.' +  'PalmSpread', pinGrpBase + '.ry')
                                cmds.setAttr(target + '_Spread_Reverse_Mult3.input2X', -1)
                                cmds.setAttr(target + '_FanFwd_Reverse_Mult3.input2X', -.1)
                                cmds.setAttr(target + '_FanBack_Reverse_Mult3.input2X', -1)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult4.input2X', -1)
                                cmds.setAttr(target + '_PalmCup_Reverse_Mult5.input2X', 1)
                                cmds.setAttr(target + '_PalmSpread_Reverse_Mult2.input2X', 1)
                                
                            elif finger == hand[4]:
                                pass
                        
                        '''
                        rotGrp = cmds.group(qPoser3, n = nameSpace + finger + '_matchAxis_' + side)
                        utils.snapPivot(nameSpace + finger + 'Move' + side, rotGrp)
                        utils.snapOrient(nameSpace + finger + 'Move' + side, rotGrp)
                        '''
                
                #cleanUp
                cmds.parent(cmds.listRelatives(IKJoints[0], p =1),pinGrp, allGrp) 

                
                if finger == hand[0] :
                    indexJointsIK.append(IKJoints)
                if finger == hand[1] :
                    middleJointsIK.append(IKJoints)
                if finger == hand[2] :
                    ringJointsIK.append(IKJoints)
                if finger == hand[3] :
                    pinkyJointsIK.append(IKJoints)
                if finger == hand[4] :
                    thumbJointsIK.append(IKJoints)
                
                
                    #HandAttrs
                    attrs = ['Curl','Spread','FanBack','FanFwd','IndexCurl','IndexSpread','MiddleCurl','MiddleSpread','IndexSpread','MiddleSpread','IndexSpread','MiddleSpread']

                


################################
################################
################################
#
#          TENTACLE RIG
# 
################################
################################
################################
'''
tentacleMove(nameSpace = '', name = 'Tentacle')
tentacleRig(nameSpace = '', name = 'Tentacle')
'''

def tentacleMove(nameSpace, name = 'Tentacle') :

    if cmds.objExists(nameSpace + 'skn_' + 'name' + '1') == True :
        cmds.confirmDialog( title='Duplicate Character', message='Please define a NameSpace for your second character.', button=['OK'], defaultButton='OK',  )
        
    elif utils.checkDuplicate(nameSpace + 'crv_' +  name ) == False :


        utils.multiJoint_Ribbon_Move(nameSpace, obj = name , jnum = 8, height = 5, color = 27, size = .05 )      
        
        cmds.setAttr(nameSpace + name + 'Move.rx', 90)
        cmds.setAttr(nameSpace + name + 'Move.ty', -1.5)
              
        
       
        cmds.setAttr(nameSpace + name + 'Move.sx', .4)
        cmds.setAttr(nameSpace + name + 'Move.sy', .4)
        cmds.setAttr(nameSpace + name + 'Move.sz', .4)
        
        utils.adjustWoldSpace_RibbonSpline(obj = name, nameSpace = nameSpace, side = '', all = nameSpace + name + 'Move')

        list = utils.pfx_ControlList(nameSpace + name + '_Move')
        utils.moverRename_sfx(nameSpace, list, index = 6, side = '')
                          
        grp = cmds.group( n = nameSpace + 'grp' + name + 'Move', em = 1)
        cmds.parent(nameSpace + name + 'Move',grp)
                          
        print name + " Movers Built Successfully!"

    else:
        print "Duplcate item may exist"



def tentacleRig( nameSpace = '', name = 'Tentacle'):
    
    
    world = nameSpace + 'World'
    character = nameSpace + 'Character'
    grpJoints = nameSpace + 'grpJoints'
    grpEx = nameSpace + 'grpEX'
        
    side = ''
    obj = name
    jnum = 5
    plane = nameSpace + 'nrb_' + obj + side + 'Plane'

    move = nameSpace + obj + 'Move' + side

    if cmds.objExists(move) == True:

        conList = utils.rigRibbon(nameSpace, obj, plane, side, jnum = 10)
        IK = controls.orient(name = nameSpace + 'TentacleEnd')
        utils.snap(conList[-2],IK)
        for item in conList :
            cmds.setAttr(item + '.overrideColor', 30) 
            grp = cmds.group(item, n = nameSpace + 'grp' + item)
            trans = controls.fatDoubleArrow(name = nameSpace + 'trans_' + item)
            utils.snap(item,trans)
            utils.freeze(trans)
            cmds.setAttr(trans + '.rz',90)
            utils.freeze(trans)
            childJ = cmds.listRelatives(item,children =  1)[-1]
            cmds.parent(childJ,trans)
            grpTrans = cmds.group(trans, n = 'grp' + trans)
            cmds.parent(grpTrans,item)
            

            cmds.addAttr(trans, ln='Parent', at='double', min = 0, max = 1)
            cmds.setAttr(trans + '.Parent', e = 1, keyable=1,)

            constr = cmds.parentConstraint(item, IK, grpTrans, mo = 1)
            cmds.setDrivenKeyframe (constr,cd = trans + '.Parent',dv = 0, attribute =  '.' + item + 'W0',v=1) 
            cmds.setDrivenKeyframe (constr,cd = trans + '.Parent',dv = 0, attribute =  '.TentacleEndW1',v=0) 
            cmds.setDrivenKeyframe (constr,cd = trans + '.Parent',dv = 1, attribute =  '.' + item + 'W0',v=0) 
            cmds.setDrivenKeyframe (constr,cd = trans + '.Parent',dv = 1, attribute =  '.TentacleEndW1',v=1) 
            
            if item != conList[0]:
                index = conList.index(item)
                cmds.parent(grp, conList[index - 1])



        
        cmds.parent(cmds.group(IK, n = 'grp' + IK),conList[-2])

        grpAll = cmds.group(n = nameSpace + 'Controls' + obj + side, em = 1)
        grpMin = cmds.rename(nameSpace + 'grp' + obj + side, nameSpace + 'grp' + obj + '_Minor_' + side)
        cmds.parent(grpMin, grpAll)

        spJoints = utils.splineJoints2Curve(nameSpace = '', obj = obj, jnum = 60, pfx = 'skn_', side = 'RT')
        cmds.select(spJoints,plane)
        mel.eval('source djRivet.mel; djRivet;')

        utils.lockAttr(list = conList, vis = True)

        cmds.parent(nameSpace + obj + side + '_follicle', grpJoints)                        
        
        grp = cmds.group(plane, n = nameSpace + 'grp' + obj + 'EX')
        cmds.parent(grp, grpEx)
                    
        #builds custom tentacle type stuffs
        
        
        print obj + side + ' Rig Built Successfully!'

    else:
        print obj + side + ' Move not found. Item Skipped'



