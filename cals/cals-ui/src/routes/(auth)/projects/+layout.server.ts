import { redirect } from '@sveltejs/kit';
import {fetcher} from "$lib/utils.js";


export async function load({ params, cookies }) {
	const token = cookies.get('token');
	if (!token) {
		redirect(303, '/login');
	}

	const res = await fetcher('/projects', { method: "GET" }, token);
	if (res.ok) {
		const projects = await res.json();
		return {
			projects
		}
	} else if (res.status === 401) {
		redirect(303, '/login')
	}

	return {
		projects: []
	}
}