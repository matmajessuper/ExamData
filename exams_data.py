import argparse
from database_setup import DBapi, Row


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
        # get all expected values of territory, year, and sex and put it to arrays

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
        # calculate passing percentage of given territory in given year

        if not self.sex_filter:  # check if filter is used
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
        # compares passing percentage of two territories in all years

        if not self.validate_input(territory=territory1) or not self.validate_input(territory=territory2):
            print("Error: bad arguments, choose between:")
            print(self.territory_array)
            return

        print("This territory had better passing percentage in year")

        for year in self.year_array:
            per1 = self.calculate_percentage(territory1, year)
            per2 = self.calculate_percentage(territory2, year)
            if per1 is False or per2 is False:
                return
            elif per1 > per2:
                print(str(year) + " - " + territory1)
            else:
                print(str(year) + " - " + territory2)

    def detect_regression(self):
        # detects which territories had regression in passing exams

        print("These territories had regression in passing exams in year:")

        for territory in self.territory_array:
            for year in self.year_array[1::]:
                p1 = self.calculate_percentage(territory, year-1)
                p2 = self.calculate_percentage(territory, year)
                if p1 > p2:
                    print(territory + " " + str(year-1) + " -> " + str(year))  # + " " + str(p1) + " -> " + str(p2))

    def mean_values(self, territory, year):
        # calculates mean values of students attending exams in given territory from 2010 to given year

        if not self.validate_input(territory=territory, year=year):
            print("Error: bad arguments, choose between:")
            print(self.territory_array)
            print(self.year_array)
            return

        endYear = year
        currentYear = self.year_array[0]
        students = []

        while currentYear <= endYear:
            if not self.sex_filter:  # check if filter is used
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

        print("Mean value of students attending exams in " + territory)
        if endYear != self.year_array[0]:
            print(str(self.year_array[0]) + " - " + str(endYear) + "  " + str(mean))
        else:
            print(str(endYear) + "  " + str(mean))

    def passing_percentage(self, territory):
        # calculates passing percentage of given territory

        if not self.validate_input(territory=territory):
            print("Error: bad arguments, choose between:")
            print(self.territory_array)
            return

        print("Passing percentage of " + territory)

        for year in self.year_array:
            percentage = self.calculate_percentage(territory, year)
            print(str(year) + " - " + str(percentage) + "%")

    def best_in_year(self, year):
        # check which territory had best passing percentage in given year

        if not self.validate_input(year=year):
            print("Error: bad arguments, choose between:")
            print(self.year_array)
            return

        best = {'territory': "", 'percentage': 0}
        for territory in self.territory_array:
            if territory != "Polska":
                percentage = self.calculate_percentage(territory, year)
                if percentage > best['percentage']:
                    best['territory'] = territory
                    best['percentage'] = percentage

        print("Best passing percentage had:")
        print(str(year) + " - " + best['territory'] + " " + str(best['percentage']) + "%")

    def validate_input(self, territory=None, year=None):
        # check whether input is valid, default values None, because not every function takes both arguments

        if territory and territory not in self.territory_array:
            return False
        if year and year not in self.year_array:
            return False
        return True


if __name__ == "__main__":
    parser = Parser()

    if parser.args.get_data:  # don't create Exams object, until there is no data in database
        handler = DBapi()
        handler.create_tables()
        handler.request_and_insert_data()
    else:
        ex = Exams()

        if parser.args.filter:  # first check filters independently from rest
            if parser.args.filter in ex.sex_array:
                ex.sex_filter = parser.args.filter
            else:
                print("Error: bad filter, choose between: ")
                print(ex.sex_array)
        if parser.args.mean:
            terr, year = parser.args.mean
            ex.mean_values(str(terr), int(year))
        elif parser.args.passing_percentage:
            ex.passing_percentage(parser.args.passing_percentage)
        elif parser.args.best_in_year:
            ex.best_in_year(parser.args.best_in_year)
        elif parser.args.regression:
            ex.detect_regression()
        elif parser.args.compare:
            terr1, terr2 = parser.args.compare
            ex.compare(terr1, terr2)
        else:
            print("Error: bad arguments")












