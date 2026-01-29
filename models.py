"""
Maintenance Log Data Model
Represents a single maintenance task/log entry
"""
from datetime import datetime
from typing import Optional


class MaintenanceLog:
    """
    Represents a maintenance log entry
    """
    
    def __init__(
        self,
        date: datetime,
        task_type: str,
        description: str,
        hours_spent: float,
        materials_cost: float = 0.0,
        technician_name: Optional[str] = None,
        location: Optional[str] = None,
        priority: Optional[str] = None,
        notes: Optional[str] = None
    ):
        self.date = date
        self.task_type = task_type.lower().strip()
        self.description = description
        
        # Validate and set hours_spent
        hours_spent = float(hours_spent)
        if hours_spent < 0:
            raise ValueError(f"hours_spent cannot be negative: {hours_spent}")
        self.hours_spent = hours_spent
        
        # Validate and set materials_cost
        materials_cost = float(materials_cost)
        if materials_cost < 0:
            raise ValueError(f"materials_cost cannot be negative: {materials_cost}")
        self.materials_cost = materials_cost
        
        self.technician_name = technician_name
        self.location = location
        self.priority = priority
        self.notes = notes
        
    def calculate_inhouse_cost(self, hourly_rate: float) -> float:
        """Calculate total in-house cost (labor + materials)"""
        labor_cost = self.hours_spent * hourly_rate
        return labor_cost + self.materials_cost
    
    def calculate_contractor_cost(self, hourly_rate: float) -> float:
        """
        Calculate total contractor cost (labor + materials)
        Note: Currently uses same calculation as in-house for labor.
        Future enhancement: Add contractor markup/overhead percentage.
        """
        labor_cost = self.hours_spent * hourly_rate
        return labor_cost + self.materials_cost
    
    def calculate_savings(self, inhouse_rate: float, contractor_rate: float) -> float:
        """Calculate cost savings by doing work in-house"""
        contractor_total = self.calculate_contractor_cost(contractor_rate)
        inhouse_total = self.calculate_inhouse_cost(inhouse_rate)
        return contractor_total - inhouse_total
    
    def to_dict(self) -> dict:
        """Convert to dictionary for export"""
        return {
            "date": self.date.strftime("%Y-%m-%d"),
            "task_type": self.task_type,
            "description": self.description,
            "hours_spent": self.hours_spent,
            "materials_cost": self.materials_cost,
            "technician_name": self.technician_name,
            "location": self.location,
            "priority": self.priority,
            "notes": self.notes
        }
    
    def __str__(self) -> str:
        return f"MaintenanceLog({self.date.strftime('%Y-%m-%d')}, {self.task_type}, {self.hours_spent}hrs)"
    
    def __repr__(self) -> str:
        return self.__str__()
