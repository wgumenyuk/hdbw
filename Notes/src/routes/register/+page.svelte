<script lang="ts">
    import { base } from "$app/paths";
    import { UserPlusIcon } from "lucide-svelte";
    import { Card } from "$components/Card";
    import { TextInput, PasswordInput } from "$components/Input";
    import { Button } from "$components/Button";
    import { Link } from "$components/Link";

    // Types
    import type { ActionData } from "./$types";

    /**
        Form-Action-Daten.
    */
    export let form: ActionData;
</script>

<svelte:head>
    <title>
        Registrieren &ndash; Notizen
    </title>
</svelte:head>

{#if form?.error}
    <Card variant="error">
        <span>
            {form.error}
        </span>
    </Card>
{/if}

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
        <Link href="{base}/login">Anmelden</Link>.
    </span>
</Card>