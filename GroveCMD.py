#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback
import math
app = adsk.core.Application.get()
ui  = app.userInterface
design = adsk.fusion.Design.cast(app.activeProduct)
component = design.activeComponent
distance_x_left = .5
distance_x_right =.5
distance_y_left=.5
distance_y_right=.5
thickness = 1
tongue_height = 0.4
groove_deep = 0.4

rootComp = design.rootComponent
cornerPoints = []
def getCorner(selectedFace):
    try:
        # ui.messageBox('ok')
        # Get the bounding box of the face.
        bbox = selectedFace.boundingBox
        # Get the bounding box of the face.
        bbox = selectedFace.boundingBox

        # Compute the four corner points.
        cornerPoints = [
            adsk.core.Point3D.create(bbox.minPoint.x, bbox.minPoint.y, bbox.minPoint.z),
            adsk.core.Point3D.create(bbox.maxPoint.x, bbox.minPoint.y, bbox.minPoint.z),
            adsk.core.Point3D.create(bbox.minPoint.x, bbox.minPoint.y, bbox.maxPoint.z),
            adsk.core.Point3D.create(bbox.maxPoint.x, bbox.minPoint.y, bbox.maxPoint.z)
        ]

        # Draw a point marker at each corner point.
        for i, cornerPoint in enumerate(cornerPoints):
            sketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
            sketch.sketchPoints.add(cornerPoint)
            sketch.sketchPoints[0].isFixed = True
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
def run(context):
    try:
        # Get the selected face.
        faceSel = ui.selectEntity('Select a face', 'Faces')
        selectedFace = adsk.fusion.BRepFace.cast(faceSel.entity)

        # ========================================================
        # Create a sketch plane from selected face
        sketch_planes = component.constructionPlanes
        sketch_plane_input = sketch_planes.createInput()
        offsetValue = adsk.core.ValueInput.createByReal(0.0)
        sketch_plane_input.setByOffset(selectedFace, offsetValue)
        sketch_plane = sketch_planes.add(sketch_plane_input)
        # Get the health state of the plane
        health = sketch_plane.healthState
        if health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState or health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState:
            message = sketch_plane.errorOrWarningMessage
        # ========================================================

        # create a sketch on that plane
        sketches = rootComp.sketches
        sketch = sketches.add(sketch_plane)


        # Project the face onto the sketch
        projected_sketch = sketch.project(selectedFace)

        points = sketch.sketchPoints
        point1 = points.item(0).geometry
        point2 = points.item(1).geometry
        point3 = points.item(2).geometry
        point4 = points.item(3).geometry
        point5 = points.item(4).geometry

        # for point in points:
        # ui.messageBox('The four points of the sketch are:\n{}\n{}\n{}\n{}'.format(point1.asArray(), point2.asArray(), point3.asArray(), point4.asArray()))
            # message += f"X: {point.geometry.x}, Y: {point.geometry.y}, Z: {point.geometry.z}\n"

        # Create sketch circle
        # sketchCircles = sketch.sketchCurves.sketchCircles
        # centerPoint = adsk.core.Point3D.create(0, 0, 0)
        # sketchCircles.addByCenterRadius(point1, 1.0)

        sketchline = sketch.sketchCurves.sketchLines
        line1 = sketchline.addByTwoPoints(point2, point3)
        line2 = sketchline.addByTwoPoints(point3, point4)
        line3 = sketchline.addByTwoPoints(point4, point5)
        line4 = sketchline.addByTwoPoints(point5, point2)

        # Offset the line by a specified distance
        # features = rootComp.features
        # offsetFeatures = features.offsetFeatures

        # distance = adsk.core.ValueInput.createByReal(0.1)
        curves1 = sketch.findConnectedCurves(line1)
        curves2 = sketch.findConnectedCurves(line2)
        curves3 = sketch.findConnectedCurves(line3)
        curves4 = sketch.findConnectedCurves(line4)

        dirPoint = adsk.core.Point3D.create(0, .5, 0)
        # x , y = calculate_length_width(point1, point2, point3, point4)


        offsetLine = sketch.offset(curves1, dirPoint, distance_x_left)
        offsetLine = sketch.offset(curves1, dirPoint, thickness)

        offsetLine = sketch.offset(curves2, dirPoint, distance_y_right)
        offsetLine = sketch.offset(curves2, dirPoint, thickness)

        offsetLine = sketch.offset(curves3, dirPoint, distance_x_left)
        offsetLine = sketch.offset(curves3, dirPoint, thickness)

        offsetLine = sketch.offset(curves4, dirPoint, distance_y_left)
        offsetLine = sketch.offset(curves4, dirPoint, thickness)

        extrudeFeatures = rootComp.features.extrudeFeatures

        # Create the feature.
        # ======================================================
        ui.messageBox('Select Profile to cut')
        profile = ui.selectEntity('Select the fact to create a sketch', 'Profiles').entity
        # Define the required input.
        operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        extrudeFeatures = rootComp.features.extrudeFeatures
        input: adsk.fusion.ExtrudeFeatureInput = extrudeFeatures.createInput(profile, operation)
        distance = adsk.core.ValueInput.createByReal(groove_deep)
        distanceExtent = adsk.fusion.DistanceExtentDefinition.create(distance)
        direction = adsk.fusion.ExtentDirections.NegativeExtentDirection
        input.setOneSideExtent(distanceExtent, direction)
        # Create the feature.
        extrudeFeature = extrudeFeatures.add(input)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
def calculate_length_width(point1, point2, point3, point4):
    # Calculate the length of the rectangle
    length = math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2 + (point1.z - point2.z)**2)

    # Calculate the width of the rectangle
    corner_points = [point1, point2, point3, point4]
    remaining_points = [point for point in corner_points if point not in [point1, point2]]

    width_vector = adsk.core.Vector3D.create(remaining_points[0].x - point1.x, remaining_points[0].y - point1.y, remaining_points[0].z - point1.z)
    length_vector = adsk.core.Vector3D.create(point2.x - point1.x, point2.y - point1.y, point2.z - point1.z)
    normal_vector = length_vector.crossProduct(width_vector)

    width = normal_vector.length / length
    # start = adsk.core.Point3D.create(distFromEdge_right,distFromEdge_right,0)
    # stop =  adsk.core.Point3D.create(thickness_right,height-thickness_right,0)
    # square = lines.addTwoPointRectangle(start,stop)
    # ui.messageBox('length{:.2f}, width{:.2f}'.format(length,width))
    return length, width