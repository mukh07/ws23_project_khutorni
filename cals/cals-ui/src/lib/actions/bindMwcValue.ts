// Svelte action for connecting Material Web components with svelte bind:value
type GenericValue = string | number | boolean | Date | null;

interface BindMwcValueParams<T> {
  initialValue: T | undefined;
  getValueFromElement?: (event: Event) => T;
}

export function bindMwcValue<T extends GenericValue>(
  node: HTMLElement & { value?: string; checked?: boolean; type?: string },
  { initialValue, getValueFromElement }: BindMwcValueParams<T>
) {
  let value = initialValue;

  const defaultGetValueFromEvent = (event: Event): T => {
    // Determine the appropriate value retrieval method once, upon initialization
    if (node.type === 'checkbox') {
      return (event.target as HTMLInputElement).checked as unknown as T;
    } else if (node.type === 'number' || node.type === 'range') {
      return parseFloat((event.target as HTMLInputElement).value) as unknown as T;
    } else if (node.type === 'date' || node.type === 'date-local') {
      return new Date((event.target as HTMLInputElement).value) as unknown as T;
    } else {
      // Default to retrieving the value directly for other types
      return (event.target as HTMLInputElement).value as unknown as T;
    }
  }

  const effectiveGetValueFromEvent = getValueFromElement || defaultGetValueFromEvent;

  const handleInput = (event: Event) => {
      const newValue = effectiveGetValueFromEvent(event);
      value = newValue;
      // node.dispatchEvent(new CustomEvent('input', { detail: newValue }));
  };

  node.addEventListener('input', handleInput);

  // Optional: Dispatch the event upon initialization if needed
  // This depends on whether you need to synchronize initial state or trigger behaviors
  node.dispatchEvent(new CustomEvent('input', { detail: initialValue }));

  return {
    update(newValue: T) {
      console.log("called update")
      if (value !== newValue) {
        value = newValue;
        node.value = newValue === undefined ? '' : newValue.toString()
      }
    },
    destroy() {
      node.removeEventListener('input', handleInput);
    },
  };
}
