from pydantic import BaseModel, Field

class Proxy(BaseModel):
    host: str
    port: int
    score: int = Field(default=10, ge=0, le=100)
    protocol: str = "http"
    anonymous: bool = True
    source: str | None = None

    @property
    def string(self) -> str:
        return f"{self.host}:{self.port}"
