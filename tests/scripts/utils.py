from snakemake.io import expand
import os
import subprocess
import shutil
import yaml

def setUp():
    # This utility setUp is intended to be run once before all tests are run
    # It is intended the set up all the necessary fake data in order to test
    # the rules and scipt files.  

    # Load the configuration file to get basic parameters 
    with open(r'tests/settings/testing_config.yaml') as file:
        configs = yaml.full_load(file)

        # Get the settings 
        pids = configs['PIDS']

    
    # Reset the test data files  
    for pid in pids:
        # Remove old data files if they exist
        despath = os.path.join('data/raw/', pid)
        if os.path.exists(despath) and os.path.isdir(despath):
            shutil.rmtree(despath)

        # Remove old processed files if they exist
        propath = os.path.join('data/processed/', pid)
        if os.path.exists(propath) and os.path.isdir(propath):
            shutil.rmtree(propath)

        # Create a fresh PID data directories necessary for this round of tests
        os.mkdir(despath)

        # Copy necessary data files
        srcpath = os.path.join('tests/data/raw', pid)
        srcfiles = os.listdir(srcpath)
        for srcfile in srcfiles:
            srcfile_path = os.path.join(srcpath, srcfile)
            desfile = os.path.join(despath, srcfile)
            shutil.copy(srcfile_path, desfile)
    
    return configs


 
def generate_file_list(configs, sensor):
    # Generates the list of files that would be produced for one sensor
    # i.e. The sensor passed into the function. 

    # Initialize string of file path for both expected and actual metric values
    act_str = "data/processed/features/{pid}/{sensor}_{sensor_type}{time_segment}.csv"
    exp_str = "tests/data/processed/features/period/{pid}/{sensor}_{sensor_type}{time_segment}.csv"
    
    sensor_cap = sensor.upper()
    if 'TIME_SEGMENTS' and 'FEATURES' in configs[sensor_cap]:
        sensor_type = []
        if 'TYPES' in configs[sensor_cap]:
            for each in configs[sensor_cap]['TYPES']:
                sensor_type.append(each+'_')

    act_file_list = expand(act_str,pid=configs["PIDS"],
                                   sensor = sensor,
                                   sensor_type = sensor_type,
                                   time_segment = configs[sensor_cap]["TIME_SEGMENTS"])
    
    exp_file_list = expand(exp_str,pid=configs["PIDS"],
                                   sensor = sensor,
                                   sensor_type = sensor_type,
                                   time_segment = configs[sensor_cap]["TIME_SEGMENTS"])

    return zip(act_file_list, exp_file_list)


def generate_sensor_file_lists(configs):
    # Go through the configs and select those sensors with COMPUTE = True.
    # Also get TIME_SEGMENTS, and optionally TYPES then create expected 
    # files. Return dictionary with list of file paths of expected and 
    # actual files for each sensor listed in the config file. Added for Travis.

    # Initialize string of file path for both expected and actual metric values
    segment = configs['TIME_SEGMENTS']['TYPE'].lower()
    print(segment)
    act_str = "data/processed/features/"+segment+"/{pid}/{sensor_key}.csv"
    exp_str = "tests/data/processed/features/"+segment+"/{pid}/{sensor_key}.csv"

    # List of available sensors that can be tested by the testing suite
    TESTABLE_SENSORS = ['PHONE_MESSAGES', 'PHONE_CALLS', 'PHONE_SCREEN', 'PHONE_BATTERY', 'PHONE_BLUETOOTH', 'PHONE_WIFI_VISIBLE', 'PHONE_WIFI_CONNECTED', 'PHONE_LIGHT', 'PHONE_APPLICATIONS_FOREGROUND', 'PHONE_ACTIVITY_RECOGNITION', 'PHONE_CONVERSATION']

    # Build list of sensors to be tested. 
    sensors = []
    for sensor in TESTABLE_SENSORS:
        if sensor in configs.keys():
            for provider in configs[sensor]["PROVIDERS"]:
                if configs[sensor]["PROVIDERS"][provider]["COMPUTE"]:
                    sensors.append(sensor.lower())

    act_file_list = expand(act_str,pid=configs["PIDS"],sensor_key = sensors)                                
    exp_file_list = expand(exp_str, pid=configs["PIDS"],sensor_key = sensors)
    sensor_file_lists = list(zip(act_file_list,exp_file_list))          
    #sensor_file_lists[sensor] = list(zip(act_file_list,exp_file_list))

    return sensor_file_lists