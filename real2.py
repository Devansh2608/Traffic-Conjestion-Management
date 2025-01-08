SIMULATION_TIME = 3600
PROBABILITY_DISTRIBUTION_ARRAY_OF_LANES = [25, 65, 80, 100]

PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES= [25, 40, 72, 79, 100]

PRESENT_GREEN = 0
UPCOMING_GREEN = (PRESENT_GREEN + 1) % 4

TRAVEL_SPEEDS = {'CAR_TYPE': [1.2, 1.25], 'BUS_TYPE': [1.1,1.16], 'TRUCK_TYPE': [1.1,1.16], 'AMBULANCE_TYPE': [1.2, 1.26],
                 'BIKE_TYPE': [1.5, 2]}

PRIORITY_CHANGE_RATE= {'CAR_TYPE': 0.1, 'BUS_TYPE': 0.2, 'TRUCK_TYPE': 0.18, 'AMBULANCE_TYPE': 1,
                 'BIKE_TYPE': 0.03}

MINIMUM_DEFAULT_TIME = 8
MAXIMUM_DEFAULT_TIME = 64

PRIORITY_OF_AMBULANCE = 7
PRIORITY_OF_BIKE = 0.5
PRIORITY_OF_TRUCK = 1.2
PRIORITY_OF_CAR = 0.8
PRIORITY_OF_BUS = 1.2

import pygame
import sys
import os
import time
import threading
import random


DEFAULT_YELLOW_SIGNAL_TIME = 5
DEFAULT_GREEN_SIGNAL_TIME = 30
DEFAULT_RED_SIGNAL_TIME = 150


EPSILON = 0.5
THRESHOLD_PRIORITY = 30

CURRENT_PRIORITY = 0
CURRENT_GREEN_SIGNAL_TIME = 0

PREVIOUS_GREEN_SIGNAL_TIME = DEFAULT_GREEN_SIGNAL_TIME

AMBULANCES_ROUTE_LANE1 = []
AMBULANCES_ROUTE_LANE2 = []
AMBULANCES_ROUTE_LANE3 = []
AMBULANCES_ROUTE_LANE4 = []

TOTAL_AMBULANCES1 = 0
TOTAL_AMBULANCES2 = 0
TOTAL_AMBULANCES3 = 0
TOTAL_AMBULANCES4 = 0

GREEN_ROUTE_LANE1 = [DEFAULT_GREEN_SIGNAL_TIME]
GREEN_ROUTE_LANE2 = []
GREEN_ROUTE_LANE3 = []
GREEN_ROUTE_LANE4 = []

ROUTE_LANE1 = []
ROUTE_LANE2 = []
ROUTE_LANE3 = []
ROUTE_LANE4 = []
TRAFFIC_LIGHTS = []


TOTAL_NO_OF_SIGNALS = 4
#######################

ELAPSED_TIMER = 0


UPCOMING_GREEN2= 0

PRESENT_YELLOW = 0

# Different Vehicles Count
CAR_COUNT = 0
BIKE_COUNT = 0
BUS_COUNT = 0
TRUCK_COUNT = 0
AMBULANCE_COUNT = 0

VEHICLE_COUNT = 0
ANGLE_OF_ROTATION = 3

RED_SIGNAL_DETECTION_TIME = 5

LIST_VEH = {'RS': {0: [], 1: [], 2: [], 'HAS_PASSED': 0}, 'DS': {0: [], 1: [], 2: [], 'HAS_PASSED': 0},
            'LS': {0: [], 1: [], 2: [], 'HAS_PASSED': 0}, 'US': {0: [], 1: [], 2: [], 'HAS_PASSED': 0}}
TYPE_VEH = {0: 'CAR_TYPE', 1: 'BUS_TYPE', 2: 'TRUCK_TYPE', 3: 'AMBULANCE_TYPE', 4: 'BIKE_TYPE'}
PATH_TYPE = {0: 'RS', 1: 'DS', 2: 'LS', 3: 'US'}

X_COORDINATE= {'RS': [1, 1, 1], 'DS': [754, 726, 698], 'LS': [1399, 1401, 1399], 'US': [601, 625, 658]}
Y_COORDINATE = {'RS': [350, 369, 400], 'DS': [1, 1, 1], 'LS': [500, 468, 435], 'US': [799, 801, 799]}


COORDINATES_OF_SIGNAL = [(531, 231), (811, 231), (811, 571), (531, 571)]
COORDINATES_OF_SIGNAL_TIMER = [(531, 211), (811, 211), (811, 551), (531, 551)]
COORDINATES_OF_VEHICLE_COUNT = [(479, 209), (879, 209), (879, 549), (479, 549)]
VEHICLE_COUNT_TEXTS = ["0", "0", "0", "0"]

STOP_POSITION_LINES = {'RS': 589, 'DS': 329, 'LS': 799, 'US': 534}
PRIMARY_STOP_POSITION = {'RS': 580, 'DS': 320, 'LS': 810, 'US': 545}
STOP_COORDINATES = {'RS': [579, 579, 580], 'DS': [319, 321, 319], 'LS': [809, 809, 809], 'US': [544, 544, 546]}

MID_POINT_COORDINATE = {'RS': {'X_COORDINATE': 703, 'Y_COORDINATE': 446}, 'DS': {'X_COORDINATE': 694, 'Y_COORDINATE': 451}, 'LS': {'X_COORDINATE': 693, 'Y_COORDINATE': 423},
       'US': {'X_COORDINATE': 694, 'Y_COORDINATE': 399}}
ANGLE_OF_ROTATION = 3

GAPPING = 17
GAPPING2 = 17  # moving GAPPING

