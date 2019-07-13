def assert_meta_subclass(cls, name, base):
    assert hasattr(cls._meta, name), '%s.Meta.%s is not defined' % (cls.__name__, name)
    assert issubclass(getattr(cls._meta, name), base), '%s.Meta.%s is not subclass of %s' % (cls.__name__, name, base.__name__)


def assert_instance(inst, base):
    assert isinstance(inst, base), '%s object is not a instance of %s' % (inst.__class__.__name__, base.__name__)


def assert_callable(cls, name):
    assert hasattr(cls, name), '%s.%s is not defined' % (cls.__name__, name)
    assert callable(getattr(cls, name)), '%s.%s is not callable' % (cls.__name__, name)


class MetaOption(type):
    def validate_meta_class(cls):
        pass

    def merge_meta(cls):
        metas = tuple([base.__dict__['Meta'] for base in cls.__bases__ if 'Meta' in base.__dict__])
        Meta = cls.__dict__['Meta'] if 'Meta' in cls.__dict__ else None
        abstract = False

        if Meta is None:
            abstract = False
        else:
            default_meta = type('Meta', (), {
                'abstract': True
            })
            metas = (Meta,) + metas + (default_meta,)
            abstract = Meta.__dict__.get('abstract', False)

        return type('Meta', metas, {
            'abstract': abstract
        })

    @classmethod
    def new_attrs(cls, attrs, bases):
        return attrs

    def __new__(cls, name, bases, attrs):
        super_new = super(MetaOption, cls).__new__

        if not any(map(lambda x: isinstance(x, MetaOption), bases)):
            return super_new(cls, name, bases, attrs)

        new_class = super_new(cls, name, bases, attrs)
        Meta = cls.merge_meta(cls=new_class)
        new_class.Meta = Meta
        new_class._meta = Meta()

        if not Meta.abstract:
            cls.validate_meta_class(cls=new_class)
        return new_class
