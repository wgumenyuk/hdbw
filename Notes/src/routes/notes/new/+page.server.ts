import { redirect } from "@sveltejs/kit";

// Intern
import { base } from "$app/paths";
import { logger } from "$server/logger";
import {
    createNote,
    noteSchema
} from "$server/services/notes";

// Types
import type { Actions } from "./$types";

/**
    Form-Actions.
*/
export const actions: Actions = {
    async default({ locals, request }) {
        const data = Object.fromEntries(await request.formData());
        const form = await noteSchema.safeParseAsync(data);

        if(!form.success) {
            return {
                success: false,
                error: form.error.issues[0].message
            };
        }

        try {
            const { error } = await createNote(locals.user!, form.data);

            if(error) {
                return {
                    success: false,
                    error
                };
            }
        } catch(err) {
            logger.error(err, "[Notiz] Notiz konnte nicht gespeichert werden");

            return {
                success: false,
                error: "Ein unbekannter Fehler ist aufgetreten."
            };
        }

        throw redirect(303, `${base}/notes`);
    }
};