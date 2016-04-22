***Settings ***
Documentation     Boundary Meter Plugin Automation Tool

Library           TestCaseLibrary.py
Library           Process
Suite Teardown    Terminate All Processes    kill=True

*** Test Cases  For  Plugins ***

Boundary meter status check
        ${ret} =    checkBoundaryMeterIsRunning
        Should Be Equal   ${ret}    ok
        
Plugin started
        ${ret} =    isPluginStarted  
        Should Be Equal   ${ret}    yes
        
Plugin successfully established connection
        ${ret} =    isConnectionEstablished  
        Should Be Equal   ${ret}    no
        
Total number of metrics are available
	  ${ret} =    totalNumberOfMetrics    ${BMC_LIST_OF_METRICS}
      Should Be Equal   ${ret}    ${BMC_NUMBER_OF_METRICS}
       
    
   

      
       
