import { z } from "zod";

// Intern
import { logger } from "$server/logger";
import { redis } from "$server/databases/redis";
import { User } from "$server/models/user";
import {
    scrypt,
    randomId,
    randomBytes,
    encryptAes,
    hashPassword,
    comparePassword
} from "$server/services/crypto";
import { setCookie, deleteCookie } from "$server/services/cookies";

// Types
import type { Cookies } from "@sveltejs/kit";

/**
    Name des Sitzungs-Cookies.
*/
export const SESSION_COOKIE_NAME = "sessionId";

/**
    Gültigkeit des Sitzungs-Cookies.
*/
export const SESSION_EXPIRES_IN = 60 * 60 * 24 * 7;

/**
    Regex für Nutzernamen.
*/
const USERNAME_REGEX = /[a-z]/;

/**
    Regex für Passwörter.
*/
const PASSWORD_REGEX = /[A-z0-9*.!@#$%^&(){}[\]:;<>,/~_+-=|]/;

/**
    Schema für das Anmelde- und Registrierungsformular.
*/
export const authSchema = z.object({
    // Nutzername
    username: z
        .string()
        .min(1, "Gebe einen Nutzernamen an.")
        .max(16, "Der Nutzername darf maximal 16 Zeichen lang sein.")
        .regex(
            USERNAME_REGEX,
            "Der Nutzername darf nur aus Kleinbuchstaben bestehen."
        ),

    // Passwort
    password: z
        .string()
        .min(6, "Das Passwort muss mindestens 6 Zeichen lang sein.")
        .max(32, "Das Passwort darf maximal 32 Zeichen lang sein.")
        .regex(PASSWORD_REGEX, "Gebe ein gültiges Passwort an")
});

/**
    Leitet den Passwort-Schlüssel aus einem Passwort ab.
*/
const derivePasswordKey = async (password: string, createdAt: number) => {
    const key = await scrypt(
        password,
        Buffer.from(createdAt.toString())
    );

    return key.toString("hex");
};

/**
    Meldet einen Nutzer an.
*/
export const loginUser = async (
    cookies: Cookies,
    data: z.infer<typeof authSchema>
): App.ServiceResult<null> => {
    const { username, password } = data;

    const user = await User.findOne({
        username
    });

    if(!user) {
        return {
            success: false,
            error: "Der Nutzername wurde nicht gefunden."
        };
    }

    const isPasswordOk = await comparePassword(password, user.password);

    if(!isPasswordOk) {
        return {
            success: false,
            error: "Das Passwort stimmt nicht überein."
        };
    }

    const sessionId = randomId();
    const passwordKey = await derivePasswordKey(password, user.createdAt);

    // Sitzung in Redis speichern
    await Promise.all([
        redis.set(`${sessionId}:id`, user.id, "EX", SESSION_EXPIRES_IN),
        redis.set(`${sessionId}:username`, username, "EX", SESSION_EXPIRES_IN),
        redis.set(`${sessionId}:key`, passwordKey, "EX", SESSION_EXPIRES_IN),
        redis.set(`${sessionId}:loggedInAt`, Date.now(), "EX", SESSION_EXPIRES_IN)
    ]);
    
    setCookie(
        cookies,
        SESSION_COOKIE_NAME,
        sessionId,
        SESSION_EXPIRES_IN
    );

    logger.info(`[Auth] Nutzer "${username}" angemeldet`);

    return {
        success: true,
        data: null
    };
};

/**
    Registriert einen neuen Nutzer.
*/
export const registerUser = async (
    data: z.infer<typeof authSchema>
): App.ServiceResult<null> => {
    const { username, password } = data;

    const isUsernameTaken = await User.exists({
        username
    });

    if(isUsernameTaken) {
        return {
            success: false,
            error: "Der Nutzername ist bereits vergeben."
        };
    }

    const createdAt = Date.now();

    const passwordHash = await hashPassword(password);
    const passwordKey = await derivePasswordKey(password, createdAt);
    
    const dataKey = await encryptAes(
        randomBytes(16).toString("hex"),
        passwordKey
    );

    const user = await User.create({
        id: randomId(),
        username,
        password: passwordHash,
        dataKey,
        createdAt
    });

    await user.save();

    logger.info(`[Auth] Nutzer "${username}" registriert`);

    return {
        success: true,
        data: null
    };
};

/**
    Meldet einen Nutzer ab.
*/
export const logoutUser = async (cookies: Cookies, session: App.Session) => {
    const { sessionId, username } = session;

    // Sitzung aus Redis entfernen
    await Promise.all([
        redis.del(`${sessionId}:id`),
        redis.del(`${sessionId}:username`),
        redis.del(`${sessionId}:key`),
        redis.del(`${sessionId}:loggedInAt`)
    ]);

    deleteCookie(cookies, SESSION_COOKIE_NAME);

    logger.info(`[Auth] Nutzer "${username}" abgemeldet`);
};