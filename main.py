from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class CityTemperature(db.Model):
    """
    class CityTemperature to represent the temperature in
    city at te beginning of each month
    """
    id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.Date)
    avg_temperature = db.Column(db.Float)
    avg_temperature_uncertainty = db.Column(db.Float)
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))

    def __init__(self, dt, avg_temperature, avg_temperature_uncertainty, city, country, latitude, longitude):
        """
        Constructs all the necessary attributes for CityTemperature object.
        :param dt: date
        :param avg_temperature: the average temperature
        :param avg_temperature_uncertainty: the average temperature uncertainty
        :param city: the city
        :param country: the country
        :param latitude: coordinates latitude
        :param longitude: coordinates longitude
        """
        self.dt = dt
        self.avg_temperature = avg_temperature
        self.avg_temperature_uncertainty = avg_temperature_uncertainty
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude


@app.route('/')
def index():
    """
    loading data from database and using html template to visualize it
    limiting the number here to 100 is one of the points to improve by
    either using different web framework or different approach
    index.html contain table where data is loaded and two buttons add and edit
    """
    all_data = CityTemperature.query.limit(100).all()
    return render_template("index.html", cite_temp=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    """
    when clicking the add button a pop-up form is called
    after adding needed info and insert request  is called
    """
    if request.method == 'POST':
        dt = request.form['dt']
        avg_temperature = request.form['avg_temperature']
        avg_temperature_uncertainty = request.form['avg_temperature_uncertainty']
        city = request.form['city']
        country = request.form['country']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        my_data = CityTemperature(dt,
                                  avg_temperature,
                                  avg_temperature_uncertainty,
                                  city,
                                  country,
                                  latitude,
                                  longitude)
        db.session.add(my_data)
        db.session.commit()

        flash("New Row Added")
        return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """
    when clicking the update button a pop-up form is called
    there was a problem when using date, city and country as primary keys
    since some cities in the same country had different coordinates
    so in this case an id is added but this is another problem to fix
    so in this case we update the entry by id
    """
    if request.method == 'POST':
        id = request.form.get('id')
        date = request.form.get('dt')
        city = request.form.get('city')
        my_data = CityTemperature.query.get({"id": id})

        my_data.avg_temperature = request.form['avg_temperature']
        my_data.avg_temperature_uncertainty = request.form['avg_temperature_uncertainty']

        db.session.commit()

        flash("Row updated")
        return redirect(url_for('index'))


@app.route('/top_list', methods=['GET', 'POST'])
def get_top_list():
    """
    to visualize the top N cities that have the highest monthly AverageTemperature
    /top_list endpoint is called using the template top_list
    by using the date pickers we can select a date range
    then get_top_list make select query to db
    since the date picker not working properly , the date in this case are hardcoded
    """
    start = '2000-01-01'
    end = '2013-09-01'
    sql = '''
        select EXTRACT(year from dt) as year, city, country, latitude, longitude, max(avg_temperature) as h_m_avg
        from city_temperature
        where dt >= '{}'
        and dt <= '{}'
        group by 1, 2, 3, 4, 5
        order by h_m_avg desc, year, city
        limit 10
        '''.format(start, end)
    result = db.engine.execute(sql)
    return render_template("top_list.html", top_city_temp=result)


if __name__ == "__main__":
    app.run(debug=True)
