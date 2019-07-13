import types
from unittest import TestCase
from ..observer import Observer, Subject


class OtherObserver(Observer):
    def update(self, value):
        raise NotImplementedError()


class CounterObserver(Observer):
    value = 0

    class Meta:
        abstract = True


class DoubleObserver(CounterObserver):
    def update(self, value):
        self.value += value * 2


class CounterSubject(Subject):
    class Meta:
        observer = CounterObserver


class TripleObserver(CounterObserver):
    def update(self, value):
        self.value += value * 3


class TestObserver(TestCase):
    def test_no_update_func(self):
        with self.assertRaises(AssertionError) as context:
            class Obs(Observer):
                update = 3
        self.assertEqual(context.exception.args[0], 'Obs.update is not callable')

    def test_hash(self):
        observer = DoubleObserver()
        self.assertEqual(hash(observer), id(observer))

    def test_eq(self):
        observer1 = DoubleObserver()
        observer2 = DoubleObserver()

        self.assertNotEqual(observer1, observer2)

    def test_in_set(self):
        observer1 = DoubleObserver()
        observer2 = DoubleObserver()
        s = set([observer1, observer2])
        self.assertSetEqual(s, set([observer1, observer2]))

        s.remove(observer2)
        self.assertEqual(s, set([observer1]))

        s.add(observer2)
        s.remove(observer1)
        self.assertEqual(s, set([observer2]))

    def test_call(self):
        observer = DoubleObserver()
        observer(4)
        self.assertEqual(observer.value, 8)


class TestSubject(TestCase):
    def test_register(self):
        observer = DoubleObserver()
        subject = CounterSubject()
        self.assertEqual(subject.observers, set())

        subject.register(observer)
        self.assertSetEqual(subject.observers, set([observer]))

    def test_register_two(self):
        observer1 = DoubleObserver()
        observer2 = DoubleObserver()
        subject = CounterSubject()

        self.assertEqual(subject.observers, set())

        subject.register(observer1)
        subject.register(observer2)
        self.assertSetEqual(subject.observers, set([observer1, observer2]))

    def test_register_duplicate(self):
        observer = DoubleObserver()
        subject = CounterSubject()
        self.assertEqual(subject.observers, set())

        subject.register(observer)
        self.assertSetEqual(subject.observers, set([observer]))

        subject.register(observer)
        self.assertSetEqual(subject.observers, set([observer]))

    def test_unregister(self):
        observer1 = DoubleObserver()
        observer2 = DoubleObserver()
        subject = CounterSubject()

        subject.register(observer1)
        subject.register(observer2)
        self.assertSetEqual(subject.observers, set([observer1, observer2]))

        subject.unregister(observer1)
        self.assertSetEqual(subject.observers, set([observer2]))

        subject.unregister(observer2)
        self.assertSetEqual(subject.observers, set([]))

    def test_wrong_meta_observer(self):
        with self.assertRaises(AssertionError) as context:
            class Subj(Subject):
                class Meta:
                    observer = type
        self.assertEqual(context.exception.args[0], 'Subj.Meta.observer is not subclass of Observer')

    def test_notify(self):
        observer = DoubleObserver()
        subject = CounterSubject()
        subject.register(observer)
        self.assertEqual(observer.value, 0)

        subject.notify(3)
        self.assertEqual(observer.value, 6)


class TestMixedObserverSubject(TestCase):
    def test_notify(self):
        double = DoubleObserver()
        triple = TripleObserver()
        subject = CounterSubject()

        subject.register(double)
        subject.register(triple)

        subject.notify(3)

        self.assertEqual(double.value, 6)
        self.assertEqual(triple.value, 9)

    def test_register_wrong_observer(self):
        other = OtherObserver()
        subject = CounterSubject()

        with self.assertRaises(AssertionError) as context:
            subject.register(other)
        self.assertEqual(context.exception.args[0], 'OtherObserver object is not a instance of CounterObserver')


class TestSubjectregisterDecorator(TestCase):
    def setUp(self):
        self.set = set()
        self.subject = subject = CounterSubject()

        @subject.register
        def func(value):
            v = value + 1
            self.set.add(v)
            return v

        self.func = func

    def test_register(self):
        func = self.func
        subject = self.subject

        self.assertIsInstance(func, types.FunctionType)
        self.assertSetEqual(subject.observers, set([func]))

    def test_notify(self):
        self.assertSetEqual(self.set, set())
        self.subject.notify(3)
        self.assertSetEqual(self.set, set([4]))

    def test_still_function(self):
        # make sure it still works like function
        self.assertEqual(self.func(3), 4)

    def test_unregister(self):
        self.subject.unregister(self.func)
        self.assertSetEqual(self.subject.observers, set())
