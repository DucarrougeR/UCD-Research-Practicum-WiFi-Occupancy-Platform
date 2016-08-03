import os
import sys
from subprocess import call
python_version = sys.version_info.major
if not python_version == 3:
    print("Requires python 3")
    sys.exit(1)

if not call(["pip", "install", "-r", "requirements.txt"]) == 0:
    print("Error install python dependencies. Please ensure pip is correctly installed")
    sys.exit(1)

os.chdir("app/static")
if not call(["node", "--version"]) == 0:
    print("This requires node js to be installed. Please install node before continuing")
    sys.exit(1)

if not call(["node", "--help"]) == 0:
    print("This requires node js to be installed. Please install node before continuing")
    sys.exit(1)

if not call(["npm", "--help"]) == 0:
    print("This requires npm to be installed. Please install npm before continuing")
    sys.exit(1)

if not call(["bower", "--help"]) == 0:
    print("This requires bower to be installed. Installing now")
    call(["npm", "-g", "install", "bower"])

print("Installing global libraries with NPM...")
call(["npm", "install", "-g", "nodemon", "node-sass"])
print("Installing npm project dependencies")
call(["npm", "install"])
print("Should be good to go!")