pygame.init()
TRAFFIC_OBJECTS = pygame.sprite.Group()


class INITIALIZE_VEH(pygame.sprite.Sprite):
    #global TOTAL_AMBULANCES1, TOTAL_AMBULANCES2
    def __init__(self, ROUTE_LANE, type_of_vehicle, dir_index, DIR_TYPE, is_Turning):

        pygame.sprite.Sprite.__init__(self)
        self.HAS_PASSED = 0
        self.X_COORDINATE = X_COORDINATE[DIR_TYPE][ROUTE_LANE]
        self.Y_COORDINATE = Y_COORDINATE[DIR_TYPE][ROUTE_LANE]
        self.has_turned = 0
        self.time= ELAPSED_TIMER
        self.stop_position = -1
        self.DIR_TYPE = DIR_TYPE
        self.ROUTE_LANE = ROUTE_LANE
        self.type_of_vehicle = type_of_vehicle
        #print(self.type_of_vehicle)
        probability= random.randint(0,100)
        lower_speed= TRAVEL_SPEEDS[type_of_vehicle][0]
        upper_speed= TRAVEL_SPEEDS[type_of_vehicle][1]
        travel_speed= lower_speed + (upper_speed-lower_speed)* probability * 0.01
        self.travel_speed = travel_speed
        self.dir_index = dir_index

        # pygame.sprite.Sprite.__init__(self)
        self.VEH_ANGLE_OF_ROTATION = 0
        self.shouldTurn = is_Turning
        self.CHANGE_DIRECTION = 0
        LIST_VEH[DIR_TYPE][ROUTE_LANE].append(self)

        self.VEH_IND = len(LIST_VEH[DIR_TYPE][ROUTE_LANE]) - 1

        IMG_ROUTE = DIR_TYPE + "/" + type_of_vehicle + ".png"

        self.VEH_CURR_IMG = pygame.image.load(IMG_ROUTE)
        self.VEH_IMG = pygame.image.load(IMG_ROUTE)

        if (DIR_TYPE == 'DS'):
            if (len(LIST_VEH[DIR_TYPE][ROUTE_LANE]) <= 1 or LIST_VEH[DIR_TYPE][ROUTE_LANE][
                self.VEH_IND - 1].HAS_PASSED != 0):
                self.stop_position = PRIMARY_STOP_POSITION[DIR_TYPE]

            else:
                self.stop_position = LIST_VEH[DIR_TYPE][ROUTE_LANE][self.VEH_IND - 1].stop_position - \
                                     LIST_VEH[DIR_TYPE][ROUTE_LANE][
                                         self.VEH_IND - 1].VEH_CURR_IMG.get_rect().height - GAPPING
            dummy = self.VEH_CURR_IMG.get_rect().height + GAPPING
            Y_COORDINATE[DIR_TYPE][ROUTE_LANE] -= dummy
            STOP_COORDINATES[DIR_TYPE][ROUTE_LANE] -= dummy


        elif (DIR_TYPE == 'US'):
            if (len(LIST_VEH[DIR_TYPE][ROUTE_LANE]) <= 1 or LIST_VEH[DIR_TYPE][ROUTE_LANE][
                self.VEH_IND - 1].HAS_PASSED != 0):
                self.stop_position = PRIMARY_STOP_POSITION[DIR_TYPE]
            else:
                self.stop_position = LIST_VEH[DIR_TYPE][ROUTE_LANE][self.VEH_IND - 1].stop_position + \
                                     LIST_VEH[DIR_TYPE][ROUTE_LANE][
                                         self.VEH_IND - 1].VEH_CURR_IMG.get_rect().height + GAPPING
            dummy = self.VEH_CURR_IMG.get_rect().height + GAPPING
            Y_COORDINATE[DIR_TYPE][ROUTE_LANE] += dummy
            STOP_COORDINATES[DIR_TYPE][ROUTE_LANE] += dummy


        elif (DIR_TYPE == 'LS'):
            if (len(LIST_VEH[DIR_TYPE][ROUTE_LANE]) <= 1 or LIST_VEH[DIR_TYPE][ROUTE_LANE][
                self.VEH_IND - 1].HAS_PASSED != 0):
                self.stop_position = PRIMARY_STOP_POSITION[DIR_TYPE]
            else:
                self.stop_position = LIST_VEH[DIR_TYPE][ROUTE_LANE][self.VEH_IND - 1].stop_position + \
                                     LIST_VEH[DIR_TYPE][ROUTE_LANE][
                                         self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width + GAPPING

            dummy = self.VEH_CURR_IMG.get_rect().width + GAPPING
            X_COORDINATE[DIR_TYPE][ROUTE_LANE] += dummy
            STOP_COORDINATES[DIR_TYPE][ROUTE_LANE] += dummy



        elif (DIR_TYPE == 'RS'):
            if (len(LIST_VEH[DIR_TYPE][ROUTE_LANE]) <= 1 or LIST_VEH[DIR_TYPE][ROUTE_LANE][
                self.VEH_IND - 1].HAS_PASSED != 0):
                self.stop_position = PRIMARY_STOP_POSITION[DIR_TYPE]
            else:
                self.stop_position = LIST_VEH[DIR_TYPE][ROUTE_LANE][self.VEH_IND - 1].stop_position - \
                                     LIST_VEH[DIR_TYPE][ROUTE_LANE][
                                         self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width - GAPPING

            # Set new starting and stop_positionping coordinate
            dummy = GAPPING + self.VEH_CURR_IMG.get_rect().width
            STOP_COORDINATES[DIR_TYPE][ROUTE_LANE] -= dummy
            X_COORDINATE[DIR_TYPE][ROUTE_LANE] -= dummy

        TRAFFIC_OBJECTS.add(self)

    def vehicleMovement(self):
        global TOTAL_AMBULANCES1, TOTAL_AMBULANCES2, TOTAL_AMBULANCES3, TOTAL_AMBULANCES4

        ###############################################################################################################

        if (self.DIR_TYPE == 'DS'):
            if (self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height > STOP_POSITION_LINES[
                self.DIR_TYPE] and self.HAS_PASSED != 1):
                self.HAS_PASSED = 1
                LIST_VEH[self.DIR_TYPE]['HAS_PASSED'] += 1

                if (self.type_of_vehicle == 'AMBULANCE_TYPE'):
                    TOTAL_AMBULANCES2 += 1
#/ /////////////////////mark
            if (self.shouldTurn != 0):
                if (self.HAS_PASSED != 1 or MID_POINT_COORDINATE[self.DIR_TYPE]['Y_COORDINATE'] > self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height ):
#////////////////////////////////////////////
                    if (( self.stop_position >= self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height or (
                            PRESENT_GREEN == 1 and PRESENT_YELLOW == 0) or self.HAS_PASSED == 1) and (
                            self.VEH_IND == 0 or self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height < (
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE - GAPPING2) or
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION != 0)):
                        self.Y_COORDINATE += self.travel_speed

                else:

                    if (self.CHANGE_DIRECTION != 1):
                        self.VEH_CURR_IMG = pygame.transform.rotate(self.VEH_IMG, -self.VEH_ANGLE_OF_ROTATION)
                        self.X_COORDINATE -= 2.49
                        self.Y_COORDINATE += 1.99
                        self.VEH_ANGLE_OF_ROTATION += ANGLE_OF_ROTATION

                        if (self.VEH_ANGLE_OF_ROTATION == 90):
                            self.CHANGE_DIRECTION = 1

                    else:

                        if (self.VEH_IND == 0 or self.X_COORDINATE > (LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE +
                                                         LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                                             self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width + GAPPING2) or self.Y_COORDINATE < (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE - GAPPING2)):
                            self.X_COORDINATE -= self.travel_speed

            else:

                if ((self.HAS_PASSED != 0 or self.stop_position >= self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height    or (
                        PRESENT_GREEN == 1 and PRESENT_YELLOW == 0)) and (
                        self.VEH_IND == 0 or self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height < (
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE - GAPPING2) or (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION != 0))):
                    self.Y_COORDINATE += self.travel_speed

            ####################################################################################
        elif (self.DIR_TYPE == 'RS'):
            if (self.HAS_PASSED != 1 and self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width > STOP_POSITION_LINES[
                self.DIR_TYPE]):  # if the image has HAS_PASSED stop_position line now
                self.HAS_PASSED = 1
                LIST_VEH[self.DIR_TYPE]['HAS_PASSED'] += 1
                if (self.type_of_vehicle == 'AMBULANCE_TYPE'):
                    TOTAL_AMBULANCES1 += 1
            if (self.shouldTurn != 0):
                if (self.HAS_PASSED != 1 or self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width < MID_POINT_COORDINATE[self.DIR_TYPE]['X_COORDINATE']):
                    if ((self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width <= self.stop_position or (
                            PRESENT_GREEN == 0 and PRESENT_YELLOW == 0) or self.HAS_PASSED != 0) and (
                            self.VEH_IND == 0 or self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width < (
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE - GAPPING2) or
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION != 0)):
                        self.X_COORDINATE += self.travel_speed
                else:
                    if (self.CHANGE_DIRECTION != 1):
                        self.VEH_ANGLE_OF_ROTATION += ANGLE_OF_ROTATION
                        self.VEH_CURR_IMG = pygame.transform.rotate(self.VEH_IMG, -self.VEH_ANGLE_OF_ROTATION)
                        self.X_COORDINATE += 1.99
                        self.Y_COORDINATE += 1.79
                        if (self.VEH_ANGLE_OF_ROTATION == 90):
                            self.CHANGE_DIRECTION = 1
                    else:
                        if (self.VEH_IND == 0 or self.Y_COORDINATE + self.VEH_CURR_IMG.get_rect().height < (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                    self.VEH_IND - 1].Y_COORDINATE - GAPPING2) or self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width < (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE - GAPPING2)):
                            self.Y_COORDINATE += self.travel_speed
            else:
                if ((self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width <= self.stop_position or self.HAS_PASSED != 0 or (
                        PRESENT_GREEN == 0 and PRESENT_YELLOW == 0)) and (
                        self.VEH_IND == 0 or self.X_COORDINATE + self.VEH_CURR_IMG.get_rect().width < (
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE - GAPPING2) or (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION != 0))):
                    # (if the image has not reached its stop_position coordinate or has HAS_PASSED stop_position line or has green signal) and (it is either the first vehicle in that ROUTE_LANE or it is has enough GAPPING to the next vehicle in that ROUTE_LANE)
                    self.X_COORDINATE += self.travel_speed  # vehicleMovement the vehicle

        # ////////////////////

        ###########################################

        elif (self.DIR_TYPE == 'US'):
            if (self.HAS_PASSED != 1 and STOP_POSITION_LINES[self.DIR_TYPE] > self.Y_COORDINATE ):
                self.HAS_PASSED = 1
                LIST_VEH[self.DIR_TYPE]['HAS_PASSED'] += 1
                if (self.type_of_vehicle == 'AMBULANCE_TYPE'):
                    TOTAL_AMBULANCES4 += 1
            if (self.shouldTurn != 0):

                if (self.HAS_PASSED != 1 or MID_POINT_COORDINATE[self.DIR_TYPE]['Y_COORDINATE'] < self.Y_COORDINATE  ):
                    if ((self.Y_COORDINATE >= self.stop_position or (
                            PRESENT_GREEN == 3 and PRESENT_YELLOW == 0) or self.HAS_PASSED != 0) and (
                            self.VEH_IND == 0 or self.Y_COORDINATE > (
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE +
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                self.VEH_IND - 1].VEH_CURR_IMG.get_rect().height + GAPPING2) or
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                self.VEH_IND - 1].CHANGE_DIRECTION != 0)):
                        self.Y_COORDINATE -= self.travel_speed
                else:
                    if (self.CHANGE_DIRECTION != 1):

                        self.X_COORDINATE += 1
                        self.Y_COORDINATE -= 1
                        self.VEH_ANGLE_OF_ROTATION += ANGLE_OF_ROTATION
                        self.VEH_CURR_IMG = pygame.transform.rotate(self.VEH_IMG, -self.VEH_ANGLE_OF_ROTATION)
                        if (self.VEH_ANGLE_OF_ROTATION == 90):
                            self.CHANGE_DIRECTION = 1
                    else:
                        if (self.VEH_IND == 0 or self.X_COORDINATE < (LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE -
                                                         LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                                             self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width - GAPPING2) or self.Y_COORDINATE > (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE + GAPPING2)):
                            self.X_COORDINATE += self.travel_speed
            else:
                if ((self.HAS_PASSED != 0 or self.Y_COORDINATE >= self.stop_position  or (
                        PRESENT_GREEN == 3 and PRESENT_YELLOW == 0)) and (
                        self.VEH_IND == 0 or self.Y_COORDINATE > (
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE +
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                            self.VEH_IND - 1].VEH_CURR_IMG.get_rect().height + GAPPING2) or (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION != 0))):
                    self.Y_COORDINATE -= self.travel_speed

        #         //
        elif (self.DIR_TYPE == 'LS'):
            if (self.HAS_PASSED != 1 and self.X_COORDINATE < STOP_POSITION_LINES[self.DIR_TYPE]):
                self.HAS_PASSED = 1
                LIST_VEH[self.DIR_TYPE]['HAS_PASSED'] += 1
                if (self.type_of_vehicle == 'AMBULANCE_TYPE'):
                    TOTAL_AMBULANCES3 += 1

            if (self.shouldTurn != 0):
                if (self.HAS_PASSED != 1 or self.X_COORDINATE > MID_POINT_COORDINATE[self.DIR_TYPE]['X_COORDINATE']):
                    if ((self.X_COORDINATE >= self.stop_position or (
                            PRESENT_GREEN == 2 and PRESENT_YELLOW == 0) or self.HAS_PASSED != 0) and (
                            self.VEH_IND == 0 or self.X_COORDINATE > (
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE +
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width + GAPPING2) or
                            LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                self.VEH_IND - 1].CHANGE_DIRECTION != 0)):
                        self.X_COORDINATE -= self.travel_speed
                else:
                    if (self.CHANGE_DIRECTION != 1):
                        self.VEH_ANGLE_OF_ROTATION += ANGLE_OF_ROTATION
                        self.VEH_CURR_IMG = pygame.transform.rotate(self.VEH_IMG, -self.VEH_ANGLE_OF_ROTATION)
                        self.X_COORDINATE -= 1.79
                        self.Y_COORDINATE -= 2.49
                        if (self.VEH_ANGLE_OF_ROTATION == 90):
                            self.CHANGE_DIRECTION = 1
                    else:
                        if (self.VEH_IND == 0 or self.Y_COORDINATE > (LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].Y_COORDINATE +
                                                         LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                                                             self.VEH_IND - 1].VEH_CURR_IMG.get_rect().height + GAPPING2) or self.X_COORDINATE > (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE + GAPPING2)):
                            self.Y_COORDINATE -= self.travel_speed
            else:
                if ((self.X_COORDINATE >= self.stop_position or self.HAS_PASSED != 0 or (
                        PRESENT_GREEN == 2 and PRESENT_YELLOW == 0)) and (
                        self.VEH_IND == 0 or self.X_COORDINATE > (
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].X_COORDINATE +
                        LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][
                            self.VEH_IND - 1].VEH_CURR_IMG.get_rect().width + GAPPING2) or (
                                LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND - 1].CHANGE_DIRECTION == 1))):
                    # (if the image has not reached its stop_position coordinate or has HAS_PASSED stop_position line or has green signal) and (it is either the first vehicle in that ROUTE_LANE or it is has enough GAPPING to the next vehicle in that ROUTE_LANE)
                    self.X_COORDINATE -= self.travel_speed  # vehicleMovement the vehicle
            # if((self.x>=self.stop_position or self.HAS_PASSED == 1 or (PRESENT_GREEN==2 and PRESENT_YELLOW==0)) and (self.VEH_IND==0 or self.x>(LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND-1].x + LIST_VEH[self.DIR_TYPE][self.ROUTE_LANE][self.VEH_IND-1].VEH_CURR_IMG.get_rect().width + GAPPING2))):
            #     self.x -= self.travel_speed


