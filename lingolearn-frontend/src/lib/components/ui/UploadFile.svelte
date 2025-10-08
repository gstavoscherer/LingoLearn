<script lang="ts">
	import { Button } from "$lib/components/ui";
	import { UploadIcon, Trash2 } from "@lucide/svelte";

	let fileInput: HTMLInputElement | undefined = $state();
	let previewUrl: string | null = $state(null);
	let fileName: string = $state("");

	interface UploadProps {
		onUpload: (fileContent: string) => void; // for .txt we'll send text, else ""
	}
	let { onUpload }: UploadProps = $props();

	async function handleFileSelect(event: Event) {
		const target = event.target as HTMLInputElement;
		if (!target.files?.length) return;
		const file = target.files[0];
		fileName = file.name;

		if (file.type.startsWith("image/")) {
			if (previewUrl) URL.revokeObjectURL(previewUrl);
			previewUrl = URL.createObjectURL(file);
		}

		const text =
			file.type.startsWith("text/") || /\.txt$/i.test(file.name)
				? await file.text().catch(() => "")
				: "";
		onUpload(text);
	}

	function clearFile() {
		if (previewUrl) URL.revokeObjectURL(previewUrl);
		previewUrl = null;
		fileName = "";
		if (fileInput) fileInput.value = "";
		onUpload("");
	}

	$effect(() => () => {
		if (previewUrl) URL.revokeObjectURL(previewUrl);
	});
</script>

<div
	class="upload"
	style={previewUrl
    ? `background-image:url('${previewUrl}');background-size:cover;background-position:center;background-repeat:no-repeat;`
    : ""}
>
	{#if !previewUrl}
		<UploadIcon size={48} color={"var(--text-secondary)"} />
		<div class="upload-text">
			<h3>Arraste e solte seus arquivos aqui</h3>
			<p>Ou clique para selecionar arquivos</p>
		</div>
		<Button size="small" onclick={() => fileInput?.click()}>Selecionar</Button>
	{/if}

	{#if previewUrl}
		<div class="preview-bar">
			<span title={fileName}>{fileName}</span>
			<button type="button" class="icon-btn" onclick={clearFile} aria-label="Remover arquivo">
				<Trash2 size={16} />
			</button>
		</div>
	{/if}

	<input
		type="file"
		accept=".pdf,.epub,.txt,image/*"
		bind:this={fileInput}
		onchange={handleFileSelect}
		hidden
	/>
</div>

<style>
    .upload {
        display: flex;
        gap: 1rem;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        background: var(--background-gray);
        border-radius: 10px;
        outline: 2px dashed var(--border-focus);
        min-height: 260px;
        width: 100%;
        position: relative;
        text-align: center;
    }
    .upload-text { text-align: center; }
    .preview-bar {
        position: absolute;
        left: 0; right: 0; bottom: 0;
        display: flex; align-items: center; justify-content: space-between;
        gap: .5rem;
        padding: .5rem .75rem;
        background: rgba(0,0,0,.45);
        color: #fff;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    .icon-btn {
        background: none; border: 0; cursor: pointer;
        display: grid; place-items: center; padding: .2rem;
        color: #fff;
    }
</style>
