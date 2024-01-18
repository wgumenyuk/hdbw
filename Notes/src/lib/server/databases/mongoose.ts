import mongoose from "mongoose";

// Intern
import { logger } from "$server/logger";
import { MONGODB_URI } from "$env/static/private";

let isConnected = false;

/**
    Initialisiert die Verbindung zu MongoDB.
*/
export const initMongodDb = async () => {
    if(isConnected) {
        return;
    }

    try {
        await mongoose.connect(MONGODB_URI, {
            dbName: "notes",
            authSource: "admin"
        });
    } catch(err) {
        logger.fatal(err, "[Datenbank] Verbindung zu MongoDB gescheitert");
        process.exit(1);
    }
    
    isConnected = true;
    logger.info("[Datenbank] MongoDB verbunden");
};