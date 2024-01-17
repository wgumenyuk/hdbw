import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/**
    @type {import("@sveltejs/kit").Config}
*/
const config = {
    preprocess: vitePreprocess(),
    kit: {
        adapter: adapter(),
        alias: {
            "$server": "./src/lib/server",
            "$components": "./src/lib/components"
        }
    }
};

export default config;