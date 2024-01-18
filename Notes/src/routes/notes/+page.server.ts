import { getNotes } from "$server/services/notes";

// Types
import type { PageServerLoad } from "./$types";

/**
    Wird ausgeführt, sobald die Seite lädt.
*/
export const load: PageServerLoad = async ({ locals }) => {
    return {
        notes: await getNotes(locals.user!)
    };
};