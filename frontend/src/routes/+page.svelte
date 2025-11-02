<script>
	import { onMount } from 'svelte';
	import { tasks, loading, error, theme } from '../stores/tasks.js';
	import { api } from '../lib/api.js';
	import { sanitizeInput, validateTitle, validateDescription } from '../lib/validation.js';
	
	let newTaskTitle = '';
	let newTaskDescription = '';
	let editingTaskId = null;
	let editTitle = '';
	let editDescription = '';
	let validationErrors = {};

	// Load tasks on component mount
	onMount(async () => {
		await loadTasks();
		
		// Load theme preference
		const savedTheme = localStorage.getItem('theme') || 'light';
		theme.set(savedTheme);
		document.documentElement.setAttribute('data-theme', savedTheme);
	});

	async function loadTasks() {
		loading.set(true);
		error.set(null);
		
		try {
			const taskList = await api.getTasks();
			tasks.set(taskList);
		} catch (err) {
			error.set('Failed to load tasks');
			console.error('Error loading tasks:', err);
		} finally {
			loading.set(false);
		}
	}

	async function addTask() {
		// Clear previous validation errors
		validationErrors = {};
		
		// Validate and sanitize inputs
		const titleError = validateTitle(newTaskTitle);
		const descError = validateDescription(newTaskDescription);
		
		if (titleError) {
			validationErrors.title = titleError;
			return;
		}
		
		if (descError) {
			validationErrors.description = descError;
			return;
		}
		
		const sanitizedTitle = sanitizeInput(newTaskTitle);
		const sanitizedDescription = newTaskDescription ? sanitizeInput(newTaskDescription) : null;
		
		if (!sanitizedTitle.trim()) {
			validationErrors.title = 'Title cannot be empty';
			return;
		}
		
		loading.set(true);
		error.set(null);
		
		try {
			const task = await api.createTask({
				title: sanitizedTitle.trim(),
				description: sanitizedDescription?.trim() || null
			});
			
			tasks.update(list => [task, ...list]);
			newTaskTitle = '';
			newTaskDescription = '';
			validationErrors = {};
		} catch (err) {
			error.set('Failed to create task');
			console.error('Error creating task:', err);
		} finally {
			loading.set(false);
		}
	}

	async function toggleTask(task) {
		loading.set(true);
		error.set(null);
		
		try {
			const updatedTask = task.status === 'pending' 
				? await api.completeTask(task.id)
				: await api.reopenTask(task.id);
			
			tasks.update(list => 
				list.map(t => t.id === task.id ? updatedTask : t)
			);
		} catch (err) {
			error.set('Failed to update task');
			console.error('Error updating task:', err);
		} finally {
			loading.set(false);
		}
	}

	async function deleteTask(taskId) {
		loading.set(true);
		error.set(null);
		
		try {
			await api.deleteTask(taskId);
			tasks.update(list => list.filter(t => t.id !== taskId));
		} catch (err) {
			error.set('Failed to delete task');
			console.error('Error deleting task:', err);
		} finally {
			loading.set(false);
		}
	}

	function startEdit(task) {
		editingTaskId = task.id;
		editTitle = task.title;
		editDescription = task.description || '';
	}

	function cancelEdit() {
		editingTaskId = null;
		editTitle = '';
		editDescription = '';
		validationErrors = {};
	}

	async function saveEdit() {
		// Clear previous validation errors
		validationErrors = {};
		
		// Validate and sanitize inputs
		const titleError = validateTitle(editTitle);
		const descError = validateDescription(editDescription);
		
		if (titleError) {
			validationErrors.editTitle = titleError;
			return;
		}
		
		if (descError) {
			validationErrors.editDescription = descError;
			return;
		}
		
		const sanitizedTitle = sanitizeInput(editTitle);
		const sanitizedDescription = editDescription ? sanitizeInput(editDescription) : null;
		
		if (!sanitizedTitle.trim()) {
			validationErrors.editTitle = 'Title cannot be empty';
			return;
		}
		
		loading.set(true);
		error.set(null);
		
		try {
			const updatedTask = await api.updateTask(editingTaskId, {
				title: sanitizedTitle.trim(),
				description: sanitizedDescription?.trim() || null
			});
			
			tasks.update(list => 
				list.map(t => t.id === editingTaskId ? updatedTask : t)
			);
			
			cancelEdit();
		} catch (err) {
			error.set('Failed to update task');
			console.error('Error updating task:', err);
		} finally {
			loading.set(false);
		}
	}

	function handleEditKeydown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			saveEdit();
		} else if (event.key === 'Escape') {
			cancelEdit();
		}
	}

	function toggleTheme() {
		theme.update(current => {
			const newTheme = current === 'light' ? 'dark' : 'light';
			localStorage.setItem('theme', newTheme);
			document.documentElement.setAttribute('data-theme', newTheme);
			return newTheme;
		});
	}

	function handleKeydown(event) {
		if (event.key === 'Enter') {
			addTask();
		}
	}
