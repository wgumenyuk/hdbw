import { error } from "@sveltejs/kit";
import { z } from "zod";

// Intern
import { Note } from "$server/models/note";
import { User } from "$server/models/user";
import { encryptAes, decryptAes, randomId } from "$server/services/crypto";

// Types
import type { Note as NoteSchema } from "$server/models/note";
import { logger } from "$server/logger";

/**
    Schema für das Notizformular.
*/
export const noteSchema = z.object({
    // Titel
    title: z
        .string()
        .max(128, "Der Titel darf maximal 128 Zeichen lang sein."),

    // Inhalt
    content: z
        .string()
        .max(2048, "Der Inhalt darf maximal 2048 Zeichen lang sein.")
});

/**
    Ruft alle Metadaten von den Notizen eines Nutzers ab.
*/
export const getNotes = async (session: App.Session) => {
    const { userId } = session;

    const notes = await Note.find(
        {
            ownerId: userId
        },
        {
            _id: false,
            id: true,
            title: true,
            updatedAt: true
        },
        {
            lean: true,
            sort: {
                updatedAt: -1
            }
        }
    );

    return notes as Pick<NoteSchema, "id" | "title" | "updatedAt">[];
};

/**
    Ruft eine Notiz ab.
*/
export const getNote = async (
    session: App.Session,
    noteId: string
): App.ServiceResult<Pick<NoteSchema, "id" | "title" | "content" | "updatedAt">> => {
    const { userId, passwordKey } = session;

    const user = await User.findOne({
        id: userId
    });

    if(!user) {
        return {
            success: false,
            error: "Nutzer wurde nicht gefunden."
        };
    }

    const note = await Note.findOne({
        id: noteId,
        ownerId: userId
    });

    if(!note) {
        throw error(404);
    }

    const dataKey = await decryptAes(user.dataKey, passwordKey);
    const decryptedContent = await decryptAes(note.content, dataKey);

    return {
        success: true,
        data: {
            id: note.id,
            title: note.title,
            content: decryptedContent,
            updatedAt: note.updatedAt
        }
    };
};

/**
    Speichert eine neue Notiz.
*/
export const createNote = async (
    session: App.Session,
    data: z.infer<typeof noteSchema>
): App.ServiceResult<null> => {
    const { userId, passwordKey } = session;
    const { title, content } = data;

    const user = await User.findOne({
        id: userId
    });

    if(!user) {
        return {
            success: false,
            error: "Nutzer wurde nicht gefunden."
        };
    }

    const dataKey = await decryptAes(user.dataKey, passwordKey);
    const encryptedContent = await encryptAes(content, dataKey);

    const noteId = randomId();

    const note = await Note.create({
        id: noteId,
        ownerId: userId,
        title,
        content: encryptedContent,
        updatedAt: Date.now(),
        createdAt: Date.now()
    });

    await note.save();

    logger.info(`[Notiz] Notiz "${noteId}" erstellt`);

    return {
        success: true,
        data: null
    };
};

/**
    Aktualisiert eine Notiz.
*/
export const updateNote = async (
    session: App.Session,
    noteId: string,
    data: z.infer<typeof noteSchema>
): App.ServiceResult<null> => {
    const { userId, passwordKey } = session;
    const { title, content } = data;

    const user = await User.findOne({
        id: userId
    });

    if(!user) {
        return {
            success: false,
            error: "Nutzer wurde nicht gefunden."
        };
    }

    const note = await Note.findOne({
        id: noteId,
        ownerId: userId
    });

    if(!note) {
        throw error(404);
    }

    const dataKey = await decryptAes(user.dataKey, passwordKey);
    const encryptedContent = await encryptAes(content, dataKey);

    await note.updateOne({
        title,
        content: encryptedContent,
        updatedAt: Date.now()
    });

    logger.info(`[Notiz] Notiz "${noteId}" aktualisiert`);

    return {
        success: true,
        data: null
    };
};

/**
    Löscht eine Notiz.
*/
export const deleteNote = async (
    session: App.Session,
    noteId: string
): App.ServiceResult<null> => {
    const { userId } = session;

    const user = await User.findOne({
        id: userId
    });

    if(!user) {
        return {
            success: false,
            error: "Nutzer wurde nicht gefunden."
        };
    }

    const note = await Note.findOne({
        id: noteId,
        ownerId: userId
    });

    if(!note) {
        return {
            success: false,
            error: "Notiz wurde nicht gefunden."
        };
    }

    await note.deleteOne();

    logger.info(`[Notiz] Notiz "${noteId}" gelöscht`);
    
    return {
        success: true,
        data: null
    };
};