# #########################################################################

class SIGNAL_LIGHT:
    def __init__(self, SIGNAL_RED_LIGHT, SIGNAL_YELLOW_LIGHT, SIGNAL_GREEN_LIGHT):
        self.SIGNAL_RED_LIGHT = SIGNAL_RED_LIGHT
        self.SIGNAL_YELLOW_LIGHT = SIGNAL_YELLOW_LIGHT
        self.SIGNAL_GREEN_LIGHT = SIGNAL_GREEN_LIGHT

        #self.signalText = "30"
        self.totalGreenTime = 0



# Initialization of signals with default values
def trafficLightInitializer():
    TRAFFIC_SIGNAL1 = SIGNAL_LIGHT(0, DEFAULT_YELLOW_SIGNAL_TIME, DEFAULT_GREEN_SIGNAL_TIME)
    TRAFFIC_LIGHTS.append(TRAFFIC_SIGNAL1)
    TRAFFIC_SIGNAL2 = SIGNAL_LIGHT(TRAFFIC_SIGNAL1.SIGNAL_RED_LIGHT + TRAFFIC_SIGNAL1.SIGNAL_YELLOW_LIGHT + TRAFFIC_SIGNAL1.SIGNAL_GREEN_LIGHT, DEFAULT_YELLOW_SIGNAL_TIME, DEFAULT_GREEN_SIGNAL_TIME)
    TRAFFIC_LIGHTS.append(TRAFFIC_SIGNAL2)
    TRAFFIC_SIGNAL3 = SIGNAL_LIGHT(DEFAULT_RED_SIGNAL_TIME, DEFAULT_YELLOW_SIGNAL_TIME, DEFAULT_GREEN_SIGNAL_TIME)
    TRAFFIC_LIGHTS.append(TRAFFIC_SIGNAL3)
    TRAFFIC_SIGNAL4 = SIGNAL_LIGHT(DEFAULT_RED_SIGNAL_TIME, DEFAULT_YELLOW_SIGNAL_TIME, DEFAULT_GREEN_SIGNAL_TIME)
    TRAFFIC_LIGHTS.append(TRAFFIC_SIGNAL4)
    recursor()


