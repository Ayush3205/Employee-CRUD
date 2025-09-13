from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_collection
from models import Employee, EmployeeUpdate, EmployeeResponse, AverageSalaryResponse, MessageResponse
from pymongo.errors import DuplicateKeyError
import logging

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=EmployeeResponse)
async def create_employee(employee: Employee):
    """Create a new employee"""
    collection = get_collection()
    
    try:
        result = await collection.insert_one(employee.dict())
        
        if result.inserted_id:
            return EmployeeResponse(**employee.dict())
        else:
            raise HTTPException(status_code=500, detail="Failed to create employee")
            
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    except Exception as e:
        logging.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/avg-salary", response_model=List[AverageSalaryResponse])
async def get_average_salary_by_department():
    """Get average salary by department using MongoDB aggregation"""
    collection = get_collection()
    
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "department": "$_id",
                "avg_salary": {"$round": ["$avg_salary", 2]}
            }
        },
        {
            "$sort": {"department": 1}
        }
    ]
    
    cursor = collection.aggregate(pipeline)
    results = await cursor.to_list(length=None)
    if not results:
        return []
    return [AverageSalaryResponse(**result) for result in results]

@router.get("/search", response_model=List[EmployeeResponse])
async def search_employees_by_skill(
    skill: str = Query(..., description="Skill to search for"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Search employees by skill"""
    collection = get_collection()
    query_filter = {"skills": {"$in": [skill]}}
    
    cursor = collection.find(query_filter).skip(skip).limit(limit)
    employees = await cursor.to_list(length=limit)
    
    result = []
    for employee in employees:
        employee.pop("_id", None)
        result.append(EmployeeResponse(**employee))
    
    return result

@router.get("/", response_model=List[EmployeeResponse])
async def list_employees_by_department(
    department: Optional[str] = Query(None, description="Filter by department"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """List employees by department, sorted by joining_date (newest first)"""
    collection = get_collection()
    
    query_filter = {}
    if department:
        query_filter["department"] = department
    
    cursor = collection.find(query_filter).sort("joining_date", -1).skip(skip).limit(limit)
    employees = await cursor.to_list(length=limit)
    
    result = []
    for employee in employees:
        employee.pop("_id", None)
        result.append(EmployeeResponse(**employee))
    
    return result

@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str):
    """Get employee by ID"""
    collection = get_collection()
    
    employee = await collection.find_one({"employee_id": employee_id})
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.pop("_id", None)
    return EmployeeResponse(**employee)

@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: str, employee_update: EmployeeUpdate):
    """Update employee details (partial updates allowed)"""
    collection = get_collection()
    
    update_data = {k: v for k, v in employee_update.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await collection.update_one(
        {"employee_id": employee_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    updated_employee = await collection.find_one({"employee_id": employee_id})
    updated_employee.pop("_id", None)
    
    return EmployeeResponse(**updated_employee)

@router.delete("/{employee_id}", response_model=MessageResponse)
async def delete_employee(employee_id: str):
    """Delete employee"""
    collection = get_collection()
    
    result = await collection.delete_one({"employee_id": employee_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return MessageResponse(message="Employee deleted successfully")