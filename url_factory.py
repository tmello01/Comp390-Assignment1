

def create_location_url(key, search_term):
    return f'http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={key}&q={search_term}'


def create_five_day_url(key, location_key):
    return f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}?apikey={key}'


def create_current_url(key, location_key):
    return f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={key}'