# Set time according to formula
def DYNAMIC_GREEN_TIME():
    global CAR_COUNT, BIKE_COUNT, BUS_COUNT, TRUCK_COUNT, AMBULANCE_COUNT, noOfROUTE_LANEs
    global PREVIOUS_GREEN_SIGNAL_TIME, CURRENT_GREEN_SIGNAL_TIME, CURRENT_PRIORITY, THRESHOLD_PRIORITY, EPSILON



    CNT= [0, 0, 0]

    CAR_COUNT, BUS_COUNT, TRUCK_COUNT, AMBULANCE_COUNT, BIKE_COUNT = 0, 0, 0, 0, 0
    for bike_index in range(len(LIST_VEH[PATH_TYPE[UPCOMING_GREEN]][0])):
        bike = LIST_VEH[PATH_TYPE[UPCOMING_GREEN]][0][bike_index]

        if (bike.HAS_PASSED == 0):
            CNT[0]+=1

    for semi_Lane in range(1, 3):
        for veh in range(len(LIST_VEH[PATH_TYPE[UPCOMING_GREEN]][semi_Lane])):
            vehicle = LIST_VEH[PATH_TYPE[UPCOMING_GREEN]][semi_Lane][veh]
            if (vehicle.HAS_PASSED == 0):
                CNT[semi_Lane]+=1

    maxi= max(CNT[0], CNT[1], CNT[2])



    greenTime = 3+ maxi
    greenTime= DEFAULT_GREEN_SIGNAL_TIME

    if (greenTime < MINIMUM_DEFAULT_TIME):
        greenTime = MINIMUM_DEFAULT_TIME
    elif (greenTime > MAXIMUM_DEFAULT_TIME):
        greenTime = MAXIMUM_DEFAULT_TIME

    TRAFFIC_LIGHTS[UPCOMING_GREEN % (TOTAL_NO_OF_SIGNALS)].SIGNAL_GREEN_LIGHT = greenTime

    CAR_COUNT = 0
    BUS_COUNT = 0
    TRUCK_COUNT = 0
    AMBULANCE_COUNT = 0
    BIKE_COUNT = 0

    if (UPCOMING_GREEN == 0):
        GREEN_ROUTE_LANE1.append(greenTime)

    elif (UPCOMING_GREEN == 1):
        GREEN_ROUTE_LANE2.append(greenTime)

    elif (UPCOMING_GREEN == 2):
        GREEN_ROUTE_LANE3.append(greenTime)

    else:
        GREEN_ROUTE_LANE4.append(greenTime)

