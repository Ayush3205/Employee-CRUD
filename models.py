from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Employee(BaseModel):
    employee_id: str = Field(..., description="Unique employee identifier")
    name: str = Field(..., description="Employee name")
    department: str = Field(..., description="Department name")
    salary: float = Field(..., gt=0, description="Employee salary")
    joining_date: str = Field(..., description="Joining date in YYYY-MM-DD format")
    skills: List[str] = Field(..., description="List of skills")

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = Field(None, gt=0)
    joining_date: Optional[str] = None
    skills: Optional[List[str]] = None

class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: str
    skills: List[str]

class AverageSalaryResponse(BaseModel):
    department: str
    avg_salary: float

class MessageResponse(BaseModel):
    message: str