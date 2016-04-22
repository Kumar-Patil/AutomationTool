'''
Created on 18-Mar-2016

@author: Santosh Patil
'''

import sys
from customLog import customLog
from Util import Util

bmcCustomeLog = customLog()

def destroyCreatedVM(bmcVMName):
    try:
        # This block clean all, such as(downloaded files and vagrant destroy etc...)
        bmcCustomeLog.log("\n Destroying Created VM : " + bmcVMName)
        retval = bmcUtil.vagrantDestroyCMD()
        bmcCustomeLog.log("\nDestroyed VM:" + bmcVMName)
        bmcCustomeLog.log("\n Retval:" + retval)
    except StandardError as error:
            bmcCustomeLog.log("\n Exception accured  in clean method")

def cleanDownloadedFiles(bmcPluginName,bmcVagrantFolderName,bmcVMName):
    try:
       
        bmcCustomeLog.log("\n Removing AppVariable file(AppVariables.py)...!")
        bmcUtil.removeFile("AppVariables.py")
        bmcCustomeLog.log("\n successfully deleted  AppVariable file(AppVariables.py)...!")
        bmcCustomeLog.log("\n Deleting manifests folder!")
        bmcUtil.deleteFolders("manifests")
        bmcCustomeLog.log("\n successfully deleted  manifests folder...!")
        bmcCustomeLog.log("\n Removing Vagrantfile file(Vagrantfile)...!")
        bmcUtil.removeFile("Vagrantfile")
        bmcCustomeLog.log("\n successfully deleted  Vagrantfile file(Vagrantfile)...!")
        bmcCustomeLog.log("\n Removing " + bmcVagrantFolderName + " this folder")
        bmcUtil.deleteFolders(bmcVagrantFolderName)
        bmcCustomeLog.log("\n successfully deleted  " + bmcVagrantFolderName + " !")
        
        bmcCustomeLog.log("\n Removing .env file(.env)...!")
        bmcUtil.removeFile(".env")
        bmcCustomeLog.log("\n successfully deleted  .env file(.env)...!")
        
        bmcCustomeLog.log("\n Removing plugin folder ("+bmcPluginName+") started.....!")
        bmcUtil.deleteFolders(bmcPluginName)
        bmcCustomeLog.log("\n successfully deleted  plugin folder ("+bmcPluginName+")...!")
        
    except StandardError as error:
            bmcCustomeLog.log("\n Exception accured  in clean method")
def startSpinUP(bmcPluginName):
    try:
        bmcVagrantFolderName = ""
        if bmcUtil.checkIsPluginBlackListed(bmcPluginName) != 'yes':
            # download app variable file from git hub
            bmcIsFoundAppvariableFile = bmcUtil.downloadAppConfigFile(bmcPluginName)
            if bmcIsFoundAppvariableFile == True:
                # dwonload vagrant folder
                bmcCustomeLog.log("\n Application variable file downloaded successfully!")
                bmcVagrantUrl = bmcUtil.readLocalAppVariableFile("BMC_VAGRANT_URL")
                retVal = bmcUtil.downloadVagrantFromGitHub(bmcPluginName)  # download Vagrant folder
                bmcVagrantFolderName = bmcUtil.getVagrantNameFromVagrantURL(bmcVagrantUrl)
                bmcPath = ""
                if bmcUtil.getTypeOfOS() == "Windows":
                    bmcPath = bmcVagrantFolderName + "\\.git"
                else:
                    bmcPath = bmcVagrantFolderName + "/.git"
                bmcUtil.deleteFolders(bmcPath)
                bmcUtil.copyDiectory(bmcVagrantFolderName)
                
            else:
                bmcCustomeLog.log("\n Application variable file does not exist in !" + bmcPluginName)
                return
            bmcUtil.getPluginFromGitHub(bmcPluginName)
            bmcUtil.writePluginName(bmcPluginName)
            bmcListOfVMsSpinUp = bmcUtil.removeDoubleQuotas(bmcUtil.readLocalAppVariableFile("BMC_TYPE_OS_VM_SPIN_UP")).split(",")
            for bmcVMName in bmcListOfVMsSpinUp:
                bmcCustomeLog.log("\n Plugin name ------------ " + bmcPluginName)
                bmcCustomeLog.log("\n Setting boundary API token as environment variable is started.....!")
                bmcBoundaryAPIToken = bmcUtil.readConfigIniFile("DEFAULT", "BMC_BOUNDARY_METER_API_TOKEN")
                if bmcBoundaryAPIToken != None and bmcBoundaryAPIToken != "":
                    bmcUtil.writeEnvironmentVariableToFile(bmcBoundaryAPIToken)
                else:
                    bmcBoundaryAPIToken = bmcUtil.removeDoubleQuotas(bmcUtil.readLocalAppVariableFile("BMC_BOUNDARY_METER_API_TOKEN"))
                    if bmcBoundaryAPIToken != None and bmcBoundaryAPIToken != "":
                        bmcUtil.writeEnvironmentVariableToFile(bmcBoundaryAPIToken)
                    else:
                        bmcCustomeLog.log("\n Boundary API token is mandatory please add in config.ini file or AppVariable.py file!")
                    return
                bmcCustomeLog.log("\n Setting boundary API token as environment variable is completed.....!")
                bmcCustomeLog.log("\n VM Spin Up started ------------ " + bmcUtil.removeDoubleQuotas(bmcVMName))
                retVal = bmcUtil.vagrantCMD(bmcUtil.getVagrantCreationCMD(bmcUtil.removeDoubleQuotas(bmcVMName)))
                bmcCustomeLog.log("\n return values -------------" + retVal)
                bmcCustomeLog.log("\n VM Spin Up Completed!" + bmcUtil.removeDoubleQuotas(bmcVMName))
                # retVals = bmcUtil.vagrantCMD(bmcUtil.copyServerFile(bmcVMName))
                bmcCustomeLog.log("\n Installing pip started..........!")
                bmcCMD = bmcUtil.installPIP(bmcUtil.removeDoubleQuotas(bmcVMName))
                retVal = bmcUtil.shellcmd(bmcCMD)
                bmcCustomeLog.log("\n Installing pip end..............!"+retVal)
                
                bmcCustomeLog.log("\n Dependency installation started..........!")
                bmcCMD = bmcUtil.installDependencies(bmcUtil.removeDoubleQuotas(bmcVMName))
                retVal = bmcUtil.shellcmd(bmcCMD)
                bmcCustomeLog.log("\n Dependency installation ended..............!")
                
                bmcCustomeLog.log("\n Plugin started execution!")
                bmcUtil.vagrantCMD(bmcUtil.getVagrantSSHCMD(bmcUtil.removeDoubleQuotas(bmcVMName), bmcPluginName))
                bmcCustomeLog.log("\n Execution completed!")
                destroyCreatedVM(bmcVMName)
                
            bmcCustomeLog.log("\n Clean up Started!--------------")
            cleanDownloadedFiles(bmcPluginName,bmcVagrantFolderName,bmcVMName)
            bmcCustomeLog.log("\n Clean up End!--------------")
        else:
            bmcCustomeLog.log("\n The given plugin is (" + bmcPluginName + ") black listed ..So ignoring testing...")
            
    except StandardError as e:
            print e
            bmcCustomeLog.log("\n Exception accured  in startSpinUP method" )
    
