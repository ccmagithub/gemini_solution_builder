# gemini_solution_builder

Installation

checkout gemini solution builder code
$ git clone https://github.com/ccmagithub/gemini_solution_builder.git
$ cd gemini_solution_builder

switch to develop branch if you want to use latest code.
$ git checkout develop

before building virtualenv, make sure you have installed virtualenv package
$ pip install virtualenv 
create virtualenv
$ virtualenv ../venv
enter virtualenv
$ source ../venv/bin/activate

If you want to leave the virtual environment for the moment.
$ deactivate

install required packages
$ pip install -r requirements.txt
install gsb package
$ pip install -e .
you should have gsb installed.
$ gsb -h

