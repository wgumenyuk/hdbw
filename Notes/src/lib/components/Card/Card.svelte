<script lang="ts">
    import clsx from "clsx";

    /**
        Variante der Karte.
    */
    type CardVariant = "default" | "error" | "success";

    /**
        Variante der Karte.
    */
    export let variant: CardVariant = "default";

    const styles: Record<CardVariant, string> = {
        default: "bg-neutral-50",
        error: "bg-red-500/25",
        success: "bg-green-500/25"
    };

    const cardClass = clsx(
        "p-8",
        "border",
        "border-neutral-300",
        "rounded-lg",
        styles[variant]
    );
</script>

<div class={cardClass}>
    <slot/>
</div>