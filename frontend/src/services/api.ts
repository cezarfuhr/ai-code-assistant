/**
 * API service for communicating with the backend.
 */
import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface CodeGenerationRequest {
  prompt: string;
  language: string;
  context?: string;
}

export interface CodeExplanationRequest {
  code: string;
  language: string;
}

export interface BugDetectionRequest {
  code: string;
  language: string;
}

export interface RefactorRequest {
  code: string;
  language: string;
  instructions?: string;
}

export interface DocumentationRequest {
  code: string;
  language: string;
  style?: string;
}

export interface Bug {
  line: number | null;
  severity: string;
  description: string;
  suggestion: string;
}

export interface CodeResponse {
  success: boolean;
  code?: string;
  explanation?: string;
  bugs?: Bug[];
  language: string;
}

export interface HealthResponse {
  status: string;
  version: string;
  service: string;
}

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api/v1`,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 60000, // 60 seconds for AI operations
    });
  }

  async healthCheck(): Promise<HealthResponse> {
    const response = await this.client.get<HealthResponse>('/health');
    return response.data;
  }

  async generateCode(request: CodeGenerationRequest): Promise<CodeResponse> {
    const response = await this.client.post<CodeResponse>('/generate', request);
    return response.data;
  }

  async explainCode(request: CodeExplanationRequest): Promise<CodeResponse> {
    const response = await this.client.post<CodeResponse>('/explain', request);
    return response.data;
  }

  async detectBugs(request: BugDetectionRequest): Promise<CodeResponse> {
    const response = await this.client.post<CodeResponse>('/detect-bugs', request);
    return response.data;
  }

  async refactorCode(request: RefactorRequest): Promise<CodeResponse> {
    const response = await this.client.post<CodeResponse>('/refactor', request);
    return response.data;
  }

  async generateDocumentation(request: DocumentationRequest): Promise<CodeResponse> {
    const response = await this.client.post<CodeResponse>('/document', request);
    return response.data;
  }
}

export const apiService = new APIService();
