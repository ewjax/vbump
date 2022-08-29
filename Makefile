
PACKAGE=versionbump

##############################################################################
# do this while not in venv
venv:
	python -m venv .venv

venv.clean:
	rm -rfd .venv



##############################################################################
# do these while in venv
run: libs.quiet
	py $(PACKAGE).py


# libs make targets ###########################
libs: requirements.txt
	pip install -r requirements.txt

libs.quiet: requirements.txt
	pip install -q -r requirements.txt

libs.clean:
	pip uninstall -r requirements.txt


# exe make targets ###########################
exe: libs

exe.clean: libs.clean




# general make targets ###########################

all: libs exe

all.clean: libs.clean exe.clean

clean: all.clean
