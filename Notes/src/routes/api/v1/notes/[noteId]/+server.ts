import { logger } from "$server/logger";
import { json } from "$server/json";
import { deleteNote } from "$server/services/notes";

// Types
import type { RequestHandler } from "./$types";

/**
    Löscht eine Notiz.
*/
export const DELETE: RequestHandler = async ({ locals, params }) => {
    const { noteId } = params;

    try {
        const { error } = await deleteNote(locals.user!, noteId);

        if(error) {
            return json(400, {
                success: false,
                error
            });
        }
    } catch(err) {
        logger.error(err, "[Notiz] Notiz konnte nicht gelöscht werden");

        return json(500, {
            success: false,
            error: "Ein unbekannter Fehler ist aufgetreten."
        });
    }

    return json(200, {
        success: true
    });
};