""" Esquemas para validação de dados de entrada e formatação de respostas da API, utilizando Pydantic. """

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class AtoBase(BaseModel):
    tipo_ato: str = Field(..., min_length=1)
    numero_ato: str = Field(..., min_length=1)
    orgao: str = Field(..., min_length=1)
    data_publicacao: date
    ementa: str = Field(..., min_length=1)


class AtoCreate(AtoBase):
    pass


class AtoUpdate(BaseModel):
    tipo_ato: Optional[str] = None
    numero_ato: Optional[str] = None
    orgao: Optional[str] = None
    data_publicacao: Optional[date] = None
    ementa: Optional[str] = None


class AtoResponse(AtoBase):
    id: int
    is_deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DashboardItem(BaseModel):
    label: str
    total: int


class DashboardResponse(BaseModel):
    total_registros: int
    por_tipo_ato: list[DashboardItem]
    por_orgao: list[DashboardItem]