import type { JSONValue } from "~/lib/types";

export const formatName = (data: JSONValue | undefined) => {
  const firstName = data?.first_name;
  const lastName = data?.last_name;

  return (
    [firstName, lastName]
      .filter(
        (name): name is string =>
          typeof name === "string" && name.trim() !== "",
      )
      .map((name) => name.trim())
      .join(" ") || "Unknown"
  );
};
