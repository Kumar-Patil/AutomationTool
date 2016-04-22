# Explictly set to avoid warning message
#Author : Santosh Patil
Package {
  allow_virtual => false,
}

#This block will install all dependencies in ubuntu OS
node /^ubuntu/ {

  file { 'bash_profile':
    path    => '/home/vagrant/.bash_profile',
    ensure  => file,
    source  => '/vagrant/manifests/bash_profile',
    }

  #updating packages
  exec { 'update-apt-packages':
    command =>'/usr/bin/apt-get update -y',
  }
   
  #curl installation
  exec{ 'apt-get-install-curl':
	command =>'/usr/bin/apt-get install curl -y',
  }
  
  #python pip installation
  exec { 'python-pip':
    command =>'/usr/bin/apt-get install python-pip -y',
  }
  
  #supported libs installation
  exec { 'apt-get install -y build-essential':
    command =>'/usr/bin/apt-get install -y build-essential -y',
  }
  #node js installation
  exec { 'apt-get install nodejs':
    command =>'/usr/bin/apt-get install nodejs -y',
  }
  
  #npm installation
  exec { 'apt-get install npm':
    command =>'/usr/bin/apt-get install npm -y',
  }
  
  #lua installation
  exec { 'apt-get install liblua5.1-0-dev liblua50-dev liblualib50-dev':
    command =>'/usr/bin/apt-get install liblua5.1-0-dev liblua50-dev liblualib50-dev -y',
  }
  
  #supported libs installation
  exec { 'apt-get install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip':
    command =>'/usr/bin/apt-get install build-essential libssl-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip -y',
    require => Exec['update-apt-packages'],
  }
  
  #git hub installation
  exec { 'apt-get install git':
    command =>'/usr/bin/apt-get install git -y',
    require => Exec['update-apt-packages'],
  }
  #Executing Requirement file
  exec { 'pip install -r requirements.txt':
    command =>'/usr/bin/pip install -r /home/vagrant//AutomationTool/requirements.txt',
    require => Exec['python-pip'],
  }
  
  #installing boundary meter
  #class { 'boundary':
  #  token => $::boundary_api_token,
  #}
  
}

#This block will install all dependencies in cent OS
node /^centos/ {

  file { 'bash_profile':
    path    => '/home/vagrant/.bash_profile',
    ensure  => file,
    source  => '/vagrant/manifests/bash_profile'
  }

  #curl installation
  exec{'apt-get-install-curl':
	command =>'/usr/bin/apt-get install curl -y'
  }
  exec { 'update-rpm-packages':
    command => '/usr/bin/yum update -y'
  }

  #fetching latest pip
  wget::fetch { 'python get-pip.py':
  source      => 'https://bootstrap.pypa.io/get-pip.py',
  destination => '/home/get-pip.py'
  }
  #class { 'boundary':
  #token => $::boundary_api_token
  #}

}
