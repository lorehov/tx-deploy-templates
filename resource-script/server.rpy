from twisted.web import resource
import ConfigParser

class SomeLeafResource(resource.Resource):

    isLeaf = True

    def render(self, request):
        return config.get('settings', 'greeting')

config = ConfigParser.ConfigParser()
config.read('config.conf')
resource = resource.Resource()
resource.putChild('leaf', SomeLeafResource())
