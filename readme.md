# Exams statistics
- download project from github
```sh
git clone https://github.com/matmajessuper/Exams.git
```
- create virtualenv

- install required packages
```
pip install -r requirements.txt
```
- download data and upload to database "data.db"
```
python exams_data.py --get_data
```
- run script
```
python exams_data.py [OPTION] [FILTER]
```

with one of available options:
- mean value of students attending exam in given territory from 2010 to given year
```
--mean [TERRITORY] [YEAR]
```
- passing percentage of given territory over years
```
--passing_percentage [TERRITORY]
```
- territory with best passing percentage in given year
```
--best_in_year [YEAR]
```
- detect territory with regression in following year
```
--regression
```
- compares two territories, which one had better passing percentage over the years
```
--compare [TERRITORY1] [TERRITORY2]
```
- optional filter by sex, default for both
```
--filter [SEX]
```

Available territories:
- Zachodniopomorskie
- Wielkopolskie
- Warmińsko-Mazurskie
- Świętokrzyskie
- Śląskie
- Pomorskie
- Podlaskie
- Podkarpackie
- Opolskie
- Mazowieckie
- Małopolskie
- Łódzkie
- Lubuskie
- Lubelskie
- Kujawsko-pomorskie
- Dolnośląskie
- Polska

Available years:
- 2010 - 2018

Available filters:
- mężczyźni
- kobiety

To run test:
```
py.test tests.py
```