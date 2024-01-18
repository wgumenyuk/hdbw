<script lang="ts">
    import { goto } from "$app/navigation";

    // Komponente
    import { PlusIcon } from "lucide-svelte";
    import { Card } from "$components/Card";
    import { Button } from "$components/Button";

    // Types
    import type { PageServerData } from "./$types";

    /**
        Vom Server erhaltene Daten.
    */
    export let data: PageServerData;

    const { format: formatDate } = new Intl.DateTimeFormat("de-DE", {
        day: "2-digit",
        month: "short",
        hour: "2-digit",
        minute: "2-digit"
    });

    const { notes } = data;
</script>

<svelte:head>
    <title>
        Notizen
    </title>
</svelte:head>

<div class="flex justify-between items-center">
    <span class="text-neutral-500 text-sm">
        Insgesamt {notes.length} {(notes.length === 1) ? "Notiz" : "Notizen"}
    </span>
    <Button on:click={() => goto("/notes/new")}>
        <div class="bg-neutral-50 hover:bg-neutral-100 p-2 rounded">
            <PlusIcon size="20px"/>
        </div>
    </Button>
</div>

<Card>
    <div class="flex flex-col gap-4">
        {#each notes as note, i}
            <a
                href="/notes/edit/{note.id}"
                class="
                    flex
                    flex-col
                    gap-2
                    hover:bg-neutral-100
                    p-8
                    active:outline-none
                    focus:outline-neutral-400
                    border
                    border-neutral-300
                    rounded
                    transition-colors
                "
            >
                <span class="text-xl font-bold">
                    {note.title}
                </span>
                <span class="text-neutral-500 text-sm">
                    #{i + 1} &ndash; Aktualisiert am {formatDate(note.updatedAt)}
                </span>
            </a>
        {/each}
    </div>
</Card>