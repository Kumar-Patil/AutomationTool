#!/usr/bin/python
import sys
from robot.api import logger
import os
from Util import Util
from array import array
from sys import getsizeof
class TestCaseLibrary:
        def __init__(self):
                self._result = "success"

        
            
        def checkBoundaryMeterIsRunning(self):
                util = Util()
                return util.checkBoundaryMeterIsRunning()

        def isPluginStarted(self):
                bmcUtil = Util()
                isPluginStarted = ""
                bmcPluginName = bmcUtil.readPluginName()
                bmcIsRpcORStdout = bmcUtil.readLocalAppVariableFile("BMC_TYPE_OF_OUTPUT")
                bmcIsRpcORStdout = bmcUtil.removeDoubleQuotas(bmcIsRpcORStdout)
                if bmcIsRpcORStdout == "stdout":
                    bmcFileData = bmcUtil.readVagrantStdoutFile(bmcPluginName)
                    bmcMsg = bmcUtil.readLocalAppVariableFile("BMC_PLUGIN_STARTED_MSG")
                    bmcMsg = bmcUtil.removeDoubleQuotas(bmcMsg)
                    isPluginStarted = bmcUtil.serchSubstring(bmcFileData, bmcMsg)
                else:
                    bmcFileData = bmcUtil.readVagrantRPCLogFile(bmcPluginName)
                    bmcMsg = bmcUtil.readLocalAppVariableFile("BMC_PLUGIN_STARTED_MSG")
                    bmcMsg = bmcUtil.removeDoubleQuotas(bmcMsg)
                    isPluginStarted = bmcUtil.serchSubstring(bmcFileData, bmcMsg)
                    
                return isPluginStarted
            
        def isConnectionEstablished(self):
            bmcUtil = Util()
            bmcPluginName = bmcUtil.readPluginName()
            bmcIsRpcORStdout = bmcUtil.readLocalAppVariableFile("BMC_TYPE_OF_OUTPUT")
            bmcIsRpcORStdout = bmcUtil.removeDoubleQuotas(bmcIsRpcORStdout)
            if bmcIsRpcORStdout == "stdout":
                bmcfileData = bmcUtil.readVagrantStdoutFile(bmcPluginName)
                bmcMsg = bmcUtil.readLocalAppVariableFile("BMC_ERROR_MSG")
                bmcMsg = bmcUtil.removeDoubleQuotas(bmcMsg)
                bmcIsConnectionEstablished = bmcUtil.serchSubstring(bmcfileData, bmcMsg)
            else:
                bmcfileData = bmcUtil.readVagrantRPCLogFile(bmcPluginName)
                bmcMsg = bmcUtil.readLocalAppVariableFile("BMC_ERROR_MSG")
                bmcMsg = bmcUtil.removeDoubleQuotas(bmcMsg)
                bmcIsConnectionEstablished = bmcUtil.serchSubstring(bmcfileData, bmcMsg)
            return bmcIsConnectionEstablished
        
        def totalNumberOfMetrics(self,bmcListOfMetrics):
            bmcUtil = Util()
            bmcPluginName = bmcUtil.readPluginName()
            bmcIsRpcORStdout = bmcUtil.readLocalAppVariableFile("BMC_TYPE_OF_OUTPUT")
            bmcIsRpcORStdout = bmcUtil.removeDoubleQuotas(bmcIsRpcORStdout)
            bmcListOfMetricsArray = []
            bmcMetricsCount = []
            bmcListOfMetricsArray = bmcListOfMetrics.split(",")
            if bmcIsRpcORStdout == "stdout":
                bmcfileData = bmcUtil.readVagrantStdoutFile(bmcPluginName)
                for name in bmcListOfMetricsArray:
                    bmcIsFound = bmcUtil.serchSubstring(bmcfileData, name)
                    if bmcIsFound == "yes":
                        bmcMetricsCount.append(bmcIsFound)
            else:
                bmcfileData = bmcUtil.readVagrantRPCLogFile(bmcPluginName)
                for name in bmcListOfMetricsArray:
                    bmcIsFound = bmcUtil.serchSubstring(bmcfileData, name)
                    if bmcIsFound == "yes":
                        bmcMetricsCount.append(bmcIsFound)
            return len(bmcMetricsCount)
