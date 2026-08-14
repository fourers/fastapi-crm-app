import { createStore } from "~/stores/factory";
import { type JSONValue } from "~/utils/types";

export const useUserStore = createStore<JSONValue[]>("/api/user", []);
