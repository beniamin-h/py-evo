from Objects.Life import Life


class StatsDumper(object):

    def __init__(self, environment):
        self.species_populations = {}
        self.avg_features = {
            'food': {},
            'bionts': {},
            'raptors': {}
        }
        for group in self.avg_features:
            for param in Life.mutating_params:
                self.avg_features[group][param] = []
        self.environment = environment
        self.environment_stats = {}
        for param in environment.get_params():
            self.environment_stats[param] = []
        self.last_tick_counter = 0

    def dumps(self, lifeCollection, tick_counter):
        for species_group_idx in lifeCollection.speciesListDict:
            sum_params = {}
            for param in Life.mutating_params:
                sum_params[param] = 0
            for species in lifeCollection.speciesListDict[species_group_idx].species_list:
                if species.name not in self.species_populations:
                    self.species_populations[species.name] = {
                        'name': species.name,
                        'type': species_group_idx,
                        'start_tick': tick_counter,
                        'populations': [],
                        'features': ['%s:%s' % (param[0:3], species.life_obj.__getattribute__(param)) for param in Life.mutating_params]
                    }
                self.species_populations[species.name]['populations'].append('%s' % species.population)
                self.species_populations[species.name]['end_tick'] = tick_counter
                for param in Life.mutating_params:
                    sum_params[param] += species.life_obj.__getattribute__(param) * species.population
            for param in Life.mutating_params:
                if len(lifeCollection.__getattribute__(species_group_idx)):
                    self.avg_features[species_group_idx][param].append(
                        str(round(float(sum_params[param]) /
                                  len(lifeCollection.__getattribute__(species_group_idx)), 4)))
        for (param, param_value) in self.environment.get_params().items():
            self.environment_stats[param].append(str(param_value))
        self.last_tick_counter = tick_counter

    def write_to_file(self):
        for species_name in self.species_populations:
            for i in xrange(0, self.species_populations[species_name]['start_tick']):
                self.species_populations[species_name]['populations'].insert(0, '0')
                self.species_populations[species_name]['start_tick'] = 0
        for species_name in self.species_populations:
            for i in xrange(self.species_populations[species_name]['end_tick'], self.last_tick_counter):
                self.species_populations[species_name]['populations'].append('0')
                self.species_populations[species_name]['end_tick'] = self.last_tick_counter
        with open('/tmp/evo-populations.txt', 'w') as f:
            for species_name in self.species_populations:
                species = self.species_populations[species_name]
                f.write('%s;%s;%s;%s\n' % (species['name'], species['type'],
                                           ';'.join(species['features']), ';'.join(species['populations'])))
        with open('/tmp/evo-features.txt', 'w') as f:
            for group in self.avg_features:
                for param in self.avg_features[group]:
                    f.write('%s;%s;%s\n' % (group, param, ';'.join(self.avg_features[group][param])))
        with open('/tmp/evo-env.txt', 'w') as f:
            for param in self.environment_stats:
                f.write('%s;%s\n' % (param, ';'.join(self.environment_stats[param])))