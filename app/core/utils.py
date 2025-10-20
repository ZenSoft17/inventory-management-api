from typing import Any, Dict
from datetime import datetime

def success_response(data: Any, message: str = "Operación exitosa") -> Dict:
    return {
        "success": True,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }

def error_response(message: str, details: Any = None) -> Dict:
    response = {
        "success": False,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    if details:
        response["details"] = details
    return response
