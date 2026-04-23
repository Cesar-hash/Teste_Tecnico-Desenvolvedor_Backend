""" API Router para a aplicação. Este router inclui todos os endpoints para os diferentes módulos da aplicação,
como autenticação, atos, dashboard, RPA e web app. 
Cada módulo tem seu próprio router que é incluído no router principal da API com um prefixo específico e tags. """

from fastapi import APIRouter
from .endpoints import atos, auth, dashboard, rpa, web


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(atos.router, prefix="/atos", tags=["Atos"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(rpa.router, prefix="/rpa", tags=["RPA"])
api_router.include_router(web.router, prefix="/web", tags=["Web"])