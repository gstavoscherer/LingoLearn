<script lang="ts">
    import { BookOpen } from "@lucide/svelte";

    type Size = 'small' | 'medium';

    interface LogoProps {
        size?: Size
    }

    let { size='medium' }: LogoProps = $props();
    let iconSize: number = $derived.by(() => {
        switch (size) {
            case 'small':
                return 24;
            case 'medium':
                return 28;
            default:
                return 28;
        }
    });

</script>

<div 
    class="logo"
    class:small={ size === 'small'}
    class:medium={ size === 'medium'}
>
    <BookOpen size={iconSize}/>
    <span>LingoLearn</span>
</div>

<style>
    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        color: var(--primary-blue);
    }

    .small {
        font-size: 1.25rem;
    }

    .medium {
        font-size: 1.5rem;
    }
</style>