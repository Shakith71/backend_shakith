from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import mysql.connector
import mysql.connector
from geopy.distance import geodesic
from flask import Flask, render_template
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'yedhukku'
app.permanent_session_lifetime = timedelta(days=1)

def zip_lists(list1, list2):
    return zip(list1, list2)
app.jinja_env.filters['zip_lists'] = zip_lists

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'MOVIE'
}

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(**db_config)

@app.route('/')
def login():
    return render_template('LOGIN.html')

@app.route('/register', methods=['POST'])
def register():
    # Retrieve form data
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    salt = request.form['salt']
    phone = request.form['phone']
    gender = request.form['gender']
    age = request.form['age']
    city = request.form['city']
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (name, email, password, salt, phone, gender, age, city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, (name, email, password, salt, phone, gender, age, city))
    conn.commit()
    cursor.close()
    conn.close()
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
    detail = cursor.fetchall()
    return render_template('LOGIN.html')
    
@app.route('/email_check', methods=['POST'])
def email_check():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        select_query = "SELECT email FROM USERS;"
        cursor.execute(select_query)
        registered_emails = [email[0] for email in cursor.fetchall()]
        return jsonify(registered_emails)
    except Exception as e:
        return str(e), 500  # Return the error message with status code 500

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_email = request.form.get('email')  # Retrieve email from form data
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT salt FROM users WHERE email = %s;", (user_email,))
    salt = cursor.fetchone()  # Fetch single row
    conn.close()
    if salt:
        return salt[0]  # Return salt as response
    else:
        return 'User not found', 404  # Return error message with status code 404

@app.route('/H')
def H():
    return render_template('H.html', name=session.get('name'), email=session.get('email'), phone=session.get('phone'), location=session.get('location'))

@app.route('/check', methods=['POST'])
def check():
    hpe = request.form.get('passwordl')
    user_email = request.form.get('emaill')  # Retrieve email from form data
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s;", (user_email,))
    hps = cursor.fetchone()    
    conn.close()
    h = (hpe, hps)

    if(hpe == hps[0]):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE email = %s;", (user_email,))
        name = cursor.fetchone()
        cursor.execute("SELECT email FROM users WHERE email = %s;", (user_email,))
        email = cursor.fetchone()
        cursor.execute("SELECT phone FROM users WHERE email = %s;", (user_email,))
        phone = cursor.fetchone()
        cursor.execute("SELECT city FROM users WHERE email = %s;", (user_email,))
        city = cursor.fetchone()
        session['name'] = name[0]
        session['email'] = email[0]
        session['phone'] = phone[0]
        session['location'] = city[0]

        name=session.get('name')
        email=session.get('email')
        phone=session.get('phone')
        location=session.get('location')
        detail = (name, email, phone, location)
        return render_template('HOME.html', details = detail)
    else:
        return render_template("LOGIN.html", error = "Invalid Email or Password!")
   
@app.route('/home')
def home():
    name=session.get('name')
    email=session.get('email')
    phone=session.get('phone')
    location=session.get('location')
    detail = (name, email, phone, location)
    return render_template('HOME.html', details = detail)

@app.route('/get_movies')
def get_movies():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies;")
    columns = [col[0] for col in cursor.description]
    movies = []
    for row in cursor.fetchall():
        movie_details = {
            'id' : row[0],
            'title': row[1],
            'genre': row[2],
            'rating': row[3],
            'description': row[4],
            'image': row[5],
            'runtime': row[6],
            'rdate' : row[7],
        }
        movies.append(movie_details)
    return jsonify(movies=movies)

