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
kafka = kf.KafkaClient("localhost:9099,localhost:9092,localhost:9093")
producer = kf.SimpleProducer(kafka)

## Find popular movies for the day
movie = tm.Movie()
popular = movie.popular()

## Create dict of the relevant information
for p in popular:
    movie_data = {}
    m = movie.details(p.id)
    movie_data['adult'] = m.adult
    movie_data['budget'] = m.budget
    movie_data['genres'] = m.genres #dict
    movie_data['id'] = m.id
    movie_data['original_language'] = m.original_language
    movie_data['popularity'] = m.popularity
    movie_data['production_companies'] = m.production_companies #dict
    movie_data['production_countries'] = m.production_countries #dict
    movie_data['release_date'] = m.release_date
    movie_data['revenue'] = m.revenue
    movie_data['runtime'] = m.runtime
    movie_data['spoken_languages'] = m.spoken_languages #dict
    movie_data['status'] = m.status
    movie_data['title'] = m.title
    movie_data['vote_average'] = m.vote_average
    movie_data['vote_count'] = m.vote_count
    ## Send data to Kafka brokers as json
    producer.send_messages("capstone", bytes(json.dumps(movie_data), 'utf-8'))
