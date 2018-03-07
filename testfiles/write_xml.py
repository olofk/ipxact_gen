import sys

import ipxact

if __name__ == "__main__":
    component = ipxact.parse(open(sys.argv[1]), True)

    component.vendor = "helpimahack"

    component.export(sys.stdout, 0, 'ipxact:', 'component')
