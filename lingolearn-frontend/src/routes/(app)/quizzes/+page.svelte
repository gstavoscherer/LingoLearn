<script lang="ts">
	import type { PageProps } from './$types';
	import { Progress } from '$lib/components/ui';
	import type { QuizResponse } from '$lib/types';
	import Button from '$lib/components/ui/Button.svelte';
	import { Check, X } from '@lucide/svelte';
	import QuizModalFinish from '$lib/components/quiz/QuizModalFinish.svelte';
	import QuizModalNoReview from '$lib/components/quiz/QuizModalNoReview.svelte';
	import { goto } from '$app/navigation';
	import { getToastState } from '$lib/toast-state.svelte';
	import { onMount } from 'svelte';
	import { sendStudyTime } from '$lib/utils';
	import { page } from '$app/state';

	const toastState = getToastState();

	let { data }: PageProps = $props();
	let quiz: QuizResponse = $state(data?.quiz);
	let current = $state(0);
	let total = $derived(quiz.length);
	let selectedOption = $state<number | null>(null);

	let showFeedback = $state(false);
	let showOverlay = $state(false);
	let showFinish = $derived(current >= quiz.length - 1);
	let showNoReview = $derived(quiz.length == 0);

	let isCorrect = $state(false);
	let feedbackMessage = $state('');
	let pulseAnimation = $state(false);
	let isContinue = $state(false);
	let questionTime = $state(Date.now());

	const correctMessages = [
		'Excelente! 🎉',
		'Você é demais! 🔥',
		'Perfeito! 💫',
		'Incrível! 🚀',
		'Mandou bem! 👏'
	];

	const wrongMessages = [
		'Quase lá! 💪',
		'Continue tentando! 🌟',
		'Na próxima você acerta! 📚',
		'Aprendendo sempre! 🧠',
		'Boa tentativa! 💫'
	];

	onMount(() => {
		const startTime = Date.now();

		return () => {
			const endTime = Date.now();
			const secondsSpent = Math.floor((endTime - startTime) / 1000);

			if (secondsSpent > 10) {
				sendStudyTime(secondsSpent, page.data.token);
			}
		};
	});

	async function handleOptionOnClick(optionId: number) {
		if (isContinue) return;
		if (showFeedback) return;

		selectedOption = optionId;
		showFeedback = true;
		pulseAnimation = true;
		showOverlay = true;

		isCorrect = validadeAnswer(optionId);

		feedbackMessage = isCorrect
			? correctMessages[Math.floor(Math.random() * correctMessages.length)]
			: wrongMessages[Math.floor(Math.random() * wrongMessages.length)];

		// Feedback visual por 1.5 segundos antes de avançar
		await new Promise((resolve) => setTimeout(resolve, 1500));

		pulseAnimation = false;
		showOverlay = false;

		isContinue = true;
	}

	function handleContinue() {
		isContinue = false;

		showFeedback = false;
		selectedOption = null;

		// Moves answer to the end of array
		if (!isCorrect && quiz[current].quality == 3) {
			const item = quiz.splice(current, 1)[0];
			quiz.push(item);
			return;
		}

		current += 1;
	}

	function validadeAnswer(optionId: number) {
		const isAnswerCorrect = optionId === quiz[current].correctAnswerId;

		const isInTime = Date.now() - questionTime <= 30 * 1000; // 30 seconds

		switch (quiz[current].quality) {
			// First try
			case 5:
				if (!isAnswerCorrect) {
					quiz[current].quality = 3;
				} else if (!isInTime) {
					quiz[current].quality = 4;
				}
				break;

			// Second try
			case 3:
				if (!isAnswerCorrect) {
					quiz[current].quality = 0;
				} else if (!isInTime) {
					quiz[current].quality = 2;
				}
				break;

			default:
				break;
		}

		return isAnswerCorrect;
	}

	function getOptionClass(optionId: number) {
		if (!showFeedback) return 'option';

		const classes = ['option'];

		if (optionId === selectedOption) {
			classes.push(isCorrect ? 'correct' : 'incorrect');
		}

		if (showFeedback && optionId === quiz[current].correctAnswerId) {
			classes.push('show-correct');
		}

		if (pulseAnimation && optionId === selectedOption) {
			classes.push('pulse');
		}

		return classes.join(' ');
	}

	async function handleQuizFinish() {
		try {
			const responses = quiz.map((question) => ({
				word_id: question.correctAnswerId,
				response_quality: question.quality || 0
			}));

			const formData = new FormData();
			formData.append('responses', JSON.stringify(responses));

			const response = await fetch(`?/submitQuiz`, {
				method: 'POST',
				body: formData
			});

			const result = await response.json();

			if (result.type === 'success') {
				console.log(result);
				goto('/home');
			} else {
				toastState.add('Erro', 'Ocorreu um erro ao salvar', 'error');
			}
		} catch (error) {
			console.error('Erro na requisição:', error);
			toastState.add('Erro', 'Ocorreu um erro ao salvar', 'error');
		}
	}
