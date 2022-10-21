#!/bin/bash
# ref: https://linuxways.net/ubuntu/how-to-install-metasploit-framework-on-ubuntu-20-04/
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall
