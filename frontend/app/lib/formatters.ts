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

export const formatResponse = async (response: Response): Promise<string> => {
  const prefix = `${response.status} Error`;

  const payload = await response.json().catch(() => null);
  if (payload?.detail) {
    if (Array.isArray(payload.detail)) {
      return `${prefix}\n${payload.detail
        .map((item: JSONValue) => item.summary ?? JSON.stringify(item))
        .join("\n")}`;
    }

    if (typeof payload.detail === "string") {
      return `${prefix}\n${payload.detail}`;
    }
  }

  const text = await response.text();
  return `${prefix}\n${text ?? response.statusText}`;
};
