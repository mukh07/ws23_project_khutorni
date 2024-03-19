import {fetcher} from "$lib/utils.js";
import {redirect} from "@sveltejs/kit";
import type { Actions } from '$types';


export async function load({ parent, params, cookies }) {
    const { project, workflows } =  await parent();
    const workflow_name = params.workflow_name;

    const workflow = workflows.find(w => w.name === workflow_name)

    return {
        project,
        workflow
    }
}

export const actions = {
	default: async (event) => {
		const data = await event.request.formData();
		const workflow_name = data.get('workflow_name');
		const project_id = data.get('project_id');
		const action = data.get('action');

		console.log("Running action: ", action)

		const res = await fetcher(
            `/projects/${project_id}/workflows/${workflow_name}/${action}`, {
			method: "POST",
		}, event.cookies.get('token'));
		if (res.ok) {
			const json = await res.json()
			console.log(json);
			return { status: "success", ...json }
		} else {
			console.log("ERROR");
			return { status: "error" }
		}
	}
} satisfies Actions;
