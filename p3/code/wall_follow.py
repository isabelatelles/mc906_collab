import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

import math
import time
import sys
sys.path.insert(0, '../src')
from robot import Robot


class WallFollow:
    """
    Configure the robot behaviour to follow the wall to the right
    """
    def __init__(self):
        self.FRONT_SENSORS = [3, 4]
        self.max_speed = 2.0

    def init_fuzzy(self):
        """
        Make fuzzy setup by defining membership functions and rules
        """

        # Set the difference between the right frontal sensor and the right back sensor
        difference_right_sensors = ctrl.Antecedent(np.arange(-1.0, 1.0, 0.001), 'difference_right_sensors')
        difference_right_sensors['negative'] = fuzz.trimf(difference_right_sensors.universe, [-1.0, -1.0, 0.0])
        difference_right_sensors['zero'] = fuzz.trimf(difference_right_sensors.universe, [-0.015, 0.0, 0.015])
        difference_right_sensors['positive'] = fuzz.trimf(difference_right_sensors.universe, [0.0, 1.0, 1.0])

        # Define available velocities for each wheel
        v_left = ctrl.Consequent(np.arange(-self.max_speed, 1.0 + self.max_speed, 0.001), 'vl')
        v_right = ctrl.Consequent(np.arange(-self.max_speed, 1.0 + self.max_speed, 0.001), 'vr')

        # Define the membership functions for the wheels speed
        v_left['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed, self.max_speed])
        v_left['zero'] = fuzz.trimf(v_left.universe, [-0.15, 0.0, 0.15])
        v_right['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed, self.max_speed])
        v_right['zero'] = fuzz.trimf(v_right.universe, [-0.15, 0.0, 0.15])

        # Rules to make the robot follow the wall by turning left, right or going forward
        # Turn left
        rule_l1 = ctrl.Rule(difference_right_sensors['negative'], v_left['zero'])
        rule_r1 = ctrl.Rule(difference_right_sensors['negative'], v_right['positive'])

        # Turn right
        rule_l2 = ctrl.Rule(difference_right_sensors['positive'], v_left['positive'])
        rule_r2 = ctrl.Rule(difference_right_sensors['positive'], v_right['zero'])

        # Go forward, next to the wall
        rule_l3 = ctrl.Rule(difference_right_sensors['zero'], v_left['positive'])
        rule_r3 = ctrl.Rule(difference_right_sensors['zero'], v_right['positive'])

        vel_ctrl = ctrl.ControlSystem([rule_l1, rule_l2, rule_l3, rule_r1, rule_r2, rule_r3])
        self.fuzzy_system = ctrl.ControlSystemSimulation(vel_ctrl)

    def get_vel(self, ultrassonic):
        """
        Get velocity of each wheel based on the fuzzy system configured
        :param ultrassonic: list of distances given by the ultrassonic sensors
        :return: velocities of the left wheel and the right wheel
        """
        self.fuzzy_system.input['difference_right_sensors'] = ultrassonic[self.RIGHT_SENSORS[0]] - \
                                                              ultrassonic[self.RIGHT_SENSORS[1]]

        self.fuzzy_system.compute()
        print(self.fuzzy_system.input)
        return [self.fuzzy_system.output['vl'], self.fuzzy_system.output['vr']]


def main():
    robot = Robot()
    wf = WallFollow()
    wf.init_fuzzy()

    gamma = math.degrees(robot.get_current_orientation()[2])
    print(gamma)
    for x in range(500):
        ultrassonic = robot.read_ultrassonic_sensors()[0:9]
        vel = wf.get_vel(ultrassonic)
        print("Ultrassonic: ", ultrassonic)
        print("vel: ", vel)
        robot.set_left_velocity(vel[0])  # rad/s
        robot.set_right_velocity(vel[1])
        time.sleep(0.2)


if __name__ == '__main__':
    main()
