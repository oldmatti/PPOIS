from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .employee import Employee
    from .professor import Professor

class Department:
    """Class representing an academic department within a faculty."""

    def __init__(self, department_id: str, name: str, head_of_department: 'Professor'):
        self.department_id = department_id
        self.name = name
        self.head_of_department = head_of_department
        self.employees: List['Employee'] = []

    def add_employee(self, employee: 'Employee'):
        """Adds an employee to the department and establishes a two-way link."""
        self.employees.append(employee)
        employee.assign_department(self)