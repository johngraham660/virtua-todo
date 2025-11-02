// Input validation and sanitization utilities
export function sanitizeInput(input) {
	if (!input || typeof input !== 'string') {
		return '';
	}
	
	// Trim whitespace
	let sanitized = input.trim();
	
	// Remove HTML tags
	sanitized = sanitized.replace(/<[^>]*>/g, '');
	
	// Remove script-related content
	sanitized = sanitized.replace(/javascript:/gi, '');
	sanitized = sanitized.replace(/on\w+\s*=/gi, '');
	
	// Encode HTML entities
	const div = document.createElement('div');
	div.textContent = sanitized;
	sanitized = div.innerHTML;
	
	return sanitized;
}

export function validateTitle(title) {
	if (!title || typeof title !== 'string') {
		return 'Title is required';
	}
	
	const sanitized = sanitizeInput(title);
	if (!sanitized.trim()) {
		return 'Title cannot be empty';
	}
	
	if (sanitized.length > 200) {
		return 'Title must be 200 characters or less';
	}
	
	return null;
}

export function validateDescription(description) {
	if (!description) {
		return null; // Description is optional
	}
	
	if (typeof description !== 'string') {
		return 'Description must be text';
	}
	
	const sanitized = sanitizeInput(description);
	if (sanitized.length > 1000) {
		return 'Description must be 1000 characters or less';
	}
	
	return null;
}