from random import randint

# Car er det overordnede objekt, som styrer simulationen.
# Engine håndterer brændstof.
# Gearbox overfører motorens bevægelse til hjulene.
# Wheel simulerer fysisk rotation.
# Tank styrer brændstofmængde.


class Car(object):
    """Car repræsenterer bilen som helhed og samler motor, gearkasse og hjul."""
    def __init__(self):
        self.theEngine = Engine()

    def updateModel(self,dt):
        self.theEngine.updateModel(dt) # Her bliver model opdateret

class Wheel(object):
    """Wheel repræsenterer et enkelt hjul og dets rotation."""
    def __init__(self):
        self.orientation: int = randint(0,360) # Vi simuler realistisk hjulposition

    def rotate(self,revolutions):
        revs_in_degrees = 360 * revolutions # Omsætning til grader
        self.orientation = (self.orientation + revs_in_degrees) % 360 # Værdien er kun mellem 0-360


class Engine(object):
    """Engine styrer bilens motor, omdrejninger og brændstofforbrug."""
    def __init__(self):
        self.throttlePosition: float = 0 # Hvor meget speederen er trykket ned
        self.theGearbox = Gearbox()
        self.currentRpm: int = 0
        self.consumptionConstant: float = 0.0025 # Hvor meget brændstof per RPM
        self.maxRpm: int = 100
        self.theTank = Tank()
    pass

    def updateModel(self,dt):
        if self.theTank.contents > 0: # Checker om tanken ikke er tom
            self.currentRpm = self.throttlePosition * self.maxRpm
            self.theTank.remove(self.currentRpm * self.consumptionConstant)
            self.theGearbox.rotate(self.currentRpm * (dt / 60))  # Sender bevægelse videre til hjulene via gearkassen
        if self.theTank == 0:
            self.currentRpm = 0 # Motoren stopper

class Gearbox(object):
    """Gearbox overfører motorens bevægelse til hjulene gennem gear."""
    def __init__(self):
        self.wheels: dict = {"frontLeft": Wheel(),
                     "frontRight": Wheel(),
                     "rearLeft": Wheel(),
                     "rearRight": Wheel()}
        # Gear kassen styre 4 hjul
        self.gears: list = [0,0.8,1,1.4,2.2,3.8] # Gear forhold
        self.currentGear: int = 0
        self.clutchEngaged: bool = False

    def shiftUp(self):
        if self.currentGear < 5 and self.clutchEngaged == False:
            self.currentGear += 1

    def shiftDown(self):
        if self.currentGear > 0 and self.clutchEngaged == False:
            self.currentGear -= 1

    def rotate(self,revolutions):
        if self.clutchEngaged: # Hvis koblingen er nede
            for wheel in self.wheels.values(): # Looper igennem wheels.value altså kun Wheel-klassen
                wheel.rotate(revolutions * self.gears[self.currentGear]) # for hvert wheel skal den rotates





class Tank(object):
    """Tank holder styr på brændstofmængde."""
    def __init__(self):
        self.capacity: int = 500
        self.contents: int = self.capacity

    def remove(self,amount):
        self.contents = self.contents - amount
        if self.contents < 0:
            self.contents = 0

    def refuel(self):
        self.contents = self.capacity


