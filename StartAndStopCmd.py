'''
Created on 11-Mar-2016

@author: Santosh Patil
'''
import threading
import ctypes
from customLog import customLog
from JsonRPCServer import JsonRPCServer
from Util import Util
class StartAndStopCmd(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    def __init__(self,bmcTypeOfExecution,bmcPluginName):
        super(StartAndStopCmd, self).__init__()
        self._stop = threading.Event()
        self.name = bmcTypeOfExecution
        self.bmcPluginName = bmcPluginName

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
    
    def run(self):
        self.startExecution(self.name,self.bmcPluginName)
        
    def startExecution(self,bmcTypeCmdExecution,bmcPluginName):
        bmcLog = customLog()
        bmcUtil = Util()
        bmcJsonRPCServer = JsonRPCServer()
        if bmcTypeCmdExecution == "RPC": #starte RPC Server Method here
            bmcLog.log("Executing RPC server to handle json rpc data")
            bmcJsonRPCServer.callJSONRPCServer(bmcPluginName)
            
        if bmcTypeCmdExecution == "startApp":
            bmcLog.log("\n Executing Start Application Command")
            bmcUtil.runPlugin(bmcPluginName)
            
        if bmcTypeCmdExecution == "stdout":
            bmcLog.log("\n Executing stdout application  Command")
            bmcUtil.runPlugin(bmcPluginName)
     
    def terminate_thread(self,thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")   
