## The end to end automation project for ova deployment from Jenkins

### Software Requirements

    Python 3.5

### Python Virtual Environment

1. Create Python virtual environment

        $ virtualenv <name-of-folder>

2. Activate virtual environment

        $ source <path-to-folder>/bin/activate

3. Deactivate virtual environment

        $ deactivate


### Install requirements

* Install python project dependencies for dev environment


        $ pip3 install -r requirements.txt

### Run Flake8 before commit (run on the root of the project)

        $ flake8

### Build and Run the project locally

1. Execute build.sh from project root - to generate build artifacts in the dist directory

        $ ./build.sh


# Here is the work flow:

    Step 1: Copy the base OVA file from artifactory to the docker container

    Base OVA location:
    https://artifactory.com:443/artifactory/core-generic-local/base.ova

    Step2: Create virtualenv for python3 in the docker container

    Step3: Clone the git project and install the projects requirements to generate tar file

    Step4: Generate the tar file

    Step5: Specify the properties of the ova in the config.yaml file located in conf folder

    Step6: Deploy VM on vcenter with OVA (downloaded in step 1)

    Script to execute the python file (ova_deployment\pyvmomi_scripts):

    Example: python3 deploy_ova.py -s '10.100.28.108' -o 443 -u <username> -p <password> --datacenter 'VC8_DC' --datastore 'Datastore' --resource-pool 'HA' --ova-path $dir/base.ova --configpath $dir/conf/config.yaml

    Step7: Power on the VM

    Example:

    Python3 power_cycles.py -s '10.100.28.108' -o 443 -u <username> -p <password> --vmname 'demo_vj' --powercycle 'power_on'

    Step8: Copy the tar file geenerated in step 4 to the deployed VM

    Example:	python3 remote_operations.py <dir of config.yaml>  <source tar file path> <dest tar file path>

# Export OVF scrip:

    Example:

    python export_vm.py -s '10.100.28.108' -o 443 -u <username> -p <password> --vmname <deployed vm name> -w <location to save ovf file>

# Cleanup Scripts:

    Power off VM:

    Example:

    Python3 power_cycles.py -s '10.100.28.108' -o 443 -u <username> -p <password> --vmname 'demo_vj' --powercycle 'power_off'

    Destroy VM:

    python3 delete_vm.py -s '10.100.28.108' -o 443 -u -u <username> -p <password> --vmname 'demo_vj'
