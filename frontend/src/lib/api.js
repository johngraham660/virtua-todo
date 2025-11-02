// API utilities for interacting with the backend
const API_BASE = '/api';

class ApiError extends Error {
	constructor(message, status) {
		super(message);
		this.status = status;
	}
}

async function apiRequest(endpoint, options = {}) {
	const url = `${API_BASE}${endpoint}`;
	const config = {
		headers: {
			'Content-Type': 'application/json',
			...options.headers,
		},
		...options,
	};

	try {
		const response = await fetch(url, config);
		
		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));
			throw new ApiError(errorData.error || 'Request failed', response.status);
		}

		// Handle 204 No Content responses
		if (response.status === 204) {
			return null;
		}

		return await response.json();
	} catch (error) {
		if (error instanceof ApiError) {
			throw error;
		}
		throw new ApiError('Network error', 0);
	}
}

export const api = {
	// Get all tasks
	getTasks: () => apiRequest('/tasks'),
	
	// Create a new task
	createTask: (task) => apiRequest('/tasks', {
		method: 'POST',
		body: JSON.stringify(task),
	}),
	
	// Update a task
	updateTask: (id, task) => apiRequest(`/tasks/${id}`, {
		method: 'PUT',
		body: JSON.stringify(task),
	}),
	
	// Complete a task
	completeTask: (id) => apiRequest(`/tasks/${id}/complete`, {
		method: 'PUT',
	}),
	
	// Reopen a task
	reopenTask: (id) => apiRequest(`/tasks/${id}/reopen`, {
		method: 'PUT',
	}),
	
	// Delete a task
	deleteTask: (id) => apiRequest(`/tasks/${id}`, {
		method: 'DELETE',
	}),
};