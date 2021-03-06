# Features.smk #########################################################################################################
def find_features_files(wildcards):
    feature_files = []
    for provider_key, provider in config[(wildcards.sensor_key).upper()]["PROVIDERS"].items():
        if provider["COMPUTE"]:
            feature_files.extend(expand("data/interim/{{pid}}/{sensor_key}_features/{sensor_key}_{language}_{provider_key}.csv", sensor_key=wildcards.sensor_key.lower(), language=provider["SRC_LANGUAGE"].lower(), provider_key=provider_key.lower()))
    return(feature_files)

def optional_steps_sleep_input(wildcards):
    if config["STEP"]["EXCLUDE_SLEEP"]["EXCLUDE"] == True and config["STEP"]["EXCLUDE_SLEEP"]["TYPE"] == "FITBIT_BASED":
        return  "data/raw/{pid}/fitbit_sleep_summary_with_datetime.csv"
    else:
        return []

def input_merge_sensor_features_for_individual_participants(wildcards):
    feature_files = []
    for config_key in config.keys():
        if config_key.startswith(("PHONE", "FITBIT")) and "PROVIDERS" in config[config_key] and isinstance(config[config_key]["PROVIDERS"], dict):
            for provider_key, provider in config[config_key]["PROVIDERS"].items():
                if "COMPUTE" in provider.keys() and provider["COMPUTE"]:
                    feature_files.append("data/processed/features/{pid}/" + config_key.lower() + ".csv")
                    break
    return feature_files

def get_phone_sensor_names():
    phone_sensor_names = []
    for config_key in config.keys():
        if config_key.startswith(("PHONE")) and "PROVIDERS" in config[config_key]:
            if config_key != "PHONE_DATA_YIELD" and config_key not in phone_sensor_names:
                    phone_sensor_names.append(config_key)
    return phone_sensor_names

