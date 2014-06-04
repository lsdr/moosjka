# run "make" to install development requirements and dependencies 

all: env

install_requirement:
	@pip install -r requirements.txt

env: install_requirement
	@printf "\nWorking environment is \033[1;32mready\033[0m for action.\n";

