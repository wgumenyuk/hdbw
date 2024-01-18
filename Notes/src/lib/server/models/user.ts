import mongoose, { Schema, model } from "mongoose";

// Types
import type { Model } from "mongoose";

/**
    Nutzer.
*/
type User = {
    /**
        UUID.
    */
    id: string;

    /**
        Nutzername.
    */
    username: string;

    /**
        Passwort-Hash.
    */
    password: string;

    /**
        Kryptografierter Schlüssel zum Verschlüsseln der Notizen.
    */
    dataKey: string;

    /**
        Erstelldatum des Kontos.
    */
    createdAt: number;
};

const userSchema = new Schema<User>({
    id: {
        type: String,
        required: true
    },
    username: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    dataKey: {
        type: String,
        required: true
    },
    createdAt: {
        type: Number,
        required: true
    }
});

/**
    `User`-Modell in MongoDB.
*/
export const User: Model<User> =
    mongoose.models.User ||
    model("User", userSchema);