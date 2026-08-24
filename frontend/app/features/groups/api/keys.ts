export const groupKeys = {
  all: ["group"] as const,

  lists: () => [...groupKeys.all, "list"] as const,

  details: () => [...groupKeys.all, "detail"] as const,

  detail: (id: string) => [...groupKeys.details(), id] as const,
};
