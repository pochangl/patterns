import six
from .meta import MetaOption, assert_meta_subclass, assert_callable


class StepMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert_callable(cls, 'run')


class Step(six.with_metaclass(StepMetaOption)):
    def initialize(self):
        pass


class PipelineMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert_meta_subclass(cls=cls, name='step', base=Step)


class Pipeline(six.with_metaclass(PipelineMetaOption)):
    def __init__(self):
        self.steps = []

    def register(self, step):
        base = self._meta.step
        assert issubclass(step, base), '%s is not a subclass of %s' % (step.__name__, base.__name__)

        instance = step()
        self.steps.append(instance)
        instance.initialize()

    def __iter__(self):
        for step in self.steps:
            yield step

    def run(self, **kwargs):
        data = self.get_initial_data()
        for step in self:
            new_data = step.run(**kwargs)
            if new_data:
                data = self.merge_data(data, new_data)
        return data

    def merge_data(self, data1, data2):
        data = data1.copy()
        data.update(data2)
        return data

    def __call__(self, **kwargs):
        return self.run(**kwargs)
