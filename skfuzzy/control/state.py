"""
state.py : Contains framework to hold variables unique to a simulation.

This allows simulations to be precalculated and then referenced later for a
dramatic efficiency gain. This gain is only realized for smaller systems,
usually with discrete-valued inputs. However, if your controller can contain
all possible input states in memory and repeat values are likely, enabling
caching will result in major efficiency gains.
"""


class StatefulProperty(object):

    def __init__(self, initial_condition=None):
        self.default = initial_condition
        self.data = {'current': initial_condition}

    def __get__(self, instance, owner):
        if instance is None:
            return self

        try:
            return self.data[instance]
        except KeyError:
            val = StatePerSimulation(self.default)
            self.data[instance] = val
            return val

    def __set__(self, instance, value):
        raise AttributeError("Property is read-only. "
                             "Did you mean to access via a simulation?")

    def clear(self, initial_condition=None):
        self.__init__(self.default)


class StatePerSimulation(object):

    def __init__(self, initial_condition=None):
        self.default = initial_condition
        self._sim_data = {'current': initial_condition}

    def __getitem__(self, key):
        from .controlsystem import ControlSystemSimulation

        # Shortcut for current sim value, to carry across unique ID updates
        if key == 'current':
            return self._sim_data[key]

        assert isinstance(key, ControlSystemSimulation)

        # Access all state data via the unique identifier string
        key_id = key.unique_id
        try:
            return self._sim_data[key_id]
        except KeyError:
            if isinstance(self.default, dict) and len(self.default) == 0:
                # Create a new empty dictionary and remember it
                result = dict()
                self._sim_data[key_id] = result
                return result
            else:
                return self.default

    def __setitem__(self, key, value):
        from .controlsystem import ControlSystemSimulation

        # Shortcut for current sim value, to carry across unique ID updates
        if key == 'current':
            self._sim_data[key] = value
            return

        assert isinstance(key, ControlSystemSimulation)

        # Access all state data via the unique identifier string
        self._sim_data[key.unique_id] = value

    def clear(self, initial_condition=None):
        self.__init__(self.default)
