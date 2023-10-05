"""
Read KML format flight path EXPORTED BY MATLAB and Fly in the 2-D space
"""
import re
import time
from airsimgeo import AirSimGeoClient

SRID = 'EPSG:3857'
ORIGIN = (114.20438, 22.42089, 6.0)

def read_xml(file_path="MATLAB.xml"):
    diagram_coordinates = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

        grab_next_line = False
        count = 0
        co_num = 0

        for line in lines:
            if "<coordinates>" in line:
                count += 1
                grab_next_line = True
            else:
                grab_next_line = False

            if grab_next_line:
                line = line.strip()
                line = line.strip('<coordinates> ')
                line = line.strip('</coordinates>')
                line = re.split(',| ', line)

                for coordinate_pair in line:
                    if co_num < 3:
                        try:
                            diagram_coordinates[count].append(coordinate_pair)
                        except KeyError:
                            diagram_coordinates[count] = []
                            diagram_coordinates[count].append(coordinate_pair)
                        co_num += 1
                    else:
                        co_num = 0
                        count += 1
    return diagram_coordinates

def main():
    client = AirSimGeoClient(srid=SRID, origin=ORIGIN)
    client.simSetTraceLine([0.0, 1.0, 0.0, 0.5], 50) # RGB Alpha
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)
    # Take off
    client.takeoffAsync(timeout_sec=5).join()
    gps = client.getGpsLocation()
    # Go up by 30 meters
    # gps_new = (gps[0], gps[1], gps[2] + 5.0)
    gps_new = (gps[0], gps[1], 5.0)
    print("Going Higher")
    client.moveToPositionAsyncGeo(gps=gps_new, velocity=5).join()

    xml = read_xml('C:/Users/RayWong/Desktop/gps.kml')

    # Original kml control code
    for key, gps_xml in xml.items():
        # gps_new = (gps_xml[0], gps_xml[1], 50.0)
        gps_new = (gps_xml[0], gps_xml[1], gps_xml[2]-143)
        print("Moving to: " + gps_xml[0] + ', ' + gps_xml[1] + ', ' + gps_xml[2])
        client.moveToPositionAsyncGeo(gps=gps_new, velocity=5,).join()
        if key is 1:
            print('Ready to ACT!')
            client.hoverAsync().join()
            time.sleep(5)

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