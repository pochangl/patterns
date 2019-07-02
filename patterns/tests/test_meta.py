import unittest
import six
from ..meta import MetaOption


class MetaBase(MetaOption):
    def validate_meta_class(cls):
        assert 'run' in dir(cls), '%s.run is not defined' % cls.__name__


@six.add_metaclass(MetaBase)
class Base(six.with_metaclass(MetaBase)):
    pass


class TestMetaOption(unittest.TestCase):
    def test_inheritance(self):
        class Child1(Base):
            run = None

            class Meta:
                option1 = 1
                option2 = 1
                option3 = 1

        class Child2(Child1):
            class Meta:
                option2 = 2
                option4 = 2

        class Child3(Child2):
            class Meta:
                option3 = 3
                option5 = 3

        meta = Child3()._meta

        self.assertEqual(meta.option1, 1)
        self.assertEqual(meta.option2, 2)
        self.assertEqual(meta.option3, 3)
        self.assertEqual(meta.option4, 2)
        self.assertEqual(meta.option5, 3)

    def test_concrete(self):
        class Child(Base):
            run = 3

        self.assertFalse(Child()._meta.abstract)

    def test_abstract(self):
        class Child(Base):
            class Meta:
                abstract = True
        self.assertTrue(Child()._meta.abstract)

    def test_invalid(self):
        # invalid class has no run attribute
        with self.assertRaises(AssertionError) as context:
            class Child(Base):
                pass
        self.assertEqual(context.exception.args[0], 'Child.run is not defined')
