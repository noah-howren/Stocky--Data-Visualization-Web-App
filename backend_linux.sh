
set -x
VIRTUAL_ENV=$(pwd)/venv
PATH=$VIRTUAL_ENV/bin:$PATH
export VIRTUAL_ENV
export PATH
export FLASK_APP=stocky
export FLASK_ENV=development
cd backend
flask run