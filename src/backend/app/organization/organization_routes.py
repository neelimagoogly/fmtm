# Copyright (c) 2022, 2023 Humanitarian OpenStreetMap Team
#
# This file is part of FMTM.
#
#     FMTM is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     FMTM is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with FMTM.  If not, see <https:#www.gnu.org/licenses/>.
#

from typing import Union,Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from fastapi.logger import logger as logger
from sqlalchemy.orm import Session

from ..db import database
from . import organization_crud

router = APIRouter(
    prefix="/organization",
    tags=["organization"],
    dependencies=[Depends(database.get_db)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
def get_organisations(
    db: Session = Depends(database.get_db),

):
    """Get api for fetching organization list."""
    organizations = organization_crud.get_organisations(db)
    return organizations


@router.post("/")
async def create_organization(
    name: str = Form(),  # Required field for organization name
    description: str = Form(None),  # Optional field for organization description
    url: str = Form(None),  # Optional field for organization URL
    logo: UploadFile = File(None),  # Optional field for organization logo
    db: Session = Depends(database.get_db),  # Dependency for database session
):
    """
    Create an organization with the given details.

    Parameters:
        name (str): The name of the organization. Required.
        description (str): The description of the organization. Optional.
        url (str): The URL of the organization. Optional.
        logo (UploadFile): The logo of the organization. Optional.
        db (Session): The database session. Dependency.

    Returns:
        dict: A dictionary with a message indicating successful creation of the organization.
    """
    # Check if the organization with the same already exists
    if await organization_crud.get_organisation_by_name(db, name=name):
        raise HTTPException(status_code=400, detail=f"Organization already exists with the name {name}")

    await organization_crud.create_organization(db, name, description, url, logo)

    return {"Message": "Organization Created Successfully."}
