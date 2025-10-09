from .Template import Template

class Execute(Template):
    async def execute(self, i):
        '''
        Internal method. Returns result and calls module-defined implementation()
        '''

        if hasattr(self, "beforeExecute") == True:
            self.beforeExecute(i)

        response = await self.implementation(i)
        if response == None:
            return self.getResult()

        return response
