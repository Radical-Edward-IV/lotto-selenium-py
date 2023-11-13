### .ipynb 변환
---
`jupyter nbconvert --to script _FILENAME_.ipynb`

### crontab 편집
```
#  _______________ minute (0 - 59)
# |  _______________ hour (0 - 23)
# | |  _______________ day of the month (1 - 31)
# | | |  _______________ month (1 - 12)
# | | | |  _______________ day of the week (0 - 7)
# | | | | |
# * * * * * command to execute

0 21 * * 5 /Users/hello/anaconda3/envs/selenium-with-py/bin/python/Users/edward/Projects/Python/selenium/Lotto.py >> /Users/edward/Projects/Python/selenium/log/crontab_$(date+\%Y\%m\%d).log 2>&1 
 
30 * * * 6 /Users/edward/anaconda3/envs/selenium-with-py/bin/python/Users/edward/Projects/Python/selenium/Lotto.py >> /Users/edward/Projects/Python/selenium/log/crontab_$(date+\%Y\%m\%d).log 2>&1 
```