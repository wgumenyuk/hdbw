import { redirect } from "@sveltejs/kit";

// Intern
import { base } from "$app/paths";

// Types
import type { PageServerLoad } from "./$types";

/**
    Wird ausgeführt, wenn die Seite lädt.
*/
export const load: PageServerLoad = ({ locals }) => {
    throw redirect(303, (locals.user) ? `${base}/notes` : `${base}/login`);
};