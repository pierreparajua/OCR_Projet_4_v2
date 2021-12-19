from colorama import Fore, init
from dateutil.parser import parse

init(autoreset=True)


def check_date_format(date: str) -> bool:
    """Check if the date is in DD/MM/YYYY.
    Args:
        date(str):  date
    Returns:
        Boolean
    """
    if not is_date(date):
        return False
    split_date = date.split("/")
    if len(split_date) != 3:
        return False
    elif len(split_date[0]) > 2:
        return False
    elif len(split_date[1]) > 2:
        return False
    elif split_date[1] not in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
        return False
    elif len(split_date[2]) != 4:
        return False
    return True


def check_name_format(name: str) -> bool:
    """
    Check if the args is a first or last name
    Args:
        name(str): first or last name
    Returns:
        Booleans
    """
    if not name:
        return False
    for char in name:
        if not ord(char) == 32 and \
                not 45 <= ord(char) <= 46 and \
                not 65 <= ord(char) <= 90 and \
                not 97 <= ord(char) <= 122 and \
                not 192 <= ord(char) <= 214 and \
                not 216 <= ord(char) <= 254:
            return False
    return True


def check_ranking_format(ranking: str) -> bool:
    """
    Check if the args is a figure
    Args:
        ranking(str): first or last name
    Returns:
        Booleans
    """
    for char in ranking:
        if not 48 <= ord(char) <= 57:
            return False
    return True


def check_name(name):
    if name:
        while not check_name_format(name):
            name = wrong_entry(name)
    return name


def check_date(date):
    if date:
        while not check_date_format(date):
            date = wrong_entry(date)
    return date


def check_ranking(ranking):
    if ranking:
        while not check_ranking_format(ranking):
            ranking = wrong_entry(ranking)
    return ranking


def get_choice(choices: list) -> str:
    """
        Get a choice and check it and return it.
        Args:
            choices(list): possible choices for the user

        Returns:
            choice(str): user's choice
        """
    choice = input(Fore.LIGHTBLUE_EX + "Choix: ").lower()
    while choice not in choices:
        choice = wrong_entry(choice)

    return choice


def is_date(string: str, fuzzy=False) -> bool:
    """
    Check if the args is in date format.
    Args:
        fuzzy:
        string(str): date
    Returns:
        Boolean
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def replace_for_date(date):
    """Replace characters to get the desired format."""
    return date.replace("-", "/") \
        .replace(".", "/") \
        .replace(" ", "/")


def wrong_entry(choice: str):
    """ Display error message"""
    value = input(Fore.LIGHTRED_EX + f"{choice} : n' est pas un choix valide.\n"
                                     f"Veuillez ressaisir votre choix: \n")
    return value
