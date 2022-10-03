from abc import abstractmethod, ABC


# WeatherURL is a base abstract class used by other urls, and eventually
# the factory.
class WeatherURL:
    @abstractmethod
    def create_url(self, params):
        pass


class LocationURL(WeatherURL):
    def create_url(self, params):
        pass


class ForecastURL(WeatherURL):
    def create_url(self, params):
        return f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{params[0]}'


class CurrentConditionsURL(WeatherURL):
    def create_url(self, params):
        pass
