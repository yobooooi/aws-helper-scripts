class Thing(object):
    def __init__(self, name):
        self.name = name

    def debug_name(function):
        def debug_wrapper(*args):
            self = args[0]
            print('self.name = ' + self.name)
            print('running function {}()'.format(function.__name__))
            function(*args)
            print ('self.name = ' + self.name)
        return debug_wrapper

    @debug_name
    def set_name(self, new_name):
        self.name = new_name