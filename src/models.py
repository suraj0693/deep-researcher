from pydantic import BaseModel


class QueryPlanResponse(BaseModel):
    queryies: list[str]