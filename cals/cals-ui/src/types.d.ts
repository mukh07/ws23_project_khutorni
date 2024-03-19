export interface WorkflowMetadata {
  status: string;
  current_task: number;
}

export interface Workflow {
  name: string;
  description?: string;
  created_at: string;
  project_id: number;
  batch_size: number;
  model: string;
  query_strategy: string;
  completed: number;
  queued: number;
  selected?: number;
  metadata: WorkflowMetadata;
}

interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
}

export interface Project {
  id: number;
  url: string;
  name: string;
  dimension: string;
  status: string;
  created_date: string;
  updated_date: string;
  tasks_count: number;
  task_subsets: string[];
  owner: User;
  assignee?: User,
}