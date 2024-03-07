/** @type {import('@sveltejs/kit').ParamMatcher} */
export function match(param: string): boolean {
  return /^\d+$/.test(param);
}