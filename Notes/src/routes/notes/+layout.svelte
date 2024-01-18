<script lang="ts">
    import { Top } from "$components/Top";
</script>

<div class="
    grid
    grid-rows-[auto,auto,1fr]
    gap-8
    max-w-screen-sm
    h-screen
    mx-auto
    py-8
">
    <Top/>
    <slot/>
</div>