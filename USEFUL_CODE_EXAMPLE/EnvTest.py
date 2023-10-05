import airsim
import time

# Connect to the AirSim simulater
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True) # get control
client.armDisarm(True) # unlock
client.takeoffAsync().join() # takeoff

# square flight
client.moveToZAsync(-2, 1).join()
client.moveByVelocityZAsync(8, 0, -2, 2).join()     # 第三阶段：以8m/s速度向前飞2秒钟
client.moveByVelocityZAsync(0, 8, -2, 2).join()     # 第三阶段：以8m/s速度向右飞2秒钟
client.moveByVelocityZAsync(-8, 0, -2, 2).join()    # 第三阶段：以8m/s速度向后飞2秒钟
client.moveByVelocityZAsync(0, -8, -2, 2).join()    # 第三阶段：以8m/s速度向左飞2秒钟

client.hoverAsync().join()          # 第四阶段：悬停6秒钟
time.sleep(6)

client.landAsync().join() # land
client.armDisarm(False) # lock
client.enableApiControl(False) # release control
