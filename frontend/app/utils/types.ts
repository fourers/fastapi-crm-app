export type JSONValue = Record<string, string | number | null>;

export class AuthError extends Error {
  constructor(message: string, options?: ErrorOptions) {
    super(message, options);
  }
}
