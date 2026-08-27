export interface Group {
  id: number;
  name: string | null;
  parent_id: number | null;
}

export interface UserSummary {
  id: number;
  first_name: string;
  last_name: string;
}
