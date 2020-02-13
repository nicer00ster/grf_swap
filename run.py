from __future__ import print_function, unicode_literals
import pip
import subprocess
import os, sys, fnmatch
import shutil

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

try:
    import chalk
except ImportError, e:
    install('pychalk')
finally:
    import chalk

try:
    import PyInquirer
except ImportError, e:
    install('PyInquirer')
finally:
    from PyInquirer import prompt, print_json, Separator


ragnarok_path = sys.argv[1] if len(sys.argv) > 1 else 'C:/Program Files (x86)/Gravity Interactive, Inc/Ragnarok Online Transcendence'

if not (ragnarok_path):
    print(chalk.red('Please supply a path to your Ragnarok folder'))
    print(chalk.yellow('You can do so by providing the path of your Ragnarok folder while calling this script!'))
    print(chalk.yellow('Example: ') + chalk.green('python run.py "C:/path/to/ragnarok/folder"'))
    exit()

def get_data_files(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
                result.append(Separator())

    result.remove(ragnarok_path + '\\data.grf')
    return result

def get_preset_dirs(path):
    directories = []
    for root, dirs, files in os.walk(path):
        for folder in dirs:
            directories.append(folder)
            directories.append(Separator())
    return directories

questions = [
    {
        'type': 'list',
        'name': 'chosen_grf',
        'message': 'Which data.grf file would you like to use?',
        'choices': get_data_files('*.grf', ragnarok_path)
    }
]

has_preset_dirs = [
    {
        'type': 'confirm',
        'name': 'has_preset_dirs',
        'message': 'Do you have a folder already created you\'d like to put the current GRF under?',
        'default': False,
    },
]

preset_dirs = [
    {
        'type': 'list',
        'name': 'preset_dir',
        'message': 'Choose the preset folder you\'d like to put the current GRF under.',
        'choices': get_preset_dirs(ragnarok_path + '/preset_grf'),
    }
]

chosen_folder_name = [
    {
        'type': 'input',
        'name': 'new_dir_name',
        'message': 'Type a name for the folder you want the old GRF under.',
    },
]

answers = prompt(questions)

try:
    if not os.path.exists(ragnarok_path + '/preset_grf'):
        os.makedirs(ragnarok_path + '/preset_grf', 0777)

    has_dirs = prompt(has_preset_dirs)

    if has_dirs['has_preset_dirs'] == True:
        preset_dirs = prompt(preset_dirs)
        shutil.move(ragnarok_path + '/data.grf', ragnarok_path + '/preset_grf/' + preset_dirs['preset_dir'])
    else:
        new_dir = prompt(chosen_folder_name)

        if not os.path.exists(ragnarok_path + '/preset_grf/' + new_dir['new_dir_name']):
            os.makedirs(ragnarok_path + '/preset_grf/' + new_dir['new_dir_name'], 0777)

        shutil.move(ragnarok_path + '/data.grf', ragnarok_path + '/preset_grf/' + new_dir['new_dir_name'])

except OSError as error:
    print(chalk.red("Creation of the directory %s failed" % ragnarok_path, error))
    exit()
else:
    if has_dirs['has_preset_dirs'] == False:
        print(chalk.green("Successfully created the directory %s " % ragnarok_path + '/preset_grf/' + new_dir['new_dir_name']))
    else:
        print(chalk.green("Successfully moved GRF to %s " % ragnarok_path + '/preset_grf/' + preset_dirs['preset_dir']))
finally:
    shutil.move(answers['chosen_grf'], ragnarok_path + '/data.grf')

print(chalk.green("Now using chosen GRF from %s " % answers['chosen_grf']))
