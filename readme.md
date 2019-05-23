# Exams statistics
- download project from github
```sh
git clone https://github.com/matmajessuper/Exams.git
```
- create virtualenv

Available commands:
- mean value of students attending exam in given territory from 2010 to given year
```
--mean [TERRITORY] [YEAR]
```
- passing percentage of given territory over years
```
--pass_percentage [TERRITORY]
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
- downloads data and uploads to database "data.db"
```
--get_data
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

Available years:
- 2010 - 2018

Available sex:
- mężczyźni
- kobiety