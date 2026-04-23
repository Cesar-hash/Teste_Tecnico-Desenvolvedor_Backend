""" Endpoints relacionados à autenticação de usuários, incluindo registro e login.
Este módulo é responsável por gerenciar a criação de usuários, autenticação e geração de tokens JWT para acesso aos endpoints protegidos da API. 
Ele utiliza as funções de segurança definidas em api.security para hash de senhas e criação de tokens, 
e as funções de serviço em api.services para interagir com o banco de dados. """

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.schemas.schemas import TokenResponse, UserCreate, UserResponse, UserLogin
from api.security import create_access_token, hash_password, verify_password
from api.services import create_user, get_user_by_username


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    user = create_user(db, payload.username, hash_password(payload.password))
    return user


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(db, payload.username)

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    return TokenResponse(access_token=create_access_token(user.username))