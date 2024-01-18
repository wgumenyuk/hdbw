import { dev as isDev } from "$app/environment";

// Types
import type { Cookies } from "@sveltejs/kit";

/**
    Setzt einen Cookie.
*/
export const setCookie = (
    cookies: Cookies,
    name: string,
    value: string,
    expiresIn?: number
) => {
    cookies.set(
        name,
        value,
        {
            path: "/",
            sameSite: true,
            httpOnly: true,
            secure: !isDev,
            maxAge: expiresIn || 60 * 60 * 24 * 7
        }
    );
};

/**
    Ruft einen Cookie ab.
*/
export const getCookie = (cookies: Cookies, name: string) => {
    return cookies.get(name);
};

/**
    Löscht einen Cookie.
*/
export const deleteCookie = (cookies: Cookies, name: string) => {
    cookies.delete(name, {
        path: "/"
    });
};