def spinUPVM(bmcPluginName):
    bmcUtil = Util()
    bmcUtil.removeFile("automation.log")
    if bmcPluginName == "All":
        # All
        bmcCustomeLog.log("\n Multiple plugin testing started here........." + bmcPluginName)
        bmcListOfPluginArray = bmcUtil.getWhiteListedPlugins()
        bmcCustomeLog.log(len(bmcListOfPluginArray))
        if len(bmcListOfPluginArray) >= 1:
                    bmcCustomeLog.log("\n White listed plugins list.......!  ")
                    bmcCustomeLog.log(bmcListOfPluginArray)
        else:    
                bmcListOfPluginArray = bmcUtil.getFinalListPluginList()
                
        if len(bmcListOfPluginArray) >= 1:
                for bmcPluginName in bmcListOfPluginArray:
                    startSpinUP(bmcPluginName)
        
    else:
        bmcCustomeLog.log("\n Started Execution................!")
        startSpinUP(bmcPluginName)
        bmcCustomeLog.log("\n Execution is END.................!")

bmcUtil = Util()
if len(sys.argv) == 1:
        bmcPluginName = "All"
        bmcTypeOfExecution = bmcUtil.removeDoubleQuotas(bmcUtil.readConfigIniFile("DEFAULT", "BMC_EXECUTE_PLUGINS_IN_LOCAL_VAGRANT"))
        if bmcTypeOfExecution == "vagrant":
            bmcCustomeLog.log("\n Started running in vagrant(All)")
            bmcCustomeLog.log("\n Type of execution--------" + bmcTypeOfExecution)
            spinUPVM(bmcPluginName)
        else:
            bmcCustomeLog.log("\n Started running in local ")  # Current machine. Test All white listed plugins
            # This will be in loop
            # bmcExecutionCommand = "python " + bmcPluginName +  "single"
            # bmcUtil.shellcmd(bmcExecutionCommand)
else:
        bmcPluginName = sys.argv[1]
        bmcUtil = Util()
        bmcTypeOfExecution = bmcUtil.removeDoubleQuotas(bmcUtil.readConfigIniFile("DEFAULT", "BMC_EXECUTE_PLUGINS_IN_LOCAL_VAGRANT"))
        if bmcTypeOfExecution == "vagrant":
            bmcCustomeLog.log("\n Started running in vagrant...............")
            bmcCustomeLog.log("\n Type of execution--------" + bmcTypeOfExecution)
            spinUPVM(bmcPluginName)
        else:
            bmcCustomeLog.log("\n Started running in local............")
            # bmcExecutionCommand = "python " + bmcPluginName +  "single"
            # bmcUtil.shellcmd(bmcExecutionCommand)
