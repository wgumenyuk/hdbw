import { redirect } from "@sveltejs/kit";


// Intern
import { logger } from "$server/logger";
import {
    authSchema,
    registerUser
} from "$server/services/auth";

// Types
import type { Actions, PageServerLoad } from "./$types";

/**
    Wird ausgeführt, wenn die Seite lädt.
*/
export const load: PageServerLoad = ({ locals }) => {
    if(locals.user) {
        throw redirect(303, "/notes");
    }
};

/**
    Form-Actions.
*/
export const actions: Actions = {
    async default({ request }) {
        const data = Object.fromEntries(await request.formData());
        const form = await authSchema.safeParseAsync(data);

        if(!form.success) {
            return {
                success: false,
                error: form.error.issues[0].message
            };
        }

        try {
            const { error } = await registerUser(form.data);
            
            if(error) {
                return {
                    success: false,
                    error
                };
            }
        } catch(err) {
            logger.error(err, "[Auth] Registrierung fehlgeschlagen");

            return {
                success: false,
                error: "Ein unbekannter Fehler ist aufgetreten."
            };
        }

        throw redirect(303, "/login");
    }
};