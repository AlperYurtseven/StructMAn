import os
import subprocess
import shutil

from structman.base_utils.base_utils import calc_checksum

def retrieve_raw_data(config):
    cmds = ' '.join(['wget', 'https://conglab.swmed.edu/humanPPI/downloads/best_models.tar.gz', '--no-check-certificate'])
    p = subprocess.Popen(cmds, shell=True, cwd = config.complex_model_db_path)
    p.wait()

def complex_model_id_to_folder_path(config):
    cmds = ' '.join(['tar', '-xvzf', 'best_models.tar.gz'])
    p = subprocess.Popen(cmds, shell=True, cwd = config.complex_model_db_path)
    p.wait()

    cmds = ' '.join(['rm', 'best_models.tar.gz'])
    p = subprocess.Popen(cmds, shell=True, cwd = config.complex_model_db_path)
    p.wait()

    for foldername in os.listdir(os.path.join(config.complex_model_db_path, 'best_models')):
        if not os.path.isdir(f'{config.complex_model_db_path}/best_models/{foldername}'):
            continue
        splitted = foldername.split("_")
        first_entry = splitted[0]
        first_folder = first_entry[-2:]
        second_folder = first_entry[-4:-2]

        target_dir = f'{config.complex_model_db_path}/{first_folder}/{second_folder}'
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)
        for file in os.listdir(f'{config.complex_model_db_path}/best_models/{foldername}'):
            if file.endswith('.pdb'):
                src = f'{config.complex_model_db_path}/best_models/{foldername}/{file}'
                dst = f'{target_dir}/{file}'
                shutil.move(src, dst)
                cmds = ' '.join(['gzip', dst])
                p = subprocess.Popen(cmds, shell=True)
                p.wait()
        shutil.rmtree(f'{config.complex_model_db_path}/best_models/{foldername}')
    shutil.rmtree(f'{config.complex_model_db_path}/best_models')

def main(config):
    print('Updating local Complex model DB')
    retrieve_raw_data(config)
    complex_model_id_to_folder_path(config)
