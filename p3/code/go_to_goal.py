import numpy as np
from math import pi, atan2
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import sys
sys.path.insert(0, '../src')
from robot import Robot


class go_to_goal():
    ''' Class to configure the robot behavior to go to some defined goal

        Args:
        goal (float, float): The goal where the robot should walk to

        Attributes:
        goal(float, float): goal
        NUM_SENSORS(int): number of sensors of the robot
        max_speed(float): Maximum speed of each wheel
        steps(float): Size of each step of the robot
    '''
    def __init__(self, goal, defuzzify_method = 'centroid'):
        self.goal = goal
        self.NUM_SENSORS = 8
        self.max_speed = pi
        self.steps = 0.01
        self.defuzzify_method = defuzzify_method

    def init_fuzzy(self):
        ''' Make the fuzzy setup by defining membership functions and rules
        '''
        # Set the distances to avoid obstacles
        distance = []
        for i in range(0, self.NUM_SENSORS):
            distance.append(ctrl.Antecedent(np.arange(0, 5.0, self.steps), 's'
                                                                    + str(i)))
            distance[i]['close'] = fuzz.trapmf(distance[i].universe, [0.0, 0.0,
                                                                      0.3, 0.6])
            distance[i]['away'] = fuzz.trapmf(distance[i].universe, [0.3, 0.6,
                                                                      5.0, 5.0])

        # Set the direction to align the robot to its goal
        direction = ctrl.Antecedent(np.arange(-pi, pi, 0.0001), "direction")
        direction['left'] = fuzz.trimf(direction.universe, [-pi, -pi/2, 0])
        direction['right'] = fuzz.trimf(direction.universe, [0, pi/2, pi])
        direction['front'] = fuzz.trimf(direction.universe, [-pi/2, 0, pi/2])

        # Define available velocities for each wheel
        v_left = ctrl.Consequent(np.arange(-self.max_speed, 1.0 +
        self.max_speed, 0.01), 'vl')
        v_right = ctrl.Consequent(np.arange(-self.max_speed, 1.0 +
        self.max_speed, 0.01), 'vr')

        # Define the membership functions for the wheels speed
        v_left['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed
                                                   - 0.1, self.max_speed - 0.1])
        v_left['negative'] = fuzz.trimf(v_left.universe, [-self.max_speed,
                                                          -self.max_speed, 0.0])
        v_right['positive'] = fuzz.trimf(v_left.universe, [0.0, self.max_speed,
                                                                self.max_speed])
        v_right['negative'] = fuzz.trimf(v_left.universe, [-self.max_speed
                                             + 0.1, -self.max_speed + 0.1, 0.0])

        v_left.defuzzify_method = self.defuzzify_method
        v_right.defuzzify_method = self.defuzzify_method

        # Group sensor reading by its positions
        far_from_obstacles = distance[0]['away'] & distance[1]['away'] & \
                             distance[2]['away'] & distance[3]['away'] & \
                             distance[4]['away'] & distance[5]['away'] & \
                             distance[6]['away'] & distance[7]['away']
        obstacle_on_right = distance[4]['close'] | distance[5]['close'] | \
                            distance[6]['close'] | distance[7]['close']
        obstable_on_left = distance[0]['close'] | distance[1]['close'] | \
                           distance[2]['close'] | distance[3]['close']
        obstacle_in_front = distance[2]['close'] | distance[3]['close'] | \
                            distance[4]['close'] | distance[5]['close']

        # Rules for left wheel
            # Rules to avoid obstacles and don't get stuck due to confliting
            # rules (obstacle + alignment)
        rule_l1 = ctrl.Rule(obstable_on_left, v_left['positive'])
        rule_l2 = ctrl.Rule(obstacle_on_right & obstacle_in_front,
                                                             v_left['negative'])
        rule_l3 = ctrl.Rule(obstacle_on_right & ~ obstacle_in_front,
                                                             v_left['positive'])
            # Rules to align the robot to its goal and walk towards it
        rule_l4 = ctrl.Rule(far_from_obstacles & (direction['front'] |
                                        direction['right']), v_left['positive'])
        rule_l5 = ctrl.Rule(far_from_obstacles & direction['left'],
                                                             v_left['negative'])

        # Rules for right wheel
            # Rules to avoid obstacles and don't get stuck due to confliting
            # rules (obstacle + alignment)
        rule_r1 = ctrl.Rule(obstable_on_left & obstacle_in_front,
                                                            v_right['negative'])
        rule_r2 = ctrl.Rule(obstable_on_left & ~ obstacle_in_front,
                                                            v_right['positive'])
        rule_r3 = ctrl.Rule(obstacle_on_right, v_right['positive'])
            # Rules to align the robot to its goal and walk towards it
        rule_r4 = ctrl.Rule(far_from_obstacles & (direction['front'] |
                                        direction['left']), v_right['positive'])
        rule_r5 = ctrl.Rule(far_from_obstacles & direction['right'],
                                                            v_right['negative'])

        vel_ctrl = ctrl.ControlSystem([rule_l1, rule_l2, rule_l3, rule_l4,
                          rule_l5, rule_r1, rule_r2, rule_r3, rule_r4, rule_r5])

        self.fuzzy_system = ctrl.ControlSystemSimulation(vel_ctrl)

    def _sum_angles(self, a, b):
        ''' Sum angles and convert the result to [-pi, pi) interval.

            Args:
            a(float): 1st angle to sum. Needs to be in [-pi, pi) interval
            b(float): 2nd angle to sum. Needs to be in [-pi, pi) interval

            Returns:
            float: angle in [-pi, pi) interval.
        '''
        angle_1 = a + 2*pi
        angle_2 = b + 2*pi
        result = (angle_1 + angle_2) % (2*pi)
        if result < pi:
            return result
        else:
            return result - 2*pi

    def get_vel(self, dist, pos, orient):
        ''' Get the velocity of each wheel based on the fuzzy system configured
            at "self.init_fuzzy()".

            Args:
            dist(float list): the distance read in each sensor of the robot
            pos(float, float, float): position of the robot
            orient(float, float, float): Array with the euler angles (alpha,
            beta and gamma) to describe the robot orientation

            Returns:
            [float, float]: velocities of the left wheel and the right wheel
        '''
        # Calculate the angle between the goal and the robot's current position
        a = atan2(pos[1] - self.goal[1], self.goal[0] - pos[0])
        # Get the angle the robot needs to rotate
        angle = self._sum_angles(a, orient[2])
        #print("Angle: ", angle)
        self.fuzzy_system.input["direction"] = angle

        for i in range(len(dist)):
            self.fuzzy_system.input['s' + str(i)] = dist[i]

        self.fuzzy_system.compute()
        return [self.fuzzy_system.output['vl'], self.fuzzy_system.output['vr']]

    def goal_test(self, position):
        ''' Test if the robot reached the goal

            Args:
            position(float, float, float): position of the robot

            Returns:
            bool: if robot is at the goal position
        '''
        # Compares the robot position and the goal, assuming a +/-0.25 tolerance
        # (approximate size/2 of the robot)
        return round(position[0], 1) > round(self.goal[0] - 0.25, 1) \
            and round(position[0], 1) < round(self.goal[0] + 0.25 , 1) \
            and round(position[1], 1) > round(self.goal[1] - 0.25, 1) \
            and round(position[1], 1) < round(self.goal[1] + 0.25, 1)

