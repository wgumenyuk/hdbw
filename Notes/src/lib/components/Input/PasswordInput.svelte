<script lang="ts">
    import { EyeIcon, EyeOffIcon } from "lucide-svelte";

    /**
        Name des Inputs.
    */
    export let name: string;

    /**
        Label.
    */
    export let label: string;

    let isHidden = true;
</script>

<label class="flex flex-col gap-2">
    <span class="text-sm">
        {label}
    </span>
    <div class="relative">
        <input
            {name}
            type={(isHidden) ? "password" : "text"}
            placeholder={"\u2022".repeat(8)}
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
            "
        />
        <button
            class="
                absolute
                text-neutral-500
                top-1/2
                right-2.5
                -translate-y-1/2
                active:outline-none
                focus:outline-neutral-400
                p-0.5
                rounded
            "
            on:click|preventDefault={() => (isHidden = !isHidden)}
        >
            {#if isHidden}
                <EyeIcon size="20px"/>
            {:else}
                <EyeOffIcon size="20px"/>
            {/if}
        </button>
    </div>
</label>