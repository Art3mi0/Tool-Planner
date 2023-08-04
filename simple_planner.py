#!/usr/bin/env python3

import rospy
import math

# import the plan message
from ur5e_control.msg import Plan
from geometry_msgs.msg import Twist

r = .05
inc = .3
robot_params = Twist()
got_params = False

def robot_callback(data):
	global robot_params
	global got_params
	robot_params.linear.x = data.linear.x
	robot_params.linear.y = data.linear.y
	robot_params.linear.z = data.linear.z
	robot_params.angular.x = data.angular.x
	robot_params.angular.y = data.angular.y
	robot_params.angular.z = data.angular.z
	got_params = True


def createPlanLine(rStart):
	# define variables
	plan = Plan()
	plan_point = Twist()
	# define a point close to the initial position
	plan_point.linear.x = rStart.linear.x
	plan_point.linear.y = rStart.linear.y
	plan_point.linear.z = rStart.linear.z
	plan_point.angular.x = rStart.angular.x
	plan_point.angular.y = rStart.angular.y
	plan_point.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point)
	
	plan_point2 = Twist()
	plan_point2.linear.x = rStart.linear.x + .1
	plan_point2.linear.y = rStart.linear.y + .1
	plan_point2.linear.z = rStart.linear.z
	plan_point2.angular.x = rStart.angular.x
	plan_point2.angular.y = rStart.angular.y
	plan_point2.angular.z = rStart.angular.z
	plan.points.append(plan_point2)
	return plan

def createPlanSquare(rStart):
	# define variables
	plan = Plan()
	plan_point1 = Twist()
	# define a point close to the initial position
	plan_point1.linear.x = rStart.linear.x
	plan_point1.linear.y = rStart.linear.y
	plan_point1.linear.z = rStart.linear.z
	plan_point1.angular.x = rStart.angular.x
	plan_point1.angular.y = rStart.angular.y
	plan_point1.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point1)
	
	plan_point2 = Twist()
	plan_point2.linear.x = rStart.linear.x + .1
	plan_point2.linear.y = rStart.linear.y
	plan_point2.linear.z = rStart.linear.z
	plan_point2.angular.x = rStart.angular.x
	plan_point2.angular.y = rStart.angular.y
	plan_point2.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point2)
	
	plan_point3 = Twist()
	plan_point3.linear.x = rStart.linear.x + .1
	plan_point3.linear.y = rStart.linear.y + .1
	plan_point3.linear.z = rStart.linear.z
	plan_point3.angular.x = rStart.angular.x
	plan_point3.angular.y = rStart.angular.y
	plan_point3.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point3)
	
	plan_point4 = Twist()
	plan_point4.linear.x = rStart.linear.x
	plan_point4.linear.y = rStart.linear.y + .1
	plan_point4.linear.z = rStart.linear.z
	plan_point4.angular.x = rStart.angular.x
	plan_point4.angular.y = rStart.angular.y
	plan_point4.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point4)
	
	return plan
	
def createPlanCircle(rStart):
	# define variables
	plan = Plan()

	theta = 0
	stop = 2 * math.pi
	
	plan_point1 = Twist()
	# define a point close to the initial position
	plan_point1.linear.x = rStart.linear.x
	plan_point1.linear.y = rStart.linear.y
	plan_point1.linear.z = rStart.linear.z
	plan_point1.angular.x = rStart.angular.x
	plan_point1.angular.y = rStart.angular.y
	plan_point1.angular.z = rStart.angular.z
	# add this point to the plan
	plan.points.append(plan_point1)
	
	while theta < stop:
		plan_point = Twist()
		plan_point.linear.x = rStart.linear.x + (r * math.cos(theta))
		plan_point.linear.y = rStart.linear.y + (r * math.sin(theta))
		plan_point.linear.z = rStart.linear.z
		plan_point.angular.x = rStart.angular.x
		plan_point.angular.y = rStart.angular.y
		plan_point.angular.z = rStart.angular.z
		# add this point to the plan
		plan.points.append(plan_point)
		theta += inc
		if theta < 0.9:
			print(rStart.linear.x,'----', r, '----', math.cos(theta), '----', plan_point.linear.x)
			
			print(plan)
		
	return plan

if __name__ == '__main__':
	# initialize the node
	rospy.init_node('simple_planner', anonymous = True)
	# add a publisher for sending joint position commands
	plan_pub = rospy.Publisher('/plan', Plan, queue_size = 10)
	# define a subscriber to read robot parameters
	param_pub = rospy.Subscriber('/ur5e/toolpose', Twist, robot_callback)
	# set a 10Hz frequency for this loop
	loop_rate = rospy.Rate(10)
	planCreated = False
	
	while not rospy.is_shutdown():
		if not planCreated and got_params:
			#plan = createPlanLine(robot_params)
			#plan = createPlanSquare(robot_params)
			plan = createPlanCircle(robot_params)
			planCreated = True
			print("plan created")
			
		# publish the plan
		if planCreated:
			plan_pub.publish(plan)
		# wait for 0.1 seconds until the next loop and repeat
		loop_rate.sleep()
