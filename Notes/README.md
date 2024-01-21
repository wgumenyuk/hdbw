**Semester**|**Kurs**|**Datum**
-----|-----|-----
WiSe 2023|Datenbanken 2|18.01.2024

# Notes
Online-Notizapp mit Verschlüsselung.

> Bei diesem Projekt handelt es sich um ein benotetes Projekt.

## Übersicht
- [Installation](#installation)
- [Technische Aspekte](#technische-aspekte)
- [Projektstruktur](#projektstruktur)

## Installation
### 1. Dependencies installieren
Dependencies für Node.js `v18.0.0` oder neuer mit NPM oder PNPM installieren:

```bash
$ npm install
```

### 2. Umgebungsvariablen konfigurieren
Die Dateien `.env.development` und `.env.production` konfigurieren die Umgebungsvariablen. Siehe `.env.example` für ein Beispiel.

### 3. Build erstellen

```bash
$ npm run build
```

### 4. Server ausführen

```bash
$ ORIGIN=http://localhost:3000 node ./build
```

## Technische Aspekte
- SvelteKit
- Tailwind CSS
- MongoDB (über [`mongoose`](https://github.com/Automattic/mongoose))
- Redis (über [`ioredis`](https://github.com/redis/ioredis))

### Verschlüsselung
Für alle kryptographischen Operationen wird das native Kryptomodul [`node:crypto`](https://nodejs.org/api/crypto.html) verwendet (siehe [`crypto.ts`](./src/lib/server/services/crypto.ts)).

- Passwort-Hashing: [scrypt](https://de.wikipedia.org/wiki/Scrypt)
- Verschlüsselung: [AES-256-CBC](https://de.wikipedia.org/wiki/Advanced_Encryption_Standard)

> ⚠️ In diesem Projekt ist die Änderung von Passwörtern nicht vorgesehen.

![Database encryption chart](./database_encryption.png)

<p align="center">
    <i>Vorgehensweise beim Verschlüsseln von Notizen.</i>
</p>

## Projektstruktur
> Der Code ist an allen wichtigen Stellen mit Kommentaren und Dokumentation versehen.

|Ordner / Datei|Erklärung|
|--|--|
|`src/lib/components`|Svelte-Komponente für das Frontend.|
|`src/lib/server`|Backend-spezifischer Code.|
|`src/lib/server/databases`|Initialisierung von `mongoose` und `ioredis`.|
|`src/lib/server/models`|Definition von `mongoose`-Modellen für MongoDB.|
|`src/lib/server/services`|Services für spezifische Aufgaben.|
|`src/lib/routes`|Routen, die im Browser aufgerufen werden können. Backend- und Frontend-spezifischer Code.|
|`src/hooks.server.ts`|Initialisierung der Datenbankverbindungen und der Sitzungslogik.|