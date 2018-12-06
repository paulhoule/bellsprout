#
# original Javascript
#
# * https://github.com/gre/bezier-easing
# * BezierEasing - use bezier curve for transition easing function
# * by Gaëtan Renaudeau 2014 - 2015 – MIT License
#

NEWTON_ITERATIONS = 4;
NEWTON_MIN_SLOPE = 0.001;
SUBDIVISION_PRECISION = 0.0000001;
SUBDIVISION_MAX_ITERATIONS = 10;

kSplineTableSize = 11;
kSampleStepSize = 1.0 / (kSplineTableSize - 1.0);


def A (aA1, aA2):
    return 1.0 - 3.0 * aA2 + 3.0 * aA1

def B (aA1, aA2):
    return 3.0 * aA2 - 6.0 * aA1;

def C(aA1):
    return 3.0 * aA1;

# Returns x(t) given t, x1, and x2, or y(t) given t, y1, and y2.
def calcBezier (aT, aA1, aA2):
    return ((A(aA1, aA2) * aT + B(aA1, aA2)) * aT + C(aA1)) * aT

# Returns dx/dt given t, x1, and x2, or dy/dt given t, y1, and y2.
def getSlope (aT, aA1, aA2):
    return 3.0 * A(aA1, aA2) * aT * aT + 2.0 * B(aA1, aA2) * aT + C(aA1)

def binarySubdivide (aX, aA, aB, mX1, mX2):
  i = 0
  while True:
    currentT = aA + (aB - aA) / 2.0;
    currentX = calcBezier(currentT, mX1, mX2) - aX;
    if (currentX > 0.0):
      aB = currentT
    else:
      aA = currentT

    i += 1
    if abs(currentX) < SUBDIVISION_PRECISION or i >= SUBDIVISION_MAX_ITERATIONS:
        return currentT


def newtonRaphsonIterate (aX, aGuessT, mX1, mX2):
    for i in range(0,NEWTON_ITERATIONS):
        currentSlope = getSlope(aGuessT, mX1, mX2)
        if (currentSlope == 0.0):
         return aGuessT;

        currentX = calcBezier(aGuessT, mX1, mX2) - aX
        aGuessT -= currentX / currentSlope

    return aGuessT

def LinearEasing (x):
  return x


def cubic_bezier (mX1, mY1, mX2, mY2):
    """
    Returns a function of one variable that computes y = f(x).  In the context of an animation the X
    coordinate is time,  and the Y coordinate is the time varying parameter.

    Both X (time) and Y are polynomial functions of t,  the parametric variable.  To solve for Y as
    a function of X we have to numerically solve for t,  then we evaluate a polynomial for X.


    :param mX1: time value of first control point
    :param mY1: parameter value for first control point
    :param mX2: time value of second control point
    :param mY2: parameter value for second control point
    :return: function of time value to parameter
    """
    if mX1 < 0  or  mX1 > 1 or mX2 <0 or mX2 >1:
        raise ValueError('bezier x values must be in [0, 1] range')

    if mX1 == mY1 and mX2 == mY2:
        return LinearEasing

    sampleValues = []
    for i in range(0,kSplineTableSize):
        sampleValues.append(calcBezier(i * kSampleStepSize, mX1, mX2))

    def getTForX (aX):
        intervalStart = 0.0
        currentSample = 1
        lastSample = kSplineTableSize - 1

        while currentSample < lastSample and sampleValues[currentSample] <= aX:
          intervalStart += kSampleStepSize
          currentSample += 1

        currentSample -= 1

        dist = (aX - sampleValues[currentSample]) / (sampleValues[currentSample + 1] - sampleValues[currentSample]);
        guessForT = intervalStart + dist * kSampleStepSize

        initialSlope = getSlope(guessForT, mX1, mX2)
        if initialSlope >= NEWTON_MIN_SLOPE:
            return newtonRaphsonIterate(aX, guessForT, mX1, mX2)
        elif initialSlope == 0.0:
          return guessForT
        else:
          return binarySubdivide(aX, intervalStart, intervalStart + kSampleStepSize, mX1, mX2)

    def BezierEasing (x):
        if x == 0 or x == 1:
            return x

        return calcBezier(getTForX(x), mY1, mY2);

    return BezierEasing

class Easings:
    easeInSine = [0.47, 0, 0.745, 0.715]
    easeOutSine = [0.39, 0.575, 0.565, 1]
    easeInOutSine = [0.445, 0.05, 0.55, 0.95]

    easeInQuad = [0.55, 0.085, 0.68, 0.53]
    easeOutQuad = [0.25, 0.46, 0.45, 0.94]
    easeInOutQuad = [0.455, 0.03, 0.515, 0.955]
    
    easeInQuart = [0.895, 0.03, 0.685, 0.22]
    easeOutQuart = [0.25, 0.46, 0.45, 0.94]
    easeInOutQuart = [0.77, 0, 0.175, 1]

    easeInQuint = [0.755, 0.05, 0.855, 0.06]
    easeOutQuint = [0.23, 1, 0.32, 1]
    easeInOutQuint = [0.86, 0, 0.07, 1]
    
    easeInExpo = [0.95, 0.05, 0.795, 0.035]
    easeOutExpo = [0.19, 1, 0.22, 1]
    easeInOutExpo = [1, 0, 0, 1]
    
    easeInCirc = [0.6, 0.04, 0.98, 0.335]
    easeOutCirc = [0.075, 0.82, 0.165, 1]
    easeInOutCirc = [0.785, 0.135, 0.15, 0.86]

    #
    # the easing functions below will be rejected by our cubic_bezier function because the 'Y'
    # coordinates are outside the range of 0 to 1.  The code above might be able to handle
    # it anyway if the numerical solution we're shooting for is unambiguous
    #

    # easeInBack = [0.6, -0.28, 0.735, 0.045]
    # easeOutBack = [0.175, 0.885, 0.32, 1.275]
    # easeInOutBack = [0.68, -0.55, 0.265, 1.55]


