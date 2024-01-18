import crypto from "node:crypto";

// Types
import type { BinaryLike } from "node:crypto";

export {
    randomBytes,
    randomUUID as randomId
} from "node:crypto";

/**
    Zu verwendender Modus des AES-256-Algorithmus.
*/
const AES_256_ALGORITHM = "aes-256-cbc";

/**
    Leitet einen Schlüssel aus einem Passwort ab.
*/
export const scrypt = (password: string, salt: BinaryLike) => {
    return new Promise<Buffer>((resolve, reject) => {
        crypto.scrypt(password, salt, 32, (err, key) => {
            if(err) {
                return reject(err);
            }

            resolve(key);
        });
    });
};

/**
    Leitet einen Hash aus einem Passwort ab.
*/
export const hashPassword = async (password: string) => {
    const salt = crypto.randomBytes(16);
    const key = await scrypt(password, salt);

    const hash = Buffer.concat([
        salt,
        key
    ]);

    return hash.toString("hex");
};

/**
    Vergleicht ein Passwort mit einem Hash.
*/
export const comparePassword = async (password: string, hash: string) => {
    const buffer = Buffer.from(hash, "hex");

    const salt = buffer.subarray(0, 16);
    const originalKey = buffer.subarray(16);

    const comparisonKey = await scrypt(password, salt);

    return crypto.timingSafeEqual(originalKey, comparisonKey);
};

/**
    Verschlüssel einen String mit AES-256-CBC.
*/
export const encryptAes = async (data: string, password: string) => {
    const iv = crypto.randomBytes(16);
    const salt = crypto.randomBytes(16);

    const key = await scrypt(password, salt);

    const cipher = crypto.createCipheriv(
        AES_256_ALGORITHM,
        key,
        iv
    );

    const encrypted = Buffer.concat([
        iv,
        salt,
        cipher.update(data),
        cipher.final()
    ]);

    return encrypted.toString("hex");
};

/**
    Entschlüsselt einen String mit AES-256-CBC.
*/
export const decryptAes = async (data: string, password: string) => {
    const buffer = Buffer.from(data, "hex");

    const iv = buffer.subarray(0, 16);
    const salt = buffer.subarray(16, 32);
    const encrypted = buffer.subarray(32);

    const key = await scrypt(password, salt);

    const decipher = crypto.createDecipheriv(
        AES_256_ALGORITHM,
        key,
        iv
    );

    const decrypted = Buffer.concat([
        decipher.update(encrypted),
        decipher.final()
    ]);

    return decrypted.toString("utf-8");
};