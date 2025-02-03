import { shallowMount } from '@vue/test-utils'
import App from '@/App.vue'
import fetch from 'cross-fetch' // Use cross-fetch

// Mock the fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([]), // Mock an empty response
    ok: true,
  })
)

describe('App.vue', () => {
  it('renders the to-do list title', () => {
    const wrapper = shallowMount(App)
    expect(wrapper.text()).toMatch('To-Do List')
  })

  it('fetches tasks on creation', async () => {
    const wrapper = shallowMount(App)
    await wrapper.vm.$nextTick() // Wait for the fetch call to complete
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/tasks')
  })

  it('handles fetch errors', async () => {
    global.fetch.mockImplementationOnce(() =>
      Promise.reject(new Error('Failed to fetch'))
    )

    const wrapper = shallowMount(App)
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.tasks).toEqual([]) // Ensure tasks remain empty on error
  })
})