def calc_upcoming_green():
    global UPCOMING_GREEN, PRESENT_GREEN, CAR_COUNT, BUS_COUNT, TRUCK_COUNT, AMBULANCE_COUNT, BIKE_COUNT, UPCOMING_GREEN2

    cp= 0
    for i in range (0, 4):
        dynamic_priority = 0

        CAR_COUNT, BUS_COUNT, TRUCK_COUNT, AMBULANCE_COUNT, BIKE_COUNT = 0, 0, 0, 0, 0
        t= ELAPSED_TIMER
        for bike_index in range(len(LIST_VEH[PATH_TYPE[i]][0])):
            bike = LIST_VEH[PATH_TYPE[i]][0][bike_index]
            veh_time = bike.time
            if (bike.HAS_PASSED == 0):
                BIKE_COUNT += 1
                dynamic_priority += (t-veh_time)*(PRIORITY_CHANGE_RATE['BIKE_TYPE'])
        for semi_Lane in range(1, 3):
            for veh in range(len(LIST_VEH[PATH_TYPE[i]][semi_Lane])):
                vehicle = LIST_VEH[PATH_TYPE[i]][semi_Lane][veh]
                if (vehicle.HAS_PASSED == 0):
                    vehicle_class = vehicle.type_of_vehicle
                    veh_time = vehicle.time
                    if (vehicle_class == 'CAR_TYPE'):
                        CAR_COUNT += 1
                    elif (vehicle_class == 'BUS_TYPE'):
                        BUS_COUNT += 1
                    elif (vehicle_class == 'TRUCK_TYPE'):
                        TRUCK_COUNT += 1
                    elif (vehicle_class == 'AMBULANCE_TYPE'):
                        AMBULANCE_COUNT += 1

                    dynamic_priority+= (t-veh_time)*(PRIORITY_CHANGE_RATE[vehicle_class])

        curr_priority = CAR_COUNT * PRIORITY_OF_CAR + BIKE_COUNT * PRIORITY_OF_BIKE + AMBULANCE_COUNT * PRIORITY_OF_AMBULANCE + TRUCK_COUNT * PRIORITY_OF_TRUCK + BUS_COUNT * PRIORITY_OF_BUS + dynamic_priority
        if(curr_priority > cp and i!=PRESENT_GREEN):
            cp= curr_priority
            UPCOMING_GREEN= i


    CAR_COUNT, BUS_COUNT, TRUCK_COUNT, AMBULANCE_COUNT, BIKE_COUNT = 0, 0, 0, 0, 0

