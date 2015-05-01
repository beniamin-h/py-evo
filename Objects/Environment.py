

class Environment(object):

    base_uv_radiation_sensitivity = 0.1
    base_x_radiation_sensitivity = 0.4
    base_chemical_mutagens_sensitivity = 0.5

    def __init__(self):
        self._humidity = 0.5  # float: 0.0 - 1.0
        self._insolation = 0.5  # float: 0.0 - 1.0
        self._insolation_uv_radiation = None  # float: 0.0 - 1.0
        self.temperature = None  # float: 0.0 - 1.0
        self._uv_radiation = 0.0  # float: 0.0 - 1.0
        self._x_radiation = 0.0  # float: 0.0 - 1.0
        self._chemical_mutagens = 0.0  # float: 0.0 - 1.0
        #self.viruses = []
        self._recalculate_temperature()
        self._recalculate_insolation_uv_radiation()

    def get_params(self):
        return {
            'humidity': self.humidity,
            'insolation': self.insolation,
            'temperature': self.temperature,
            'uv_radiation': self.uv_radiation,
            'x_radiation': self.x_radiation,
            'chemical_mutagens': self.chemical_mutagens
        }

    @staticmethod
    def _validate_value(value):
        value = 1.0 if value > 1 else value
        value = 0 if value < 0 else value
        return value

    def _recalculate_temperature(self):
        self.temperature = (1 - self.humidity + self.insolation) / 2.0

    def _recalculate_insolation_uv_radiation(self):
        self._insolation_uv_radiation = self._insolation / 10.0

    @property
    def humidity(self):
        return self._humidity

    @humidity.setter
    def humidity(self, new_value):
        self._humidity = self._validate_value(new_value)
        self._recalculate_temperature()

    @property
    def insolation(self):
        return self._insolation

    @insolation.setter
    def insolation(self, new_value):
        self._insolation = self._validate_value(new_value)
        self._recalculate_temperature()
        self._recalculate_insolation_uv_radiation()

    @property
    def uv_radiation(self):
        return self._uv_radiation + self._insolation_uv_radiation

    @uv_radiation.setter
    def uv_radiation(self, new_value):
        self._uv_radiation = self._validate_value(new_value - self._insolation_uv_radiation)

    @property
    def x_radiation(self):
        return self._x_radiation

    @x_radiation.setter
    def x_radiation(self, new_value):
        self._x_radiation = self._validate_value(new_value)

    @property
    def chemical_mutagens(self):
        return self._chemical_mutagens

    @chemical_mutagens.setter
    def chemical_mutagens(self, new_value):
        self._chemical_mutagens = self._validate_value(new_value)

    def _calculate_property_factor(self, property, likeness):
        # float: 0.0 - 1.0
        return getattr(self, property) * likeness + (1 - getattr(self, property)) * (1 - likeness)

    def _calculate_harmful_property_factor(self, property, sensitivity):
        # float: 0.0 - 1.0
        return getattr(self, property) * sensitivity

    def calculate_speed_factor(self, humidity_likeness, temperature_likeness):
        # float: 0.0 - 1.0
        return self._calculate_property_factor('humidity', humidity_likeness) * \
               self._calculate_property_factor('temperature', temperature_likeness)

    def calculate_defence_factor(self, humidity_likeness, temperature_likeness):
        # float: 0.0 - 1.0
        return self._calculate_property_factor('humidity', humidity_likeness) * \
               self._calculate_property_factor('temperature', temperature_likeness)

    def calculate_attack_factor(self, humidity_likeness, temperature_likeness):
        # float: 0.0 - 1.0
        return self._calculate_property_factor('humidity', humidity_likeness) * \
               self._calculate_property_factor('temperature', temperature_likeness)

    def calculate_reproducing_factor(self, humidity_likeness, temperature_likeness):
        # float: 0.0 - 1.0
        return self._calculate_property_factor('humidity', humidity_likeness) * \
               self._calculate_property_factor('temperature', temperature_likeness)

    def calculate_mutable_factor(self, uv_radiation_sensitivity, x_radiation_sensitivity, chemical_mutagens_sensitivity):
        # float: 0.0 - 1.0
        return self.uv_radiation * uv_radiation_sensitivity * self.base_uv_radiation_sensitivity + \
               self.x_radiation * x_radiation_sensitivity * self.base_x_radiation_sensitivity + \
               self.chemical_mutagens * chemical_mutagens_sensitivity * self.base_chemical_mutagens_sensitivity

    def calculate_energy_drain_factor(self, humidity_likeness, temperature_likeness):
        # float: 0.0 - 1.0
        return self._calculate_property_factor('humidity', humidity_likeness) * \
               self._calculate_property_factor('temperature', temperature_likeness)

    def calculate_health_harmfulness_factor(self, uv_radiation_sensitivity, x_radiation_sensitivity,
                                            chemical_mutagens_sensitivity):
        # float: 0.0 - 1.033
        return (self._calculate_harmful_property_factor('uv_radiation', uv_radiation_sensitivity) +
               self._calculate_harmful_property_factor('x_radiation', x_radiation_sensitivity) +
               self._calculate_harmful_property_factor('chemical_mutagens', chemical_mutagens_sensitivity)) / 3.0