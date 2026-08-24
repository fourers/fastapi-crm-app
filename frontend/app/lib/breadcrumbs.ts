export interface HeaderPath {
  href: string;
  displayName: string;
}

export const headerPaths = {
  home: () => [{ href: "/", displayName: "Home" }] as HeaderPath[],
  clients: () =>
    [
      ...headerPaths.home(),
      { href: "/clients", displayName: "Clients" },
    ] as HeaderPath[],
  groups: () =>
    [
      ...headerPaths.home(),
      { href: "/groups", displayName: "Groups" },
    ] as HeaderPath[],
};
