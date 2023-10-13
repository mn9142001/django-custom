from wsgi.request import Request

class PaginateByPaginator:
    
    def __init__(self, request : Request, paginate_by = 5, max_paginate_by = 15) -> None:
        self.request = request
        self.paginate_py = paginate_by
        self.max_paginate_by = max_paginate_by
        
    async def get_limit(self):
        offset = self.offset
        limit = self.limit

        if limit - offset > self.max_paginate_by:
            return offset + self.max_paginate_by
        return limit
        
    async def paginate(self, queryset):
        offset = self.offset
        limit = await self.get_limit()
        return queryset[offset:limit]
    
    @property
    def offset(self): 
        try:                
            return int(self.request.params.get('offset', 0))
        except ValueError as e:
            return 0
        
    @property
    def limit(self):
        try:                
            return int(self.request.params.get('limit', self.offset + self.paginate_py))
        except ValueError as e:
            return self.offset + self.paginate_py