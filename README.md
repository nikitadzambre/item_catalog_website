# Item Catalog Website
## Synopsis
This website shows a catalog of sports' items while providing a user registration and authentication system. It allows users to add, edit or delete an item.
## Installation
This project runs on a VM which has Python3 and SQLite installed. To access this VM,
### Install VirtualBox
Install the platform package for your operating system from [here](https://www.virtualbox.org/wiki/Downloads)
### Install Vagrant
Install the version for your operating system from [here](https://www.vagrantup.com/downloads.html)
### Download the VM configuration
Download and unzip the following folder: [FSND-virtual-machine.zip](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip) or Github to fork and clone the repository https://github.com/udacity/fullstack-nanodegree-vm
### Start the VM
From the terminal, inside the vagrant subdirectory, run the command **vagrant up**
When vagrant up is finished running, you will get your shell prompt back. At this point, you can run **vagrant ssh** to log in to your newly installed Linux VM!
## Running the project
* Download the project zip file.
* Copy the 'catalog' folder to the 'vagrant' folder on VM.
* From the terminal, navigate to the folder 'catalog'.
* Run python database_setup.py
* Run python database_entries.py
* Run python application.py
* Open the link 'http://localhost:8000/catalog/' in the browser to access the website.
## License
This software is released under the MIT License, see LICENSE.txt.