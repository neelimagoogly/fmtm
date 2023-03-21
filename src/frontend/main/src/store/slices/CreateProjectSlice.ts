import CoreModules from "../../shared/CoreModules";


const CreateProject = CoreModules.createSlice({
    name: 'createproject',
    initialState: {
        projectDetails:{},
        projectDetailsResponse:null,
        projectDetailsLoading:false,
        projectArea:null,
        projectAreaLoading:false,
    },
    reducers: {
        SetProjectDetails(state, action) {
            state.projectDetails = {...state.projectDetails,[action.payload.key]:action.payload.value}
        },
        CreateProjectLoading(state, action) {
            state.projectDetailsLoading = action.payload
        },
        PostProjectDetails(state, action) {
            state.projectDetailsResponse = action.payload
        },
        ClearCreateProjectFormData(state, action) {
            state.projectDetailsResponse = null
            state.projectDetails = {}
            state.projectArea = null
        },
        UploadAreaLoading(state, action) {
            state.projectAreaLoading = action.payload
        },
        PostUploadAreaSuccess(state, action) {
            state.projectArea = action.payload
        },
    }
})


export const CreateProjectActions = CreateProject.actions;
export default CreateProject;