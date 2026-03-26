import yaml

def parse_configuration(filepath: str) -> dict[str, any]:
    try:
        with open(filepath, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError:
                raise yaml.YAMLError(f"Yaml file is invalid: {filepath}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    try:
        output: dict[str, any] = {
            "url": data["site"]["url"],
            "pagination": data["site"]["pagination"]["pattern"],
            "limiter": data["site"]["pagination"]["limiter"],
            "fields": data["site"]["fields"]
        }
    except KeyError:
        raise KeyError("Configuration is missing one or more required fields. (required fields: site, url, pagination, limiter, fields)")
    return output