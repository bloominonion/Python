from Vector import Vector
import unittest

class TestVector(unittest.TestCase):
    def testMagnitude1(self):
        v = Vector(1,0,0)
        self.assertEqual(v.Magnitude(), 1)
    def testMagnitude2(self):
        v = Vector(2,0,0)
        self.assertEqual(v.Magnitude(), 2)
    def testMagnitude5(self):
        v = Vector(5,0,0)
        self.assertEqual(v.Magnitude(), 5)
    def testMagnitude10(self):
        v = Vector(10,0,0)
        self.assertEqual(v.Magnitude(), 10)

    def testAngle90(self):
        u = Vector(1,0,0)
        v = Vector(0,1,0)
        self.assertEqual(u.AngleDegrees(v), 90)

    def testAngle180(self):
        u = Vector(1,0,0)
        v = Vector(-1,0,0)
        self.assertEqual(u.AngleDegrees(v), 180)

    def testReverse(self):
        u = Vector(1,1,1)
        v = Vector(-1,-1,-1)
        u.Reverse()
        self.assertEqual(u, v)

    def testCross(self):
        u = Vector(0,1,0)
        v = Vector(1,0,0)
        w = v.Cross(u)
        self.assertEqual(w, Vector(0,0,1))

    def testAbs(self):
        v = Vector(-1,-1,-1)
        self.assertEqual(abs(v), Vector(1,1,1))

    def testDot(self):
        x = Vector(0,1,0)
        y = Vector(1,0,0)
        nY = Vector(*y)
        nY.Reverse()
        self.assertEqual(y.Dot(y), 1)  # Parallel
        self.assertEqual(x.Dot(y), 0)  # Perpendicular
        self.assertEqual(y.Dot(nY), -1)# Parallel (180 degrees)

    def testEquals(self):
        a = Vector(1,1,0)
        b = Vector(1,1,0)
        self.assertEqual(a, b)

    def testParallel(self):
        a = Vector(1,1,1)
        b = Vector(2,2,2)
        self.assertTrue(a.Parallel(b, 0.01))

    def testAbsParallel(self):
        a = Vector(1,1,1)
        b = Vector(-1,-1,-1)
        self.assertTrue(a.Parallel(abs(b), 0.01))

    def testPlanMagnitude(self):
        v = Vector(1,0,1)
        self.assertEqual(v.PlanMagnitude(), 1)
        v.y = 1
        self.assertAlmostEqual(v.PlanMagnitude(), 1.414, 3)

class TestVectorChanging(unittest.TestCase):
    def testFlipVector(self):
        v = Vector(1,1,1.414)
        self.assertAlmostEqual(v.Dip(), 45, 1)
        v.ConvertToDownDipOnly()
        self.assertAlmostEqual(v.DipDirection(), 225, 1)
    def testReverseVectorDip(self):
        v = Vector(-1,-1,0)
        self.assertEqual(v.DipDirection(), 225)
        v.Reverse()
        self.assertAlmostEqual(v.DipDirection(), 45, 5)

class TestVectorOctant(unittest.TestCase):
    def testOctant1(self):
        v = Vector(1,1,0)
        self.assertEqual(v.quadrant, 1)
        self.assertEqual(v.octant, 1)
    def testOctant2(self):
        v = Vector(1,-1,0)
        self.assertEqual(v.quadrant, 2)
        self.assertEqual(v.octant, 2)
    def testOctant3(self):
        v = Vector(-1,-1,0)
        self.assertEqual(v.quadrant, 3)
        self.assertEqual(v.octant, 3)
    def testOctant4(self):
        v = Vector(-1,1,0)
        self.assertEqual(v.quadrant, 4)
        self.assertEqual(v.octant, 4)
    def testOctant5(self):
        v = Vector(1,1,-1)
        self.assertEqual(v.quadrant, 1)
        self.assertEqual(v.octant, 5)
    def testOctant6(self):
        v = Vector(1,-1,-1)
        self.assertEqual(v.quadrant, 2)
        self.assertEqual(v.octant, 6)
    def testOctant7(self):
        v = Vector(-1,-1,-1)
        self.assertEqual(v.quadrant, 3)
        self.assertEqual(v.octant, 7)
    def testOctant8(self):
        v = Vector(-1,1,-1)
        self.assertEqual(v.quadrant, 4)
        self.assertEqual(v.octant, 8)

class TestVectorDipDirection(unittest.TestCase):
    vectors = [
        [ 0, 0, 0],  #   0
        [ 1, 1, 0],  #  45
        [ 1, 0, 0],  #  90
        [ 0,-1, 0],  # 180
        [-1,-1, 0],  # 225
        [-1, 0, 0],  # 270
        [-1, 1, 0],  # 315
    ]

    expected = [0,45,90,180,225,270,315]
    def testAngles(self):
        for i, vec in enumerate(self.vectors):
            v = Vector(*vec)
            dipDir = v.DipDirection()
            self.assertAlmostEqual(dipDir, self.expected[i])

class TestVectorStrike(unittest.TestCase):
    vectors = [
                     # Dip dir
        [ 0, 0, 0],  #   0
        [ 1, 1, 0],  #  45
        [ 1, 0, 0],  #  90
        [ 0,-1, 0],  # 180
        [-1,-1, 0],  # 225
        [-1, 0, 0],  # 270
        [-1, 1, 0],  # 315
    ]

    expected = [270,315,0,90,135,180,225]
    def testAngles(self):
        for i, vec in enumerate(self.vectors):
            v = Vector(*vec)
            strike = v.Strike()
            self.assertAlmostEqual(strike, self.expected[i])

class TestVectorDip(unittest.TestCase):
    vectors = [
        [ 0, 0, 1],  #  90
        [ 1, 0, 1],  #  45
        [ 1, 0, 0],  #   0
        [ 1, 0,-1],  # -45
        [ 0, 0,-1],  # -90
    ]
    expected = [90, 45, 0, -45, -90]
    def testAngles(self):
        for i, vec in enumerate(self.vectors):
            v = Vector(*vec)
            dip = v.Dip()
            self.assertAlmostEqual(dip, self.expected[i])

if __name__ == '__main__':
    unittest.main()