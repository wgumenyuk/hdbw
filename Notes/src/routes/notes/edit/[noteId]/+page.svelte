<script lang="ts">
    import { base } from "$app/paths";
    import { goto } from "$app/navigation";

    // Komponente
    import { Trash2Icon, SaveIcon } from "lucide-svelte";   
    import { Card } from "$components/Card";
    import { Button } from "$components/Button";
    import { TextInput, TextArea } from "$components/Input";

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

    const { note } = data;

    let formElement: HTMLFormElement;

    /**
        Löscht die Notiz.
    */
    const deleteNote = async () => {
        const response = await fetch(`${base}/api/v1/notes/${note.data?.id}`, {
            method: "DELETE"
        });

        const { error } = await response.json();

        if(error) {
            // TODO
            return;
        }

        return goto(`${base}/notes`);
    };
</script>

<svelte:head>
    <title>
        {note.data?.title} &ndash; Notizen
    </title>
</svelte:head>

<div class="flex justify-between items-center">
    <span class="flex flex-col gap-0.5">
        <h1 class="font-bold">
            Notiz bearbeiten
        </h1>
        <span class="text-neutral-500 text-sm">
            Zuletzt bearbeitet am {formatDate(note.data?.updatedAt)}
        </span>
    </span>

    <div class="flex gap-4">
        <!-- Löschen -->
        <Button on:click={deleteNote}>
            <div class="
                bg-red-500/10
                hover:bg-red-500/15
                p-2
                rounded
                transition-colors
            ">
                <Trash2Icon size="20px"/>
            </div>
        </Button>

        <!-- Speichern -->
        <Button on:click={() => formElement.submit()}>
            <div class="
                bg-neutral-50
                hover:bg-neutral-100
                p-2
                rounded
                transition-colors
            ">
                <SaveIcon size="20px"/>
            </div>
        </Button>
    </div>
</div>

<Card>
    <form
        method="post"
        class="grid grid-rows-[auto,1fr] gap-8 h-full"
        bind:this={formElement}
    >
        <!-- Titel -->
        <TextInput
            name="title"
            placeholder={note.data?.title}
            label="Titel"
            value={note.data?.title}
        />

        <!-- Inhalt -->
        <TextArea
            name="content"
            placeholder="..."
            value={note.data?.content}
        />
    </form>
</Card>