<script lang="ts">
    import clsx from "clsx";

    /**
        Variante des Knopfes.
    */
    type ButtonVariant = "primary" | "secondary" | "tertiary";

    /**
        Variante des Knopfes.
    */
    export let variant: ButtonVariant = "primary";

    const styles: Record<ButtonVariant, string> = {
        primary: "bg-neutral-100 hover:bg-neutral-200/50",
        secondary: "hover:bg-neutral-200/50",
        tertiary: "hover:text-neutral-500 border-transparent"
    };

    const buttonClass = clsx(
        "active:outline-none",
        "focus:outline-neutral-400",
        "border",
        "border-neutral-300",
        "rounded",
        "select-none",
        "transition-colors",
        styles[variant]
    );
</script>

<button class={buttonClass} on:click>
    <slot/>
</button>