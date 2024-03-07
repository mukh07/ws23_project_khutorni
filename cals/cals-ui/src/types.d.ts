export interface Workflow {
  id: number;
  name: string;
  // description?: string;
  batch_size: number;
  created_by: number;
}

export interface Project {
  id: number;
  name: string;
  image?: URL;
  description: string;
  owner_id: number;
  assignee_id?: number;
}
