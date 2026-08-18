export async function apiFetch<T>(
  input: RequestInfo | URL,
  init?: RequestInit,
): Promise<T> {
  const response = await fetch(input, init);

  if (!response.ok) {
    throw new Error(await formatResponse(response));
  }

  return response.json();
}

async function formatResponse(response: Response): Promise<string> {
  const prefix = response.status ? `${response.status}: ` : "";
  const text = await response.text();
  return `${prefix}${text || response.statusText}`;
}
