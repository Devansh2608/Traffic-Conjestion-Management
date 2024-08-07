

# *** IMAGE XY COOD IS TOP LEFT
import random
import math
import time
import threading
# from vehicle_detection import detection
import pygame
import sys
import os



# Default values of signal times

defaultRed = 150
defaultYellow = 5
defaultGreen = 20
defaultMinimum = 10
defaultMaximum = 30

ambulances_lane1=[]
ambulances_lane2=[]

total_ambulances1 = 0
total_ambulances2 = 0

#defining priority
car_priority=1
bus_priority=1
ambulance_priority=5
bike_priority=1


green_lane1= [defaultGreen]
green_lane2= []

lane1 = []
lane2 = []
signals = []
noOfSignals = 2
simTime = 120
# change this to change time of simulation
timeElapsed = 0


currentGreen = 0  # Indicates which signal is green
# nextGreen = (currentGreen+1)%noOfSignals
nextGreen = (currentGreen + 1) % 2

currentYellow = 0  # Indicates whether yellow signal is on or off

# Average times for vehicles to pass the intersection
carTime = 2
bikeTime = 1
ambulanceTime = 2.25
busTime = 2.5
truckTime = 2.5

# Count of vehicles at a traffic signal
noOfCars = 0
noOfBikes = 0
noOfBuses = 0
noOfTrucks = 0
noOfambulances = 0
noOfLanes = 2

totalVehicles=0

# Red signal time at which cars will be detected at a signal
detectionTime = 5

speeds = {'car': 2.25, 'bus': 1.8, 'truck': 1.8, 'ambulance': 2, 'bike': 2.25}  # average speeds of vehicles

# Coordinates of start
x = {'right': [0, 0, 0], 'down': [755, 727, 697]}
y = {'right': [348, 370, 398], 'down': [0, 0, 0]}

vehicles = {'right': {0: [], 1: [], 2: [], 'crossed': 0}, 'down': {0: [], 1: [], 2: [], 'crossed': 0},
           'left': {0: [], 1: [], 2: [], 'crossed': 0}, 'up': {0: [], 1: [], 2: [], 'crossed': 0}}

vehicleTypes = {0: 'car', 1: 'bus', 2: 'truck', 3: 'ambulance', 4: 'bike'}
#directionNumbers = {0: 'right', 1: 'down', 2: 'left', 3: 'up'}
directionNumbers = {0: 'right', 1: 'down'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530, 230), (810, 230)]
signalTimerCoods = [(530, 210), (810, 210)]
vehicleCountCoods = [(480, 210), (880, 210)]
vehicleCountTexts = ["0", "0"]


stopLines = {'right': 590, 'down': 330}
defaultStop = {'right': 580, 'down': 320}
stops = {'right': [580, 580, 580], 'down': [320, 320, 320]}


# mid = {'right': {'x': 705, 'y': 445}, 'down': {'x': 695, 'y': 450}}
# rotationAngle = 3

# Gap between vehicles
gap = 15  # stopping gap
gap2 = 15  # moving gap

pygame.init()
simulation = pygame.sprite.Group()


class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green

        #self.signalText = "30"
        self.totalGreenTime = 0


