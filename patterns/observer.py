import six
from .meta import MetaOption, assert_meta_subclass, assert_callable, assert_instance


__all__ = ['ObserverMetaOption', 'Observer', 'SubjectMetaOption', 'Subject']


class ObserverMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert_callable(cls=cls, name='update')


class Observer(six.with_metaclass(ObserverMetaOption)):
    def __hash__(self):
        return id(self)

    def __eq__(self, observer):
        return id(self) == id(observer)

    def __call__(self, *args, **kwargs):
        return self.update(*args, **kwargs)


class SubjectMetaOption(MetaOption):
    def validate_meta_class(cls):
        assert_meta_subclass(cls=cls, name='observer', base=Observer)


class Subject(six.with_metaclass(SubjectMetaOption)):
    def __init__(self):
        super().__init__()
        self.observers = set()

    def register(self, observer):
        assert_instance(inst=observer, base=self._meta.observer)
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            observer(*args, **kwargs)
