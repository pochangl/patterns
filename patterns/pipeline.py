import six
from .meta import MetaOption


class StepMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert hasattr(cls, 'run'), '%s.run is not defined' % cls.__name__
        assert callable(cls.run), '%s.run is not callable' % cls.__name__


class Step(six.with_metaclass(StepMetaOption)):
    def initialize(self):
        pass


class PipelineMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert hasattr(cls._meta, 'step'), '%s.Meta.step is not defined' % cls.__name__
        assert issubclass(cls._meta.step, Step), '%s.Meta.step is not subclass of %s' % (cls.__name__, Step.__name__)


class Pipeline(six.with_metaclass(PipelineMetaOption)):
    steps = []

    def register(self, step):
        base = self._meta.step
        assert issubclass(step, base), '%s is not a subclass of %s' % (step.__name__, base.__name__)

        instance = step()
        self.steps.append(instance)
        instance.initialize()

    def run(self, **kwargs):
        data = self.get_initial_data()
        for step in self.steps:
            new_data = step.run(**kwargs)
            if new_data:
                data = self.merge_data(data, new_data)
        return data

    def merge_data(self, data1, data2):
        data = data1.copy()
        data.update(data2)
        return data
