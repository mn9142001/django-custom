from wsgi.response import Response
from wsgi.router import Router
from wsgi.request import Request
from wsgi.views.cbv import View
from apis.schema import UserSchema, UserReadSchema
from user.models import User
from wsgi.paginate import PaginateByPaginator

router = Router()

@router.get('users/list', response_schema = UserReadSchema)
async def index_page(request : Request):    
    users = await User.objects.async_all()
    return await PaginateByPaginator(request).paginate(users)


@router.post('users/signup', validator = UserSchema)
async def index_page(request : Request):
    """You can either return a full response object or the data directly"""
    
    user = await UserSchema.create(await request.body)
    
    data = {"message" : "Hello from post index page!", "query" : request.params.query, "body" : await request.body}
    
    response = Response(
        data,
        request
    )
    
    return response


class HomeView(View):
    
    async def get(self):        
        return "hello from cbv"    


router.register_as_view('cbv', HomeView.as_view())