</script>

<main class:show-feedback={showOverlay}>
	{#if showOverlay}
		<div class="feedback-overlay {isCorrect ? 'correct' : 'incorrect'}">
			<div class="feedback-content">
				<div class="feedback-icon {isCorrect ? 'correct' : 'incorrect'}">
					{#if isCorrect}
						<svg width="80" height="80" viewBox="0 0 24 24" fill="none">
							<path
								d="M20 6L9 17L4 12"
								stroke="currentColor"
								stroke-width="3"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
					{:else}
						<svg width="80" height="80" viewBox="0 0 24 24" fill="none">
							<path
								d="M18 6L6 18M6 6L18 18"
								stroke="currentColor"
								stroke-width="3"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
					{/if}
				</div>
				<div class="feedback-message">{feedbackMessage}</div>
			</div>
		</div>
	{/if}

	{#if showFinish}
		<QuizModalFinish onContinue={handleQuizFinish} />
	{:else if showNoReview}
		<QuizModalNoReview />
	{:else}
		<section class="quiz-header card">
			<div class="header-title">
				<h1>Progresso</h1>
			</div>
			<div class="header-body">
				<div class="progress">
					<Progress {current} {total} />
				</div>
			</div>
		</section>

		<section class="quiz-section">
			<div class="quiz card">
				<div class="question">
					{quiz[current]?.question}
				</div>
				<div class="options">
					{#each quiz[current]?.options as option (option.id)}
						<button
							class={getOptionClass(option.id!)}
							onclick={() => handleOptionOnClick(option.id!)}
						>
							<span class="option-text">{option.word}</span>
							{#if showFeedback && option.id === quiz[current].correctAnswerId}
								<div class="correct-indicator">
									<svg width="20" height="20" viewBox="0 0 24 24" fill="none">
										<path
											d="M20 6L9 17L4 12"
											stroke="currentColor"
											stroke-width="3"
											stroke-linecap="round"
											stroke-linejoin="round"
										/>
									</svg>
								</div>
							{/if}
						</button>
					{/each}
				</div>
			</div>
		</section>

		<footer>
			<div class="feedback-section">
				{#if showFeedback}
					<div class="feedback-content {isCorrect ? 'correct' : 'incorrect'}">
						<div class="feedback-icon">
							{#if isCorrect}
								<Check size={32} strokeWidth={3} />
							{:else}
								<X size={32} strokeWidth={3} />
							{/if}
						</div>
						<div class="feedback-text">
							{#if isCorrect}
								<span class="correct-message">Certo!</span>
							{:else}
								<div class="incorrect-message">
									<span class="incorrect-label">Alternativa correta:</span>
									<span class="correct-option">
										{quiz[current].options.find(
											(opt) => opt.id === quiz[current].correctAnswerId
										)?.word}
									</span>
								</div>
							{/if}
						</div>
					</div>
				{/if}
			</div>

			<Button
				size="large"
				onclick={handleContinue}
				disabled={!showFeedback}
				class="continue-btn"
			>
				Continuar
			</Button>
		</footer>
	{/if}
</main>

<style>
	:global(:root) {
		--color-correct: #10b981;
		--color-incorrect: #ef4444;
		--color-correct-light: #d1fae5;
		--color-incorrect-light: #fee2e2;
		--color-correct-dark: #047857;
		--color-incorrect-dark: #dc2626;
	}

	main {
		height: 100%;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
		align-items: center;
		position: relative;
	}

	main.show-feedback .quiz-section {
		filter: blur(2px);
		transition: filter 0.3s ease;
	}

	footer {
		width: 100%;
		display: flex;
		justify-content: space-around;
		align-items: center;
		border: 1px solid var(--border);
		padding: 1rem;
		border-radius: 8px;
		background-color: var(--background-white);
		height: 120px;
		gap: 1rem;
	}

	.feedback-section {
		flex: 1;
		display: flex;
		justify-content: center;
	}

	.feedback-content {
		display: flex;
		align-items: center;
		gap: 1rem;
		padding: 0.75rem 1.5rem;
		border-radius: 50px;
		animation: slideIn 0.3s ease-out;
	}

	.feedback-content.correct {
		background-color: var(--toast-success-bg);
	}

	.feedback-content.incorrect {
		background-color: var(--toast-error-bg);
	}

	.feedback-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 50px;
		height: 50px;
		border-radius: 50%;
		flex-shrink: 0;
	}

	.feedback-content.correct .feedback-icon {
		background-color: var(--success-green);
		color: white;
		margin: 0px;
	}

	.feedback-content.incorrect .feedback-icon {
		background-color: var(--error-red);
		color: white;
		margin: 0px;
	}

	.feedback-text {
		display: flex;
		flex-direction: column;
	}

	.correct-message {
		color: var(--success-green);
		font-weight: 700;
		font-size: 1.4rem;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		letter-spacing: -0.5px;
	}

	.incorrect-message {
		display: flex;
		flex-direction: column;
		gap: 0.1rem;
	}

	.incorrect-label {
		color: var(--error-red);
		font-weight: 600;
		font-size: 1.3rem;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
	}

	.correct-option {
		color: var(--success-green);
		font-weight: 700;
		font-size: 1.3rem;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		letter-spacing: -0.5px;
		text-transform: capitalize;
	}

	.continue-btn {
		flex-shrink: 0;
		min-width: 140px;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateX(-20px);
		}
		to {
			opacity: 1;
			transform: translateX(0);
		}
	}

	.feedback-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		animation: fadeIn 0.3s ease;
	}

	.feedback-overlay.correct {
		background: linear-gradient(
			135deg,
			rgba(16, 185, 129, 0.1) 0%,
			rgba(34, 197, 94, 0.05) 100%
		);
	}

	.feedback-overlay.incorrect {
		background: linear-gradient(
			135deg,
			rgba(239, 68, 68, 0.1) 0%,
			rgba(220, 38, 38, 0.05) 100%
		);
	}

	.feedback-content {
		text-align: center;
		animation: slideUp 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.feedback-message {
		font-size: 1.5rem;
		font-weight: 700;
		color: #1f2937;
		animation: fadeInUp 0.5s ease 0.1s both;
	}

	.feedback-icon {
		margin-bottom: 1rem;
		animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
	}

	.feedback-icon.correct {
		color: var(--color-correct);
	}

	.feedback-icon.incorrect {
		color: var(--color-incorrect);
	}

	.feedback-circle {
		background-color: var(--primary-blue);
		width: 80px;
		height: 80px;
		border-radius: 50%;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.quiz-header {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
	}

	section {
		width: 100%;
		padding: 2rem;
	}

	.card {
		border: 1px solid var(--border);
		padding: 2rem;
		border-radius: 8px;
		background-color: var(--background-white);
	}

	.quiz-section {
		display: flex;
		justify-content: center;
		transition: filter 0.3s ease;
	}

	.quiz {
		width: 50%;
		display: flex;
		flex-direction: column;
		gap: 1.5rem;
		justify-content: center;
	}

	.question {
		border-left: 2px solid var(--primary-blue);
		padding: 1rem;
		border-radius: 10px;
		background-color: var(--primary-blue-lightest);
		font-size: 1.1rem;
		font-weight: 500;
	}

	.options {
		display: grid;
		grid-template-columns: 1fr 1fr;
		grid-template-rows: 1fr 1fr;
		gap: 1rem;
	}

	.option {
		text-transform: capitalize;
		text-align: center;
		padding: 1rem 0rem;
		border-radius: 12px;
		border: 2px solid #e5e7eb;
		background: white;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		font-size: 18px;
		font-weight: 600;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		position: relative;
		overflow: hidden;
	}

	.option:not(.correct, .incorrect):hover {
		border-color: var(--primary-blue);
		background-color: var(--primary-blue-lightest);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
	}

	.option.correct {
		background-color: var(--color-correct);
		color: white;
		border-color: var(--color-correct-dark);
		transform: scale(1.02);
		box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
	}

	.option.incorrect {
		background-color: var(--color-incorrect);
		color: white;
		border-color: var(--color-incorrect-dark);
		transform: scale(1.02);
		box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
	}

	.option.show-correct {
		background-color: var(--color-correct-light);
		color: var(--color-correct-dark);
		border-color: var(--color-correct);
		border-style: dashed;
	}

	.option.pulse {
		animation: pulse 0.6s ease;
	}

	.correct-indicator {
		position: absolute;
		top: 8px;
		right: 8px;
		color: var(--color-correct);
	}

	.option-text {
		z-index: 1;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}

	@keyframes slideUp {
		from {
			opacity: 0;
			transform: translateY(30px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes scaleIn {
		from {
			opacity: 0;
			transform: scale(0.8);
		}
		to {
			opacity: 1;
			transform: scale(1);
		}
	}

	@keyframes fadeInUp {
		from {
			opacity: 0;
			transform: translateY(20px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1.02);
		}
	}
</style>
