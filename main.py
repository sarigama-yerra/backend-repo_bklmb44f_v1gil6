import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents
from schemas import Lead, Newsletter, Testimonial

app = FastAPI(title="Northmann Group API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Northmann Group backend running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# ------------------------
# Business endpoints
# ------------------------

@app.post("/api/leads")
async def create_lead(lead: Lead):
    try:
        doc_id = create_document("lead", lead)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/newsletter")
async def subscribe(newsletter: Newsletter):
    try:
        doc_id = create_document("newsletter", newsletter)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TestimonialsResponse(BaseModel):
    items: List[Testimonial]


@app.get("/api/testimonials", response_model=TestimonialsResponse)
async def list_testimonials(limit: int = 10):
    try:
        docs = get_documents("testimonial", {}, limit)
        # Convert ObjectId and unknown fields gracefully
        cleaned = []
        for d in docs:
            item = {
                "author": d.get("author", ""),
                "role": d.get("role"),
                "quote": d.get("quote", "")
            }
            cleaned.append(item)
        # Provide graceful defaults if empty
        if not cleaned:
            cleaned = [
                {"author": "Fortune 500 COO", "role": "Manufacturing",
                 "quote": "Their team delivered measurable value within the first quarter."},
                {"author": "Private Equity Partner", "role": "Portfolio Ops",
                 "quote": "A rare blend of strategic clarity and execution discipline."}
            ]
        return {"items": cleaned[:limit]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
