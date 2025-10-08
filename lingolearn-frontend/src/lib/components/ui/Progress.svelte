<script lang="ts">
    let {current, total} = $props();
    let percentage = $derived.by(() => {
        return total > 0 ? Math.round((current / total) * 100) : 0;
    });
    
</script>

<div class="progress-container">
    <div class="progress-bar">
      <div class="progress-fill" style="width: {percentage}%"></div>
    </div>
    <span class="progress-text">{percentage}%</span>
</div>
  
<style>
    .progress-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        min-width: 500px;
    }

    .progress-bar {
        flex-grow: 1;
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background-color: var(--primary-blue);
        transition: width 0.3s ease;
    }

    .progress-text {
        font-size: 1.1rem;
        font-weight: 1000;
        color: var(--primary-blue);
        min-width: 40px;
        text-align: right;
        margin-left: 1rem
    }
</style>