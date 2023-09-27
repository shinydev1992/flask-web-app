<template>
  <div class="left-menu">
    <h3>Točke dnevnog reda:</h3>
    <ul>
      <li v-for="item in agendaItems" :key="item.agenda_item_id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'LeftMenu',
  data() {
    return {
      agendaItems: [],
      sessionId: null  // Ovdje možete postaviti ID trenutne sjednice. Možda ćete ga dobiti kao prop ili izvući iz route-a.
    };
  },
  created() {
    this.fetchAgendaItems();
  },
  methods: {
    async fetchAgendaItems() {
      try {
        const response = await fetch(`/sessions/${this.sessionId}/agendas`);  // Pretpostavljam da imate endpoint za dohvaćanje točaka dnevnog reda za određenu sjednicu.
        const data = await response.json();
        this.agendaItems = data;
      } catch (error) {
        console.error("Došlo je do pogreške prilikom dohvaćanja točaka dnevnog reda:", error);
      }
    }
  }
}
</script>

<style scoped>
.left-menu {
  width: 25%;
  border-right: 1px solid #ddd;
  padding: 10px;
}
</style>
