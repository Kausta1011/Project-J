import os

app = os.getenv("APP_NAME", "MyApp")
port = int(os.getenv("PORT",'8000'))
debug = os.getenv(str("DEBUG_MODE"), "false").lower() == "true"
print(f"Starting {app} on port {port} | Debug: {bool(debug)}")


def calculate_order_total(item_name : str, quantity : int, price_per_unit: float, apply_discount: bool) -> tuple[str,float]: 
    if apply_discount:
        return item_name, quantity * price_per_unit * 0.9
    return item_name, quantity * price_per_unit


from pydantic import BaseModel

class JobApplication(BaseModel):
    applicant_name : str
    years_of_experience: int
    skills : list[str]
    expected_salary: float | None = None
    is_remote: bool | None = False


candidate1 = JobApplication(applicant_name = "Kaustubh",years_of_experience= 2, skills= ["python", "fastapi", "ML"],expected_salary = None ,is_remote=True)
print(candidate1.applicant_name, candidate1.skills)














