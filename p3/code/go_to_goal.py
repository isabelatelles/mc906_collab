import numpy as np
from math import pi, atan2
import skfuzzy as fuzz
from skfuzzy import control as ctrl

import math
import time
import sys
sys.path.insert(0, '../src')
from robot import Robot


class go_to_goal():
    def __init__(self, goal):
        self.goal = goal
        self.NUM_SENSORS = 8
        self.max_speed = math.pi
        self.steps = 0.01

    def init_fuzzy(self):
        distance = []
        for i in range(0, self.NUM_SENSORS):
            distance.append(ctrl.Antecedent(np.arange(0, 5.0, self.steps), 's' + str(i)))
            distance[i]['close'] = fuzz.trapmf(distance[i].universe, [0.0, 0.0, 0.3, 0.6])
            distance[i]['away'] = fuzz.trapmf(distance[i].universe, [0.3, 0.6, 5.0, 5.0])

        direction = ctrl.Antecedent(np.arange(-pi, pi, 0.0001), "direction")
        direction['left'] = fuzz.trimf(direction.universe, [-pi, -pi/2, 0])
        direction['right'] = fuzz.trimf(direction.universe, [0, pi/2, pi])
        direction['front'] = fuzz.trimf(direction.universe, [-pi/2, 0, pi/2])

        v_left = ctrl.Consequent(np.arange(-self.max_speed, 1.0 + self.max_speed, 0.01), 'vl')
        v_right = ctrl.Consequent(np.arange(-self.max_speed, 1.0 + self.max_speed, 0.01), 'vr')

        v_left['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed - 0.1, self.max_speed - 0.1])
        v_left['negative'] = fuzz.trimf(v_left.universe, [-self.max_speed, -self.max_speed, 0.0])
        v_right['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed, self.max_speed])
        v_right['negative'] = fuzz.trimf(v_left.universe, [-self.max_speed + 0.1, -self.max_speed + 0.1, 0.0])

        far_from_obstacles = distance[0]['away'] & distance[1]['away'] & distance[2]['away'] & distance[3]['away'] & distance[4]['away'] & distance[5]['away'] & distance[6]['away'] & distance[7]['away']
        obstacle_on_right = distance[4]['close'] | distance[5]['close'] | distance[6]['close'] | distance[7]['close']
        obstable_on_left = distance[0]['close'] | distance[1]['close'] | distance[2]['close'] | distance[3]['close']
        obstacle_in_front = distance[2]['close'] | distance[3]['close'] | distance[4]['close'] | distance[5]['close']

        rule_l1 = ctrl.Rule(obstable_on_left, v_left['positive'])
        rule_l2 = ctrl.Rule(obstacle_on_right & obstacle_in_front, v_left['negative'])
        rule_l3 = ctrl.Rule(obstacle_on_right & ~ obstacle_in_front, v_left['positive'])
        rule_l4 = ctrl.Rule(far_from_obstacles & (direction['front'] | direction['right']), v_left['positive'])
        rule_l5 = ctrl.Rule(far_from_obstacles & direction['left'], v_left['negative'])
        #rule_l3 = ctrl.Rule(direction['front'] | direction['right'], v_left['positive'])
        #rule_l4 = ctrl.Rule(direction['left'], v_left['negative'])

        rule_r1 = ctrl.Rule(obstable_on_left & obstacle_in_front, v_right['negative'])
        rule_r2 = ctrl.Rule(obstable_on_left & ~ obstacle_in_front, v_right['positive'])
        rule_r3 = ctrl.Rule(obstacle_on_right, v_right['positive'])
        rule_r4 = ctrl.Rule(far_from_obstacles & (direction['front'] | direction['left']), v_right['positive'])
        rule_r5 = ctrl.Rule(far_from_obstacles & direction['right'], v_right['negative'])
        #rule_r3 = ctrl.Rule(direction['front'] | direction['left'], v_right['positive'])
        #rule_r4 = ctrl.Rule(direction['right'], v_right['negative'])

        vel_ctrl = ctrl.ControlSystem([rule_l1, rule_l2, rule_l3, rule_l4, rule_l5, rule_r1, rule_r2, rule_r3, rule_r4, rule_r5])
        #vel_ctrl = ctrl.ControlSystem([rule_l3, rule_l4, rule_r3, rule_r4])
        self.fuzzy_system = ctrl.ControlSystemSimulation(vel_ctrl)

    def _sum_angles(self, a, b):
        angle_1 = a + 2*pi
        angle_2 = b + 2*pi
        result = (angle_1 + angle_2) % (2*pi)
        if result < pi:
            return result
        else:
            return result - 2*pi

    def get_vel(self, dist, pos, orient):
        a = atan2(pos[1] - self.goal[1], self.goal[0] - pos[0])
        angle = self._sum_angles(a, orient[2])
        print("Angle: ", angle)
        self.fuzzy_system.input["direction"] = angle

        for i in range(len(dist)):
            self.fuzzy_system.input['s' + str(i)] = dist[i]

        self.fuzzy_system.compute()
        return [self.fuzzy_system.output['vl'], self.fuzzy_system.output['vr']]

    def goal_test(self, position):
        return position[0] > self.goal[0] - 0.05 \
            and position[0] < self.goal[0] + 0.05 \
            and position[1] > self.goal[1] - 0.05 \
            and position[1] < self.goal[1] + 0.05

def main():
    robot = Robot()
    a = go_to_goal((-5, 1.7))
    a.init_fuzzy()

    while(not a.goal_test(robot.get_current_position())):
        ultrassonic = robot.read_ultrassonic_sensors()[0:8]
        pos = robot.get_current_position()
        orient = robot.get_current_orientation()
        vel = a.get_vel(ultrassonic, pos, orient)
        #print("Orientation: ", orient)
        #print("Pos: ", pos)
        #print("Ultrassonic: ", ultrassonic)
        #print("vel: ", vel)
        robot.set_left_velocity(vel[0])  # rad/s
        robot.set_right_velocity(vel[1])
        time.sleep(0.2)

    for i in range(4):
        robot.set_left_velocity(0)
        robot.set_right_velocity(0)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
