"""
    __init.py

    Roolien formaatti:
        ...
        <sampoid>_rooli / _rooli
        kayttaja@email.com
        kayttaja@email.com

        <sampoid>_rooli
        No Members

        <sampoid>_rooli
        kayttaja@email.com
        ...

    Parsitaan ja lasketaan kaikki roolit yhteen
    Sampoid:t haettu kannasta (data/kaynnissa_olevat)
    Jotka vastaavat urakkanimiä (data/urakkanimet) 
"""
import argparse

import __utils as u
import __debug as d
import __report as r


class RoleParser:
    def __init__(self, prefs, merge=True):
        # Files
        self.file_roolit = prefs.get('files', {}).get('roolit')  # Kaikki roolit ja käyttäjät
        self.file_ended = prefs.get('files', {}).get('paattyneet')  # Päättyneiden urakoiden sampoidt
        self.file_ongoing = prefs.get('files', {}).get('kaynnissa')  # Käynnissä olevien urakoiden sampoidt
        self.file_yllapito = prefs.get('files', {}).get('korjaukset')  # Käynnissä olevat ylläpitourakat sampoidt
        self.file_urakkanimet = prefs.get('files', {}).get('urakka_nimet')  # Urakoiden nimet samassa järjestyksessä (vastaa käynnissä olevia)

        # Dict
        self.roles = {}
        self.role_type_counts = {}

        # Set
        self.role_types = set()
        self.roles_ongoing = set()

        # Arr
        self.roles_with_members = []  # Roolit jotka sisältää käyttäjiä 
        self.roles_without_members = []  # Roolit ilman käyttäjiä 
        self.roles_without_members_ongoing = []  # Roolit ilman käyttäjiä (vain käynnissä olevat urakat )
        self.sampoidt = u.parse_file(self.file_ongoing, "utf-8", [])
        self.urakkanimet = u.parse_file(self.file_urakkanimet, "utf-8", [])

        # Bool
        self.merge_roles = merge  # Mergetäänkö tilaajan / ely roolit?

    def append_ongoing(self, current_role, ended_roles, line):
        """
        Prosessoi käynnissä olevien  urakoiden rooleja TODO 

        Parameters:
            roles_ongoing (set):        Käynnissä olevien urakoiden roolit 
            current_role (str):         Iteroinnissa oleva rooli 
            role_type_counts (dict):    - 
            ended_roles (list of str):  Päättyneiden urakoiden roolit 
            line                        -
        
        Returns:
            -
        """
        if "No members" in line:
            # Rivi sanoo että roolilla ei ole käyttäjää
            self.roles_without_members.append(current_role)

        if not any(e in current_role for e in ended_roles):
            self.roles_ongoing.add(current_role)
            self.role_type_counts[u.parse_name(current_role)] += 1

            if "No members" in line:
                # Lisätään tähän tyhjät (vain käynnissä olevat urakat )
                self.roles_without_members_ongoing.append(current_role)

    def parse(self):

        skip = False
        current_role = None
        all_roles = u.parse_file(self.file_roolit, 'utf-16', [])
        ended_roles = u.parse_file(self.file_ended, 'utf-8', [])

        # Mergetään ely roolit tilaajan rooleihin
        tilaaja_roolit = ['Tilaajan_Kayttaja', 'Tilaajan_Urakanvalvoja', 'Tilaajan_laadunvalvoja', 'Tilaajan_turvallisuusvastaava']

        for line in all_roles:

            line = line.strip()

            if not line:
                continue

            # Rivi on käyttäjä
            if "@" in line or line == 'Jarjestelmavastaava':

                # Rooli jo olemassa
                # (esim jos mergetään ely -> tilaajan rooleihin, sama rooli tulee kahdesti)
                if skip:
                    # => seuraava rivi
                    continue

                # Rooli ei ole tyhjä
                if current_role:
                    # Kaikki roolit tähän
                    self.roles[current_role].append(line)
                    # Vain käynnissä olevat urakat
                    self.append_ongoing(current_role, ended_roles, line)

            # Rivi sanoo että roolilla ei ole käyttäjiä
            elif "No members" in line:

                # Rivi jo olemassa
                if skip:
                    # Seuraava rivi on rooli, skip voi laittaa pois päältä
                    skip = False
                    # => seuraava rivi
                    continue

                # Rooli ei ole tyhjä
                if current_role:
                    # Vain käynnissä olevat urakat
                    self.append_ongoing(current_role, ended_roles, line)

                # => seuraava rivi
                continue

            # Rivi on roolin nimi
            else:

                skip = False # Hypätäänkö roolin yli? (duplikaatteja voi tulla mergen kanssa)

                if self.merge_roles:
                    # Rooli on tilaajan rooli, muuta se -> ELY rooliksi
                    if any(r in line for r in tilaaja_roolit):
                        standardized_line = line.replace("Tilaajan_", "ELY_")
                        standardized_line = standardized_line.replace("ELY_laadunvalvoja", "ELY_Laadunvalvoja")  # Ely Laadunvalvoja on uppercase
                        current_role = standardized_line
                    else:
                        # Rooli ei ole tilaajan rooli
                        current_role = line
                else:
                    # Ei mergetä tilaajan / ely rooleja
                    current_role = line

                # Rooli on jo olemassa
                if current_role in self.roles:
                    skip = True
                    # => seuraava rivi
                    continue

                # Roolien käyttäjät
                self.roles[current_role] = []

                # Palauttaa roolin nimen ilman urakka spesifiä sampoidtä
                r_type = u.parse_name(current_role)
                self.role_types.add(r_type)

                # Lisää roolityyppi mahdollisiin rooleihin
                if r_type not in self.role_type_counts:
                    self.role_type_counts[r_type] = 0

        # u.log(f"Rooleja yhteensä: {len(self.roles)}")
        # u.log(f"Rooleja yhteensä, vain käynnissä olevat: {len(self.roles_ongoing)}")
        pass


if __name__ == "__main__":
    # Entry point
    prefs = u.load_clientprefs('prefs.yml')

    # Args
    parser_args = argparse.ArgumentParser()
    parser_args.add_argument("--m", 
                             action="store_true", 
                             help="Enabloi roolien mergetys "+ \
                                  "(tilaajan / ely roolit mergetään, lasketaan vain käynnissä olevat urakat)")
    parser_args.add_argument("--v", 
                             action="store_true", 
                             help="Enabloi datan visualisointi")

    args = parser_args.parse_args()
    u.log(f"Käynnistetään.. \n Merge: {args.m}\n Visualisoi: {args.v}")

    # Parser
    parser = RoleParser(prefs, merge=args.m)
    parser.parse()

    # Käynnissä olevat urakat, käyttäjät mukana
    roles_dict_ongoing = (
        {k: v for k, v in parser.roles.items() if k in parser.roles_ongoing}
        if args.m
        else parser.roles
    )
    # Roolit jotka ovat tyhjiä
    roles_without_members = (
        parser.roles_without_members_ongoing
        if args.m
        else parser.roles_without_members
    )

    # Visualisointi
    if args.v:
        d.visualize(parser.roles_ongoing, roles_without_members, roles_dict_ongoing)

    print("\n")
    u.log(f"Rooleja yhteensä: {len(parser.roles)}")
    u.log(f"Rooleja yhteensä, vain käynnissä olevat: {len(parser.roles_ongoing)}")

    # Tee raportti
    report = r.ReportGenerator()
    report.report(roles_dict_ongoing, parser.sampoidt, parser.urakkanimet)
