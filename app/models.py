from pydantic import BaseModel, Field, field_validator
from typing import Optional

class MessageBase(BaseModel):
    """
    Modelo base para mensagens enviadas ao chatbot.
    """
    content: str = Field(..., min_length=1, max_length=500, description="O conteúdo da mensagem do usuário.")
    user_id: Optional[str] = Field(None, max_length=50, description="Um identificador opcional para o usuário.")

class MessageSchema(MessageBase):
    """
    Esquema de validação de mensagem com regras extras, usado para validação via Pydantic.
    """
    class Config:
        extra = 'forbid'  # Não permitir campos extras na entrada
        json_schema_extra = {
            "example": {
                "content": "Qual o horário de funcionamento?",
                "user_id": "usr_12345"
            }
        }

    # Exemplo de validador customizado (opcional):
    # @field_validator('user_id')
    # def user_id_must_be_alphanumeric(cls, value):
    #     if value and not value.isalnum():
    #         raise ValueError('user_id must be alphanumeric')
    #     return value
