cd $HOME/django
python3 -m venv .venv
source $HOME/django/.venv/bin/activate
pip install -r $HOME/django/requirements.txt

python3 $HOME/django/manage.py collectstatic