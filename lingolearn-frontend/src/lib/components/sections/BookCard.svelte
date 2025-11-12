<script lang="ts">
	export let cover = '';
	export let title = '';
	export let author = '';
	export let language = 'Inglês';
	export let progress = 0;
	export let words = 0;
</script>

<article class="book-card">
	<div class="cover">
		<img src={cover} alt={title} />
	</div>

	<div class="meta">
		<h3 class="title">{title}</h3>
		<p class="author">{author}</p>
		<span class="lang">{language}</span>
	</div>

	<div class="progress">
		<div class="row">
			<span>Progresso</span>
			<span class="strong">{progress}%</span>
		</div>
		<div class="track">
			<div class="fill" style={`width:${progress}%`}></div>
		</div>
		<p class="words">Palavras <span class="strong">{words}</span></p>
	</div>

	<button class="btn">Continuar</button>
</article>

<style>
	.book-card {
		display: flex;
		flex-direction: column;
		background: var(--background-white);
		border: 1px solid var(--border-light);
		border-radius: 16px;
		padding: 12px;
		box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
	}
	.cover {
		aspect-ratio: 4/5;
		border-radius: 12px;
		overflow: hidden;
		background: var(--background-gray);
		border: 1px solid var(--border-light);
	}
	.cover img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		display: block;
	}
	.meta {
		margin-top: 10px;
		display: flex;
		flex-direction: column;
		gap: 4px;
	}
	.title {
		font-size: 14px;
		font-weight: 700;
		color: var(--text-primary);
		line-height: 1.3;
	}
	.author {
		font-size: 12px;
		color: var(--text-secondary);
	}
	.lang {
		margin-top: 2px;
		width: max-content;
		font-size: 11px;
		color: var(--text-secondary);
		background: var(--background-gray);
		border: 1px solid var(--border-light);
		border-radius: 8px;
		padding: 2px 8px;
	}
	.progress {
		margin-top: 10px;
	}
	.row {
		display: flex;
		justify-content: space-between;
		font-size: 12px;
		color: var(--text-secondary);
	}
	.track {
		margin-top: 6px;
		height: 8px;
		border-radius: 999px;
		overflow: hidden;
		background: var(--background-gray);
		border: 1px solid var(--border-light);
	}
	.fill {
		height: 100%;
		background: var(--primary-blue);
	}
	.words {
		margin-top: 8px;
		font-size: 12px;
		color: var(--text-secondary);
	}
	.strong {
		color: var(--text-primary);
		font-weight: 600;
	}
	.btn {
		margin-top: 12px;
		border-radius: 12px;
		padding: 10px 12px;
		background: var(--primary-blue);
		color: #fff;
		font-weight: 600;
	}
	.btn:hover {
		background: var(--primary-blue-hover);
	}
</style>
