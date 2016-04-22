'''
Created on 11-Mar-2016

@author: Santosh Patil
'''
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
from Util import Util

class JsonRPCServer(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    @Request.application
    def application(self,request):
        # Dispatcher is dictionary {<method_name>: callable}
        bmcUtil = Util()
        bmcListOfMethods = {}
        bmcListOfMethod = bmcUtil.readLocalAppVariableFile("BMC_JSONRPCCALL_METHODS")
        bmcListOfMethod = bmcUtil.removeDoubleQuotas(bmcListOfMethod)
        bmcListOfMethods = bmcListOfMethod.split(",")
        for methodName in bmcListOfMethods:
            dispatcher[methodName] = lambda methodName: methodName
            #dispatcher["event"] = lambda a: a
        response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
        print response.json
        bmcUtil.writeRPCCallDataTOFile(response.json)
        return Response(response.json, mimetype='application/json')

    def callJSONRPCServer(self,bmcPluginName):
        bmcUtil = Util()
        bmcUtil.setValue(bmcPluginName)
        bmcHostName = bmcUtil.readLocalAppVariableFile("BMC_JSONRPCCALL_HOST_NAME")
        bmcPortNumber = bmcUtil.readLocalAppVariableFile("BMC_JSON_RPCCALL_PORT_NUMBER")
        #Running
        run_simple(bmcUtil.removeDoubleQuotas(bmcHostName), bmcPortNumber, self.application)
