import {fetcher} from "$lib/utils.js";
import {redirect} from "@sveltejs/kit";
import type { Actions } from '$types';


export async function load({ parent, params, cookies }) {
    const token = cookies.get('token');
    const project_id = parseInt(params.project_id, 10);
    const { projects } =  await parent();

    const project = projects.find(p => p.id === project_id)
    const res = await fetcher(`/projects/${project_id}/workflows`, {
        method: "GET"
    }, token);

    let workflows = [];
    if (res.ok) {
        workflows = await res.json();
    } else {
        console.log("STATUS", res, res.status)
        if (res.status === 401) {
            redirect(303, '/login')
        }
    }

    return {
        project,
        workflows
    }
}