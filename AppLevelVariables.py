BMC_TYPE_OF_OUTPUT         ="RPC"
BMC_WAIT_PERIOD_IN_SECONDS =300
BMC_STAND_ALONE_APPLICATION_RUN_COMMAND="python  index.py"
BMC_ERROR_MSG="Could not login to the specified vCenter host"
BMC_PLUGIN_STARTED_MSG="started"
BMC_NUMBER_OF_METRICS=2
BMC_LIST_OF_METRICS="VMWARE_SYSTEM_CPU_USAGE_AVERAGE,VMWARE_SYSTEM_DISK_WRITE_AVERAGE"
BMC_ADD_REPLICA_OF_PARAM_JSON="{  'items': [{ 'app_id': 'APPP','pollInterval': 300000, 'discoveryInterval': 300000,  'host': 'vw-pun-bcm-dv11.dsl.bmc.com', 'port': 443,'username': 'administrator','password': 'bmcAdm1n','maxSamples': 60, 'maxdepth': 60  }] }"
BMC_JSONRPCCALL_METHODS="metric,event"
BMC_JSONRPCCALL_HOST_NAME="localhost"
BMC_JSON_RPCCALL_PORT_NUMBER=4000
BMC_TYPE_OS_VM_SPIN_UP="ubuntu-14.04"
#Mention local or vagrant
BMC_EXECUTE_PLUGINS_IN_LOCAL_VAGRANT="vagrant"
#Add Vagrant url
BMC_VAGRANT_URL="https://github.com/Kumar-Patil/vagrant-nginx.git"
BMC_BOUNDARY_METER_API_TOKEN="BOUNDARY_API_TOKEN=api.8ab201de07-9398"
