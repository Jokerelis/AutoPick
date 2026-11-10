import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False
)
def get_company_id(api_key: str = Depends(api_key_header)):
    vilnius_key = os.getenv("AUTOPICK_VILNIUS_KEY")
    kaunas_key = os.getenv("AUTOPICK_KAUNAS_KEY")

    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key is required to access this resource"
        )

    if secrets.compare_digest(api_key,vilnius_key):
        return 1
    if secrets.compare_digest(api_key,kaunas_key):
        return 2

    raise HTTPException(
        status_code=401,
        detail="Invalid API Key"
    )
def check_company_access(company_id, authenticated_company_id):
    if company_id != authenticated_company_id:
        raise HTTPException(
            status_code=403,
            detail="Access to another company is forbidden"
        )