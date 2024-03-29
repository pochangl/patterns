from unittest import TestCase
from ..pipeline import Step, Pipeline


class SetStep(Step):
    class Meta:
        abstract = True

    def initialize(self):
        self.initialized = True


class Step1(SetStep):
    def run(self, offset=0):
        return set([1 + offset])


class Step2(SetStep):
    def run(self, offset=0):
        return set([2 + offset])


class SetPipeline(Pipeline):
    class Meta:
        step = SetStep

    get_initial_data = set


class OtherStep(Step):
    def run(self, offset=0):
        return set([3 + offset])


class TestStep(TestCase):
    def test_no_run_attribute(self):
        with self.assertRaises(AssertionError) as context:
            class Step1(Step):
                pass

        self.assertEqual(context.exception.args[0], 'Step1.run is not defined')

    def test_run_not_callable(self):
        with self.assertRaises(AssertionError) as context:
            class Step1(Step):
                run = 1

        self.assertEqual(context.exception.args[0], 'Step1.run is not callable')


class TestPipeline(TestCase):
    def test_Meta_step_not_define(self):
        with self.assertRaises(AssertionError) as context:
            class Pipe1(Pipeline):
                pass

        self.assertEqual(context.exception.args[0], 'Pipe1.Meta.step is not defined')

    def test_Meta_step_wrong_type(self):
        with self.assertRaises(AssertionError) as context:
            class Pipe1(Pipeline):
                class Meta:
                    step = type

        self.assertEqual(context.exception.args[0], 'Pipe1.Meta.step is not subclass of Step')

    def test_register(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)

        assert len(pipeline.steps)
        assert isinstance(pipeline.steps[0], Step1)
        assert isinstance(pipeline.steps[1], Step2)

    def test_register_initialize(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)
        for step in pipeline.steps:
            step.initialized = True

        assert isinstance(pipeline.steps[0], Step1)
        assert isinstance(pipeline.steps[1], Step2)

    def test_merge(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)
        data = pipeline.run()
        self.assertSetEqual(set([1, 2]), data)

    def test_kwargs(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)
        data = pipeline.run(offset=10)
        self.assertSetEqual(set([11, 12]), data)

    def test_call(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)
        data = pipeline(offset=10)
        self.assertSetEqual(set([11, 12]), data)

    def test_register_other_step(self):
        pipeline = SetPipeline()

        with self.assertRaises(AssertionError) as context:
            pipeline.register(OtherStep)
        self.assertEqual(context.exception.args[0], 'OtherStep is not a subclass of SetStep')

    def test_iteration(self):
        pipeline = SetPipeline()
        pipeline.register(Step1)
        pipeline.register(Step2)
        step1, step2 = list(pipeline)

        self.assertEqual([step1, step2], pipeline.steps)
