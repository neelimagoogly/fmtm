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

import csv
import io
import os
import zipfile
import json
from datetime import datetime
import logging
from fastapi import HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..central.central_crud import get_odk_form, get_odk_project
from ..tasks import tasks_crud
from ..projects import project_crud, project_schemas
from osm_fieldwork.json2osm import JsonDump
from pathlib import Path
from fastapi.logger import logger as logger


def get_submission_of_project(db: Session, project_id: int, task_id: int = None):
    """Gets the submission of project.
    This function takes project_id and task_id as a parameter.
    If task_id is provided, it returns all the submission made to that particular task, else all the submission made in the projects are returned.
    """
    project_info = project_crud.get_project(db, project_id)

    # Return empty list if project is not found
    if not project_info:
        return []

    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title
    project_tasks = project_info.tasks

    if not (
        project_info.odk_central_url
        or project_info.odk_central_user
        or project_info.odk_central_password
    ):
        raise HTTPException(
            status_code=404, detail="ODK Central Credentials not found in project"
        )

    # ODK Credentials
    odk_credentials = project_schemas.ODKCentral(
        odk_central_url=project_info.odk_central_url,
        odk_central_user=project_info.odk_central_user,
        odk_central_password=project_info.odk_central_password,
    )

    xform = get_odk_form(odk_credentials)

    # If task id is not provided, submission for all the task are listed
    if task_id is None:
        task_list = []

        task_list = [x.id for x in project_tasks]

        data = []

        for id in task_list:

            # XML Form Id is a combination or project_name, category and task_id
            xml_form_id = f"{project_name}_{form_category}_{id}".split("_")[2]
            submission_list = xform.listSubmissions(odkid, xml_form_id)

            # data.append(submission_list)
            if isinstance(submission_list, list):
                for submission in submission_list:
                    data.append(submission)
        return data

    else:
        # If task_id is provided, submission made to this particular task is returned.
        xml_form_id = f"{project_name}_{form_category}_{task_id}".split("_")[2]
        submission_list = xform.listSubmissions(odkid, xml_form_id)
        for x in submission_list:
            x["submitted_by"] = f"{project_name}_{form_category}_{task_id}"
        return submission_list


def get_forms_of_project(db: Session, project_id: int):
    project_info = project_crud.get_project_by_id(db, project_id)

    # Return empty list if project is not found
    if not project_info:
        return []

    odkid = project_info.odkid
    project = get_odk_project()

    result = project.listForms(odkid)
    return result


def list_app_users_or_project(db: Session, project_id: int):
    project_info = project_crud.get_project_by_id(db, project_id)

    # Return empty list if project is not found
    if not project_info:
        return []

    odkid = project_info.odkid
    project = get_odk_project()
    result = project.listAppUsers(odkid)
    return result


def create_zip_file(files, output_file_path):
    with zipfile.ZipFile(output_file_path, mode="w") as zip_file:
        for file_path in files:
            zip_file.write(file_path)
    return output_file_path


async def convert_to_osm_for_task(odk_id: int, form_id: int, xform: any):

    # This file stores the submission data.
    file_path = f"/tmp/{odk_id}_{form_id}.json"

    # Get the submission data from ODK Central
    file = xform.getSubmissions(odk_id, form_id, None, False, True)

    with open(file_path, "wb") as f:
        f.write(file)

    jsonin = JsonDump()
    infile = Path(file_path)

    base = os.path.splitext(infile.name)[0]

    osmoutfile = f"/tmp/{base}.osm"
    jsonin.createOSM(osmoutfile)

    jsonoutfile = f"/tmp/{base}.geojson"
    jsonin.createGeoJson(jsonoutfile)

    data = jsonin.parse(infile.as_posix())

    for entry in data:
        feature = jsonin.createEntry(entry)
        # Sometimes bad entries, usually from debugging XForm design, sneak in
        if len(feature) == 0:
            continue
        if len(feature) > 0:
            if "lat" not in feature["attrs"]:
                if 'geometry' in feature['tags']:
                    if type(feature['tags']['geometry']) == str:
                        coords = list(feature['tags']['geometry'])
                        # del feature['tags']['geometry']
                    else:
                        coords = feature['tags']['geometry']['coordinates']
                        # del feature['tags']['geometry']
                    feature['attrs'] = {'lat': coords[1], 'lon': coords[0]}
                else:
                    logger.warning("Bad record! %r" % feature)
                    continue
            jsonin.writeOSM(feature)
            jsonin.writeGeoJson(feature)

    jsonin.finishOSM()
    jsonin.finishGeoJson()
    logger.info("Wrote OSM XML file: %r" % osmoutfile)
    logger.info("Wrote GeoJson file: %r" % jsonoutfile)

    return osmoutfile, jsonoutfile


