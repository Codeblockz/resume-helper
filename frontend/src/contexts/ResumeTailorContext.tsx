import React, { createContext, useReducer, useContext } from 'react';
import {
  WorkflowState,
  WorkflowDispatch,
  WorkflowActions,
  JobDescription,
  ResumeData,
  AnalysisResult
} from './types';

const initialState: WorkflowState = {
  step: 'home'
};

// Create context with default state and dispatch
export const ResumeTailorContext = createContext<{
  state: WorkflowState;
  dispatch: WorkflowDispatch;
}>({
  state: initialState,
  dispatch: () => undefined
});

// Reducer function to handle workflow actions
const workflowReducer = (state: WorkflowState, action: WorkflowActions): WorkflowState => {
  switch (action.type) {
    case 'SET_JOB_DESCRIPTION':
      return {
        ...state,
        jobDescription: action.payload,
        step: 'resumeUpload'
      };

    case 'SET_RESUME_DATA':
      return {
        ...state,
        resumeData: action.payload
      };

    case 'SET_ANALYSIS_RESULT':
      return {
        ...state,
        analysisResult: action.payload,
        step: 'analysisResults'
      };

    case 'NEXT_STEP':
      switch (state.step) {
        case 'home': return { ...state, step: 'jobDescription' };
        case 'jobDescription': return { ...state, step: 'resumeUpload' };
        case 'resumeUpload': return { ...state, step: 'analysisResults' };
        default: return state;
      }

    case 'RESET_WORKFLOW':
      return initialState;

    default:
      return state;
  }
};

// Context provider component
export const ResumeTailorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(workflowReducer, initialState);

  return (
    <ResumeTailorContext.Provider value={{ state, dispatch }}>
      {children}
    </ResumeTailorContext.Provider>
  );
};

// Custom hook to use workflow context
export const useWorkflow = () => {
  const context = useContext(ResumeTailorContext);
  if (context === undefined) {
    throw new Error('useWorkflow must be used within a ResumeTailorProvider');
  }
  return context;
};

// Action creators for convenience
export const setJobDescription = (jobDesc: JobDescription): WorkflowActions => ({
  type: 'SET_JOB_DESCRIPTION',
  payload: jobDesc
});

export const setResumeData = (resume: ResumeData): WorkflowActions => ({
  type: 'SET_RESUME_DATA',
  payload: resume
});

export const setAnalysisResult = (result: AnalysisResult): WorkflowActions => ({
  type: 'SET_ANALYSIS_RESULT',
  payload: result
});
