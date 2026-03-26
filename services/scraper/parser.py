import yaml

def parse_configuration(filepath: str) -> dict[str, any]:
    try:
        with open(filepath, "r") as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(e)
                return None
    except FileNotFoundError as e:
        return None
    
    output: dict[str, any] = {
        "url": data["site"]["url"],
        "pagination": data["site"]["pagination"]["pattern"],
        "limiter": data["site"]["pagination"]["limiter"],
        "fields": data["site"]["fields"]
    }

    print(output)
    return output

parse_configuration("./services/scraper/example.yaml")