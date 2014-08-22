
# didn't use built in enum for backwards compat
def build_enum(*sequential, **named):
  enums = dict(zip(sequential, range(len(sequential))), **named)
  reverse = dict((value, key) for key, value in enums.iteritems())
  enums['Name'] = reverse
  return type('Enum', (), enums)