class Vehicle(pygame.sprite.Sprite):
    #global total_ambulances1, total_ambulances2
    def __init__(self, lane, vehicleClass, direction_number, direction):

        pygame.sprite.Sprite.__init__(self)

        self.lane = lane
        self.vehicleClass = vehicleClass
        #print(self.vehicleClass)
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]

        # if (vehicleClass == 3):
        #     if (direction_number==0):
        #         total_ambulances1 += 1
        #     else:
        #         total_ambulances2+=1

        self.crossed = 0
        # pygame.sprite.Sprite.__init__(self)
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)
        # self.stop = stops[direction][lane]
        self.index = len(vehicles[direction][lane]) - 1
        # path = "images/" + direction + "/" + vehicleClass + ".png"
        path = direction + "/" + vehicleClass + ".png"
        # (Purpose: self.originalImage stores the original, unmodified image of the vehicle. This is the image as it was loaded from the file, with no transformations applied to it.
        # Usage: This attribute is used to retain the base image that can be re-used or reset to its original state if needed. For example, if you want to change the vehicle’s image (e.g., for different states or animations), you can use this original image to set the self.currentImage back to its unaltered form.
        # Why It Matters: Keeping the original image is useful when you need to apply transformations (like scaling, rotating, or color changes) to the self.currentImage but might need to revert to or reapply the original image for consistency or resets.)
        # self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)

        if (direction == 'right'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][
                self.index - 1].crossed == 0):  # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].currentImage.get_rect().width - gap  # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = defaultStop[direction]
            # Set new starting and stopping coordinate
            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] -= temp
            stops[direction][lane] -= temp

        elif (direction == 'down'):
            if (len(vehicles[direction][lane]) > 1 and vehicles[direction][lane][self.index - 1].crossed == 0):
                self.stop = vehicles[direction][lane][self.index - 1].stop - vehicles[direction][lane][
                    self.index - 1].currentImage.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp

        simulation.add(self)

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def move(self):
        global total_ambulances1,total_ambulances2
        if (self.direction == 'right'):
            if (self.crossed == 0 and self.x + self.currentImage.get_rect().width > stopLines[
                self.direction]):  # if the image has crossed stop line now
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.vehicleClass == 'ambulance'):
                    total_ambulances1+=1
                    #print(total_ambulances1)




            if ((self.x + self.currentImage.get_rect().width <= self.stop or self.crossed == 1 or (
                        currentGreen == 0 and currentYellow == 0)) and (
                        self.index == 0 or self.x + self.currentImage.get_rect().width < (
                        # vehicles[self.direction][self.lane][self.index - 1].x - gap2) or (
                        #         vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                        vehicles[self.direction][self.lane][self.index - 1].x - gap2))):
                    # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                    self.x += self.speed  # move the vehicle



        elif (self.direction == 'down'):
            if (self.crossed == 0 and self.y + self.currentImage.get_rect().height > stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
                if(self.vehicleClass == 'ambulance'):
                    total_ambulances2+=1


            if ((self.y + self.currentImage.get_rect().height <= self.stop or self.crossed == 1 or (
                        currentGreen == 1 and currentYellow == 0)) and (
                        # self.index == 0 or self.y + self.currentImage.get_rect().height < (
                        # vehicles[self.direction][self.lane][self.index - 1].y - gap2) or (
                        #         vehicles[self.direction][self.lane][self.index - 1].turned == 1))):
                        self.index == 0 or self.y + self.currentImage.get_rect().height < (
                        vehicles[self.direction][self.lane][self.index - 1].y - gap2))):
                        self.y += self.speed

# Initialization of signals with default values
def initialize():
    ts1 = TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts2)

    repeat()


# Set time according to formula
def setTime():
    global noOfCars, noOfBikes, noOfBuses, noOfTrucks, noOfambulances, noOfLanes
    global carTime, busTime, truckTime, ambulanceTime, bikeTime

    noOfCars, noOfBuses, noOfTrucks, noOfambulances, noOfBikes = 0, 0, 0, 0, 0
    for j in range(len(vehicles[directionNumbers[nextGreen]][0])):
        vehicle = vehicles[directionNumbers[nextGreen]][0][j]
        if (vehicle.crossed == 0):
            vclass = vehicle.vehicleClass
            # print(vclass)
            noOfBikes += 1
    for i in range(1, 3):
        for j in range(len(vehicles[directionNumbers[nextGreen]][i])):
            vehicle = vehicles[directionNumbers[nextGreen]][i][j]
            if (vehicle.crossed == 0):
                vclass = vehicle.vehicleClass
                # print(vclass)
                if (vclass == 'car'):
                    noOfCars += 1
                elif (vclass == 'bus'):
                    noOfBuses += 1
                elif (vclass == 'truck'):
                    noOfTrucks += 1
                elif (vclass == 'ambulance'):
                    noOfambulances += 1


    #//////////////////////////
    greenTime = math.ceil(((noOfCars * carTime * car_priority) + (noOfambulances * ambulanceTime * ambulance_priority) + (noOfBuses * busTime * bus_priority) + (
                noOfTrucks * truckTime) + (noOfBikes * bikeTime * bike_priority)) / (noOfLanes))

    # Take product with priority
    # greenTime = math.ceil(((noOfCars * carTime) + (noOfambulances * ambulanceTime) + (noOfBuses * busTime) + (
    #         noOfTrucks * truckTime) + (noOfBikes * bikeTime)) / (noOfLanes))

    # /////////////////////////////////////
    #greenTime= defaultGreen
    # greenTime = math.ceil((noOfVehicles)/noOfLanes)
    # greenTime=5
    #///////////////////
    #print('Green Time: ', greenTime)
    if (greenTime < defaultMinimum):
        greenTime = defaultMinimum
    elif (greenTime > defaultMaximum):
        greenTime = defaultMaximum
    # greenTime = random.randint(15,50)
    signals[(currentGreen + 1) % (noOfSignals)].green = greenTime

    if (currentGreen == 1):
        green_lane1.append(greenTime)
    else:
        green_lane2.append(greenTime)


def repeat():
    global currentGreen, currentYellow, nextGreen
    while (signals[currentGreen].green > 0):  # while the timer of current green signal is not zero
        printStatus()
        updateValues()
        if (signals[(currentGreen + 1) % (noOfSignals)].red == detectionTime):  # set time of next green signal
            thread = threading.Thread(name="detection", target=setTime, args=())
            thread.daemon = True
            thread.start()
            # setTime()
        time.sleep(1)
    currentYellow = 1  # set yellow signal on
    vehicleCountTexts[currentGreen] = "0"
    # reset stop coordinates of lanes and vehicles
    for i in range(0, 3):
        stops[directionNumbers[currentGreen]][i] = defaultStop[directionNumbers[currentGreen]]
        for vehicle in vehicles[directionNumbers[currentGreen]][i]:
            vehicle.stop = defaultStop[directionNumbers[currentGreen]]
    while (signals[currentGreen].yellow > 0):  # while the timer of current yellow signal is not zero
        printStatus()
        updateValues()
        time.sleep(1)
    currentYellow = 0  # set yellow signal off

    # reset all signal times of current signal to default times
    # signals[currentGreen].green = defaultGreen
    signals[currentGreen].yellow = defaultYellow
    # signals[currentGreen].red = defaultRed

    currentGreen = nextGreen  # set next signal as green signal
    nextGreen = (currentGreen + 1) % noOfSignals  # set next green signal
    signals[nextGreen].red = signals[currentGreen].yellow + signals[
        currentGreen].green  # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()


# Print the signal timers on cmd
# def printStatus():
#     for i in range(0, noOfSignals):
#         if (i == currentGreen):
#             if (currentYellow == 0):
#                 print(" GREEN TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#             else:
#                 print("YELLOW TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#         else:
#             print("   RED TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
#     print()
#
def printStatus():
    t=0
    # for i in range(0, noOfSignals):
    #     if (i == currentGreen):
    #         if (currentYellow == 0):
    #             print(" GREEN TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
    #         else:
    #             print("YELLOW TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
    #     else:
    #         print("   RED TS", i + 1, "-> r:", signals[i].red, " y:", signals[i].yellow, " g:", signals[i].green)
    # print()


# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if (i == currentGreen):
            if (currentYellow == 0):
                signals[i].green -= 1
                signals[i].totalGreenTime += 1
            else:
                signals[i].yellow -= 1
        else:
            signals[i].red -= 1


# Generating vehicles in the simulation
def generateVehicles():
    #global total_ambulances1, total_ambulances2

    while (True):
        vehicle_type = random.randint(0, 4)
        if (vehicle_type == 4):
            lane_number = 0
        else:
            lane_number = random.randint(0, 1) + 1

        temp = random.randint(0, 999)
        direction_number = 0
        a = [400, 800, 900, 1000]
        if (temp < a[0]):
            direction_number = 0
        elif (temp < a[1]):
            direction_number = 1
        elif (temp < a[2]):
            direction_number = 0
        elif (temp < a[3]):
            direction_number = 1
        # Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number],
        #         will_turn)

        # if(vehicle_type==3):
        #     if(direction_number == 0):
        #         total_ambulances1+=1
        #     else:
        #         total_ambulances2+=1

        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number])

        time.sleep(0.75)


def simulationTime():
    global timeElapsed, simTime, total_ambulances1, total_ambulances2
    while (True):
        timeElapsed += 1
        time.sleep(1)

        total_vehicles =0
        if (timeElapsed == simTime):
            lane1_vehicle_cnt = 0
            lane2_vehicle_cnt = 0
            for i in range(noOfSignals):
                if(vehicles[directionNumbers[i]]['crossed'] >0):
                    if(i==0):
                        lane1.append(vehicles[directionNumbers[i]]['crossed'])
                        ambulances_lane1.append(total_ambulances1)
                        #total_ambulances1 = 0
                    else:
                        lane2.append(vehicles[directionNumbers[i]]['crossed'])
                        ambulances_lane2.append(total_ambulances2)

            #totalVehicles = 0
            print('Lane-wise Vehicle Counts')
            for i in lane1:
                lane1_vehicle_cnt += i

            for i in lane2:
                lane2_vehicle_cnt += i

            total_vehicles = lane1_vehicle_cnt + lane2_vehicle_cnt
            #for i in range(noOfSignals):
                # print('Lane', i + 1, ':', vehicles[directionNumbers[i]]['crossed'])

                #totalVehicles += vehicles[directionNumbers[i]]['crossed']
            print('Vehicles passed in lane 1 :', lane1_vehicle_cnt)
            print('Vehicles passed in lane 2 :', lane2_vehicle_cnt)
            #print('No of Ambulance passed in Lane 1 :', noOfambulances)
            print('Total vehicles passed: ', total_vehicles)
            print('Total time passed: ', timeElapsed)
            print('No. of vehicles passed per unit time: ', (float(total_vehicles) / float(timeElapsed)))

            print('Lane 1 Vehicles Count')
            print(lane1)
            #print('   ')
            # for element in lane1:
            #     print(element)

            print('Lane 2 Vehicles Count')
            print(lane2)
            # for element in lane2:
            #     print(element)
            print('Lane 1 green time')
            print(green_lane1)

            print('Lane2 green time')
            print(green_lane2)


            print('Ambulances passed in lane 1')
            print(ambulances_lane1)

            print('Ambulances passed in lane 2')
            print(ambulances_lane2)



            os._exit(1)


class Main:
    global total_ambulances1, total_ambulances2
    thread4 = threading.Thread(name="simulationTime", target=simulationTime, args=())
    thread4.daemon = True
    thread4.start()

    thread2 = threading.Thread(name="initialization", target=initialize, args=())  # initialization
    thread2.daemon = True
    thread2.start()

    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Screensize
    screenWidth = 1400
    screenHeight = 700
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    background = pygame.image.load('background2.png')

    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SIMULATION")

    # Loading signal images and font
    # redSignal = pygame.image.load('images/signals/red.png')
    redSignal = pygame.image.load('signals/red.png')
    yellowSignal = pygame.image.load('signals/yellow.png')
    greenSignal = pygame.image.load('signals/green.png')
    font = pygame.font.Font(None, 30)

    thread3 = threading.Thread(name="generateVehicles", target=generateVehicles, args=())  # Generating vehicles
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background, (0, 0))  # display background in simulation
        for i in range(0, noOfSignals):  # display signal and set timer according to current status: green, yello, or red
            if (i == currentGreen):
                if (currentYellow == 1):
                #if (i==currentGreen):
                    if (signals[i].yellow == 0):
                        signals[i].signalText = "STOP"
                    else:
                        signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    if (signals[i].green == 0):
                        signals[i].signalText = "SLOW"
                    else:
                        signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if (signals[i].red <= 10):
                    if (signals[i].red == 0):
                        signals[i].signalText = "GO"
                    else:
                        signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["", "", "", ""]

        # display signal timer and vehicle count
        for i in range(0, noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i])

            if (i != currentGreen):
                if(i == 0):
                    if(vehicles[directionNumbers[i]]['crossed'] >0 ):
                        lane1.append(vehicles[directionNumbers[i]]['crossed'])
                        ambulances_lane1.append(total_ambulances1)
                        #total_ambulances1=0
                else :
                    if (vehicles[directionNumbers[i]]['crossed'] > 0):
                        lane2.append(vehicles[directionNumbers[i]]['crossed'])
                        ambulances_lane2.append(total_ambulances2)
                        #total_ambulances2=0

                #-------------------------------------------------------------------------
                totalVehicles += vehicles[directionNumbers[i]]['crossed']
                vehicles[directionNumbers[i]]['crossed'] = 0
                if(i==0):
                    total_ambulances1=0
                else:
                    total_ambulances2=0

            displayText = vehicles[directionNumbers[i]]['crossed']

            vehicleCountTexts[i] = font.render(str(displayText), True, black, white)
            screen.blit(vehicleCountTexts[i], vehicleCountCoods[i])

        timeElapsedText = font.render(("Time Elapsed: " + str(timeElapsed)), True, black, white)
        screen.blit(timeElapsedText, (1100, 50))

        # display the vehicles
        for vehicle in simulation:
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            # vehicle.render(screen)
            vehicle.move()
        pygame.display.update()



Main()


