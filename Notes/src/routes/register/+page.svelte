<script lang="ts">
    import { UserPlusIcon } from "lucide-svelte";
    import { Card } from "$components/Card";
    import { TextInput, PasswordInput } from "$components/Input";
    import { Button } from "$components/Button";
    import { Link } from "$components/Link";
</script>

<svelte:head>
    <title>
        Registrieren &ndash; Notizen
    </title>
</svelte:head>

<Card>
    <div class="flex justify-center items-center gap-4 mb-8">
        <UserPlusIcon/>
        <h1>
            Registrieren
        </h1>
    </div>

    <form method="POST" class="flex flex-col gap-8">
        <!-- Nutzername -->
        <TextInput
            name="username"
            placeholder="user123"
            label="Nutzername"
        />

        <!-- Passwort -->
        <PasswordInput
            name="password"
            label="Passwort"
        />

        <hr class="border-neutral-300 rounded"/>

        <!-- Submit -->
        <Button>
            <span class="block px-4 py-2.5">
                Konto erstellen
            </span>
        </Button>
    </form>

    <span class="block mt-4 text-sm text-center">
        Bereits ein Konto?
        <Link href="/login">Anmelden</Link>.
    </span>
</Card>