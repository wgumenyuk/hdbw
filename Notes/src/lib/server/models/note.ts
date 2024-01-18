import mongoose, { Schema, model } from "mongoose";

// Types
import type { Model } from "mongoose";

/**
    Notiz.
*/
export type Note = {
    /**
        UUID.
    */
    id: string;

    /**
        UUID des Besitzers.
    */
    ownerId: string;

    /**
        Titel.
    */
    title: string;

    /**
        Verschlüsselter Inhalt.
    */
    content: string;

    /**
        Erstelldatum der Notiz.
    */
    createdAt: number;

    /**
        Aktualisierungsdatum der Notiz.
    */
    updatedAt: number;
};

const noteSchema = new Schema<Note>({
    id: {
        type: String,
        required: true
    },
    ownerId: {
        type: String,
        required: true
    },
    title: {
        type: String,
        required: true
    },
    content: {
        type: String,
        required: true
    },
    createdAt: {
        type: Number,
        required: true
    },
    updatedAt: {
        type: Number,
        required: true
    }
});

/**
    `Note`-Modell in MongoDB.
*/
export const Note: Model<Note> =
    mongoose.models.Note ||
    model("Note", noteSchema);