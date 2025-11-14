class Writable():
    @classmethod
    def define_data(cls):
        '''
        Returns ContentUnit extension then init_subclass sets it as property.
        '''

        return None

    def init_subclass(cls):
        #if cls.ContentUnit == None:
        cls.ContentUnit = cls.define_data()