async def convert_to_osm(db: Session, project_id: int, task_id: int):

    project_info = project_crud.get_project(db, project_id)

    # Return exception if project is not found
    if not project_info:
        raise HTTPException(status_code=404, detail="Project not found")

    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title

    # ODK Credentials
    odk_credentials = project_schemas.ODKCentral(
        odk_central_url=project_info.odk_central_url,
        odk_central_user=project_info.odk_central_user,
        odk_central_password=project_info.odk_central_password,
    )

    # Get ODK Form with odk credentials from the project.
    xform = get_odk_form(odk_credentials)

    # XML Form Id is a combination or project_name, category and task_id
    xml_form_id = f"{project_name}_{form_category}_{task_id}".split("_")[2]

    # Get the task lists of the project if task_id is not provided
    tasks = [task_id] if task_id else await tasks_crud.get_task_lists(db, project_id)

    # Create a new ZIP file for the extracted files
    final_zip_file_path = f"{project_name}_{form_category}_osm.zip"

    for task in tasks:
        xml_form_id = f"{project_name}_{form_category}_{task}".split("_")[2]

        # Get the osm xml and geojson files for the task
        osmoutfile, jsonoutfile = await convert_to_osm_for_task(odkid, xml_form_id, xform)

        # Add the files to the ZIP file
        with zipfile.ZipFile(final_zip_file_path, mode="a") as final_zip_file:
            final_zip_file.write(osmoutfile)
            final_zip_file.write(jsonoutfile)

    return FileResponse(final_zip_file_path)


def download_submission(db: Session, project_id: int, task_id: int, exportJson: bool):

    project_info = project_crud.get_project(db, project_id)

    # Return empty list if project is not found
    if not project_info:
        raise HTTPException(status_code=404, detail="Project not found")

    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title
    project_tasks = project_info.tasks

    # ODK Credentials
    odk_credentials = project_schemas.ODKCentral(
        odk_central_url=project_info.odk_central_url,
        odk_central_user=project_info.odk_central_user,
        odk_central_password=project_info.odk_central_password,
    )

    # Get ODK Form with odk credentials from the project.
    xform = get_odk_form(odk_credentials)

    if not exportJson:
        file_path = f"{project_id}_submissions.zip"

        # If task id is not provided, submission for all the task are listed
        if task_id is None:
            task_list = []

            task_list = [x.id for x in project_tasks]

            # zip_file_path = f"{project_name}_{form_category}_submissions.zip"  # Create a new ZIP file for all submissions
            files = []

            for id in task_list:

                # XML Form Id is a combination or project_name, category and task_id
                # FIXME: fix xml_form_id
                xml_form_id = f"{project_name}_{form_category}_{id}".split("_")[
                    2]
                file = xform.getSubmissionMedia(odkid, xml_form_id)

                # Create a new output file for each submission
                file_path = f"{project_name}_{form_category}_submission_{id}.zip"
                with open(file_path, "wb") as f:
                    f.write(file.content)

                files.append(
                    file_path
                )  # Add the output file path to the list of files for the final ZIP file

            extracted_files = []
            for file_path in files:
                with zipfile.ZipFile(file_path, "r") as zip_file:
                    zip_file.extractall(
                        os.path.splitext(file_path)[0]
                    )  # Extract the contents of the nested ZIP files to a directory with the same name as the ZIP file
                    extracted_files += [
                        os.path.join(os.path.splitext(file_path)[0], f)
                        for f in zip_file.namelist()
                    ]  # Add the extracted file paths to the list of extracted files

            # Create a new ZIP file for the extracted files
            final_zip_file_path = f"{project_name}_{form_category}_submissions_final.zip"
            with zipfile.ZipFile(final_zip_file_path, mode="w") as final_zip_file:
                for file_path in extracted_files:
                    final_zip_file.write(file_path)

            return FileResponse(final_zip_file_path)
        else:
            xml_form_id = f"{project_name}_{form_category}_{task_id}".split("_")[
                2]
            file = xform.getSubmissionMedia(odkid, xml_form_id)
            with open(file_path, "wb") as f:
                f.write(file.content)
            return FileResponse(file_path)
    else:
        timestamp = datetime.now().strftime("%Y_%m_%d")
        headers = {
            "Content-Disposition": f"attachment; filename=Submission_data_{timestamp}.json",
            "Content-Type": "application/json",
        }

        files = []

        if task_id is None:
            task_list = [x.id for x in project_tasks]
            for id in task_list:
                xml_form_id = f"{project_name}_{form_category}_{id}".split("_")[
                    2]
                file = xform.getSubmissions(
                    odkid, xml_form_id, None, False, True)
                json_data = json.loads(file)
                json_data_value = json_data.get('value')
                if json_data_value:
                    files.extend(json_data_value)
        else:
            xml_form_id = f"{project_name}_{form_category}_{task_id}".split("_")[
                2]
            file = xform.getSubmissions(odkid, xml_form_id, None, False, True)
            json_data = json.loads(file)

        response_content = json.dumps(
            files if task_id is None else json_data, indent=4).encode()

        return Response(content=response_content, headers=headers)


