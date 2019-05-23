import argparse
from database_setup import DBapi, Row
import pytest


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("--mean",
                                 nargs=2,
                                 help="returns mean value of students attending exams in given territory from 2010 to "
                                      "given year")
        self.parser.add_argument("--passing_percentage",
                                 help="returns percentage of students, which passed exams in given "
                                      "territory over the years")
        self.parser.add_argument("--best_in_year",
                                 help="returns territory with the best passing percentage in given year",
                                 type=int)
        self.parser.add_argument("--regression",
                                 help="detect regression of passing percentage",
                                 action='store_true')
        self.parser.add_argument("--compare",
                                 help="compares two territories, which had better passing percentage over the "
                                      "years",
                                 nargs=2)
        self.parser.add_argument("--filter",
                                 help="filter results by sex, default results are for both")
        self.parser.add_argument("--get_data",
                                 help="Download data and saves in given database",
                                 action='store_true')
        self.args = self.parser.parse_args()


class Exams:
    def __init__(self):
        self.handler = DBapi()
        self.territory_array = []
        self.passed_attended_array = []
        self.sex_array = []
        self.year_array = []
        self.acquire_values()
        self.sex_filter = ""

    def acquire_values(self):
        query = """select * from exam_data"""
        rows = self.handler.select_data(query)

        for row in rows:
            r = Row(row[1::])

            if r.territory not in self.territory_array:
                self.territory_array.append(r.territory)
            if r.passed_attended not in self.passed_attended_array:
                self.passed_attended_array.append(r.passed_attended)
            if r.sex not in self.sex_array:
                self.sex_array.append(r.sex)
            if r.year not in self.year_array:
                self.year_array.append(r.year)

    def calculate_percentage(self, territory, year):
        if territory not in self.territory_array or year not in self.year_array:
            print("Error: bad arguments")
            return
        if not self.sex_filter:
            query = """select * from exam_data where territory=(?) and year=(?)"""
            dataset = (territory, year,)
        else:
            query = """select * from exam_data where territory=(?) and year=(?) and sex=(?)"""
            dataset = (territory, year, self.sex_filter)
        rows = self.handler.select_data(query, dataset)
        data = []
        for row in rows:
            r = Row(row[1::])
            data.append(r)
        passed = 0
        attended = 0
        for r in data:
            if r.passed_attended == "zdało":
                passed += r.people_number
            elif r.passed_attended == "przystąpiło":
                attended += r.people_number
        return passed / attended * 100

    def compare(self, territory1, territory2):
        for year in self.year_array:
            if self.calculate_percentage(territory1, year) > self.calculate_percentage(territory2, year):
                print(str(year) + " - " + territory1)
            else:
                print(str(year) + " - " + territory2)

    def detect_regression(self):
        for territory in self.territory_array:
            if territory != "Polska":
                for year in self.year_array[1::]:
                    p1 = self.calculate_percentage(territory, year-1)
                    p2 = self.calculate_percentage(territory, year)
                    if p1 > p2:
                        print(territory + " " + str(year-1) + " -> " + str(year))  # + " " + str(p1) + " -> " + str(p2))

    def mean_values(self, territory, year):
        if territory not in self.territory_array or year not in self.year_array:
            print("Error: bad arguments")
            return
        endYear = year
        currentYear = self.year_array[0]
        students = []

        while currentYear <= endYear:
            if not self.sex_filter:
                query = """select people_number from exam_data where territory=(?) and year=(?) and passed_attended=\"przystąpiło\""""
                dataset = (territory, currentYear,)
            else:
                query = """select people_number from exam_data where territory=(?) and year=(?) and passed_attended=\"przystąpiło\" and sex=(?)"""
                dataset = (territory, currentYear, self.sex_filter,)
            rows = self.handler.select_data(query, dataset)
            all_students = 0
            for row in rows:
                all_students += row[0]
            students.append(all_students)
            currentYear += 1
        mean = sum(students) / len(students)

        if endYear != self.year_array[0]:
            print(str(self.year_array[0]) + " - " + str(endYear) + "  " + str(mean))
        else:
            print(str(endYear) + "  " + str(mean))

    def percentage_passing(self, territory):
        for year in self.year_array:
            percentage = self.calculate_percentage(territory, year)
            print(str(year) + " - " + str(percentage) + "%")

    def best_in_year(self, year):
        best = {'territory': "", 'percentage': 0}
        for territory in self.territory_array:
            if territory != "Polska":
                percentage = self.calculate_percentage(territory, year)
                if percentage > best['percentage']:
                    best['territory'] = territory
                    best['percentage'] = percentage
        print(str(year) + " - wojewodztwo " + best['territory'] + " " + str(best['percentage']) + "%")


if __name__ == "__main__":
    parser = Parser()

    if parser.args.get_data:
        handler = DBapi()
        handler.create_tables()
        handler.request_and_insert_data()
    else:
        ex = Exams()

        if parser.args.filter:
            ex.sex_filter = parser.args.filter
        if parser.args.mean:
            terr, year = parser.args.mean
            ex.mean_values(str(terr), int(year))
        elif parser.args.passing_percentage:
            ex.percentage_passing(parser.args.passing_percentage)
        elif parser.args.best_in_year:
            ex.best_in_year(parser.args.best_in_year)
        elif parser.args.regression:
            ex.detect_regression()
        elif parser.args.compare:
            terr1, terr2 = parser.args.compare
            ex.compare(terr1, terr2)
        else:
            print("Error: bad arguments")












