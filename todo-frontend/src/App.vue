<template>
  <v-app>
    <v-container>
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6">
          <v-card>
            <v-card-title class="headline">To-Do List</v-card-title>
            <v-card-text>
              <v-form @submit.prevent="addTask">
                <v-text-field
                  v-model="newTask"
                  label="Add a new task"
                  outlined
                  dense
                  required
                ></v-text-field>
                <v-btn type="submit" color="primary">Add</v-btn>
              </v-form>
              <v-list>
                <v-list-item v-for="task in tasks" :key="task.id">
                  <v-list-item-content>
                    <v-list-item-title :class="{ 'text-decoration-line-through': task.done }">
                      {{ task.task }}
                    </v-list-item-title>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-btn icon @click="toggleDone(task.id)">
                      <v-icon :color="task.done ? 'green' : 'grey'">mdi-check</v-icon>
                    </v-btn>
                    <v-btn icon @click="deleteTask(task.id)">
                      <v-icon color="red">mdi-delete</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import fetch from 'cross-fetch' // Import the fetch polyfill

export default {
  data() {
    return {
      newTask: '',
      tasks: [],
    };
  },
  async created() {
    await this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      const response = await fetch('http://127.0.0.1:8000/tasks');
      this.tasks = await response.json();
    },
    async addTask() {
      if (this.newTask.trim()) {
        await fetch('http://127.0.0.1:8000/tasks', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ task: this.newTask }),
        });
        this.newTask = '';
        await this.fetchTasks();
      }
    },
    async toggleDone(taskId) {
      await fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
        method: 'PUT',
      });
      await this.fetchTasks();
    },
    async deleteTask(taskId) {
      await fetch(`http://127.0.0.1:8000/tasks/${taskId}`, {
        method: 'DELETE',
      });
      await this.fetchTasks();
    },
  },
};
</script>

<style>
.text-decoration-line-through {
  text-decoration: line-through;
}
</style>