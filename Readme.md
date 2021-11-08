### Task

###### Technologies choice:
- python web Framework Flask: since it is lightweight framework to create efficient and reliable web applications.
- jinja2
- postgres 

###### Steps
To create the Table in the DB
- in python shell:


    from main import db
    db.create_all()

Then Run load_csv.py to populate the table from the csv file

after the creation of the table we can run main.py to visualise the data 

###### Encoutered problems
- Some cities had different longitude and latitude so using
city, country and date a primary keys was not possible before 
fixing this data issue
- also, there were missing values for avg_temperature and avg_temperature_uncertainty so
for now it was filled by the previous row but could and avg by city and year is better option to fill

- date pickers not working

###### Time used for coding:
a working day ≈ 9 hours

##### Examples
a) Query
    
    select city, country, max(avg_temperature) as maxi
    from public.city_temperature
    where EXTRACT(year from dt) >= 2000
    group by city, country
    order by maxi desc, city, country)

Result : we can see that the entry 


![](/Images/scr1.png?raw=true)


b) Creating new entry
![](/Images/scr2.png?raw=true)

![](/Images/scr3.png?raw=true)

we can see the insert in db
![](/Images/scr4.png?raw=true)

c) we need to provide an id 
![](/Images/scr5.png?raw=true)

![](/Images/scr6.png?raw=true)

![](/Images/scr7.png?raw=true)