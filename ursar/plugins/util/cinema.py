from ursar.plugin import UrsarPlugin
from ursar.decorators import respond_to

import requests
from datetime import datetime
from fuzzywuzzy import process

CINEMAS = {
    'Arad Atrium': 1808,
    'Bacau': 1804,
    'Baia Mare': 1809,
    'Braila': 1810,
    'Bucuresti AFI Cotroceni': 1806,
    'Bucuresti Mega Mall': 1818,
    'Bucuresti Park Lake': 1824,
    'Bucuresti Sun Plaza': 1807,
    'Cluj Iulius Mall': 1803,
    'Cluj VIVO': 1815,
    'Constanta City Park': 1819,
    'Constanta VIVO': 1813,
    'Deva': 1820,
    'Drobeta Turnu Severin': 1821,
    'Galati': 1826,
    'Iasi Iulius Mall': 1801,
    'Piatra Neamt': 1825,
    'Pitesti VIVO': 1805,
    'Ploiesti AFI': 1816,
    'Ploiesti Shopping City': 1814,
    'Suceava': 1822,
    'Targu Jiu': 1817,
    'Targu Mures': 1812,
    'Timisoara Iulius Mall': 1802,
    'Timisoara Shopping City': 1823
}

BASE_URL = 'https://www.cinemacity.ro'

class CinemaPlugin(UrsarPlugin):

    @respond_to('^(cinema|movies|filme) ((in|la|for) )?(?P<cinema>.*?)(?: ((on|pe) )?(?P<date>\d{4}-\d{1,2}-\d{1,2}))?$')
    def movies(self, message, cinema, date=datetime.now().strftime('%Y-%m-%d')):
        cinema_name, cinema_id = self.get_cinema(cinema)

        url = '/ro/data-api-service/v1/quickbook/{country}/film-events/in-cinema/{cinema}/at-date/{date}?lang={lang}'.format(**{
            'country': 10107,
            'cinema': cinema_id,
            'date': date,
            'lang': 'en_GB'
        })

        response = requests.get(requests.compat.urljoin(BASE_URL, url)).json()
        if not response['body']['films']:
            return 'There are no movies for this date.'

        movies = [
            {
                'title': film['name'],
                'link': '<a href="{url}">{url}</a>'.format(url=requests.compat.urljoin(BASE_URL, film['link'])),
                'event_times': self.get_event_times(response['body']['events'], film['id'])
            } for film in response['body']['films']
        ]

        return 'Movies showing in {cinema} on {date}:\r\n\r\n{movies}'.format(**{
                'cinema': cinema_name,
                'date': date,
                'movies': '\r\n'.join(['{title} @ {event_times}\r\n{link}\r\n'.format(**movie) for movie in movies])
            })

    def get_cinema(self, cinema):
        closest_match, ratio = process.extractOne(cinema, CINEMAS.keys())
        return (closest_match.title(), CINEMAS[closest_match])

    def get_event_times(self, events, filmId):
        times = []
        for event in events:
            if event['filmId'] == filmId:
                time = self.get_time_from_string(event['eventDateTime'])
                times.append((time, '<s>%s</s>' % time)[event['soldOut']])

        return ', '.join(times)

    def get_time_from_string(self, timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S').strftime('%H:%M')
