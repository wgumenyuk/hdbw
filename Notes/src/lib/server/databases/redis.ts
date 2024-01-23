import { Redis } from "ioredis";

// Intern
import { logger } from "$server/logger";
import { REDIS_HOST, REDIS_PASSWORD } from "$env/static/private";

let isConnected = false;

/**
    Redis-Client.
*/
export const redis = new Redis({
    host: REDIS_HOST,
    password: REDIS_PASSWORD,
    lazyConnect: true,
    keepAlive: 1000
});

/**
    Initialisiert die Verbindung zu Redis.
*/
export const initRedis = async () => {
    if(isConnected) {
        return;
    }

    logger.info(`[Datenbank] Verbinde zu Redis "${REDIS_HOST}"`);

    try {
        await redis.connect();
    } catch(err) {
        logger.fatal(err, "[Datenbank] Verbindung zu Redis gescheitert");
        process.exit(1);
    }
    
    isConnected = true;
    logger.info("[Datenbank] Redis verbunden");
};