def main():
    DEFUZZIFICATION_METHODS = ['centroid', 'bisector', 'mom', 'som', 'lom']
    defuzzify_method = DEFUZZIFICATION_METHODS[0]

    robot = Robot()
    goal = (4, 5)
    a = go_to_goal(goal, defuzzify_method)
    a.init_fuzzy()

    all_velocities = []
    all_positions = []

    (x, y, z) = robot.get_current_position()
    initial_position = (round(x, 1), round(y, 1))
    print("Initial position: {}".format(initial_position))

    with open("../outputs/g2g/velocities_{}_{}_{}.csv".format(initial_position, goal, defuzzify_method), 'w') as fv:
        with open("../outputs/g2g/positions_{}_{}_{}.csv".format(initial_position, goal, defuzzify_method), 'w') as fp:
            while(not a.goal_test(robot.get_current_position())):
                ultrassonic = robot.read_ultrassonic_sensors()[0:8]
                pos = robot.get_current_position()
                orient = robot.get_current_orientation()
                vel = a.get_vel(ultrassonic, pos, orient)
                fv.write(str(vel[0]) + ", " + str(vel[1]) + "\n")
                fp.write(str(pos[0]) + ", " + str(pos[1]) + "\n")
                #print("Orientation: ", orient)
                #print("Pos: ", pos)
                #print("Ultrassonic: ", ultrassonic)
                #print("vel: ", vel)
                robot.set_left_velocity(vel[0])  # rad/s
                robot.set_right_velocity(vel[1])
                time.sleep(0.2)

    # Make sure the robot stop when get to the goal - This for was added due to
    # some failures at sensor writing
    for i in range(4):
        robot.set_left_velocity(0)
        robot.set_right_velocity(0)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
