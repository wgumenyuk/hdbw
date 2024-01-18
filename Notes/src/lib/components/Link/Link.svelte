<script lang="ts">
    /**
        Seite, auf die verlinkt wird.
    */
    export let href: string;
</script>

<a
    {href}
    class="
        text-blue-500
        active:outline-none
        focus:outline-offset-2
        focus:outline-neutral-400
        hover:underline
        underline-offset-2
    "
>
    <slot/>
</a>