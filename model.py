from random import randint

# Car er det overordnede objekt, som styrer simulationen.
# Engine håndterer energi og brændstof.
# Gearbox overfører motorens bevægelse til hjulene.
# Wheel simulerer fysisk rotation.
# Tank styrer brændstofmængde.


class Car(object):
    def __init__(self):
        self.theEngine = Engine() # Motoren requires

    def updateModel(self,dt):
        self.theEngine.updateModel(dt) # Her bliver model opdateret

class Wheel(object):
    def __init__(self):
        self.orientation: int = randint(0,360) # Vi simuler realistisk hjulposition

    def rotate(self,revolutions):
        revs_in_degrees = 360 * revolutions # Omsætning til grader
        self.orientation = (self.orientation + revs_in_degrees) % 360 # Værdien er kun mellem 0-360


class Engine(object):
    def __init__(self):
        self.throttlePosition: float = 0
        self.theGearbox = Gearbox()
        self.currentRpm: int = 0
        self.consumptionConstant: float = 0.0025
        self.maxRpm: int = 100
        self.theTank = Tank()
    pass

    def updateModel(self,dt):
        if self.theTank.contents > 0: # Checker om tanken ikke er tom
            self.currentRpm = self.throttlePosition * self.maxRpm
            self.theTank.remove(self.currentRpm * self.consumptionConstant)
            self.theGearbox.rotate(self.currentRpm * (dt / 60))  # Sender bevægelse videre til hjulene via gearkassen
        if self.theTank == 0:
            self.currentRpm = 0

class Gearbox(object):
    def __init__(self):
        self.wheels: dict = {"frontLeft": Wheel(),
                     "frontRight": Wheel(),
                     "rearLeft": Wheel(),
                     "rearRight": Wheel()}
        # Gear kassen styre 4 hjul
        self.gears: list = [0,0.8,1,1.4,2.2,3.8]
        self.currentGear: int = 0
        self.clutchEngaged: bool = True

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
    def __init__(self):
        self.capacity: int = 500
        self.contents: int = self.capacity

    def remove(self,amount):
        self.contents = self.contents - amount
        if self.contents < 0:
            self.contents = 0

    def refuel(self):
        self.contents = self.capacity


