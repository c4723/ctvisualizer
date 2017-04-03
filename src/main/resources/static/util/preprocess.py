"""
Preprocess CT data and output a JSON representing the data required by the visualizer
"""
import argparse
import json
import logging
import csv

class CTData(object):
    # we expect a dictionary of data in the format
    # {'Latin': '130', 'North American ': '1195', 'East Asian': '75', 'CT': '0832.00', 'Middle Eastern': '0',
    #  'Aboriginal': '85', 'Oceania': '0', 'Other Asian': '0', 'African': '25', 'Carribean': '75',
    #  'Total': '3760', 'South Asian': '0', 'European': '3170'}
    def __init__(self, data):
        self.ethnicityStats = {}

        totalPopulation = int(data['Total'])
        for key in data:
            if key.strip.lower() in ['total', 'ct', 'oceania', 'other asian']:
                continue

            population = int(data[key])
            ethnicity = key.strip()

            self.ethnicityStats[ethnicity] = {}
            self.ethnicityStats[ethnicity]['points'] = int(population / _args.scale)
            self.ethnicityStats[ethnicity]['percent'] = int(population * 100 / totalPopulation)


class Stats(object):
    def fatal(self, msg):
        self.logger.error(msg)
        exit(1)

    def __init__(self, inputFile, outputFile):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        sysHandler = logging.StreamHandler()
        fmt = logging.Formatter('[%(levelname)s]: %(message)s')
        sysHandler.setFormatter(fmt)

        if _args.debug:
            sysHandler.setLevel(logging.DEBUG)
        else:
            sysHandler.setLevel(logging.INFO)

        self.logger.addHandler(sysHandler)

        self.ctStats = {}
        with open(inputFile, 'r') as f:
            csvreader = csv.DictReader(f, delimiter=',')
            for row in csvreader:
                self.logger.debug(row)
                self.ctStats[row['CT']] = CTData(row)

        if outputFile:
            with open(outputFile, 'w') as f:
                json.dump(self.ctStats, f, default=lambda o: o.__dict__)

        self.logger.debug(json.dumps(self.ctStats, default=lambda o: o.__dict__))


if __name__ == "__main__":
    _parser = argparse.ArgumentParser()
    _parser.add_argument('-i', '--input', help='CSV file containing the census data', required=True)
    _parser.add_argument('-s', '--scale', help='Scale of the population dots', default=40, type=int)
    _parser.add_argument('-o', '--output', help='File to which the JSON representation should be output')
    _parser.add_argument('-d', '--debug', help='Debug', default=False, required=False, action='store_true')

    _args = _parser.parse_args()

    _stats = Stats(_args.input, _args.output)
