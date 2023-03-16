import unittest

from app import app


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app.config.update({
            'TESTING': True
        })
        cls._client = app.test_client()

    def test_health_check(self):
        response = self._client.get('/')
        content = response.json

        self.assertEqual(content['status'], 'OK')

    def test_production_plan(self):
        request_body = {
            "load": 100,
            "fuels": {
                "gas(euro/MWh)": 13.4,
                "kerosine(euro/MWh)": 50.8,
                "co2(euro/ton)": 20,
                "wind(%)": 50
            },
            "powerplants": [{
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 30,
                "pmax": 60
            }, {
                "name": "tj1",
                "type": "turbojet",
                "efficiency": 0.3,
                "pmin": 0,
                "pmax": 26
            }, {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 34
            }]
        }
        response = self._client.post('/productionplan', json=request_body)

        content = response.json

        self.assertEqual(content[0]['name'], 'windpark1')
        self.assertAlmostEqual(content[0]['p'], 17.0, delta=0.1)
        self.assertEqual(content[1]['name'], 'gasfiredbig1')
        self.assertAlmostEqual(content[1]['p'], 60, delta=0.1)
        self.assertEqual(content[2]['name'], 'tj1')
        self.assertAlmostEqual(content[2]['p'], 23, delta=0.1)


if __name__ == '__main__':
    unittest.main()
