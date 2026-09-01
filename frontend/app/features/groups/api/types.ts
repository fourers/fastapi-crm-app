export interface Group {
  id: number;
  name: string | null;
  parent_id: number | null;
}

export interface GroupInput {
  name: string;
}

export interface GroupSummary {
  id: number;
  name: string;
}

export interface UserSummary {
  id: number;
  first_name: string;
  last_name: string;
}
