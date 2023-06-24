![](images/hot_logo.png)

[![All Contributors](https://img.shields.io/github/all-contributors/hotosm/fmtm?color=ee8449&style=flat-square)](#contributors-)

**Production Workflows**

| PyTest | Build & Deploy  | Wiki Docs |
|---|---|---|
| [![pytest](https://github.com/hotosm/fmtm/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/hotosm/fmtm/actions/workflows/pytest.yml) | [![Build and Deploy](https://github.com/hotosm/fmtm/actions/workflows/build_and_deploy.yml/badge.svg?branch=main)](https://github.com/hotosm/fmtm/actions/workflows/build_and_deploy.yml) | [![Publish Docs to Wiki](https://github.com/hotosm/fmtm/actions/workflows/wiki.yml/badge.svg?branch=main)](https://github.com/hotosm/fmtm/actions/workflows/wiki.yml) |

**Development Workflows**

| PyTest | Build & Deploy  |
|---|---|
| [![pytest](https://github.com/hotosm/fmtm/actions/workflows/pytest.yml/badge.svg?branch=development)](https://github.com/hotosm/fmtm/actions/workflows/pytest.yml) | [![Build and Deploy](https://github.com/hotosm/fmtm/actions/workflows/build_and_deploy.yml/badge.svg?branch=development)](https://github.com/hotosm/fmtm/actions/workflows/build_and_deploy.yml) |

# Field Mapping Tasking Manager (FMTM)

A project to provide tools for Open Mapping campaigns

While we have pretty good field mapping applications, we don’t have great tools to coordinate field mapping. However, we have most of the elements needed to create a field mapping-oriented version of the HOT Tasking Manager, which allows people to select specific areas and complete tasks in a coordinated, organized fashion.

It’s already possible to implement a sort of Field Mapping Tasking Manager workflow using existing tools (mostly based on ODK, particularly the new "select from map" functionality), but it’s pretty labor-intensive and tricky. We’re working on some automation to ease the pain points, which moves us closer to a fully-fledged Field Mapping Tasking Manager (FMTM).

Background and description of the project and idea are here: please have a look at this [blog](https://www.hotosm.org/updates/field-mapping-is-the-future-a-tasking-manager-workflow-using-odk/) if you haven't yet! [Overview, timeline & relevant links](https://docs.google.com/presentation/d/1UrBG1X4MXwVd8Ps498FDlAYvesIailjjPPJfR_B4SUs/edit#slide=id.g15c1f409958_0_0)
for the Field Mapping Tasking Manager (FMTM)

## [side project] FMTM Turkey Earthquake Response Support

Field mapping, especially for damage assessments, is limited by coordination of all the response actors in the affected areas. Yer Çizenler, and OSM community in Turkey, has reported that there is a huge coordination challenge for mapping impacted areas. It is nearly impossible to know what has already been mapped, and duplications and gaps in mapping pose a challenge to building an effective understanding of the impact.

In the wake of the 2010 Haiti earthquake, seeing a similar coordination challenge with mapping affected areas, OSM volunteers developed the Tasking Manager, which allowed mapping volunteers around the world to support building an open-source map of areas without map data. Now with over 500,000 volunteer mappers, the Tasking Manager is a go-to resource for volunteers to contribute to the development of OSM.

HOT is already in the early stages of developing the Field Mapping Tasking Manager (FMTM), but we now need to accelerate this effort and provide a working version for use as soon as possible to the OSM Turkey community and on-the-ground data collectors. We are asking for your developer contributions: calling for 4 developers to work with us on this for 2 weeks See [contributor guidance](https://github.com/hotosm/fmtm/wiki/Contribution) for more detail.

# How to contribute

👍🎉We are actively looking for contributors for this project- from design, user testing and both front and backend developers. We have a specific request for volunteer developers at the moment!
![image](https://user-images.githubusercontent.com/98902727/218812430-3c07b60e-4fd2-4f05-a289-bf37d6f0b9cd.png)
Please take a look at our [Wiki pages](https://github.com/hotosm/fmtm/wiki/Home/90b86d34ddd42f0eafd03ea7e6d443eb37db2df6) and [contributor guidance](https://github.com/hotosm/fmtm/wiki/Contribution) for more details! Reach out to us if any questions! 👍🎉

# Using OpenDataKit's Select From Map feature

As of mid-2022, ODK incorporates a new functionality, select from map, that allows field mappers to select an object from a map, view the existing attributes, and fill out a form adding new information and attributes to that object. For example, a mapper can approach a building, select that building from a map view within ODK on their mobile phone, and add the opening hours, number of floors, construction material, or any number of useful attributes in a well-structured questionnaire format

To prepare the appropriate map files for ODK, we are taking our inspiration from the [HOT Tasking Manager](https://tasks.hotosm.org/), which allows remote mappers to choose well-defined small "task" areas, ensuring full coverage of the project area and no unintended duplication of tasks.

# Users

## Campaign managers

Campaign managers select an Area of Interest (AOI) and organize field mappers to go out and collect data. They need to:

- Select an AOI polygon by creating a GeoJSON or by tracing a polygon in a Web map
- Choose a task division scheme (number of features or area per task, and possibly variations on what features to use as the preferred splitting lines)
- Provide specific instructions and guidance for field mappers on the project.
- Provide a URL to a mobile-friendly Web page where field mappers can, from their mobile phone, select a task that is not already "checked out" (or possibly simply allocate areas to the field mappers).
- See the status of tasks (open, "checked out", completed but not validated, requires rework, validated, etc) in the Web browser on their computer

## Field mappers

Field mappers select (or are allocated) individual tasks within a project AOI and use ODK Collect to gather data in those areas. They need to:

- Visit a mobile-friendly Web page where they can see available tasks on a map
- Choose an area and launch ODK Collect with the form corresponding to their allocated area pre-loaded

## Validators

Validators review the data collected by field mappers and assess its quality. If the data is good, the validators merge the portion of the data that belongs in OpenStreetMap to OSM. If it requires more work, the validators either fix it themselves (for minor stuff like spelling or capitalization mistakes that don't seem to be systematic) or inform the field mappers that they need to fix it. They need to:

- Access completed data sets of "submissions" as Comma Separated Values and/or OSM XML so that they can review it.
- Mark areas as validated or requiring rework
- Communicate with field mappers if rework is necessary
- Merge good-quality data into OSM (probably from JOSM).
- Mark areas as completed and merged.

# Info for developers

The basic setup here is:

## ODK Collect

A mobile data collection tool that functions on almost all Android phones. Field mappers use ODK Collect to select features such as buildings or amenities, and fill out forms with survey questions to collect attributes or data about those features (normally at least some of these attributes are intended to become OSM tags associated with those features).

The ODK Collect app connects to a back-end server (in this case ODK Central), which provides the features to be mapped and the survey form definitions.

## ODK Central server

An ODK Central server functions as the back end for the field data collectors. ODK Collect is an application that can be downloaded on Android phones. Devs must have access to an ODK Central server with a username and password granting admin credentials.

[Here are the instructions for setting up an ODK Central server on Digital Ocean](https://docs.getodk.org/central-install-digital-ocean/) (It's very similar on AWS)

## Field Mapping Tasking Manager Web App

The FMTM web app is a Python/Flask/Leaflet app that serves as a front end for the ODK Central server, using the [ODK Central API](https://odkcentral.docs.apiary.io/#) to allocate specific areas/features to individual mappers, and receive their data submissions.

![1](https://github.com/hotosm/fmtm/assets/97789856/305be31a-96b4-42df-96fc-6968e9bd4e5f)

### Manager Web Interface (with PC browser-friendlymap view)

A computer-screen-optimized web app that allows Campaign Managers to:

- Select AOIs
- Choose task-splitting schemes
- Provide instructions and guidance specific to the project
- View areas that are at various stages of completion
- Provide a project-specific URL that field mappers can access from their mobile phones to select and map tasks.

### Steps to create a project in FMTM

- Go to [fmtm](https://fmtm.hotosm.org/) .
- If you are new then on the top right cornor click on Sign up and create an account . Else , Sign in to your existing account .
- Click the '+ CREATE NEW PROJECT' button.
- Enter the project details.

![2](https://github.com/hotosm/fmtm/assets/97789856/97c38c80-aa0e-4fe2-b8a5-f4ee43a9a63a)

- Upload Area in the GEOJSON file format.

![3](https://github.com/hotosm/fmtm/assets/97789856/680eb831-790a-48f1-8997-c20b5213909d)

- Define the tasks of the project.

![Screenshot 2023-06-07 232152](https://github.com/hotosm/fmtm/assets/97789856/b735a661-d0f6-46b8-b548-5ad7b1928480)

- Select Form .

![Screenshot 2023-06-07 232316](https://github.com/hotosm/fmtm/assets/97789856/475a6070-4897-4e84-8050-6ecf024d0095)

- Click on Submit button.

### FMTM back end

A back end that converts the project parameters entered by the Campaign Manager in the Manager Web Interface into a corresponding ODK Central project. Its functions include:

- Convert the AOI into a bounding box and corresponding Overpass API query
- Download (using the Overpass API) the OSM features that will be mapped in that bounding box (buildings and/or amenities) as well as the OSM line features that will be used as cutlines to subdivide the area
- Trim the features within the bounding box but outside the AOI polygon
- Convert the polygon features into centroid points (needed because ODK select from map doesn't yet deal with polygons; this is likely to change in the future but for now we'll work with points only)
- Use line features as cutlines to create individual tasks (squares don't make sense for field mapping, neighborhoods delineated by large roads, watercourses, and railways do)
- Split the AOI into those tasks based on parameters set in the Manager Web Interface (number of features or area per task, splitting strategy, etc).
- Use the ODK Central API to create, on the associated ODK Central server:
  - A project for the whole AOI
  - One survey form for each split task (neighborhood)
    - This might require modifying the xlsforms (to update the version ID of the forms and change the name of the geography file being referred to). This is pretty straightforward using [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/), though we have to be careful to keep the location within the spreadsheet of these two items consistent.
  - GeoJSON feature collections for each form (the buildings/amenities or whatever)
  - An App User for each form, which in turn corresponds to a single task. When the ODK Collect app on a user's phone is configured to function as that App User, they have access to _only_ the form and features/area of that task.
  - A set of QR Codes and/or configuration files/strings for ODK Collect, one for each App User

### Field Mapper Web Interface (with mobile-friendly map view)

Ideally with a link that opens ODK Collect directly from the browser, but if that's hard, the fallback is downloading a QR code and importing it into ODK Collect.

## Contributors ✨

Thanks goes to these wonderful people:

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="http://ivangayton.net"><img src="https://avatars.githubusercontent.com/u/5991943?v=4?s=100" width="100px;" alt="Ivan Gayton"/><br /><sub><b>Ivan Gayton</b></sub></a><br /><a href="#projectManagement-ivangayton" title="Project Management">📆</a> <a href="https://github.com/hotosm/fmtm/commits?author=ivangayton" title="Code">💻</a> <a href="https://github.com/hotosm/fmtm/pulls?q=is%3Apr+reviewed-by%3Aivangayton" title="Reviewed Pull Requests">👀</a> <a href="#ideas-ivangayton" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.hotosm.org"><img src="https://avatars.githubusercontent.com/u/71342768?v=4?s=100" width="100px;" alt="Rob Savoye"/><br /><sub><b>Rob Savoye</b></sub></a><br /><a href="#maintenance-robsavoye" title="Maintenance">🚧</a> <a href="#mentoring-robsavoye" title="Mentoring">🧑‍🏫</a> <a href="https://github.com/hotosm/fmtm/commits?author=robsavoye" title="Code">💻</a> <a href="https://github.com/hotosm/fmtm/pulls?q=is%3Apr+reviewed-by%3Arobsavoye" title="Reviewed Pull Requests">👀</a> <a href="#ideas-robsavoye" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/krtonga"><img src="https://avatars.githubusercontent.com/u/7307817?v=4?s=100" width="100px;" alt="krtonga"/><br /><sub><b>krtonga</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=krtonga" title="Code">💻</a> <a href="https://github.com/hotosm/fmtm/commits?author=krtonga" title="Documentation">📖</a> <a href="#tool-krtonga" title="Tools">🔧</a> <a href="#ideas-krtonga" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/spwoodcock"><img src="https://avatars.githubusercontent.com/u/78538841?v=4?s=100" width="100px;" alt="Sam"/><br /><sub><b>Sam</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=spwoodcock" title="Code">💻</a> <a href="https://github.com/hotosm/fmtm/pulls?q=is%3Apr+reviewed-by%3Aspwoodcock" title="Reviewed Pull Requests">👀</a> <a href="#infra-spwoodcock" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#ideas-spwoodcock" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.hotosm.org/people/petya-kangalova/"><img src="https://avatars.githubusercontent.com/u/98902727?v=4?s=100" width="100px;" alt="Petya "/><br /><sub><b>Petya </b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=petya-kangalova" title="Documentation">📖</a> <a href="#eventOrganizing-petya-kangalova" title="Event Organizing">📋</a> <a href="#ideas-petya-kangalova" title="Ideas, Planning, & Feedback">🤔</a></td>
      <td align="center" valign="top" width="14.28%"><a href="http://zanrevenue.org"><img src="https://avatars.githubusercontent.com/u/52991565?v=4?s=100" width="100px;" alt="Mohamed Bakari Mohamed"/><br /><sub><b>Mohamed Bakari Mohamed</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=Mudi-business" title="Code">💻</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://www.scdhub.org"><img src="https://avatars.githubusercontent.com/u/4379874?v=4?s=100" width="100px;" alt="G. Willson"/><br /><sub><b>G. Willson</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=biomassives" title="Code">💻</a></td>
    </tr>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Ndacyayisenga-droid"><img src="https://avatars.githubusercontent.com/u/58124613?v=4?s=100" width="100px;" alt="Tayebwa Noah"/><br /><sub><b>Tayebwa Noah</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=Ndacyayisenga-droid" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/mohammadareeb95"><img src="https://avatars.githubusercontent.com/u/77102111?v=4?s=100" width="100px;" alt="Mohammad Areeb"/><br /><sub><b>Mohammad Areeb</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=mohammadareeb95" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/AugustHottie"><img src="https://avatars.githubusercontent.com/u/96122635?v=4?s=100" width="100px;" alt="AugustHottie"/><br /><sub><b>AugustHottie</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=AugustHottie" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Balofire"><img src="https://avatars.githubusercontent.com/u/102294666?v=4?s=100" width="100px;" alt="Ahmeed Etti-Balogun"/><br /><sub><b>Ahmeed Etti-Balogun</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=Balofire" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/Roseford"><img src="https://avatars.githubusercontent.com/u/75838716?v=4?s=100" width="100px;" alt="Uju"/><br /><sub><b>Uju</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=Roseford" title="Documentation">📖</a></td>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/neelimagoogly"><img src="https://avatars.githubusercontent.com/u/97789856?v=4?s=100" width="100px;" alt="Neelima Mohanty"/><br /><sub><b>Neelima Mohanty</b></sub></a><br /><a href="https://github.com/hotosm/fmtm/commits?author=neelimagoogly" title="Documentation">📖</a></td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td align="center" size="13px" colspan="7">
        <img src="https://raw.githubusercontent.com/all-contributors/all-contributors-cli/1b8533af435da9854653492b1327a23a4dbd0a10/assets/logo-small.svg">
          <a href="https://all-contributors.js.org/docs/en/bot/usage">Add your contributions</a>
        </img>
      </td>
    </tr>
  </tfoot>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
