from collections import UserDict
from dataclasses import dataclass
from typing import List


class PowerPlant:
    type_to_fuel_map = {
        'gasfired': 'gas',
        'turbojet': 'kerosine',
        'windturbine': 'wind'
    }

    @staticmethod
    def from_raw(type, **raw_data):
        if type == 'windturbine':
            return WindPlant(type=type, **raw_data)
        else:
            return PowerPlant(type=type, **raw_data)

    def __init__(self, name, type, efficiency, pmin, pmax, prices: 'Prices'):
        self.name = name
        self._type = type
        self._efficiency = efficiency
        self.pmin = int(pmin)
        self.pmax = int(pmax)
        self._prices = prices

    @property
    def fueltype(self):
        return self.type_to_fuel_map.get(self._type)

    @property
    def unit_price(self):
        return (1 / self._efficiency) * getattr(self._prices, self.fueltype)

    @property
    def min_price(self):
        return self.pmin * self.unit_price

    @property
    def max_price(self):
        return self.pmax * self.unit_price

    def get_production_for_load(self, load):
        if load < self.pmin:
            return 0
        if load > self.pmax:
            return self.pmax
        return load

    def __gt__(self, other: 'PowerPlant'):
        if isinstance(other, PowerPlant):
            return self.unit_price > other.unit_price
        return super(PowerPlant, self).__gt__(other)

    def __lt__(self, other: 'PowerPlant'):
        if isinstance(other, PowerPlant):
            return self.unit_price < other.unit_price
        return super(PowerPlant, self).__lt__(other)

    def __eq__(self, other: 'PowerPlant'):
        if isinstance(other, PowerPlant):
            return self.unit_price == other.unit_price
        return super(PowerPlant, self).__eq__(other)

    def __repr__(self):
        return f"{self.name} - {self.fueltype} - {self.unit_price}"


class WindPlant(PowerPlant):

    @property
    def unit_price(self):
        return 0

    def get_production_for_load(self, load):
        max_production = self.pmax * (getattr(self._prices, self.fueltype) / 100)
        if load > max_production:
            return max_production
        return load


@dataclass
class Prices():
    gas: float
    kerosine: float
    co2: float
    wind: float

    def __get__(self, instance, owner):
        return self.__getattribute__(instance)

    def __getattr__(self, item):
        return self.__getattribute__(item)


def apply(expected_load: int, plants: List[PowerPlant]):
    plants.sort()
    result = []
    for plant in plants:
        plant_production = plant.get_production_for_load(expected_load)
        result.append({
            'name': plant.name,
            'p': plant_production

        })
        expected_load = expected_load - plant_production
    return result
