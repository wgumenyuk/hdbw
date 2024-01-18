import { json as response } from "@sveltejs/kit";

/**
    Schickt ein JSON-Objekt als Antwort zurück.
*/
export const json = (status: number, data: Record<string, any>) => {
    return response(data, {
        status
    });
};