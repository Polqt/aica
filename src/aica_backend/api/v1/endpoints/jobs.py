from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....db import models
from ....crud import crud_jobs, crud_profile
from .. import schemas
from ... import dependencies
# from ....core.vector_store import get_vector_store, create_profile_embedding
# from ....core.rag import get_rag_chain

router = APIRouter()

# Temporarily disabled while fixing certificate page
# @router.post('/match', response_model=schemas.jobs.MatchedJobsResponse)
# def get_job_matches(
#         current_user: models.User = Depends(dependencies.get_current_user)
# ):
#     profile = crud_profile.get_profile(current_user)
# 
#     # Check if user's profile is complete which is the resume builder
#     if not profile or not profile.summary:
#         raise HTTPException(status_code=400, detail="User profile is not yet complete. Please fill out all of the profile stage.")
# 
#     # Create an embedding from the user's profile
#     profile_embedding = create_profile_embedding(profile)
# 
#     # Query the vector store to get the IDs of the top N most similar jobs
#     vector_store = get_vector_store()
