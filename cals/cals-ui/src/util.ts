import {page} from "$app/stores";
import {get} from "svelte/store";

export function getDataFromPath() {
  const path = get(page).url.pathname;
  const components = path.split("/");

  const res = {}
  if (components.includes("projects") && components.length > 1) {
    res['project'] = parseInt(components.at(-1));
    const wIndex = components.includes("workflows")
    if (wIndex !== -1 && components[wIndex + 1] !== "edit") {
      res['workflow'] = components[wIndex + 1]
    }
  }

  return res
}