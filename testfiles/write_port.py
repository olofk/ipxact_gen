import sys

import ipxact

if __name__ == "__main__":
    component = ipxact.parse(open(sys.argv[1]), True)

    bif = component.busInterfaces.busInterface[0]
    print("Bus : " + bif.name)

    pm = bif.abstractionTypes.abstractionType[0].portMaps.portMap[0]
    print("logicalPort : " + pm.logicalPort.name)
    print("range child is type : " + str(pm.logicalPort.get_range()))

    print("physicalPort : " + pm.physicalPort.name)
    print("range partSelect.range is type " + str(pm.physicalPort.partSelect.get_range()))
