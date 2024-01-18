<script lang="ts">
    /**
        Name des Inputs.
    */
    export let name: string;

    /**
        Optionaler Platzhalter.
    */
    export let placeholder: string | undefined = undefined;

    /**
        Wert.
    */
    export let value: string = "";
</script>

<textarea
    {name}
    {placeholder}
    {value}
    spellcheck="false"
    autocomplete="off"
    class="
        bg-neutral-100
        placeholder:text-neutral-400
        placeholder:select-none
        px-4
        py-2.5
        focus:outline-neutral-400
        border
        border-neutral-300
        rounded
        resize-none
    "
/>