cd $HOME/django
git fetch && git checkout -f origin/master

source $HOME/django/.venv/bin/activate
pip install -r $HOME/django/requirements.txt