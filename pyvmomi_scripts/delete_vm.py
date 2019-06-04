from time import sleep
import requests
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
import argparse
import time

# disable  urllib3 warnings
if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()


def get_args():
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument('-s', '--host', required=True, action='store',
                        help='Remote host to connect to')
    parser.add_argument('-o', '--port', type=int, default=443, action='store',
                        help='Port to connect on')
    parser.add_argument('-u', '--user', required=True, action='store',
                        help='User name to use when connecting to host')
    parser.add_argument('-p', '--password', required=False, action='store',
                        help='Password to use when connecting to host')
    parser.add_argument('--vmname',
                        required=True,
                        action='store',
                        help='VM name to get instance UUID')
    args = parser.parse_args()
    return args


def get_obj(content, vimtype, name):

    """Create contrainer view and search for object in it"""
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj


def main():
    args = get_args()
    # connect to vc
    si = SmartConnectNoSSL(
        host=args.host,
        user=args.user,
        pwd=args.password,
        port=args.port)
    # disconnect vc
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()

    container = content.rootFolder  # starting point to look into
    viewType = [vim.VirtualMachine]  # object types to look for
    recursive = True  # whether we should look into it recursively
    containerView = content.viewManager.CreateContainerView(
        container, viewType, recursive)

    children = containerView.view
    uuid = None
    for child in children:
        summary = child.summary
        if summary.config.name == args.vmname:
            uuid = summary.config.instanceUuid

    if uuid == None:
        print('Unable to get the uuid with vm name')
        return 0

    VM = None
    VM = get_obj(si.content, [vim.VirtualMachine], args.vmname)
    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))

    if format(VM.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(VM.name))
        TASK = VM.PowerOffVM_Task()
        time.sleep(3)
        print("{0}".format(TASK.info.state))
    print("Destroying VM from vcenter.")
    TASK = VM.Destroy_Task()
    sleep(3)
    print("Destroying VM is completed.")


# Start program
if __name__ == "__main__":
    main()
