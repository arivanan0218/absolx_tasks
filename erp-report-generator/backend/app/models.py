from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SalesItem(BaseModel):
    date: str
    product_name: str
    units_sold: int
    revenue: float
    inventory_level: Optional[int] = None
    category: Optional[str] = None
    region: Optional[str] = None

class ReportRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
class ReportResponse(BaseModel):
    report_text: str
    metrics: dict