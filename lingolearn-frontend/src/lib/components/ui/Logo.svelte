<script lang="ts">

    type Size = 'small' | 'medium';

    interface LogoProps {
        size?: Size
    }

    let { size='medium' }: LogoProps = $props();
    let iconSize: number = $derived.by(() => {
        switch (size) {
            case 'small':
                return 32;
            case 'medium':
                return 48;
            default:
                return 48;
        }
    });

</script>

<div 
    class="logo"
    class:small={ size === 'small'}
    class:medium={ size === 'medium'}
>
    <img src="/logo.png" alt="" style="width: {iconSize}px; height: {iconSize}px;">
    <span>LingoLearn</span>
</div>

<style>
    .logo {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 700;
        color: var(--primary-blue);
        user-select: none;
    }

    .small {
        font-size: 1.25rem;
    }

    .medium {
        font-size: 1.5rem;
    }
</style>