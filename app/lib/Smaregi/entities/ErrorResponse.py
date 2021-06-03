class ErrorResponse(Exception):
    def __init__(self, response: dict):
        self.type = response.get('type')
        self.title = response.get('title')
        self.detail = response.get('detail')
        self.status = response.get('status')

    def __repr__(self):
        return f'''
            ErrorResponse(
                type: "{self.type}",
                title: "{self.title}",
                detail: "{self.detail}",
                status: "{self.status}"
            )
        '''