def recursor():
    global PRESENT_GREEN, PRESENT_YELLOW, UPCOMING_GREEN, UPCOMING_GREEN2
    while (TRAFFIC_LIGHTS[PRESENT_GREEN].SIGNAL_GREEN_LIGHT != 6):
        updateTimerValues()
        time.sleep(1)


    #calc_upcoming_green()
    UPCOMING_GREEN= (PRESENT_GREEN+1)%4
    TRAFFIC_LIGHTS[UPCOMING_GREEN].SIGNAL_RED_LIGHT = 5 + TRAFFIC_LIGHTS[PRESENT_GREEN].SIGNAL_GREEN_LIGHT
    th = threading.Thread(name="detection", target=DYNAMIC_GREEN_TIME, args=())
    th.daemon = True
    th.start()

    while (TRAFFIC_LIGHTS[PRESENT_GREEN].SIGNAL_GREEN_LIGHT != 0):
        updateTimerValues()
        time.sleep(1)

    PRESENT_YELLOW = 1  # set yellow signal on
    VEHICLE_COUNT_TEXTS[PRESENT_GREEN] = "0"
    # reset stop_position coordinates of ROUTE_LANEs and vehicles
    for semi_lane in range(0, 3):
        STOP_COORDINATES[PATH_TYPE[PRESENT_GREEN]][semi_lane] = PRIMARY_STOP_POSITION[PATH_TYPE[PRESENT_GREEN]]
        for vehicle in LIST_VEH[PATH_TYPE[PRESENT_GREEN]][semi_lane]:
            vehicle.stop_position = PRIMARY_STOP_POSITION[PATH_TYPE[PRESENT_GREEN]]
    while (TRAFFIC_LIGHTS[PRESENT_GREEN].SIGNAL_YELLOW_LIGHT > 0):  # while the timer of current yellow signal is not zero
        updateTimerValues()
        time.sleep(1)
    PRESENT_YELLOW = 0  # set yellow signal off

    TRAFFIC_LIGHTS[PRESENT_GREEN].SIGNAL_YELLOW_LIGHT = DEFAULT_YELLOW_SIGNAL_TIME

    PRESENT_GREEN = UPCOMING_GREEN
    recursor()



def vehicleGenerator():
    #global TOTAL_AMBULANCES1, TOTAL_AMBULANCES2

    while (True):
        vehicle_Class = 0
        temp= random.randint(0, 99)

        if(temp < PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES[0]):
            vehicle_Class=0

        elif(temp<PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES[1]):
            vehicle_Class=1

        elif(temp< PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES[2]):
            vehicle_Class=2

        elif(temp< PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES[3]):
            vehicle_Class=3

        else:
            vehicle_Class=4

        g=0



        # PROBABILITY_DISTRIBUTION_ARRAY_OF_VEHICLES
        if (vehicle_Class != 4):
            ROUTE_LANE_number = random.randint(0, 1) + 1
        else:
            ROUTE_LANE_number = 0
        is_Turning = 0
        if (ROUTE_LANE_number == 2):
            dummy = random.randint(0, 4)
            if (dummy > 2):
                is_Turning = 0
            elif (dummy <= 2):
                is_Turning = 1
        dummy = random.randint(0, 99)
        dir_index = 0

        if (dummy < PROBABILITY_DISTRIBUTION_ARRAY_OF_LANES[0]):
            dir_index = 0
        elif (dummy < PROBABILITY_DISTRIBUTION_ARRAY_OF_LANES[1]):
            dir_index = 1
        elif (dummy < PROBABILITY_DISTRIBUTION_ARRAY_OF_LANES[2]):
            dir_index = 2
        elif (dummy < PROBABILITY_DISTRIBUTION_ARRAY_OF_LANES[3]):
            dir_index = 3
        INITIALIZE_VEH(ROUTE_LANE_number, TYPE_VEH[vehicle_Class], dir_index, PATH_TYPE[dir_index],
                is_Turning)

        timee = random.randint(8, 14)
        aa = timee * 0.2
        time.sleep(aa)

# Updating the values of  signal timer at every second
def updateTimerValues():
    for signal_No in range(0, TOTAL_NO_OF_SIGNALS):
        if (signal_No != PRESENT_GREEN):
            TRAFFIC_LIGHTS[signal_No].SIGNAL_RED_LIGHT -= 1
        else:
            if (PRESENT_YELLOW != 0):
                TRAFFIC_LIGHTS[signal_No].SIGNAL_YELLOW_LIGHT -= 1
            else:
                TRAFFIC_LIGHTS[signal_No].SIGNAL_GREEN_LIGHT -= 1
                TRAFFIC_LIGHTS[signal_No].totalGreenTime += 1
