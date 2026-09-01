export const groupKeys = {
  all: ["group"] as const,

  lists: () => [...groupKeys.all, "list"] as const,

  details: () => [...groupKeys.all, "detail"] as const,

  detail: (id: string) => [...groupKeys.details(), id] as const,

  users: () => [...groupKeys.all, "user"] as const,

  user: (id: string) => [...groupKeys.users(), id] as const,

  subgroups: () => [...groupKeys.all, "subgroup"] as const,

  subgroup: (id: string) => [...groupKeys.subgroups(), id] as const,
};