@app.route('/avail_theater/<int:movie_id>', methods=['GET'])
def avail_theater(movie_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    location = session.get('location')
    session['selected_movie'] = movie_id
    sm = session.get('selected_movie')
    theaters_from_database = []
    sql_select_Query =  """
    SELECT DISTINCT t.theater_id, t.theater_name, t.location
    FROM THEATERS t
    JOIN TM tm ON t.theater_id = tm.theater_id
    WHERE tm.movie_id = %s
    """
    cursor.execute(sql_select_Query, (movie_id, ))
    records = cursor.fetchall()

    for record in records:
        theater_id = record[0]
        theater_name = record[1]
        theater_loc = record[2]
        dic = {"id" : theater_id, "name": theater_name, "location": theater_loc}
        theaters_from_database.append(dic)
        
    theaters = [
        {"location": "ANNA NAGAR", "latitude": 13.0878, "longitude": 80.2174},
        {"location": "T. NAGAR", "latitude": 13.0394, "longitude": 80.2337},
        {"location": "ADYAR", "latitude": 13.0064, "longitude": 80.2575},
        {"location": "MYLAPORE", "latitude": 13.0316, "longitude": 80.2670},
        {"location": "NUNGAMBAKKAM", "latitude": 13.0620, "longitude": 80.2405},
        {"location": "ALWARPET", "latitude": 13.0334, "longitude": 80.2546},
        {"location": "EGMORE", "latitude": 13.0827, "longitude": 80.2707},
        {"location": "KILPAUK", "latitude": 13.0827, "longitude": 80.2437},
        {"location": "SAIDAPET", "latitude": 13.0203, "longitude": 80.2224},
        {"location": "VELACHERY", "latitude": 12.9802, "longitude": 80.2228},
        {"location": "GUINDY", "latitude": 13.0067, "longitude": 80.2206},
        {"location": "THIRUVANMIYUR", "latitude": 12.9869, "longitude": 80.2615},
        {"location": "PORUR", "latitude": 13.0324, "longitude": 80.1679},
        {"location": "MOGAPPAIR", "latitude": 13.0832, "longitude": 80.1674},
        {"location": "ANNA SALAI", "latitude": 13.0572, "longitude": 80.2668},
        {"location": "MAMBALAM", "latitude": 13.0355, "longitude": 80.2274},
        {"location": "KODAMBAKKAM", "latitude": 13.0512, "longitude": 80.2206},
        {"location": "MOUNT ROAD", "latitude": 13.0626, "longitude": 80.2696},
        {"location": "PALLIKARANAI", "latitude": 12.9329, "longitude": 80.2135},
        {"location": "ASHOK NAGAR", "latitude": 13.0402, "longitude": 80.2123},
        {"location": "CHROMPET", "latitude": 12.9517, "longitude": 80.1401},
        {"location": "AMBATTUR", "latitude": 13.1075, "longitude": 80.1648},
        {"location": "TAMBARAM", "latitude": 12.9246, "longitude": 80.1479},
        {"location": "VADAPALANI", "latitude": 13.0501, "longitude": 80.2120},
        {"location": "ROYAPETTAH", "latitude": 13.0581, "longitude": 80.2641},
        {"location": "SHOLINGANALLUR", "latitude": 12.8990, "longitude": 80.2279},
        {"location": "AVADI", "latitude": 13.1167, "longitude": 80.1010},  
        {"location": "ENNORE", "latitude": 13.2161, "longitude": 80.3231},  
        {"location": "PALLAVARAM", "latitude": 12.9686, "longitude": 80.1504},
        {"location": "VANAGARAM", "latitude": 13.0733, "longitude": 80.2090},

    ]

    my_theaters = []

    for theater_db in theaters_from_database:
        for theater in theaters:
            if theater['location'] == theater_db['location']:
                my_theater = {
                    "id": theater_db['id'],
                    "name": theater_db['name'],
                    "location": theater['location'],
                    "latitude": theater['latitude'],
                    "longitude": theater['longitude']
                }
                my_theaters.append(my_theater)

    for i in theaters:
        if i['location'] == location:
            location_info = {'latitude': i['latitude'], 'longitude': i['longitude']}


    provided_coords = (location_info['latitude'], location_info['longitude'])
    theaters_with_distances = []

    # Calculate distances from provided location to each theater
    for theater in my_theaters:
        theater_coords = (theater['latitude'], theater['longitude'])
        distance = geodesic(provided_coords, theater_coords).kilometers
        theaters_with_distances.append({"id" : theater['id'], "name": theater['name'],"distance": distance,"location": theater['location']})

    # Sort theaters by distance
    sorted_theaters = sorted(theaters_with_distances, key=lambda x: x['distance'])
    rendering_theaters = []
    for st in sorted_theaters:
        ti = st["id"]
        tn = st["name"]
        tl = st["location"]
        td = st["distance"]
        tup = (ti, tn, tl, int(td))
        rendering_theaters.append(tup)

    # Close database connection
    cursor.close()
    conn.close()

    # Render template to display all theaters
    name=session.get('name')
    email=session.get('email')
    phone=session.get('phone')
    location=session.get('location')
    
    detail = (name, email, phone, location, sm)
    return render_template('PARTIAL_THEATERS.html', theaters=rendering_theaters, details = detail)

@app.route('/all_theaters')
def theaters():
    location = session.get('location')
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()
    theaters_from_database = []
    sql_select_Query = "SELECT * FROM THEATERS"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    for record in records:
        theater_id = record[0]
        theater_name = record[1]
        theater_loc = record[2]
        dic = {"id" : theater_id, "name": theater_name, "location": theater_loc}
        theaters_from_database.append(dic)
        
    theaters = [
        {"location": "ANNA NAGAR", "latitude": 13.0878, "longitude": 80.2174},
        {"location": "T. NAGAR", "latitude": 13.0394, "longitude": 80.2337},
        {"location": "ADYAR", "latitude": 13.0064, "longitude": 80.2575},
        {"location": "MYLAPORE", "latitude": 13.0316, "longitude": 80.2670},
        {"location": "NUNGAMBAKKAM", "latitude": 13.0620, "longitude": 80.2405},
        {"location": "ALWARPET", "latitude": 13.0334, "longitude": 80.2546},
        {"location": "EGMORE", "latitude": 13.0827, "longitude": 80.2707},
        {"location": "KILPAUK", "latitude": 13.0827, "longitude": 80.2437},
        {"location": "SAIDAPET", "latitude": 13.0203, "longitude": 80.2224},
        {"location": "VELACHERY", "latitude": 12.9802, "longitude": 80.2228},
        {"location": "GUINDY", "latitude": 13.0067, "longitude": 80.2206},
        {"location": "THIRUVANMIYUR", "latitude": 12.9869, "longitude": 80.2615},
        {"location": "PORUR", "latitude": 13.0324, "longitude": 80.1679},
        {"location": "MOGAPPAIR", "latitude": 13.0832, "longitude": 80.1674},
        {"location": "ANNA SALAI", "latitude": 13.0572, "longitude": 80.2668},
        {"location": "MAMBALAM", "latitude": 13.0355, "longitude": 80.2274},
        {"location": "KODAMBAKKAM", "latitude": 13.0512, "longitude": 80.2206},
        {"location": "MOUNT ROAD", "latitude": 13.0626, "longitude": 80.2696},
        {"location": "PALLIKARANAI", "latitude": 12.9329, "longitude": 80.2135},
        {"location": "ASHOK NAGAR", "latitude": 13.0402, "longitude": 80.2123},
        {"location": "CHROMPET", "latitude": 12.9517, "longitude": 80.1401},
        {"location": "AMBATTUR", "latitude": 13.1075, "longitude": 80.1648},
        {"location": "TAMBARAM", "latitude": 12.9246, "longitude": 80.1479},
        {"location": "VADAPALANI", "latitude": 13.0501, "longitude": 80.2120},
        {"location": "ROYAPETTAH", "latitude": 13.0581, "longitude": 80.2641},
        {"location": "SHOLINGANALLUR", "latitude": 12.8990, "longitude": 80.2279},
        {"location": "AVADI", "latitude": 13.1167, "longitude": 80.1010},  
        {"location": "ENNORE", "latitude": 13.2161, "longitude": 80.3231},  
        {"location": "PALLAVARAM", "latitude": 12.9686, "longitude": 80.1504},
        {"location": "VANAGARAM", "latitude": 13.0733, "longitude": 80.2090},

    ]


    my_theaters = []

    for theater_db in theaters_from_database:
        for theater in theaters:
            if theater['location'] == theater_db['location']:
                my_theater = {
                    "id": theater_db['id'],
                    "name": theater_db['name'],
                    "location": theater['location'],
                    "latitude": theater['latitude'],
                    "longitude": theater['longitude']
                }
                my_theaters.append(my_theater)


    for i in theaters:
        if(i['location'] == location):
            location_info = {'latitude' : i['latitude'], 'longitude' : i['longitude']}

    provided_coords = (location_info['latitude'], location_info['longitude'])
    theaters_with_distances = []

    # Calculate distances from provided location to each theater
    for theater in my_theaters:
        theater_coords = (theater['latitude'], theater['longitude'])
        distance = geodesic(provided_coords, theater_coords).kilometers
        theaters_with_distances.append({"id": theater['id'], "name": theater['name'], "distance": distance, "location": theater['location']})

    # Sort theaters by distance
    sorted_theaters = sorted(theaters_with_distances, key=lambda x: x['distance'])
    rendering_theaters = []
    for st in sorted_theaters:
        ti = st["id"]
        tn = st["name"]
        tl = st["location"]
        td = st["distance"]
        tup = (ti, tn, tl, int(td))
        rendering_theaters.append(tup)

    # Close database connection
    cursor.close()
    conn.close()
    name=session.get('name')
    email=session.get('email')
    phone=session.get('phone')
    location=session.get('location')
    detail = (name, email, phone, location)
    # Render template to display all theaters
    return render_template('ALL_THEATERS.html', theaters=rendering_theaters, details = detail)

@app.route('/avail_movies/<int:theater_id>', methods=['GET'])
def avail_movies(theater_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql_select_Query = """SELECT DISTINCT m.movie_id, m.movie_name, m.genre, m.rating, m.description, m.url, m.run_time, m.rdate 
                   FROM MOVIES m JOIN TM tm 
                   ON m.movie_id = tm.movie_id WHERE tm.theater_id = %s;"""
    cursor.execute(sql_select_Query, (theater_id, ))
    movie = cursor.fetchall()
    cursor.close()
    conn.close()

    name=session.get('name')
    email=session.get('email')
    phone=session.get('phone')
    location=session.get('location')
    detail = (name, email, phone, location, theater_id)
    return render_template('PARTIAL_MOVIES.html', details = detail, movies = movie)

@app.route('/all_movies')
def all_movies():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM MOVIES;""")
    movie = cursor.fetchall()
    cursor.close()
    conn.close()

    name=session.get('name')
    email=session.get('email')
    phone=session.get('phone')
    location=session.get('location')
    detail = (name, email, phone, location)

    return render_template('ALL_MOVIES.html', details = detail, movies = movie)

theater_id_variable = 0
@app.route('/mt_movies/<int:theater_id>')
def mt_movies(theater_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    global theater_id_variable
    theater_id_variable = theater_id
    today = '2024-05-11'
    tomorrow = '2024-05-12'

    cursor.execute("""
        SELECT MOVIES.MOVIE_ID, MOVIES.MOVIE_NAME, MOVIES.GENRE, MOVIES.RATING, MOVIES.DESCRIPTION,
               MOVIES.URL, MOVIES.RUN_TIME, 
               GROUP_CONCAT(TM.SCREEN_ID SEPARATOR ',') AS Screens,
               GROUP_CONCAT(TM.SHOW_TIME SEPARATOR ',') AS Times
        FROM MOVIES
        JOIN TM ON TM.MOVIE_ID = MOVIES.MOVIE_ID
        JOIN THEATERS ON TM.THEATER_ID = THEATERS.THEATER_ID
        WHERE THEATERS.THEATER_ID = %s AND TM.SHOW_DATE = %s
        GROUP BY MOVIES.MOVIE_ID;
    """, (theater_id, today, ))
    today_movies = cursor.fetchall()

    cursor.execute("""
        SELECT MOVIES.MOVIE_ID, MOVIES.MOVIE_NAME, MOVIES.GENRE, MOVIES.RATING, MOVIES.DESCRIPTION,
               MOVIES.URL, MOVIES.RUN_TIME, 
               GROUP_CONCAT(TM.SCREEN_ID SEPARATOR ',') AS Screens,
               GROUP_CONCAT(TM.SHOW_TIME SEPARATOR ',') AS Times
        FROM MOVIES
        JOIN TM ON TM.MOVIE_ID = MOVIES.MOVIE_ID
        JOIN THEATERS ON TM.THEATER_ID = THEATERS.THEATER_ID
        WHERE THEATERS.THEATER_ID = %s AND TM.SHOW_DATE = %s
        GROUP BY MOVIES.MOVIE_ID;
    """, (theater_id, tomorrow))
    tomorrow_movies = cursor.fetchall()

    cursor.close()
    conn.close()

    name = session.get('name')
    email = session.get('email')
    phone = session.get('phone')
    location = session.get('location')
    m = session.get('selected_movie')
    detail = (name, email, phone, location, m)

    return render_template('MOVIES.html', today_movies=today_movies, tomorrow_movies=tomorrow_movies, details=detail)

theater_id_variable = 0
@app.route('/tm_movies/<int:theater_id>/<int:movie_id>')
def tm_movies(theater_id, movie_id): 
    conn = connect_to_database()
    cursor = conn.cursor()
    global theater_id_variable
    theater_id_variable = theater_id
    today = '2024-05-11'
    tomorrow = '2024-05-12'

    cursor.execute("""
        SELECT MOVIES.MOVIE_ID, MOVIES.MOVIE_NAME, MOVIES.GENRE, MOVIES.RATING, MOVIES.DESCRIPTION,
               MOVIES.URL, MOVIES.RUN_TIME, 
               GROUP_CONCAT(TM.SCREEN_ID SEPARATOR ',') AS Screens,
               GROUP_CONCAT(TM.SHOW_TIME SEPARATOR ',') AS Times
        FROM MOVIES
        JOIN TM ON TM.MOVIE_ID = MOVIES.MOVIE_ID
        JOIN THEATERS ON TM.THEATER_ID = THEATERS.THEATER_ID
        WHERE THEATERS.THEATER_ID = %s AND TM.SHOW_DATE = %s
        GROUP BY MOVIES.MOVIE_ID;
    """, (theater_id, today, ))
    today_movies = cursor.fetchall()

    cursor.execute("""
        SELECT MOVIES.MOVIE_ID, MOVIES.MOVIE_NAME, MOVIES.GENRE, MOVIES.RATING, MOVIES.DESCRIPTION,
               MOVIES.URL, MOVIES.RUN_TIME, 
               GROUP_CONCAT(TM.SCREEN_ID SEPARATOR ',') AS Screens,
               GROUP_CONCAT(TM.SHOW_TIME SEPARATOR ',') AS Times
        FROM MOVIES
        JOIN TM ON TM.MOVIE_ID = MOVIES.MOVIE_ID
        JOIN THEATERS ON TM.THEATER_ID = THEATERS.THEATER_ID
        WHERE THEATERS.THEATER_ID = %s AND TM.SHOW_DATE = %s
        GROUP BY MOVIES.MOVIE_ID;
    """, (theater_id, tomorrow))
    tomorrow_movies = cursor.fetchall()

    cursor.close()
    conn.close()

    name = session.get('name')
    email = session.get('email')
    phone = session.get('phone')
    location = session.get('location')
    m = movie_id
    detail = (name, email, phone, location, m)

    return render_template('MOVIES.html', today_movies=today_movies, tomorrow_movies=tomorrow_movies, details=detail)



@app.route('/bookings/<int:movie_id>/<int:screen_id>/<string:time>')
def booking(movie_id, screen_id, time):
    # You can perform additional logic here if needed
    ti = theater_id_variable
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("""SELECT ELITE_SEATS, PREMIUM_SEATS FROM SCREENS WHERE THEATER_ID = %s AND SCREEN_ID = %s;""", (ti, screen_id,))
    seats = cursor.fetchall()
    return render_template('BOOKINGS.html', theater_id=ti, movie_id=movie_id, screen_id=screen_id, time=time, seats=seats)

if __name__ == '__main__':
    app.run(debug=True)
    app.debug = True
