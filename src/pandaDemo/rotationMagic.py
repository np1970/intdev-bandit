from panda3d.core import LMatrix4, LQuaternion, Vec3

def rotationFromCompass(acceleration, magnetic_field):
    down = -acceleration
    east = down.cross(magnetic_field)
    north = east.cross(down)

    east.normalize()
    north.normalize()
    down.normalize()

    r = LMatrix4()
    r.setRow(0, north)
    r.setRow(1, east)
    r.setRow(2, down)
    return r

def rotate(rotation, w, dt):
    rotation *= LQuaternion(1, w*dt/2)
    rotation.normalize()

def rotationMagic(rotation, dt, angular_velocity, acceleration, magnetic_field):
    angular_velocity = Vec3(*angular_velocity)
    acceleration = Vec3(*acceleration)
    magnetic_field = Vec3(*magnetic_field)
    correction = (0, 0, 0)

    if abs(acceleration.length() - 1) <= 0.3:
        correction_strength = 1
        rotationCompass = rotationFromCompass(acceleration, magnetic_field)
        rotationMatrix = LMatrix4()
        rotation.extractToMatrix(rotationMatrix)

        correction = rotationCompass.getRow3(0).cross(rotationMatrix.getRow3(0))
        correction += rotationCompass.getRow3(1).cross(rotationMatrix.getRow3(1))
        correction += rotationCompass.getRow3(2).cross(rotationMatrix.getRow3(2))
        correction *= correction_strength

    rotate(rotation, angular_velocity + correction, dt)
