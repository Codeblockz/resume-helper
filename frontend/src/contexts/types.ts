export interface JobDescription {
  jobTitle: string;
  company?: string;
  description: string;
}

export interface ResumeData {
  content: string;
  sections?: { [key: string]: string };
}

export interface AnalysisResult {
  resumeScore?: number;
  jobMatchPercentage?: number;
  improvementsSuggested?: string[];
  keywordsAnalysis?: {
    matched: string[];
    missing: string[];
  };
  tailoredResumePreview?: string;
}

export interface WorkflowState {
  step: 'home' | 'jobDescription' | 'resumeUpload' | 'analysisResults';
  jobDescription?: JobDescription;
  resumeData?: ResumeData;
  analysisResult?: AnalysisResult;
}

export type WorkflowDispatch = React.Dispatch<WorkflowActions>;

export type WorkflowActions =
  | { type: 'SET_JOB_DESCRIPTION'; payload: JobDescription }
  | { type: 'SET_RESUME_DATA'; payload: ResumeData }
  | { type: 'SET_ANALYSIS_RESULT'; payload: AnalysisResult }
  | { type: 'NEXT_STEP' }
  | { type: 'RESET_WORKFLOW' };
