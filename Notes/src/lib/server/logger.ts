import pino from "pino";

// Intern
import { dev as isDev } from "$app/environment";

/**
    Logger.
*/
export const logger = pino({
    level: (isDev) ? "debug" : "info",
    transport: {
        target: "pino-pretty"
    }
});