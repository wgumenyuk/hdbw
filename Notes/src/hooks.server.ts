import { redirect } from "@sveltejs/kit";

// Intern
import { redis, initRedis } from "$server/databases/redis";
import { initMongodDb } from "$server/databases/mongoose";
import { getCookie, deleteCookie } from "$server/services/cookies";
import { SESSION_COOKIE_NAME } from "$server/services/auth";

// Types
import type { Handle } from "@sveltejs/kit";

// Datenbanken initialisieren
await Promise.all([
    initRedis(),
    initMongodDb()
]);

/**
    Routen, die ohne Anmeldung aufgerufen werden können.
*/
const UNPROTECTED_ROUTES = [
    "/login",
    "/register"
];

/**
    Verarbeitet eine Serveranfrage.
*/
export const handle: Handle = async ({ event, resolve }) => {
    const { cookies, locals, url } = event;

    if(UNPROTECTED_ROUTES.includes(url.pathname)) {
        return resolve(event);
    }

    const sessionId = getCookie(cookies, SESSION_COOKIE_NAME);

    if(!sessionId) {
        throw redirect(303, "/login");
    }

    // Sitzung aus Redis abrufen
    const [ userId, username, passwordKey, loggedInAt ] = await Promise.all([
        redis.get(`${sessionId}:id`),
        redis.get(`${sessionId}:username`),
        redis.get(`${sessionId}:key`),
        redis.get(`${sessionId}:loggedInAt`)
    ]);

    if(!userId || !username || !passwordKey || !loggedInAt) {
        deleteCookie(cookies, SESSION_COOKIE_NAME);
        throw redirect(303, "/login");
    }

    locals.user = {
        userId,
        username,
        passwordKey,
        loggedInAt: parseInt(loggedInAt)
    };

    return resolve(event);
};