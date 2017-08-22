# gemini_solution_builder

## Use dockerize gsb

### manual build gsb image

In any env with docker:

```
git clone https://github.com/ccmagithub/gemini_solution_builder.git
cd gemini_solution_builder
git checkout develop
docker build -t gsb:0.1a .
```

Now you get gsb image

### How to use

`docker run -v /<abs_path_to_gsp_dir>/:/gemini_solution_builder/example/ gsb:0.1a gsb --build example/`

<abs_path_to_gsp_dir> means absolut path to the directory of gsp

Now you can see the gsp in the folder

## Installation

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


