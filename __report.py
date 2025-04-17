import os
import sys
import pdfkit
import platform
import platform
import pandas as pd

from collections import defaultdict

import __html as h
import __utils as u


class ReportGenerator:
    def __init__(self):

        # Str
        self.title = 'python'
        self.custom_css = ''
        self.wkhtml_path = ''
        self.html_content = ''

        if platform.system() == "Windows":
            import ctypes
            ctypes.windll.kernel32.SetConsoleTitleW(self.title)
            self.wkhtml_path = r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

        else:
            sys.stdout.write(f'\x1b]0;{self.title}\x07')

            path_1 = "/usr/bin/wkhtmltopdf"
            path_2 = "/usr/local/bin/wkhtmltopdf"

            if os.path.isfile(path_1):
                self.wkhtml_path = path_1
            elif os.path.isfile(path_2):
                self.wkhtml_path = path_2
            else:
                print("\n Error: wkhtmltopdf not found in standard locations.")
                sys.exit(1)

        with open("resources/__c.css", "r") as css_file:
            self.custom_css = f"<style>\n{css_file.read()}\n</style>"

    def generate(self):
        """
        Generoi PDF & html raportin 

        Parameters:
            [str] html_content 
            [str] wkhtml_path 

        Returns:
            -
        """

        with open("report.html", "w", encoding="utf-8") as f:
            f.write(self.html_content)

        # Convert to PDF
        config = pdfkit.configuration(wkhtmltopdf=self.wkhtml_path)
        pdfkit.from_file('report.html', 'report.pdf', configuration=config, options={"enable-local-file-access": ""})

    def collect_dataframe_all(self, data, fn, grouped_columns, total):
        """
        Generoi PDF & html raportin 

        Parameters:
            [tuple] data 
            [fn] function
            [arr] columns
            [int] total 

        Returns:
            [df] - TODO
        """
        df = pd.DataFrame(data, columns=grouped_columns)
        df.index = df.index + 1

        if "Yhteensä (käyttäjiä)" in df.columns:
            df["numeric_total"] = df["Yhteensä (käyttäjiä)"].astype(int)

            df["Yhteensä (käyttäjiä)"] = df.apply(
                lambda row: fn(
                    row["numeric_total"],
                    round((row["numeric_total"] / total) * 100, 1) if total > 0 else 0
                ),
                axis=1
            )

            df.drop("numeric_total", axis=1, inplace=True)
        return df

    def parse_contract_and_base_role(self, role_key):
        """
        Palauttaa sampoid:n, ja roolin nimen

        Parameters:
            [str] rooli 

        Returns:
            - TODO 
        """

        base_role = u.parse_name(role_key)
        contract_id = role_key.split("_")[0].strip()
        return (contract_id, base_role)

    def generate_separate_tables_per_role(self, roles_dict, contract_ids, contract_names):
        """
        Generoi raporttiin gridin jokaiselle roolille 

        Parameters:
            [dict]  -
            [arr]  -
            [arr]  -

        Returns:
            - TODO 
        """

        # Mäppää sampoid:t urakkanimiin
        contract_name_map = dict(zip(contract_ids, contract_names))

        # Laske käyttäjät per rooli
        role_data = defaultdict(lambda: defaultdict(int))
        for full_role_key in roles_dict:
            cid, base_role = self.parse_contract_and_base_role(full_role_key)
            role_data[base_role][cid] += len(roles_dict[full_role_key])

        html_all = ""
        total_total = 0
        priority_roles = [
            "ELY_Kayttaja",
            "ELY_Paakayttaja",
            "ELY_Peruskayttaja",
            "Tilaajan_Asiantuntija",
            "Kayttaja",
            "Laatupaallikko",
            "Paakayttaja",
            "Tilaajan_laadunvalvoja"
        ]

        organisation_roles = ["Kayttaja", "Laatupaallikko", "Paakayttaja"]
        sopimus_roles = ["ELY_Kayttaja", "ELY_Paakayttaja", "ELY_Peruskayttaja", "Tilaajan_Asiantuntija"]

        # Sorttaa prion mukaan, muuten aakkosilla
        sorted_roles = sorted(role_data.keys(), key=lambda r: (priority_roles.index(r) if r in priority_roles else 9999, r))

        for base_role in sorted_roles:

            data_rows = []

            for cid, cnt in role_data[base_role].items():
                # if cnt > 0:
                cName = contract_name_map.get(cid, "").strip().replace('"', '').replace("'", "")

                if cid == '':
                    cid = base_role
                if len(cName) == 0:

                    if base_role in organisation_roles:
                        cName = '[organisaatio rooli, ei urakkaa]'
                    elif base_role in sopimus_roles:
                        cName = '[sopimustason rooli, ei urakkaa]'
                    else:
                        cName = '[päättynyt]'

                data_rows.append([cid, cName, cnt])

            # if not data_rows:
            # continue  # jos skippaat millä ei dataa

            data_rows.sort(key=lambda row: row[2], reverse=True)

            columns = ["tunnus", "urakka", "Yhteensä (käyttäjiä)"]
            df = pd.DataFrame(data_rows, columns=columns)

            total_for_role = df["Yhteensä (käyttäjiä)"].sum()
            # all_total += total_for_role

            df = self.collect_dataframe_all(
                df.values,
                h.add_progress_bar_with_text,
                columns,
                total_for_role
            )

            # Roolien määrä (base role)
            roles_count = len(data_rows)
            total_total += total_for_role
            role_table_html = h.generate_role_table(df, columns, total_for_role, roles_count)

            html_all += f"<h2>Rooli: {base_role}</h2>\n"
            html_all += role_table_html
            html_all += "<br/><hr/>\n"

        u.log(f"Käyttäjiä rooleissa: {total_total}")

        return html_all

    def report(self, roles_dict, contract_ids, contract_names):

        # u.debug_role_parsing(roles_dict, contract_ids, contract_names)
        separate_tables_html = self.generate_separate_tables_per_role(roles_dict, contract_ids, contract_names)

        header = h.generate_header(
            " ",
            "Roolit yhteenveto",
            "()"
        )

        # HTML
        self.html_content = header + self.custom_css + separate_tables_html

        # Piechart
        self.html_content = h.piechart(
            roles_dict,
            "Käyttäjäroolit",
            self.html_content,
            chart_title="Assignattu vs. Tyhjät roolit"
        )

        self.html_content += h.generate_footer()
        self.generate()
