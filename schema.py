

class SchemaExit(SystemExit):

    pass


class is_a(object):

    def __init__(self, *args):
        self._args = args

    def validate(self, data):
        schemas = map(Schema, self._args)
        for s in schemas:
            data = s.validate(data)
        return data


class either(object):

    def __init__(self, *args):
        self._args = args

    def validate(self, data):
        schemas = map(Schema, self._args)
        for s in schemas:
            try:
                return s.validate(data)
            except:
                pass
        raise SchemaExit('did not validate %r %r' % (self, data))


class Schema(object):

    def __init__(self, schema):
        self._s = schema

    def validate(self, data):
        if hasattr(self._s, 'validate'):
            return self._s.validate(data)
        if hasattr(self._s, '__call__'):
            if self._s(data):
                return data
            else:
                raise SchemaExit('did not validate %r %r' % (self._s, data))
        if type(self._s) is list:
            data = Schema(list).validate(data)
            return [Schema(either(*self._s)).validate(d) for d in data]
        if type(self._s) is type:
            try:
                return self._s(data)
            except:
                raise SchemaExit('did not validate %r %r' % (self._s, data))
        if self._s == data:
            return data
        else:
            raise SchemaExit('did not validate %r %r' % (self._s, data))