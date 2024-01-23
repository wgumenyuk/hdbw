import { redirect } from "@sveltejs/kit";

// Intern
import { base } from "$app/paths";
import { logoutUser } from "$server/services/auth";

// Types
import type { PageServerLoad } from "./$types";

/**
    Wird ausgeführt, wenn die Seite lädt.
*/
export const load: PageServerLoad = async ({ cookies, locals }) => {
    await logoutUser(cookies, locals.user!);
    throw redirect(303, `${base}/login`);
};