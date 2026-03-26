import yaml

def parse_configuration(filepath: str) -> dict[str, any]:
    try:
        with open(filepath, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise yaml.YAMLError(f"Yaml file is invalid: {filepath}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    output: dict[str, any] = {
        "url": data["site"]["url"],
        "pagination": data["site"]["pagination"]["pattern"],
        "limiter": data["site"]["pagination"]["limiter"],
        "fields": data["site"]["fields"]
    }

    return output