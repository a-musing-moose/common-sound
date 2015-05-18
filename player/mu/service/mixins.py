

class DeferenceMixin(object):

    def dereference(self, reference):
        result = yield from self.call(
            "{0}.get".format(reference.get("$ref", None)),
            reference.get("$id", None)
        )
        return result