</script>

<svelte:head>
	<title>TODO App</title>
</svelte:head>

<main>
	<header>
		<h1>TODO</h1>
		<button class="theme-toggle" on:click={toggleTheme} aria-label="Toggle theme">
			{$theme === 'light' ? '🌙' : '☀️'}
		</button>
	</header>

	<section class="add-task">
		<input
			type="text"
			placeholder="What needs to be done?"
			bind:value={newTaskTitle}
			on:keydown={handleKeydown}
			disabled={$loading}
			class:error={validationErrors.title}
		/>
		{#if validationErrors.title}
			<div class="validation-error">{validationErrors.title}</div>
		{/if}
		
		<textarea
			placeholder="Description (optional)"
			bind:value={newTaskDescription}
			disabled={$loading}
			class:error={validationErrors.description}
		></textarea>
		{#if validationErrors.description}
			<div class="validation-error">{validationErrors.description}</div>
		{/if}
		
		<button on:click={addTask} disabled={$loading || !newTaskTitle.trim()}>
			Add Task
		</button>
	</section>

	{#if $error}
		<div class="error" role="alert">
			{$error}
		</div>
	{/if}

	{#if $loading}
		<div class="loading">Loading...</div>
	{/if}

	<section class="task-list">
		{#each $tasks as task (task.id)}
			<div class="task" class:completed={task.status === 'completed'} class:editing={editingTaskId === task.id}>
				<input
					type="checkbox"
					checked={task.status === 'completed'}
					on:change={() => toggleTask(task)}
					disabled={$loading || editingTaskId === task.id}
					aria-label={task.status === 'completed' ? 'Mark as pending' : 'Mark as completed'}
				/>
				
				{#if editingTaskId === task.id}
					<!-- Edit mode -->
					<div class="task-content edit-mode">
						<input
							type="text"
							bind:value={editTitle}
							on:keydown={handleEditKeydown}
							disabled={$loading}
							class="edit-title"
							class:error={validationErrors.editTitle}
							placeholder="Task title"
							autofocus
						/>
						{#if validationErrors.editTitle}
							<div class="validation-error">{validationErrors.editTitle}</div>
						{/if}
						
						<textarea
							bind:value={editDescription}
							on:keydown={handleEditKeydown}
							disabled={$loading}
							class="edit-description"
							class:error={validationErrors.editDescription}
							placeholder="Description (optional)"
						></textarea>
						{#if validationErrors.editDescription}
							<div class="validation-error">{validationErrors.editDescription}</div>
						{/if}
						
						<div class="edit-actions">
							<button
								class="save-btn"
								on:click={saveEdit}
								disabled={$loading || !editTitle.trim()}
							>
								Save
							</button>
							<button
								class="cancel-btn"
								on:click={cancelEdit}
								disabled={$loading}
							>
								Cancel
							</button>
						</div>
					</div>
				{:else}
					<!-- View mode -->
					<div class="task-content" on:click={() => startEdit(task)} on:keydown={(e) => e.key === 'Enter' && startEdit(task)} role="button" tabindex="0">
						<h3>{task.title}</h3>
						{#if task.description}
							<p>{task.description}</p>
						{/if}
					</div>
				{/if}
				
				{#if editingTaskId !== task.id}
					<button
						class="delete-btn"
						on:click={() => deleteTask(task.id)}
						disabled={$loading}
						aria-label="Delete task"
					>
						🗑️
					</button>
				{/if}
			</div>
		{:else}
			{#if !$loading}
				<div class="empty-state">
					No tasks yet. Add one above to get started!
				</div>
			{/if}
		{/each}
	</section>
</main>

<style>
	main {
		max-width: 600px;
		margin: 0 auto;
		padding: 2rem 1rem;
		min-height: 100vh;
	}

	header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 2rem;
	}

	h1 {
		font-size: 2.5rem;
		font-weight: 300;
		color: var(--accent-color);
	}

	.theme-toggle {
		background: none;
		border: 1px solid var(--border-color);
		border-radius: 4px;
		padding: 0.5rem;
		font-size: 1.2rem;
		cursor: pointer;
		color: var(--text-color);
		transition: border-color 0.2s ease;
	}

	.theme-toggle:hover {
		border-color: var(--accent-color);
	}

	.add-task {
		margin-bottom: 2rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	input, textarea, button {
		padding: 0.75rem;
		border: 1px solid var(--border-color);
		border-radius: 4px;
		font-size: 1rem;
		font-family: inherit;
		background-color: var(--bg-color);
		color: var(--text-color);
		transition: border-color 0.2s ease;
	}

	input:focus, textarea:focus {
		outline: none;
		border-color: var(--accent-color);
	}

	input.error, textarea.error {
		border-color: var(--error-color);
	}

	.validation-error {
		color: var(--error-color);
		font-size: 0.9rem;
		margin-top: 0.25rem;
		margin-bottom: 0.5rem;
	}

	textarea {
		resize: vertical;
		min-height: 80px;
	}

	button {
		background-color: var(--accent-color);
		color: white;
		border: none;
		cursor: pointer;
		transition: opacity 0.2s ease;
	}

	button:hover:not(:disabled) {
		opacity: 0.9;
	}

	button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.error {
		background-color: var(--error-color);
		color: white;
		padding: 1rem;
		border-radius: 4px;
		margin-bottom: 1rem;
	}

	.loading {
		text-align: center;
		padding: 2rem;
		color: var(--completed-color);
	}

	.task-list {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.task {
		display: flex;
		align-items: flex-start;
		gap: 1rem;
		padding: 1rem;
		border: 1px solid var(--border-color);
		border-radius: 4px;
		background-color: var(--bg-color);
		transition: border-color 0.2s ease;
	}

	.task:hover {
		border-color: var(--accent-color);
	}

	.task.completed {
		opacity: 0.6;
	}

	.task.completed .task-content {
		text-decoration: line-through;
		color: var(--completed-color);
	}

	input[type="checkbox"] {
		margin: 0;
		width: auto;
		flex-shrink: 0;
		margin-top: 0.25rem;
	}

	.task-content {
		flex: 1;
	}

	.task-content h3 {
		margin: 0 0 0.5rem 0;
		font-weight: 500;
	}

	.task-content p {
		margin: 0;
		color: var(--completed-color);
		font-size: 0.9rem;
	}

	.delete-btn {
		background: none;
		border: none;
		padding: 0.25rem;
		font-size: 1.2rem;
		cursor: pointer;
		color: var(--error-color);
		flex-shrink: 0;
		transition: opacity 0.2s ease;
	}

	.delete-btn:hover:not(:disabled) {
		opacity: 0.7;
	}

	.empty-state {
		text-align: center;
		padding: 3rem 1rem;
		color: var(--completed-color);
		font-style: italic;
	}

	/* Edit mode styles */
	.task.editing {
		border-color: var(--accent-color);
		background-color: var(--bg-color);
	}

	.task-content {
		cursor: pointer;
	}

	.task-content:hover:not(.edit-mode) {
		opacity: 0.8;
	}

	.edit-mode {
		cursor: default !important;
		width: 100%;
	}

	.edit-title {
		width: 100%;
		margin-bottom: 0.5rem;
		font-size: 1.1rem;
		font-weight: 500;
		padding: 0.5rem;
	}

	.edit-description {
		width: 100%;
		margin-bottom: 0.75rem;
		resize: vertical;
		min-height: 60px;
		padding: 0.5rem;
	}

	.edit-actions {
		display: flex;
		gap: 0.5rem;
		justify-content: flex-end;
	}

	.save-btn, .cancel-btn {
		padding: 0.5rem 1rem;
		font-size: 0.9rem;
	}

	.save-btn {
		background-color: var(--accent-color);
		color: white;
	}

	.cancel-btn {
		background-color: transparent;
		color: var(--text-color);
		border: 1px solid var(--border-color);
	}

	@media (max-width: 640px) {
		main {
			padding: 1rem 0.5rem;
		}
		
		h1 {
			font-size: 2rem;
		}

		.edit-actions {
			flex-direction: column;
		}
	}
</style>