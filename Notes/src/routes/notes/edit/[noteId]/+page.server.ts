import { redirect } from "@sveltejs/kit";

// Intern
import { logger } from "$server/logger";
import {
    noteSchema,
    getNote,
    updateNote
} from "$server/services/notes";

// Types
import type { Actions, PageServerLoad } from "./$types";

/**
    Wird ausgeführt, wenn die Seite lädt.
*/
export const load: PageServerLoad = async ({ params, locals }) => {
    const { noteId } = params;

    return {
        note: await getNote(locals.user!, noteId)
    };
};

/**
    Form-Actions.
*/
export const actions: Actions = {
    async default({ params, locals, request }) {
        const { noteId } = params;

        const data = Object.fromEntries(await request.formData());
        const form = await noteSchema.safeParseAsync(data);

        if(!form.success) {
            return {
                success: false,
                error: form.error.issues[0].message
            };
        }

        try {
            const { error } = await updateNote(locals.user!, noteId, form.data);

            if(error) {
                return {
                    success: false,
                    error
                };
            }
        } catch(err) {
            logger.error(err, "[Notiz] Notiz konnte nicht aktualisiert werden");

            return {
                success: false,
                error: "Ein unbekannter Fehler ist aufgetreten."
            };
        }

        throw redirect(303, "/notes");
    }
};