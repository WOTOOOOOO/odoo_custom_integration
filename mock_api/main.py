from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from routers import rs_ge, bank, payment

app = FastAPI(
    title="Mock API for Odoo Integration",
    description="Simulates RS.ge, Bank, and Payment Provider APIs",
    version="1.0.0"
)

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != "test_token_123":
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    return credentials.credentials

# Include routers
# RS.ge endpoints might not require the global bearer token for /auth/token, 
# but /einvoice/submit might. The spec says "Authorization: Bearer test_token_123" 
# under General, but RS.ge has a specific /auth/token endpoint. 
# Usually /auth/token is public or uses basic auth, and others use the token.
# For simplicity, we'll apply the dependency to the protected routes in the routers or globally with exceptions.

# Let's apply it globally but exclude /rs/auth/token and docs
# Or better, apply it in the routers.

app.include_router(rs_ge.router)
app.include_router(bank.router, dependencies=[Depends(verify_token)])
app.include_router(payment.router, dependencies=[Depends(verify_token)])

@app.get("/")
async def root():
    return {"message": "Mock API is running. Visit /docs for Swagger UI."}
