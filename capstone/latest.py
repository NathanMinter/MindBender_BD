import json
import kafka as kf
import tmdbv3api as tm

## Set auth keys
with open('/home/n/opt/MindBender_BD/Misc/keys') as keys:
    tmdb_keys = json.load(keys)
    api_key = tmdb_keys["tmdb"]["api_key"]
    read_access_token = tmdb_keys["tmdb"]["read_access_token"]
tmdb = tm.TMDb()
tmdb.api_key = api_key

## Connect to Kafka brokers
kafka = kf.KafkaClient("localhost:9099")
producer = kf.SimpleProducer(kafka)

## Find popular movies for the day
movie = tm.Movie()
latest = movie.latest()

with open('/home/n/opt/MindBender_BD/capstone/latest.txt', 'r') as l:
    movie_id = int(l.read())

for x in range(movie_id,latest.id):
    try:
        ## Select details for latest film to send to Kafka broker
        movie_data = {}
        m = movie.details(x)
        movie_data['adult'] = m.adult
        movie_data['budget'] = m.budget
        ## Select first genre from list (most important)
        try:
            movie_data['genres'] = m.genres[0]['name']
        except:
            movie_data['genres'] = dict(m.genres).get('name')
        movie_data['id'] = m.id
        movie_data['original_language'] = m.original_language
        movie_data['popularity'] = m.popularity
        ## Select first company from list (most important)
        try:
            movie_data['production_companies'] = m.production_companies[0]['name']
        except:
            movie_data['production_companies'] = dict(m.production_companies).get('name')
        ## Select first country from list (most important)
        try:
            movie_data['production_countries'] = m.production_countries[0]['name']
        except:
            movie_data['production_countries'] = dict(m.production_countries).get('name')
        movie_data['release_date'] = m.release_date
        movie_data['revenue'] = m.revenue
        movie_data['runtime'] = m.runtime
        ## Select first language from list (most important)
        try:
            movie_data['spoken_languages'] = m.spoken_languages[0]['name']
        except:
            movie_data['spoken_languages'] = dict(m.spoken_languages).get('name')
        movie_data['status'] = m.status
        movie_data['title'] = m.title
        movie_data['vote_average'] = m.vote_average
        movie_data['vote_count'] = m.vote_count

        ## Send data to Kafka brokers as json
        producer.send_messages("capstone", bytes(json.dumps(movie_data), 'utf-8'))
    except:
        print("No movie with ID: {}".format(x))

## Re-write latest.txt
with open("/home/n/opt/MindBender_BD/capstone/latest.txt", "w+") as l:
    l.write(str(latest.id))
