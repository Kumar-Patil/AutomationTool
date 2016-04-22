'''
Created on 01-Mar-2016

@author: Santosh Patil

'''
#!/usr/bin/python
import sys
from Util import Util
from customLog import customLog
from StartAndStopCmd import StartAndStopCmd
import os
from EmailClient import EmailClient
bmcCustomeLog = customLog()
if len(sys.argv) == 4:
    bmcPluginName = sys.argv[1]
    isVagrant = sys.argv[2]
    bmcEnvironment = sys.argv[3]
    bmcUtil = Util()
    if isVagrant == "vagrant":
        bmcCurrentDirectoryPath = bmcUtil.getCurrentDirectoryPath()
        bmcUtil.changeDirectory(bmcCurrentDirectoryPath + "/AutomationTool")
    
    bmcCurrentDirectory = bmcUtil.getCurrentDirectoryPath()      
    bmcListOfSubdirectoriesNames = bmcUtil.getImmediateSubdirectories(bmcUtil.getCurrentDirectoryPath())
    isFoundPlugin = False
    for subFolderName in bmcListOfSubdirectoriesNames:
        if subFolderName == bmcPluginName:
            isFoundPlugin = True
            break
    
    if isFoundPlugin == True:
        bmcCustomeLog.log("\n Already "+ bmcPluginName + " found in current directory")
        #bmcUtil.getPluginFromGitHub(bmcPluginName)
    else:
        bmcCustomeLog.log("\n Getting plugin ("+ bmcPluginName +") from github...............")
        bmcUtil.getPluginFromGitHub(bmcPluginName)    
        
    bmcRetValue = bmcUtil.checkAppVeriableFileIsExists(bmcPluginName)
    bmcUtil.setValue(bmcPluginName)
    if bmcRetValue == True:
                bmcUtil.replaceParamJsonValuesWithConfigValues(bmcPluginName)
                bmcCustomeLog.log("n Plugin test case execution ...in progress")
                #Getting Type of Operation(RPC,stdout)
                bmcTypeOfOperaion = bmcUtil.removeDoubleQuotas(bmcUtil.readLocalAppVariableFile("BMC_TYPE_OF_OUTPUT"))
                bmcCustomeLog.log("\n Type of operation is " + bmcTypeOfOperaion)
                if bmcTypeOfOperaion == "RPC":
                    bmcCustomeLog.log("\n Starting JSON RPC Server ")
                else:
                    bmcCustomeLog.log("\n stdout operation....... ")
                    
                #Start Server For listing client request
                bmcRPCStartThread = StartAndStopCmd(bmcTypeOfOperaion,bmcPluginName)
                bmcRPCStartThread.start()
                bmcCustomeLog.log("\n Json RPC server started ................")
                    
                bmcCustomeLog.log("\n Waiting to start application .............. ")
                bmcUtil.waitForExecution(2)
                    
                bmcCustomeLog.log("\n Application Started .................... ")
                bmcStartApplicationExecutionThread = StartAndStopCmd("startApp",bmcPluginName)
                bmcStartApplicationExecutionThread.start()
                    
                bmcCustomeLog.log("\n Waiting to Exit application .............. ")
                bmcUtil.waitForExecution(4)
                bmcUtil.changeDirectory(bmcCurrentDirectory)
                bmcUtil.waitForExecution(bmcUtil.readLocalAppVariableFile("BMC_WAIT_PERIOD_IN_SECONDS"))
                    
                bmcStartApplicationExecutionThread.terminate_thread(bmcStartApplicationExecutionThread) #stopping application thread here
                bmcCustomeLog.log("\n stopped application thread here.............")
                bmcRPCStartThread.terminate_thread(bmcRPCStartThread) # stopping RPC server  thread here
                bmcCustomeLog.log("\n stopping RPC server..............")
                   
                bmcCustomeLog.log("\n Staring robot framework to start  generating test report..............")
                #Need to comment below method later
                #bmcUtil.copyRPCLogFile(bmcEnvironment) 
                bmcUtil.executeRobotFrameworkCmd(bmcPluginName,bmcEnvironment)
                bmcCustomeLog.log("\n Execution successfully completed..............")
                #bmcUtil.removeFile("automation.log")
                bmcEmailSend = EmailClient()
                bmcCustomeLog.log("\n Sending email report..................")
                bmcSubject = 'Truesight Pulse  Plugin  Automation  Test Report-' + bmcPluginName + "(" + bmcEnvironment +")"
                bmcBody = "Need to Add info"
                readFromEmailIds = bmcUtil.readConfigIniFile("DEFAULT", "BMC_EMAIL_IDS_TO_SEND_TEST_RESPORTS").split(",")
                for bmcTo in readFromEmailIds:
                    bmcEmailSend.send(bmcSubject, "no-reply@bmc.com", bmcTo, bmcBody, "no-reply@bmc.com")
                    
                bmcCustomeLog.log("\n Email sending completed................")
                bmcCustomeLog.log("\n Terminating Execution")
                bmcUtil.terminateExecution(bmcEnvironment)
                bmcCustomeLog.log("\n Successfully Terminated Execution")   
    else:
        bmcCustomeLog.log("\nApplication variable file does not exists(" + bmcUtil.getCurrentDirectoryPath() + "\\" + bmcPluginName + "\\AppVariables.py" + ") in this path")
else:
    bmcCustomeLog.log("\nPlease pass plugin name as vmware,cassendra etc..")