def TIME_OF_SIMULATION():
    global  TOTAL_AMBULANCES1, TOTAL_AMBULANCES2, TOTAL_AMBULANCES3, TOTAL_AMBULANCES4, ELAPSED_TIMER, SIMULATION_TIME
    while (True):
        ELAPSED_TIMER += 1
        time.sleep(1)

        total_vehicles = 0
        if (SIMULATION_TIME == ELAPSED_TIMER):
            ROUTE_LANE1_vehicle_cnt = 0
            ROUTE_LANE2_vehicle_cnt = 0
            ROUTE_LANE3_vehicle_cnt = 0
            ROUTE_LANE4_vehicle_cnt = 0
            for lane_No in range(TOTAL_NO_OF_SIGNALS):
                if (LIST_VEH[PATH_TYPE[lane_No]]['HAS_PASSED'] > 0):
                    if (lane_No == 0):
                        ROUTE_LANE1.append(LIST_VEH[PATH_TYPE[lane_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE1.append(TOTAL_AMBULANCES1)
                        #TOTAL_AMBULANCES1 = 0
                    elif (lane_No == 1):
                        ROUTE_LANE2.append(LIST_VEH[PATH_TYPE[lane_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE2.append(TOTAL_AMBULANCES2)
                    elif (lane_No == 2):
                        ROUTE_LANE3.append(LIST_VEH[PATH_TYPE[lane_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE3.append(TOTAL_AMBULANCES3)
                    else:
                        ROUTE_LANE4.append(LIST_VEH[PATH_TYPE[lane_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE4.append(TOTAL_AMBULANCES4)

            #VEHICLE_COUNT = 0
            print('ROUTE_LANE-wise Vehicle Counts')
            for lane_Vehicle_Count in ROUTE_LANE1:
                ROUTE_LANE1_vehicle_cnt += lane_Vehicle_Count

            for lane_Vehicle_Count in ROUTE_LANE2:
                ROUTE_LANE2_vehicle_cnt += lane_Vehicle_Count

            for lane_Vehicle_Count in ROUTE_LANE3:
                ROUTE_LANE3_vehicle_cnt += lane_Vehicle_Count

            for lane_Vehicle_Count in ROUTE_LANE4:
                ROUTE_LANE4_vehicle_cnt += lane_Vehicle_Count

            total_vehicles = ROUTE_LANE1_vehicle_cnt + ROUTE_LANE2_vehicle_cnt + ROUTE_LANE3_vehicle_cnt + ROUTE_LANE4_vehicle_cnt

            print('Vehicles passed in ROUTE_LANE 1 :', ROUTE_LANE1_vehicle_cnt)
            print('Vehicles passed in ROUTE_LANE 2 :', ROUTE_LANE2_vehicle_cnt)

            print('Vehicles passed in ROUTE_LANE 3 :', ROUTE_LANE3_vehicle_cnt)
            print('Vehicles passed in ROUTE_LANE 4 :', ROUTE_LANE4_vehicle_cnt)

            #print('No of Ambulance passed in ROUTE_LANE 1 :', AMBULANCE_COUNT)
            print('Total vehicles passed: ', total_vehicles)
            print('Total time passed: ', ELAPSED_TIMER)
            print('No. of vehicles passed per unit time: ', (float(total_vehicles) / float(ELAPSED_TIMER)))

            print('ROUTE_LANE 1 Vehicles Count')
            print(ROUTE_LANE1)

            print('ROUTE_LANE 2 Vehicles Count')
            print(ROUTE_LANE2)

            print('ROUTE_LANE 3 Vehicles Count')
            print(ROUTE_LANE3)

            print('ROUTE_LANE 4 Vehicles Count')
            print(ROUTE_LANE4)

            print('ROUTE_LANE 1 green time')
            print(GREEN_ROUTE_LANE1)

            print('ROUTE_LANE 2 green time')
            print(GREEN_ROUTE_LANE2)

            print('ROUTE_LANE 3 green time')
            print(GREEN_ROUTE_LANE3)

            print('ROUTE_LANE 4 green time')
            print(GREEN_ROUTE_LANE4)

            print('Ambulances passed in ROUTE_LANE 1')
            print(AMBULANCES_ROUTE_LANE1)

            print('Ambulances passed in ROUTE_LANE 2')
            print(AMBULANCES_ROUTE_LANE2)

            print('Ambulances passed in ROUTE_LANE 3')
            print(AMBULANCES_ROUTE_LANE3)

            print('Ambulances passed in ROUTE_LANE 4')
            print(AMBULANCES_ROUTE_LANE4)

            os._exit(1)


class Main:
    global TOTAL_AMBULANCES1, TOTAL_AMBULANCES2

    black_color = (0, 0, 0)
    white_color = (255, 255, 255)

    t1 = threading.Thread(name="TIME_OF_SIMULATION", target=TIME_OF_SIMULATION, args=())
    t2 = threading.Thread(name="initialization", target=trafficLightInitializer, args=())
    t3 = threading.Thread(name="vehicleGenerator", target=vehicleGenerator, args=())

    HEIGHT_OF_SCREEN = 750
    WIDTH_OF_SCREEN = 1450

    SIZE_OF_SCREEN = (WIDTH_OF_SCREEN, HEIGHT_OF_SCREEN)

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()


    # Loading the image of intersection in the background
    CROSS_SECTION_IMAGE = pygame.image.load('cross_section_image.png')

    SIMULATION_WINDOW = pygame.display.set_mode(SIZE_OF_SCREEN)
    pygame.display.set_caption("SIMULATION")

    GREEN_LIGHT = pygame.image.load('TRAFFIC_LIGHTS/GREEN_LIGHT.png')
    RED_LIGHT = pygame.image.load('TRAFFIC_LIGHTS/RED_LIGHT.png')
    YELLOW_LIGHT = pygame.image.load('TRAFFIC_LIGHTS/YELLOW_LIGHT.png')

    SIMULATION_STYLE = pygame.font.Font(None, 30)

    while True:
        for simulation_Event in pygame.event.get():
            if simulation_Event.type == pygame.QUIT:
                sys.exit()

        SIMULATION_WINDOW.blit(CROSS_SECTION_IMAGE, (0, 0))  # IT IS USED FOR DISPLAYING SIMULATION BACKGROUND
        for current_Signal in range(0, TOTAL_NO_OF_SIGNALS):
            if (PRESENT_GREEN != current_Signal):
                if (TRAFFIC_LIGHTS[current_Signal].SIGNAL_RED_LIGHT <= 10 and TRAFFIC_LIGHTS[current_Signal].SIGNAL_RED_LIGHT >= 0):
                    if (TRAFFIC_LIGHTS[current_Signal].SIGNAL_RED_LIGHT == 0):
                        TRAFFIC_LIGHTS[current_Signal].signalText = "GO"
                    else:
                        TRAFFIC_LIGHTS[current_Signal].signalText = TRAFFIC_LIGHTS[current_Signal].SIGNAL_RED_LIGHT
                elif (TRAFFIC_LIGHTS[current_Signal].SIGNAL_RED_LIGHT < 0):
                    TRAFFIC_LIGHTS[current_Signal].signalText = "---"

                else:
                    TRAFFIC_LIGHTS[current_Signal].signalText = "---"
                SIMULATION_WINDOW.blit(RED_LIGHT, COORDINATES_OF_SIGNAL[current_Signal])

            else:
                if (PRESENT_YELLOW != 1):
                    if (TRAFFIC_LIGHTS[current_Signal].SIGNAL_GREEN_LIGHT != 0):
                        TRAFFIC_LIGHTS[current_Signal].signalText = TRAFFIC_LIGHTS[current_Signal].SIGNAL_GREEN_LIGHT
                    else:
                        TRAFFIC_LIGHTS[current_Signal].signalText = "SLOW"
                    SIMULATION_WINDOW.blit(GREEN_LIGHT, COORDINATES_OF_SIGNAL[current_Signal])
                else:
                    if (TRAFFIC_LIGHTS[current_Signal].SIGNAL_YELLOW_LIGHT != 0):
                        TRAFFIC_LIGHTS[current_Signal].signalText = TRAFFIC_LIGHTS[current_Signal].SIGNAL_YELLOW_LIGHT
                    else:
                        TRAFFIC_LIGHTS[current_Signal].signalText = "STOP"
                    SIMULATION_WINDOW.blit(YELLOW_LIGHT, COORDINATES_OF_SIGNAL[current_Signal])
                #///////////

        signalTexts = ["", "", "", ""]

        # showing vehicle count and signal timer

        for signal_No in range(0, TOTAL_NO_OF_SIGNALS):
            signalTexts[signal_No] = SIMULATION_STYLE.render(str(TRAFFIC_LIGHTS[signal_No].signalText), True, white_color, black_color)
            SIMULATION_WINDOW.blit(signalTexts[signal_No], COORDINATES_OF_SIGNAL_TIMER[signal_No])

            if (signal_No != PRESENT_GREEN):
                if (signal_No == 0):
                    if (LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'] > 0):
                        ROUTE_LANE1.append(LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE1.append(TOTAL_AMBULANCES1)
                        #TOTAL_AMBULANCES1=0
                elif (signal_No == 1):
                    if (LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'] > 0):
                        ROUTE_LANE2.append(LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE2.append(TOTAL_AMBULANCES2)
                        #TOTAL_AMBULANCES2=0

                elif (signal_No == 2):
                    if (LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'] > 0):
                        ROUTE_LANE3.append(LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE3.append(TOTAL_AMBULANCES3)
                        # TOTAL_AMBULANCES3=0
                else:
                    if (LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'] > 0):
                        ROUTE_LANE4.append(LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'])
                        AMBULANCES_ROUTE_LANE4.append(TOTAL_AMBULANCES4)
                        # TOTAL_AMBULANCES4=0

                #-------------------------------------------------------------------------
                VEHICLE_COUNT += LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED']
                LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED'] = 0
                if (signal_No == 0):
                    TOTAL_AMBULANCES1 = 0
                elif (signal_No == 1):
                    TOTAL_AMBULANCES2 = 0
                elif (signal_No == 2):
                    TOTAL_AMBULANCES3 = 0
                else:
                    TOTAL_AMBULANCES4 = 0

            print_Text = LIST_VEH[PATH_TYPE[signal_No]]['HAS_PASSED']

            VEHICLE_COUNT_TEXTS[signal_No] = SIMULATION_STYLE.render(str(print_Text), True, black_color, white_color)
            SIMULATION_WINDOW.blit(VEHICLE_COUNT_TEXTS[signal_No], COORDINATES_OF_VEHICLE_COUNT[signal_No])

        ELAPSED_TIMERText = SIMULATION_STYLE.render(("Time Elapsed: " + str(ELAPSED_TIMER)), True, black_color, white_color)
        SIMULATION_WINDOW.blit(ELAPSED_TIMERText, (1100, 50))

        # display the vehicles
        for VEH in TRAFFIC_OBJECTS:
            SIMULATION_WINDOW.blit(VEH.VEH_CURR_IMG, [VEH.X_COORDINATE, VEH.Y_COORDINATE])
            VEH.vehicleMovement()
        pygame.display.update()


Main()
