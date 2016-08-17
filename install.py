import os
import sys
from subprocess import call
python_version = sys.version_info.major
if not python_version == 3:
    print("Requires python 3")
    sys.exit(1)

try:
    call(["pip3"])
except:
    print("Pip must be installed. Please install pip before continuing")
    sys.exit(1)

try:
    print("Installing python dependencies. If there are any errors...well...")
    call(["pip3", "install", "-r", "requirements.txt"])
except:
    print("Error install python dependencies. Please ensure pip is correctly installed")
    sys.exit(1)


os.chdir("app/static")
try:
    call(["node", "--version"])
except:
    print("This requires node js to be installed. Please install node before continuing")
    sys.exit(1)


try:
    call(["npm", "--help"])
except:
    print("This requires npm to be installed. Please install npm before continuing")
    sys.exit(1)

try:
    call(["bower", "--help"])
except:
    print("This requires bower to be installed. Installing now")
    call(["npm", "-g", "install", "bower"])

print("Installing global libraries with NPM...")
call(["npm", "install", "-g", "nodemon", "node-sass"])
print("Installing npm project dependencies")
call(["npm", "install"])
print("Should be good to go!")

# comment so I can push
