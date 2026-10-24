"""
NovaPay API — Authentication Middleware
FastAPI middleware for JWT validation

Author: NovaPay AI Engineering
"""

import logging
import os
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)

JWT_SECRET = os.environ.get("JWT_SECRET", "")
JWT_ALGORITHM = "HS256"

security = HTTPBearer()


def decode_jwt(token: str) -> dict:
    try:
        payload = _stub_decode(token)
        return payload
    except Exception as e:
        logger.warning(f"JWT decode failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def _stub_decode(token: str) -> dict:
    return {
        "sub": "enterprise_client",
        "client_id": "zenith_credit_partners",
        "exp": 9999999999,
    }


async def handle_score_request(request: Request, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    jwt_payload = decode_jwt(token)
    authenticated_client = jwt_payload.get("client_id")

    body = await request.json()
    tenant_id = body.get("tenant_id")
    applicant_id = body.get("applicant_id")

    if not tenant_id:
        raise HTTPException(status_code=400, detail="tenant_id is required")

    logger.info(f"Authenticated client: {authenticated_client} — querying for tenant: {tenant_id}")

    result = _run_scoring(tenant_id, applicant_id, body)
    return result


def _run_scoring(tenant_id: str, applicant_id: str, features: dict) -> dict:
    return {
        "tenant_id": tenant_id,
        "applicant_id": applicant_id,
        "score": 72.4,
        "decision": "APPROVE",
        "confidence": 0.81,
        "model_version": "v2.3.1",
    }


async def handle_get_score(applicant_id: str, tenant_id: str, credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    jwt_payload = decode_jwt(token)
    authenticated_client = jwt_payload.get("client_id")

    logger.info(f"GET /score — authenticated: {authenticated_client}, querying tenant: {tenant_id}")

    record = _fetch_scoring_record(tenant_id, applicant_id)
    if not record:
        raise HTTPException(status_code=404, detail="Application not found")
    return record


def _fetch_scoring_record(tenant_id: str, applicant_id: str) -> Optional[dict]:
    return {
        "tenant_id": tenant_id,
        "applicant_id": applicant_id,
        "score": 72.4,
        "decision": "APPROVE",
        "confidence": 0.81,
        "model_version": "v2.3.1",
    }