def get_submission_points(db: Session, project_id: int, task_id: int = None):
    """Gets the submission points of project.
    This function takes project_id and task_id as a parameter.
    If task_id is provided, it returns all the submission points made to that particular task,
        else all the submission points made in the projects are returned.
    """
    project_info = project_crud.get_project_by_id(db, project_id)

    # Return empty list if project is not found
    if not project_info:
        raise HTTPException(status_code=404, detail="Project not found")

    odkid = project_info.odkid
    project_name = project_info.project_name_prefix
    form_category = project_info.xform_title

    # ODK Credentials
    odk_credentials = project_schemas.ODKCentral(
        odk_central_url=project_info.odk_central_url,
        odk_central_user=project_info.odk_central_user,
        odk_central_password=project_info.odk_central_password,
    )

    xform = get_odk_form(odk_credentials)

    if task_id:
        xml_form_id = f"{project_name}_{form_category}_{task_id}".split("_")[
            2
        ]  # FIXME: fix xml_form_id
        # file_path = f"{project_id}_submissions.zip"
        response_file = xform.getSubmissionMedia(odkid, xml_form_id)

        # Create a file-like object from the bytes object
        response_file_obj = io.BytesIO(response_file.content)
        try:
            # Open the zipfile
            with zipfile.ZipFile(response_file_obj, "r") as zip_ref:
                # Find the CSV file in the zipfile (assuming it has a .csv extension)
                csv_filename = [
                    f for f in zip_ref.namelist() if f.endswith(".csv")][0]
                # Open the CSV file
                with zip_ref.open(csv_filename) as csv_file:
                    # Read the CSV data
                    csv_reader = csv.DictReader(io.TextIOWrapper(csv_file))
                    geometry = []
                    for row in csv_reader:
                        # Check if the row contains the 'warmup-Latitude' and 'warmup-Longitude' columns
                        # FIXME: fix the column names (they might not be same warmup-Latitude and warmup-Longitude)
                        if "warmup-Latitude" in row and "warmup-Longitude" in row:
                            point = (row["warmup-Latitude"],
                                     row["warmup-Longitude"])

                            # Create a GeoJSON Feature object
                            geometry.append(
                                {
                                    "type": "Feature",
                                    "geometry": {"type": "Point", "coordinates": point},
                                }
                            )
                            # points.append(point)
                return geometry
        except zipfile.BadZipFile:
            print("The file is not a valid zip file.")
            return None
    else:
        return None
