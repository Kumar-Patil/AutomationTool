'''
Created on 29-Feb-2016

@author: Santosh Patil
'''
from ConfigParser import SafeConfigParser
import platform
import subprocess
from subprocess import PIPE, Popen
import os
import StringIO
import ConfigParser
import xmlrpclib
import smtplib
from smtplib import SMTPException
import time
import requests
import urllib2
from customLog import customLog
import urllib
bmcCustomeLog = customLog()
from distutils.dir_util import copy_tree
import shutil
import traceback
class Util(object):
    '''
    classdocs
    '''


    def __init__(self,
                 BMC_BOUNDARY_METER_STATUS_CHECK_WINDOWS_PLATFORM="sc query boundary_meter",
                 BMC_BOUNDARY_METER_STATUS_CHECK_OTHER_PLATFORM="boundary-meter --status -I boundary-meter",
                 BMC_IS_BOUNDARY_METER_RUNNING="ok",
                 BMC_INSTALL_BOUNDARY_METER="install",
                 BMC_IS_BOUNDARY_METER_RUNNING_IN_WINDOWS="RUNNING",
                 BMC_SET_PLUGIN_NAME=""):
        
        '''
        Constructor
        '''
        self.bmc_Boundary_Meter_Status_Check_Windows_Platform_Cmd = BMC_BOUNDARY_METER_STATUS_CHECK_WINDOWS_PLATFORM
        self.bmc_Boundary_Meter_Status_Check_Other_Platform_Cmd = BMC_BOUNDARY_METER_STATUS_CHECK_OTHER_PLATFORM
        self.bmc_Is_Boundary_Meter_RUNNING = BMC_IS_BOUNDARY_METER_RUNNING
        self.bmc_Install_BOUNDARY_METER = BMC_INSTALL_BOUNDARY_METER
        self.bmc_BMC_Is_Boundary_Meter_Running_In_Windows = BMC_IS_BOUNDARY_METER_RUNNING_IN_WINDOWS
        self.bmcPluginName = BMC_SET_PLUGIN_NAME
     
    def readConfigIniFile1(self, bmcSectionName, bmcKey):
        '''
        Reading config.ini file
        '''
        bmcParser = SafeConfigParser()
        bmcParser.read('config.ini')
        return  bmcParser.get(bmcSectionName, bmcKey)
    
    def getPlatformName(self):
        '''
        Getting platform name
        '''
        bmcPlatformName = platform.platform(aliased=True)
        return bmcPlatformName
       
    def checkPlatformNameAgainstConfig(self):
        '''
        checking platform name against config
        '''
        bmcSupportedOsArrayList = []
        bmcSupportedOsArrayList = self.readConfigIniFile("DEFAULT", "BMC_SUPPORTED_OS").split(",")
        for bmcSupportedOS in bmcSupportedOsArrayList:
                if self.getPlatformName().find(bmcSupportedOS) != -1:
                    return bmcSupportedOS;
                    break;
        
     
    def getBoundaryMeterStatusCheckCmd(self):
        '''
        Getting boundary meter status check command
        '''
        bmcPlatformName = self.checkPlatformNameAgainstConfig()
        if bmcPlatformName == 'Windows':
            return  self.bmc_Boundary_Meter_Status_Check_Windows_Platform_Cmd
        else:
            return self.bmc_Boundary_Meter_Status_Check_Other_Platform_Cmd
        
    
    def getBoundaryMeterStatus(self):
        '''
        getting the boundary meter status
        '''
        bmcCmd = self.getBoundaryMeterStatusCheckCmd()
        bmcRetval = self.shellcmd(bmcCmd)
        return bmcRetval
    
    def shellcmd(self, bmcCmd, echo=False):
        """ Run 'cmd' in the shell and return its standard out.
        """
        if not echo: print('[cmd] {0}'.format(bmcCmd))
        bmcProcess = subprocess.Popen(bmcCmd, shell=True, stdout=subprocess.PIPE)
        bmcOut = bmcProcess.communicate()[0]
        return bmcOut
    
    def checkBoundaryMeterIsRunning(self):
        '''
        getting the boundary meter status
        '''
        bmcBoundaryMeterStatus = self.getBoundaryMeterStatus()
        if self.bmc_Is_Boundary_Meter_RUNNING in bmcBoundaryMeterStatus or self.bmc_BMC_Is_Boundary_Meter_Running_In_Windows in bmcBoundaryMeterStatus:
            return self.bmc_Is_Boundary_Meter_RUNNING
        else:
            return self.bmc_Install_BOUNDARY_METER
    
     
    def readAppVariableFile(self, bmcPluginName, bmcKey):
        '''
        Reading application variable files
        '''
        config = StringIO.StringIO()
        config.write('[dummysection]\n')
        bmcCurrentDirectoryPath = self.getCurrentDirectoryPath() + "/" + bmcPluginName + "/AppVariables.py"
        config.write(open(bmcCurrentDirectoryPath).read())
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
        bmcRetValue = cp.get("dummysection", bmcKey)
        return  bmcRetValue
    
    def checkAppVeriableFileIsExists(self, bmcPluginName):
        """ checking  App Veriable File Is Exists
        """
        retVale = False
        try:
            if self.getTypeOfOS() == "Windows":
                bmcCurrentDirectoryPath = self.getCurrentDirectoryPath() + "\\"
                bmcAppVaribaleFilePath = bmcCurrentDirectoryPath + bmcPluginName + "\\AppVariables.py"
            else:
                bmcCurrentDirectoryPath = self.getCurrentDirectoryPath() + "/"
                bmcAppVaribaleFilePath = bmcCurrentDirectoryPath + bmcPluginName + "/AppVariables.py"
            retVale = os.path.exists(bmcAppVaribaleFilePath)
        except:
            pass
        return retVale
    
    def prepareRobotFrameworkCmd(self, bmcPluginName,bmcVMName):
        """ prepare Robot Framework Cmd
        """
        bmcRobotFrameworkCmd = ""
        bmcAppVaribaleFilePath = ""
        try:
            if self.getTypeOfOS() == "Windows":
                bmcAppVaribaleFilePath = self.getCurrentDirectoryPath() + "\\" + bmcPluginName + "\AppVariables.py"
                bmcRobotFrameworkCmd = " pybot -V " + bmcAppVaribaleFilePath + "  " + "keywordDrivenTestCases.robot"
            else:
                bmcAppVaribaleFilePath = self.getCurrentDirectoryPath() + "/" + bmcPluginName + "/AppVariables.py"
                bmcCMD = self.checkTypeOSCMD(bmcVMName)
                bmcRobotFrameworkCmd = " "+bmcCMD+" pybot -V " + bmcAppVaribaleFilePath + "  " + "keywordDrivenTestCases.robot"
        except:
            raise Exception
        
        return bmcRobotFrameworkCmd
        
    
    def executeRobotFrameworkCmd(self, bmcPluginName,bmcVMName):
        """ execute Robot Framework Cmd
        """
        bmcRobotCmd = self.prepareRobotFrameworkCmd(bmcPluginName,bmcVMName)
        print bmcRobotCmd
        try:
            os.system(bmcRobotCmd)
        except:
            raise Exception
        
    def getEmailIDs(self):
        '''
        Getting email ids form config.ini file
        '''
        bmcEmailArrayList = []
        bmcEmailArrayList = self.readConfigIniFile("DEFAULT", "BMC_EMAIL_IDS_TO_SEND_TEST_RESPORTS").split(",")
        return bmcEmailArrayList
    
    def getCurrentDirectoryPath(self):
        '''
        Getting current directory path
        '''
        bmcCurrentDirectoryPath = os.getcwd()
        return bmcCurrentDirectoryPath
    
    def getImmediateSubdirectories(self, bmcCurrentDirectoryPath):
        '''
        Getting Immediate subdirectories
        '''
        return [name for name in os.listdir(bmcCurrentDirectoryPath)
            if os.path.isdir(os.path.join(bmcCurrentDirectoryPath, name))]
    
    
    def getPluginFromGitHub(self, bmcPluginName):
        '''
        Get plugin from github
        '''
        try:
            bmcGithubUrl = self.readConfigIniFile("DEFAULT", "BMC_ORG_PLUGIN_URL")
            bmcGithubCloneCmd = self.readConfigIniFile("DEFAULT", "BMC_GITHUB_CLONE_COMMAND")
            self.shellcmd(bmcGithubCloneCmd + " " + bmcGithubUrl + bmcPluginName + ".git")
        except:
            pass
        
    
    
    def readStdoutFile(self):
        '''
        read stdout file
        '''
        with open("stdout.txt", 'r') as f:
            read_data = f.read()
            f.closed
        return read_data
    def serchSubstring(self, fullstring, searchString):
        '''
        search substring
        '''
        bmcIsFound = ""
        if (fullstring.find(searchString) >= 0):
            bmcIsFound = "yes"
        else:
            bmcIsFound = "no"
        return bmcIsFound
     
    def setValue(self, value):
        self.bmcPluginName = value
        self.isSet = True

    def getValue(self):
        return self.bmcPluginName
    
    def getTypeOfOutput(self, bmcPluginName):
        return self.readLocalAppVariableFile("BMC_TYPE_OF_OUTPUT")
    
    def getTypeOfOS(self):
        '''
        get Type Of OS
        '''
        bmcTypeOfOs = ""
        bmcPlatformName = self.checkPlatformNameAgainstConfig()
        if bmcPlatformName == 'Windows':
            bmcTypeOfOs = "Windows"
        else:
            bmcTypeOfOs = "other"
        return bmcTypeOfOs
    
    def removeDoubleQuotas(self, bmcMsg):
        if bmcMsg.startswith('"') and bmcMsg.endswith('"'):
            bmcMsg = bmcMsg[1:-1]
        return bmcMsg
    
    def checMetricsFoundInFile(self, bmcMetricName):
        isFound = "no"
        with open(self.readConfigIniFile("DEFAULT", "BMC_STDOUT_FILE_NAME"), 'r') as f:
            for line in f:
                print line
                if bmcMetricName.strip() in line:
                    isFound = "yes"
                break
        return isFound
    
    def sendTestReport(self, bmcPluginName):
        '''
        get Type Of OS
        '''
        bmcEmailIds = {}
        bmcEmailIds = self.readConfigIniFile("DEFAULT", "BMC_EMAIL_IDS_TO_SEND_TEST_RESPORTS").split(",")
        sender = 'from@fromdomain.com'
        message = """From: SaaS Development Team <no-reply@bmc.com>
            To: Add Group Name 
            """
        message += " Subject: Boundary Meter Plugin Test Report - " + bmcPluginName
        message += self.readTestReportFile()
        try:
            smtpObj = smtplib.SMTP('mail.bmc.com')
            for bmcEmailId in bmcEmailIds:
                smtpObj.sendmail(sender, bmcEmailId, message)         
            print "Successfully sent email"
        except SMTPException:
            print "Error: unable to send email"
    
    def readTestReportFile(self):
        '''
        read generated report html file
        '''
        with open(self.getCurrentDirectoryPath() + "\\report.html", 'r') as f:
            read_data = f.read()
            f.closed
        return read_data
    
    def runPlugin(self, bmcPluginName):
        '''
         runn plugin based on defined cmd
        '''
        # Need to handle windows
        bmcPluginRunCmd = self.readLocalAppVariableFile("BMC_STAND_ALONE_APPLICATION_RUN_COMMAND")
        bmcPluginRunCmd = self.removeDoubleQuotas(bmcPluginRunCmd)
        self.changeDirectory(self.getCurrentDirectoryPath() + "/" + bmcPluginName)
        self.shellcmd(bmcPluginRunCmd)
    
    def fileWrite(self, bmcFile, newParamJson):
            bmcFile = open(bmcFile, "w")
            bmcFile.write(newParamJson)
            bmcFile.close()
    
    def replaceParamJsonValuesWithConfigValues(self, bmcPluginName):
        '''
         replace ParamJson Values With Config Values
        '''
        bmcPath = ""
        try:
            if self.getTypeOfOS() == "Windows":
                bmcPath = self.getCurrentDirectoryPath() + "\\" + bmcPluginName + "\param.json"
            else:
                bmcPath = self.getCurrentDirectoryPath() + "/" + bmcPluginName + "/param.json"
            bmcParamJsonData = self.readLocalAppVariableFile("BMC_ADD_REPLICA_OF_PARAM_JSON")
            bmcParamJsonData = bmcParamJsonData[1:]
            bmcParamJsonData = bmcParamJsonData[:-1]
            bmcParamJsonData = bmcParamJsonData.replace("'", "\"")
            print bmcParamJsonData
            self.fileWrite(bmcPath, bmcParamJsonData)
        except:
            bmcCustomeLog.log("\n Exception accurred in replaceParamJsonValuesWithConfigValues method")
        
    def writeRPCCallDataTOFile(self, bmcRPCCallData):
        '''
         writing RPC  data to file
        '''
        try:
            file = open("stdout.txt", "a")
            file.write(bmcRPCCallData)
            file.close()
        except IOError:
                raise
            
    def createEmptyFile(self):
        '''
         creating  stdout.txt file in current directory
        '''
        try:
            open('stdout.txt', 'ab', 0).close()
        except OSError:
            pass  # see the comment above
    
    def removeFile(self, bmcFileName):
        '''
         Removing stdout.txt file from current directory
        '''
        try:
            os.remove(bmcFileName)
        except OSError:
            pass  # see the comment above
    def waitForExecution(self, bmcTimeInseconds):
        '''
         Waiting for each step execution
        '''
        try:
            time.sleep(float(str(bmcTimeInseconds).strip()))
        except OSError:
            pass
        
    def readRPCLogFile(self):
        '''
        read stdout file
        '''
        with open("automation.log", 'r') as f:
            read_data = f.read()
            f.closed
        return read_data
    
    def vagrantCMD(self, bmcVagrantCmd):
        retVal = self.shellcmd(bmcVagrantCmd)
        return retVal
    
    def readConfigIniFile(self, bmcSectionName, bmcKey):
        '''
        Reading config file
        '''
        config = StringIO.StringIO()
        bmcCurrentDirectoryPath = self.getCurrentDirectoryPath() + "/config.ini"
        config.write(open(bmcCurrentDirectoryPath).read())
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
        bmcRetValue = cp.get(bmcSectionName, bmcKey)
        return  bmcRetValue
    
    def getVagrantCreationCMD(self, bmcOSType):
        '''
        Vagrant Creation command
        '''
        bmcCreationCommand = "vagrant up " + bmcOSType
        return bmcCreationCommand
    
    def vagrantDestroyCMD(self):
        '''
        Vagrant vagrant destroyCMD
        '''
        bmcDestroyCMD = "vagrant destroy -f"
        retVal = self.shellcmd(bmcDestroyCMD)
        return retVal
    
    def getVagrantSSHCMD(self, bmchostName, bmcPluginName):
        '''
        Start execution
        '''
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" python /home/vagrant/AutomationTool/startAutomationSuite.py " + bmcPluginName + "  vagrant " + bmchostName + '"'
        bmcCustomeLog.log("VagrantSSHCMD............" + bmcCMD)
        return bmcCMD
    
    def changeDirectory(self, bmcPath):
        os.chdir(bmcPath)
        
    def copyServerFile(self, bmchostName):
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCopyCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" cp /home/vagrant/AutomationTool/serving.py /usr/local/lib/python2.7/dist-packages/werkzeug/serving.py" + '"'
        return bmcCopyCMD
    def installRequirementFile(self):
        '''
        install Requirement File
        '''
        self.shellcmd("pip install -r requirements.txt")
    
    def terminateExecution(self,bmcVMName):
        '''
        Terminate Execution
        '''
        # self.shellcmd("pkill -o -u vagrant sshd")
        bmcTypeOSCMD = self.checkTypeOSCMD(bmcVMName)
        self.shellcmd(bmcTypeOSCMD + " poweroff")
        
    def getListOfPluginNameFromGithub(self):
        '''
        get List Of Plugin Name From Github
        '''
        bmcListOfPluginName = {}
        try:
            counter = 1
            while True:
                url = "https://api.github.com/organizations/83128/repos?page=" + str(counter) + "&per_page=1000"
                counter += 1
                response = requests.get(url)
                data = response.json() 
                listSize = len(data)
                if listSize >= 1 :  
                    for x in range(0, listSize):
                        bmcName = data[x]['name']
                        if "vagrant" not in bmcName:
                            bmcListOfPluginName[bmcName] = bmcName
                else:
                    break;
            bmcUniquePluginList = set(bmcListOfPluginName)
            return bmcUniquePluginList
        except IOError:
            pass
        
    def fileExists(self, bmcUrl):
        '''
        File Exists 
        '''
        request = urllib2.Request(bmcUrl)
        request.get_method = lambda : 'HEAD'
        try:
            response = urllib2.urlopen(request)
            return True
        except urllib2.HTTPError:
            return False
     
    def getFinalListPluginList(self):
        '''
        get Final PluginList
        '''
        bmcListOfPluginName = {}
        bmcFinalPluginList = {}
        bmcListOfPluginName = self.getListOfPluginNameFromGithub()
        bmcBlackListedPluginNames = self.readConfigIniFile("DEFAULT", "BMC_BLACK_LISTED_PLUGINS")
        bmcBlackListedPluginNameArrays = {}
        bmcCustomeLog.log(len(bmcListOfPluginName))
        # Removing black listed plugins
        if bmcBlackListedPluginNames != None and bmcBlackListedPluginNames != "":
            bmcBlackListedPluginNameArrays = bmcBlackListedPluginNames.split(",")
            for bmcPluginName in bmcBlackListedPluginNameArrays:
                bmcListOfPluginName.remove(bmcPluginName)
            
        for pluginName in bmcListOfPluginName:
            bmcUrlName = self.readConfigIniFile("DEFAULT", "BMC_APPVARIABLE_FILE_EXIST")
            bmcUrlName = bmcUrlName.replace(pluginName, bmcUrlName)
            if self.fileExists(bmcUrlName) != False:
                bmcFinalPluginList[pluginName] = pluginName
        bmcCustomeLog.log(len(bmcFinalPluginList))
        return bmcFinalPluginList
    
    def readPluginName(self):
        '''
         reading plugin name from file
        '''
        try:
            
            with open("pluginName.txt", 'r') as f:
                bmcReaddata = f.read()
                f.closed
            return bmcReaddata
        except IOError:
                bmcCustomeLog.log("Exception accured in readPluginName method")
                 
    
    def writePluginName(self, bmcPluginName):
        '''
         writing plugin name to file
        '''
        try:
            file = open("pluginName.txt", "w")
            file.write(bmcPluginName)
            file.close()
        except IOError:
                bmcCustomeLog.log("Exception accured in writePluginName method")
                raise 
    
    def copyRPCLogFile(self, bmchostName):
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCopyCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" cp /home/vagrant/automation.log  /home/vagrant/AutomationTool/automation.log" + '"'
        self.shellcmd(bmcCopyCMD)
        return bmcCopyCMD
    
    def isAppVariableFileIsExist(self, pluginName):
            bmcUrlName = self.readConfigIniFile("DEFAULT", "BMC_APPVARIABLE_FILE_EXIST")
            bmcFinalUrl = bmcUrlName.replace("PLUGINNAME", pluginName)
            print bmcFinalUrl
            bmcFound = False
            if self.fileExists(bmcFinalUrl) != False:
                bmcFound = True
            return bmcFound
    def writeEnvironmentVariableToFile(self, bmcHostName):
        '''
         writing env variable name to file
        '''
        try:
            file = open(".env", "w")
            file.write(bmcHostName)
            file.close()
        except IOError:
                bmcCustomeLog.log("Exception accured in writeEnvironmentVariableToFile method")
                 
        
    
    def readEnvironmentVariableFromFile(self):
        '''
         reading env variable name from file
        '''
        try:
            
            with open(".env", 'r') as f:
                bmcReaddata = f.read()
                f.closed
            return bmcReaddata
        except IOError:
                bmcCustomeLog.log("Exception accured in readEnvironmentVariableFromFile method")
                raise
            
    def checkIsPluginBlackListed(self, bmcPluginName):
        '''
        checking is plugin black listed
        '''
        bmcBlackListPlugins = self.readConfigIniFile("DEFAULT", "BMC_BLACK_LISTED_PLUGINS")
        return self.serchSubstring(bmcBlackListPlugins, bmcPluginName)
    
    def getWhiteListedPlugins(self):
        '''
        Getting white listed plugin names
        '''
        bmcWhiteListedPluginNames = self.readConfigIniFile("DEFAULT", "BMC_WHITE_LISTED_PLUGINS")
        bmcWhiteListedPluginNamesArray = {}
        if bmcWhiteListedPluginNames != "":
            bmcWhiteListedPluginNamesArray = bmcWhiteListedPluginNames.split(",")
        return bmcWhiteListedPluginNamesArray
    
    def downloadAppConfigFile(self, bmcPluginName):
        '''
        checking is plugin white listed
        '''
        bmcIsFileDownloaded = False
        try:
            if self.isAppVariableFileIsExist(bmcPluginName) == True:
                bmcAppVariableUrl = self.readConfigIniFile("DEFAULT", "BMC_DOWNLOAD_APPVARIABLE_FILE")
                bmcAppVariableUrl = bmcAppVariableUrl.replace("PLUGINNAME", bmcPluginName)
                urllib.urlretrieve (bmcAppVariableUrl, "AppVariables.py")
                bmcIsFileDownloaded = True
        except IOError:
                bmcCustomeLog.log("Exception accured in downloadAppConfigFile method")
        return bmcIsFileDownloaded
    
    def downloadVagrantFromGitHub(self, bmcPluginName):
        '''
        download Vagrant From GitHub
        '''
        try:
            bmcVagrantFolderDownload = "git clone " + self.readLocalAppVariableFile("BMC_VAGRANT_URL")
            retVal = self.shellcmd(bmcVagrantFolderDownload)
        except IOError:
                bmcCustomeLog.log("Exception accured in downloadVagrantFromGitHub method")
        return retVal
    
    def getVagrantNameFromVagrantURL(self, bmcVagrantURL):
        '''
        get Vagrant Folder Name From Vagrant URL
        '''
        try:
            bmcVagrantURL = bmcVagrantURL.split("/")
            bmcVagrantName = bmcVagrantURL[-1]
            bmcVagrantNameArray = bmcVagrantName.split(".")
        except:
            bmcCustomeLog.log("Exception accured in getVagrantNameFromVagrantURL method")
        return bmcVagrantNameArray[0]
    
    def readLocalAppVariableFile(self, bmcKey):
        '''
        Reading application local variable files
        '''
        config = StringIO.StringIO()
        config.write('[dummysection]\n')
        bmcCurrentDirectoryPath = self.getCurrentDirectoryPath() + "/AppVariables.py"
        config.write(open(bmcCurrentDirectoryPath).read())
        config.seek(0, os.SEEK_SET)
        cp = ConfigParser.ConfigParser()
        cp.readfp(config)
        bmcRetValue = cp.get("dummysection", bmcKey)
        return  bmcRetValue
    
    def copyDiectory(self, bmcVagrantFolderName):
        # copy subdirectory example
        try:
            bmcToDirectory = self.getCurrentDirectoryPath()
            bmcFromDirectory = ""
            if self.getTypeOfOS() == "Windows":
                bmcFromDirectory = self.getCurrentDirectoryPath() + "\\" + bmcVagrantFolderName + "\\"
                print bmcFromDirectory
            else:
                bmcFromDirectory = self.getCurrentDirectoryPath() + "/" + bmcVagrantFolderName + "/"
            copy_tree(bmcFromDirectory, bmcToDirectory)
        except:
            bmcCustomeLog.log("Exception accured in copyDiectory method")
    
    def deleteFolders(self, bmcVagrantFolderName):
        '''
        Delete vagrant folder
        '''
        bmcPath = ""
        try:
                if self.getTypeOfOS() == "Windows":
                    bmcPath = self.getCurrentDirectoryPath() + "\\" + bmcVagrantFolderName
                else:
                    bmcPath = self.getCurrentDirectoryPath() + "/" + bmcVagrantFolderName 
                os.system("rm -rf " + bmcPath)
        except:
            bmcCustomeLog.log("Exception accured in deleteVagrantFolders method")
            
    def isVagrantFolderFoundInGithub(self, bmcVagrantUrl):
        '''
        checking is vagrant folder exist in github
        '''
        bmcIsVagrantFolderExistInGitHub = False
        try:
            request = requests.get('https://github.com/Kumar-Patil/vagrant-nginx.git')
            if request.status_code == 200:
                bmcIsVagrantFolderExistInGitHub = True
            else:
                bmcIsVagrantFolderExistInGitHub = False
        
        except:
                bmcCustomeLog.log("Exception accured in isVagrantFolderFoundInGithub method")
                return bmcIsVagrantFolderExistInGitHub
        
    def installPIP(self, bmchostName):
        '''
        install PIP
        '''
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" python /home/vagrant/AutomationTool/get-pip.py.py "  '"'
        return bmcCMD
    
    def installDependencies(self, bmchostName):
        '''
        install Dependencies
        '''
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" pip install -r /home/vagrant/AutomationTool/requirements.txt "  '"'
        return bmcCMD
    
    def readVagrantStdoutFile(self, bmcPluginName):
        '''
        read stdout from vagrant folder file
        '''
        with open("/home/vagrant/AutomationTool/" + bmcPluginName + "/stdout.txt", 'r') as f:
            read_data = f.read()
            f.closed
        return read_data
    
    def readVagrantRPCLogFile(self, bmcPluginName):
        '''
        read stdout file
        '''
        with open("/home/vagrant/automation.log", 'r') as f:
            read_data = f.read()
            f.closed
        return read_data
        
    def installGIT(self,bmchostName):
        bmcTypeOSCMD = self.checkTypeOSCMD(bmchostName)
        bmcCMD = "vagrant ssh " + bmchostName + " -c" + ' "' + ""+bmcTypeOSCMD+" apt-get install git "  '"'
        return bmcCMD
    
    def checkTypeOSCMD(self,bmcVMName):
        bmcCMD = ""
        if "cent" in bmcVMName or "ubunt" in bmcVMName or  "rhel" in bmcVMName:
            bmcCMD = "sudo"
        else:
            bmcCMD = ""
        return bmcCMD
        
        
            
