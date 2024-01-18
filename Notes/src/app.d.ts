import type { MaybePromise } from "@sveltejs/kit";

declare global {
    namespace App {
        /**
            Ergebnis eines Services.
        */
        type ServiceResult<T> = Promise<{
            success: true;
            data: T;
            error?: never;
        } | {
            success: false;
            error: string;
            data?: never;
        }>;

        /**
            Sitzung.
        */
        type Session = {
            /**
                Sitzungs-ID.
            */
            sessionId: string;

            /**
                Nutzer-ID.
            */
            userId: string;

            /**
                Nutzername.
            */
            username: string;

            /**
                Passwort-Schlüssel.
            */
            passwordKey: string;

            /**
                Zeitpunkt der Anmeldung.
            */
            loggedInAt: number;
        };

        // Locals
        interface Locals {
            /**
                Aktuelle Sitzung mit Nutzerdaten.
            */
            user?: Session;
        };
    }
}

export {};