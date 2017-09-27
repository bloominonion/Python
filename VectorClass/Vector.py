class Vector(object):
    '''Class: Vector
    This class is an implementation of a 3D vector class for general
    vector geometry functionality such as dot products, angles, etc'''
    # Store the class imports so they only exist in the function itself
    math = __import__('math')
    copy = __import__('copy')
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, idx):
        vals = [self.x, self.y, self.z]
        return vals[idx]

    def __setitem__(self, idx, val):
        if idx == 0:
            self.x = val
        if idx == 1:
            self.y = val
        if idx == 2:
            self.z = val

    def __len__(self):
        return 3

    def __str__(self):
        return "{},{},{}".format(self.x, self.y, self.z)

    def __eq__(self, vec):
        return self.x == vec.x and self.y == vec.y and self.z == vec.z

    def __ne__(self, vec):
        return not self == other

    def __sub__(self, vec):
        return Vector(self.x-vec.x, self.y-vec.y, self.z-vec.z)

    def __add__(self, vec):
        return Vector(self.x+vec.x, self.y+vec.y, self.z+vec.z)

    def __mul__(self, vec):
        return Vector(self.x*vec.x, self.y*vec.y, self.z*vec.z)

    def __abs__(self):
        return Vector(abs(self.x), abs(self.y), abs(self.z))

    def __invert__(self):
        return self.Reverse()

    @property
    def quadrant(self):
        '''Returns the quadrant (plan view) that the vector is in.
        Quadrants are 1->4, starting where x&y are positive, moving CW'''
        quad = 0
        if self.x > 0:
            if self.y > 0:
                quad = 1
            else:
                quad = 2
        else:
            if self.y > 0:
                quad = 4
            else:
                quad = 3
        return quad

    @property
    def octant(self):
        'Returns the octant the vector is in (quadrant + 4 if negative z)'
        octant = self.quadrant
        if self.z < 0:
            octant += 4
        return octant

    def Magnitude(self):
        'Returns the magnitude of a vector (float)'
        return float(self.math.sqrt(self.x**2 + self.y**2 +self.z**2))

    def PlanMagnitude(self):
        'Returns the plan magnitude of the vector'
        tmp = self.copy.copy(self)
        tmp.z = 0
        return tmp.Magnitude()

    def Normalize(self):
        'Normalize the vector to a unit vector'
        mag = self.Magnitude()
        if mag > 0:
            self.x /= mag
            self.y /= mag
            self.z /= mag

    def Reverse(self):
        'Reverse the direction of the vector'
        self.x *= -1
        self.y *= -1
        self.z *= -1

    def DistanceSquared(self, vec):
        'Returns the squared distance from one point to another'
        return (vec.x-self.x)**2 + (vec.y-self.y)**2 + (vec.z-self.z)**2

    def Distance(self, vec):
        'Returns the distance from one point to another'
        return self.math.sqrt(self.DistanceSquared(vec))

    def Cross(self, vec):
        '''Returns the cross product of to vectors
        This is the normal vector of the plane created by the two vectors.'''
        return Vector(self.y*vec.z - self.z*vec.y,
                      self.z*vec.x - self.x*vec.z,
                      self.x*vec.y - self.y*vec.x)

    def Dot(self, vec):
        'Returns the dot product of two vectors (float)'
        dot = self.x*vec.x + self.y*vec.y + self.z*vec.z
        return float(min(1,max(dot,-1)))

    def Parallel(self, vec, tol=0.0):
        'Returns True/False if two vectors are parallel within tolerance'
        return bool(abs(self.Angle(vec)) < tol)

    def Angle(self, vec):
        'Returns the angle between two vectors in radians'
        u = self.copy.copy(self)
        v = self.copy.copy(vec)
        u.Normalize()
        v.Normalize()
        return self.math.acos(u.Dot(v))

    def AngleDegrees(self, vec):
        'Returns the angle between two vectors in degrees'
        return self.math.degrees(self.Angle(vec))

    def DipDirection(self):
        '''Returns the dip direction of a vector
        This is the plan angle of a vector from North, measured clockwise'''
        north = Vector(0,1,0)
        planVec = self.copy.copy(self)
        planVec.z = 0
        if planVec.Magnitude() < 0.000001:
            return 0
        angle = self.math.degrees(planVec.Angle(north))
        if self.quadrant > 2:
            angle = 360 - angle
        return angle

    def Strike(self):
        '''Returns the strike of a vector
        This is the plan angle of a vector from North minus 90, measured clockwise'''
        strike = self.DipDirection()-90
        if strike < 0:
            strike += 360
        return strike

    def Dip(self):
        '''Returns the dip angle of a vector along the strike direction
        Angles are -90 (down) <-> 0 (horizontal) <-> 90 (up)'''
        if self.Magnitude() < 0.000001:
            return 0
        north = Vector(1,0,0)
        planVec = Vector(self.PlanMagnitude(), self.z, 0)
        angle = self.math.degrees(planVec.Angle(north))
        if self.z < 0:
            angle *= -1
        return angle

    def ConvertToDownDipOnly(self):
        '''Converts the vector to only have dips pointing down,
        recalculating the strike to face the opposite direction.'''
        if self.Dip() > 0:
            self.Reverse()
