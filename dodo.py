"""Make automatization."""

import glob
from doit.tools import create_folder

DOIT_CONFIG = {'default_tasks': ['all']}

def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o Clicker.pot ClickerMSU'],
            'file_dep': glob.glob('ClickerMSU/*.py'),
            'targets': ['Clicker.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D Clicker -d po -i Clicker.pot'],
            'file_dep': ['Clicker.pot'],
            'targets': ['po/ru/LC_MESSAGES/Clicker.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['ClickerMSU/ru/LC_MESSAGES']),
                'pybabel compile -D Clicker -l ru -i po/ru/LC_MESSAGES/Clicker.po -d ClickerMSU'
                       ],
            'file_dep': ['po/ru/LC_MESSAGES/Clicker.po'],
            'targets': ['ClickerMSU/ru/LC_MESSAGES/Clicker.mo'],
           }