import pytest
from exams_data import Exams
from database_setup import DBapi


class TestExams(object):

    def test_table_creation(self):
        db_handler = DBapi("test1.db")
        db_handler.create_tables()
        result = db_handler.select_data("""SELECT name from sqlite_master where type= \"table\"""")
        assert ('exam_data',) in result
        db_handler.select_data("""drop table exam_data;""")
        result = db_handler.select_data("""SELECT name from sqlite_master where type= \"table\"""")
        assert ('exam_data',) not in result

    def test_data_insertion(self):
        db_handler = DBapi("test2.db")
        db_handler.create_tables()
        data = [("test1", "test2", "test3", 1, 1,),
                ("test2", "test2", "test2", 2, 2,)]
        db_handler.insert_data(data)
        result = db_handler.select_data("""select territory, passed_attended, sex, year, people_number from exam_data;""")
        assert data == result
        db_handler.select_data("""drop table exam_data;""")

    def test_acquire_values(self):
        ex = Exams()
        ex.acquire_values()
        territories = ["Zachodniopomorskie", "Wielkopolskie", "Warmińsko-Mazurskie", "Świętokrzyskie", "Śląskie",
                       "Pomorskie", "Podlaskie", "Podkarpackie", "Opolskie", "Mazowieckie", "Małopolskie", "Łódzkie",
                       "Lubuskie", "Lubelskie", "Kujawsko-pomorskie", "Dolnośląskie", "Polska"]
        assert set(territories) == set(ex.territory_array)

    def test_calculate_percentage(self):
        ex = Exams()
        result = ex.calculate_percentage("Polska", 2018)
        assert int(result) == 79  # changed to int to avoid floats comparison

    def test_compare(self, capsys):
        ex = Exams()
        ex.compare("Wielkopolskie", "Pomorskie")
        captured = capsys.readouterr()
        assert captured.out == "2010 - Pomorskie\n2011 - Wielkopolskie\n2012 - Pomorskie\n2013 - Pomorskie\n2014 " \
                               "- Pomorskie\n2015 - Pomorskie\n2016 - Pomorskie\n2017 - Pomorskie\n2018 - Wielkopolskie\n"

    def test_detect_regression(self, capsys):
        ex = Exams()
        ex.detect_regression()
        captured = capsys.readouterr()
        assert captured.out == "Dolnośląskie 2010 -> 2011\nDolnośląskie 2013 -> 2014\nDolnośląskie 2016 -> " \
                               "2017\nKujawsko-pomorskie 2010 -> 2011\nKujawsko-pomorskie 2013 -> " \
                               "2014\nKujawsko-pomorskie 2016 -> 2017\nLubelskie 2010 -> 2011\nLubelskie 2013 -> " \
                               "2014\nLubelskie 2016 -> 2017\nLubuskie 2010 -> 2011\nLubuskie 2013 -> 2014\nLubuskie " \
                               "2016 -> 2017\nLubuskie 2017 -> 2018\nŁódzkie 2010 -> 2011\nŁódzkie 2013 -> " \
                               "2014\nŁódzkie 2016 -> 2017\nŁódzkie 2017 -> 2018\nMałopolskie 2010 -> 2011\nMałopolskie " \
                               "2013 -> 2014\nMazowieckie 2010 -> 2011\nMazowieckie 2013 -> 2014\nMazowieckie 2016 -> " \
                               "2017\nOpolskie 2010 -> 2011\nOpolskie 2013 -> 2014\nOpolskie 2016 -> 2017\nPodkarpackie " \
                               "2010 -> 2011\nPodkarpackie 2013 -> 2014\nPodkarpackie 2016 -> 2017\nPodlaskie 2010 -> " \
                               "2011\nPodlaskie 2013 -> 2014\nPodlaskie 2016 -> 2017\nPomorskie 2010 -> 2011\nPomorskie " \
                               "2013 -> 2014\nPomorskie 2016 -> 2017\nPomorskie 2017 -> 2018\nŚląskie 2010 -> " \
                               "2011\nŚląskie 2013 -> 2014\nŚląskie 2016 -> 2017\nŚwiętokrzyskie 2010 -> " \
                               "2011\nŚwiętokrzyskie 2013 -> 2014\nŚwiętokrzyskie 2016 -> 2017\nWarmińsko-Mazurskie " \
                               "2010 -> 2011\nWarmińsko-Mazurskie 2013 -> 2014\nWarmińsko-Mazurskie 2016 -> " \
                               "2017\nWielkopolskie 2010 -> 2011\nWielkopolskie 2013 -> 2014\nWielkopolskie 2016 -> " \
                               "2017\nZachodniopomorskie 2010 -> 2011\nZachodniopomorskie 2013 -> " \
                               "2014\nZachodniopomorskie 2016 -> 2017\n"

    def test_mean_values(self, capsys):
        ex = Exams()
        ex.mean_values("Mazowieckie", 2018)
        captured = capsys.readouterr()
        assert captured.out == "2010 - 2018  42462.444444444445\n"

    def test_percentage_passing(self, capsys):
        ex = Exams()
        ex.percentage_passing("Opolskie")
        captured = capsys.readouterr()
        assert captured.out == "2010 - 81.9641888225719%\n2011 - 74.93624772313296%\n2012 - 79.80964467005076%\n2013 " \
                               "- 80.80194410692589%\n2014 - 69.85218791160544%\n2015 - 75.43914680050187%\n2016 " \
                               "- 79.2014400261823%\n2017 - 77.6148904628562%\n2018 - 78.36962389778658%\n"

    def test_best_in_year(self, capsys):
        ex = Exams()
        ex.best_in_year(2013)
        captured = capsys.readouterr()
        assert captured.out == "2013 - wojewodztwo Małopolskie 83.5366055197488%\n"





