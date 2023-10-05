"""
Read KML format flight path and Fly in the 3-D space with Zag-Zig Path
"""
import re
import time
from airsimgeo import AirSimGeoClient
import airsim

SRID = 'EPSG:3857'
ORIGIN = (114.20438, 22.42089, 6.0)

def read_xml(file_path="exampleData.xml"):
    diagram_coordinates = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        grab_next_line = False
        count = 0
        co_num = 0

        for line in lines:
            if grab_next_line:

                line = line.strip()
                line = re.split(',| ', line)

                for coordinate_pair in line:
                    if co_num < 2:
                        try:
                            diagram_coordinates[count].append(coordinate_pair)
                        except KeyError:
                            diagram_coordinates[count] = []
                            diagram_coordinates[count].append(coordinate_pair)

                        co_num += 1
                    
                    else:
                        co_num = 0
                        count += 1

            if "<coordinates>" in line:
                count += 1
                grab_next_line = True
            else:
                grab_next_line = False
    
    return diagram_coordinates

def main():
    client = AirSimGeoClient(srid=SRID, origin=ORIGIN)
    client.simSetTraceLine([1.0, 0.0, 0.0, 0.5], 30)
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    # Take off
    client.takeoffAsync(timeout_sec=5).join()
    gps = client.getGpsLocation()
    # Go up by 30 meters
    gps_new = (gps[0], gps[1], gps[2])
    print("Going Higher")
    client.moveToPositionAsyncGeo(gps=gps_new, velocity=5).join()

    xml = read_xml('C:/Users/RayWong/Desktop/test.kml')

    gps_coord = []
    for key, gps_xml in xml.items():
        gps_coord.append([key, gps_xml])
        # gps_new = (gps_xml[0], gps_xml[1], 20.0)
        # print("Moving to: " + gps_xml[0] + ', ' + gps_xml[1])
        # client.moveToPositionAsyncGeo(gps=gps_new, velocity=5,).join()

    flight_step = 4
    flight_vel = 2
    
    for i in range(2):
        gps_len = range(len(gps_coord))

        drivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom
        yaw_mode = airsim.YawMode(False, 0)

        for j in gps_len:
            gpsx = gps_coord[j][1][0]
            gpsy = gps_coord[j][1][1]
            gps_new = (gpsx, gpsy, flight_step*(2*i+2))
            print("Moving to: " + gpsx + ', ' + gpsy+ ', ' + str(flight_step*(2*i+2)))

            if j is 2:
                yaw_mode = airsim.YawMode(False, -90)
                client.moveToPositionAsyncGeo(gps=gps_new, velocity=flight_vel,drivetrain=drivetrain, yaw_mode=yaw_mode).join()
            else:
                client.moveToPositionAsyncGeo(gps=gps_new, velocity=flight_vel).join()

            client.hoverAsync().join()

        for j in reversed(gps_len):
            gpsx = gps_coord[j][1][0]
            gpsy = gps_coord[j][1][1]
            gps_new = (gpsx, gpsy, flight_step*(2*i+3))
            print("Moving to: " + gpsx + ', ' + gpsy+ ', ' + str(flight_step*(2*i+3)))

            if j is 0:
                yaw_mode = airsim.YawMode(False, 0)
                client.moveToPositionAsyncGeo(gps=gps_new, velocity=flight_vel,drivetrain=drivetrain, yaw_mode=yaw_mode).join()
            else:
                client.moveToPositionAsyncGeo(gps=gps_new, velocity=flight_vel).join()
                        
            client.hoverAsync().join()

    # Original kml control code
    # for key, gps_xml in xml.items():
    #     gps_new = (gps_xml[0], gps_xml[1], 20.0)
    #     print("Moving to: " + gps_xml[0] + ', ' + gps_xml[1])
    #     client.moveToPositionAsyncGeo(gps=gps_new, velocity=5,).join()
    #     if key is 1:
    #         print('Ready to ACT!')
    #         client.hoverAsync().join()
    #         time.sleep(5)

    # # Move to new position
    # gps_new = (114.2133018, 22.4245944, 50.0)
    # print("Moving")
    # client.moveToPositionAsyncGeo(gps=gps_new, velocity=10).join()

    # Land, doesn't seem to work....
    time.sleep(5)
    print("Landing")
    client.landAsync().join()


if __name__ == '__main__':
    main()