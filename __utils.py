
import yaml


def log(str):
    print(">> {}".format(str))


def ___t(str):
    return (not str.startswith("ELY") and not str.startswith("Tilaajan"))


def __parse_role(parts):
    if len(parts) > 2 and ___t(parts[0]):
        type = f"{parts[1]}_{parts[2]}"
    elif len(parts) == 2 and ___t(parts[0]):
        type = f"{parts[1]}"
    elif len(parts) == 2 and not ___t(parts[0]):
        type = f"{parts[0]}_{parts[1]}"

    return type


def parse_name(current_role):
    """
    Palauttaa roolin nimen ilman sampoidtä

    Parameters:
        current_role (str):     - Esim: PR000001_Kelikeskus / _Kelikeskus / PR0003111_Tilaajan_turvallisuusvastaava yms.

    Returns:
        [str] Roolin nimi       - Esim: Kelikeskus / Kelikeskus / Tilaajan_turvallisuusvastaava
    """
    if '_' not in current_role:
        return current_role
    else:
        parts = current_role.split("_")
        return __parse_role(parts)


def parse_file(file_path, encoding='utf-8', lines=[]):
    """
    Lukee tekstitiedoston, palauttaa rivit (non-empty, stripped) 

    Parameters:
        file_path (str):    Path to the input file
        encoding (str):     File encoding (default 'utf-8')
        lines (list):       Placeholder list, unused 

    Returns:
        list: of non-empty strings, leading/trailing whitespace stripped 
    """
    with open(file_path, 'r', encoding=encoding) as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def load_clientprefs(file_path):
    """ 
    Lataa asetukset 

    Parameters : 
        [str] file_path

    Returns:
        TODO 
    """

    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
