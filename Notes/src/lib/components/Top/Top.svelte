<script lang="ts">
    import { goto } from "$app/navigation";

    // Komponente
    import { NotebookIcon, LogOutIcon } from "lucide-svelte";
    import { Card } from "$components/Card";
    import { Button } from "$components/Button";
</script>

<Card>
    <div class="flex justify-between items-center h-5">
        <!-- Logo -->
        <Button variant="tertiary" on:click={() => goto("/notes")}>
            <div class="flex items-center gap-2 py-2">
                <NotebookIcon size="20px"/>
                <span>
                    Notizen
                </span>
            </div>
        </Button>

        <!-- Abmelden -->
        <Button variant="tertiary" on:click={() => goto("/logout")}>
            <div class="flex items-center gap-2 py-2">
                <LogOutIcon size="20px"/>
                <span>
                    Abmelden
                </span>
            </div>
        </Button>
    </div>
</Card>