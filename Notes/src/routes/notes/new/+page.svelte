<script lang="ts">
    import { SaveIcon } from "lucide-svelte";   
    import { Card } from "$components/Card";
    import { Button } from "$components/Button";
    import { TextInput, TextArea } from "$components/Input";

    let formElement: HTMLFormElement;
</script>

<svelte:head>
    <title>
        Neue Notiz &ndash; Notizen
    </title>
</svelte:head>

<div class="flex justify-between items-center">
    <h1 class="font-bold">
        Neue Notiz
    </h1>

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

<Card>
    <form
        method="post"
        class="grid grid-rows-[auto,1fr] gap-8 h-full"
        bind:this={formElement}
    >
        <!-- Titel -->
        <TextInput
            name="title"
            placeholder="Neue Notiz"
            label="Titel"
        />

        <!-- Inhalt -->
        <TextArea
            name="content"
            placeholder="..."
        />
    </form>
</Card>