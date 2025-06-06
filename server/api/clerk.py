from typing import Annotated
from fastapi import Request, Depends, HTTPException, status
from clerk_backend_api import Clerk
from dotenv import load_dotenv
import os
from clerk_backend_api.jwks_helpers import AuthenticateRequestOptions, RequestState

load_dotenv()

CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')
FRONTEND_URL = os.getenv('FRONTEND_URL')

FRONTEND_URL = os.getenv('FRONTEND_URL')

def protected_route(request: Request):
  clerk = Clerk(bearer_auth=CLERK_SECRET_KEY)
  request_state = clerk.authenticate_request(
    request,
    AuthenticateRequestOptions(
      authorized_parties=[FRONTEND_URL]
    )
  )

  if not request_state.is_signed_in:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

  return request_state

AuthDep = Annotated[RequestState, Depends(protected_route)]